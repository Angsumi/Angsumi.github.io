"""Outbox worker: no email is sent by the request handler."""
import json
import os
import smtplib
import ssl
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage
from pathlib import Path

from .lead_store import now

TERMINAL = ('WON', 'LOST')


def smtp_send(recipient, subject, body):
    required = ('SMTP_HOST', 'SMTP_USER', 'SMTP_PASSWORD', 'MAIL_FROM', 'OWNER_EMAIL')
    if not all(os.environ.get(k) for k in required):
        raise RuntimeError('SMTP configuration incomplete')
    msg = EmailMessage()
    msg['From'] = os.environ['MAIL_FROM']
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)
    with smtplib.SMTP(os.environ['SMTP_HOST'], int(os.getenv('SMTP_PORT', '587')), timeout=20) as client:
        client.starttls(context=ssl.create_default_context())
        client.login(os.environ['SMTP_USER'], os.environ['SMTP_PASSWORD'])
        client.send_message(msg)


def schedule(store):
    """Explicitly invoked, opt-in-only sequence. No implicit enabling."""
    config = json.loads(Path(__file__).with_name('sequences.json').read_text())
    if not config['enabled']:
        return 0
    count = 0
    with store.connect() as db:
        for lead in db.execute('SELECT * FROM leads').fetchall():
            data = json.loads(lead['data'])
            if not data['marketing_consent'] or lead['replied'] or lead['opted_out'] or lead['inactive'] or lead['status'] != 'NEW':
                continue
            for day in config['days']:
                due = datetime.fromisoformat(lead['created_at']) + timedelta(days=day)
                count += db.execute('INSERT OR IGNORE INTO outbox(lead_id,kind,due_at) VALUES(?,?,?)',
                                    (lead['id'], 'follow_up_'+str(day), due.isoformat())).rowcount
    return count


def deliver(store, sender=smtp_send):
    # Single worker process. Claim jobs atomically; a crash leaves 'sending' for owner review.
    # SMTP is at-least-once: an ambiguous timeout can mean delivery occurred before failure.
    counts = {'sent': 0, 'failed': 0, 'cancelled': 0}
    with store.connect() as db:
        ids = [r['id'] for r in db.execute("SELECT id FROM outbox WHERE state='pending' AND due_at<=? AND attempts<5 ORDER BY id LIMIT 100", (now(),))]
    for job_id in ids:
        with store.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            claimed = db.execute("UPDATE outbox SET state='sending',attempts=attempts+1 WHERE id=? AND state='pending'", (job_id,)).rowcount
            if not claimed:
                continue
            job = dict(db.execute('SELECT * FROM outbox WHERE id=?', (job_id,)).fetchone())
            lead = dict(db.execute('SELECT * FROM leads WHERE id=?', (job['lead_id'],)).fetchone())
            data = json.loads(lead['data'])
            marketing = job['kind'].startswith('follow_up_')
            if marketing and (not data['marketing_consent'] or lead['replied'] or lead['opted_out'] or lead['inactive'] or lead['status'] != 'NEW'):
                db.execute("UPDATE outbox SET state='cancelled' WHERE id=?", (job_id,))
                counts['cancelled'] += 1
                continue
        try:
            subject = 'ANGSUMI inquiry ' + lead['id']
            if job['kind'] == 'owner_notification':
                recipient = os.environ.get('OWNER_EMAIL', '')
                if not recipient:
                    raise RuntimeError('Owner email not configured')
                body = f"A {data['category']} inquiry was safely saved. Reference: {lead['id']}. Priority: {lead['priority']}. Sign in to the private CRM to review."
            else:
                recipient = data['email']
                body = f"Hello {data['name']},\n\nWe received your {data['category']} inquiry. Your reference is {lead['id']}. We will review the scope and contact you about next steps. Please do not send confidential datasets by email."
                if marketing:
                    base = os.environ.get('PUBLIC_API_URL', '')
                    if not base.startswith('https://'):
                        raise RuntimeError('HTTPS unsubscribe URL not configured')
                    resources = {'research':'https://angsumi.online/resources/downloads/rna-seq-checklist.md',
                                 'digital':'https://angsumi.online/resources/downloads/digital-readiness.md',
                                 'training':'https://angsumi.online/resources/labs/'}
                    messages = {'follow_up_1':'Would a short requirements conversation help? Reply with the question you would like to resolve first.',
                                'follow_up_3':'Here is a planning resource relevant to your inquiry: '+resources[data['category']],
                                'follow_up_7':'Is your project still active? Reply if you would like to continue; tell us if your plans have changed.'}
                    body = f"Hello {data['name']},\n\n{messages.get(job['kind'], 'Reply if you would like to discuss your project.')}\n\nYou asked for relevant resources and follow-ups. Reference: {lead['id']}.\n\nStop promotional follow-ups: {base}/unsubscribe/{lead['unsubscribe_token']}"
            sender(recipient, subject, body + '\n\nANGSUMI — Research | Data | Impact')
        except Exception:
            # Deliberately avoid provider exception strings: they may contain addresses/credentials.
            retry = (datetime.now(timezone.utc) + timedelta(minutes=min(1440, 5 * 2 ** job['attempts']))).isoformat()
            with store.connect() as db:
                db.execute("UPDATE outbox SET state='pending',last_error='Delivery failed; check provider configuration',due_at=? WHERE id=?", (retry, job_id))
            counts['failed'] += 1
        else:
            with store.connect() as db:
                db.execute("UPDATE outbox SET state='sent',sent_at=?,last_error=NULL WHERE id=?", (now(), job_id))
                store.activity(db, lead['id'], 'notification_sent', job['kind'])
            counts['sent'] += 1
    return counts
