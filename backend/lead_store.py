"""Durable lead store. No networking, analytics, or provider credentials here."""
import hashlib
import json
import re
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

STATUSES = ('NEW', 'NEEDS_INFORMATION', 'CONTACTED', 'QUALIFIED', 'DISCOVERY',
            'PROPOSAL_SENT', 'NEGOTIATION', 'WON', 'LOST')
CATEGORIES = ('research', 'digital', 'training')
DETAIL_FIELDS = ('institution', 'field', 'project_type', 'dataset_type', 'samples', 'stage',
                 'deliverables', 'deadline', 'business_type', 'business_name', 'platform',
                 'workflow', 'functionality', 'level', 'interest', 'format', 'availability')
SOURCES = ('direct', 'google', 'instagram', 'github', 'youtube', 'referral', 'other')
CAMPAIGNS = ('none', 'research-checklist', 'digital-readiness', 'bioinformatics-labs', 'workshop')


def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def clean(value, limit=1000):
    if not isinstance(value, str) or len(value) > limit or '\x00' in value:
        raise ValueError('Invalid or oversized text field')
    return value.strip()


def validate(payload):
    if not isinstance(payload, dict):
        raise ValueError('Expected an inquiry object')
    data = {k: clean(payload.get(k, ''), limit) for k, limit in
            [('name', 120), ('email', 254), ('phone', 40), ('description', 3000),
             ('category', 30), ('budget', 40), ('landing_page', 200)]}
    data['email'] = data['email'].lower()
    if not data['name'] or not re.fullmatch(r'[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+', data['email']):
        raise ValueError('Enter your name and a valid email address')
    if data['category'] not in CATEGORIES or len(data['description']) < 10:
        raise ValueError('Choose a pathway and describe your goal in at least 10 characters')
    if data['budget'] not in ('', 'not_sure', 'under_5000', '5000_15000', '15000_50000', '50000_plus'):
        raise ValueError('Choose a valid budget range')
    if payload.get('contact_consent') is not True:
        raise ValueError('Permission to contact you about this inquiry is required')
    data['marketing_consent'] = payload.get('marketing_consent') is True
    data['contact_consent'] = True
    data['consent_version'] = '2026-11-08'
    data['source'] = payload.get('source') if payload.get('source') in SOURCES else 'other'
    data['campaign'] = payload.get('campaign') if payload.get('campaign') in CAMPAIGNS else 'none'
    # Store a known public path, never a query, fragment, or arbitrary external URL.
    path = data['landing_page']
    if not re.fullmatch(r'/(?:[a-z0-9_-]+/)*', path):
        data['landing_page'] = '/inquiry/'
    details = payload.get('details', {})
    if not isinstance(details, dict):
        raise ValueError('Invalid project details')
    data['details'] = {k: clean(details[k], 500) for k in DETAIL_FIELDS if k in details}
    return data


def score(data, config=None):
    config = config or json.loads(Path(__file__).with_name('scoring.json').read_text())
    d = data['details']
    conditions = {
        'category_relevance': data['category'] in CATEGORIES,
        'clear_requirements': len(data['description']) >= 80,
        'known_budget': data['budget'] not in ('', 'not_sure'),
        'ready_to_start': d.get('stage') in ('data_ready', 'requirements_ready', 'ready'),
        'defined_timeline': bool(d.get('deadline') or d.get('availability')),
        'organization_context': bool(d.get('institution') or d.get('business_name')),
    }
    reasons = {k: config[k] for k, yes in conditions.items() if yes}
    total = sum(reasons.values())
    priority = 'high' if total >= config['high_threshold'] else 'medium' if total >= config['medium_threshold'] else 'low'
    return total, priority, reasons


class Store:
    def __init__(self, path):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with self.connect() as db:
            db.executescript('''
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS leads (
                    id TEXT PRIMARY KEY, request_key TEXT UNIQUE NOT NULL,
                    fingerprint TEXT NOT NULL, created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL, data TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'NEW', score INTEGER NOT NULL,
                    priority TEXT NOT NULL, score_reasons TEXT NOT NULL,
                    assigned_to TEXT NOT NULL DEFAULT '', last_contact TEXT,
                    next_follow_up TEXT, outcome TEXT NOT NULL DEFAULT '',
                    revenue REAL, replied INTEGER NOT NULL DEFAULT 0,
                    opted_out INTEGER NOT NULL DEFAULT 0, inactive INTEGER NOT NULL DEFAULT 0,
                    unsubscribe_token TEXT UNIQUE NOT NULL
                );
                CREATE INDEX IF NOT EXISTS leads_fingerprint ON leads(fingerprint, created_at);
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY, lead_id TEXT NOT NULL REFERENCES leads(id),
                    created_at TEXT NOT NULL, kind TEXT NOT NULL, detail TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS outbox (
                    id INTEGER PRIMARY KEY, lead_id TEXT NOT NULL REFERENCES leads(id),
                    kind TEXT NOT NULL, due_at TEXT NOT NULL, state TEXT NOT NULL DEFAULT 'pending',
                    attempts INTEGER NOT NULL DEFAULT 0, last_error TEXT,
                    sent_at TEXT, UNIQUE(lead_id, kind)
                );
            ''')
        Path(path).chmod(0o600)

    def connect(self):
        db = sqlite3.connect(self.path, timeout=15)
        db.row_factory = sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON')
        return db

    def activity(self, db, lead_id, kind, detail):
        db.execute('INSERT INTO activities(lead_id,created_at,kind,detail) VALUES(?,?,?,?)',
                   (lead_id, now(), kind, detail))

    def create(self, payload, request_key):
        data = validate(payload)
        if not re.fullmatch(r'[A-Za-z0-9_-]{16,100}', request_key or ''):
            raise ValueError('A valid submission key is required; reload and retry')
        # Exact normalized inquiry duplicate within 24 hours; budget alone never rejects a lead.
        fingerprint = hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        timestamp = now()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            prior = db.execute('SELECT id,fingerprint FROM leads WHERE request_key=?', (request_key,)).fetchone()
            if prior:
                if prior['fingerprint'] != fingerprint:
                    raise ValueError('Submission key already used for a different inquiry')
                return prior['id'], True
            cutoff = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
            prior = db.execute('SELECT id FROM leads WHERE fingerprint=? AND created_at>=?', (fingerprint, cutoff)).fetchone()
            if prior:
                return prior['id'], True
            lead_id = 'ANG-' + secrets.token_hex(8).upper()
            points, priority, reasons = score(data)
            follow_up = (datetime.now(timezone.utc) + timedelta(days=1)).isoformat(timespec='seconds')
            db.execute('''INSERT INTO leads(id,request_key,fingerprint,created_at,updated_at,data,
                       score,priority,score_reasons,next_follow_up,unsubscribe_token)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?)''',
                       (lead_id, request_key, fingerprint, timestamp, timestamp, json.dumps(data),
                        points, priority, json.dumps(reasons), follow_up, secrets.token_urlsafe(32)))
            self.activity(db, lead_id, 'received', 'Inquiry saved; scoring is advisory and does not reject leads')
            for kind in ('acknowledgement', 'owner_notification'):
                db.execute('INSERT INTO outbox(lead_id,kind,due_at) VALUES(?,?,?)', (lead_id, kind, timestamp))
            return lead_id, False

    @staticmethod
    def decode(row):
        result = dict(row)
        result['data'] = json.loads(result['data'])
        result['score_reasons'] = json.loads(result['score_reasons'])
        for key in ('fingerprint', 'request_key', 'unsubscribe_token'):
            result.pop(key, None)
        return result

    def list(self):
        with self.connect() as db:
            return [self.decode(r) for r in db.execute('SELECT * FROM leads ORDER BY created_at DESC, id')]

    def get(self, lead_id):
        with self.connect() as db:
            row = db.execute('SELECT * FROM leads WHERE id=?', (lead_id,)).fetchone()
            if row is None:
                raise KeyError('Lead not found')
            result = self.decode(row)
            result['activities'] = [dict(r) for r in db.execute('SELECT * FROM activities WHERE lead_id=? ORDER BY id', (lead_id,))]
            result['notifications'] = [dict(r) for r in db.execute('SELECT kind,state,attempts,due_at,sent_at,last_error FROM outbox WHERE lead_id=?', (lead_id,))]
            return result

    def update(self, lead_id, changes):
        if not isinstance(changes, dict):
            raise ValueError('Invalid update')
        columns = {}
        for key in ('status', 'assigned_to', 'outcome', 'next_follow_up', 'last_contact'):
            if key in changes:
                value = clean(changes[key], 200)
                if key == 'status' and value not in STATUSES:
                    raise ValueError('Invalid pipeline status')
                if key in ('next_follow_up', 'last_contact') and value:
                    parsed = datetime.fromisoformat(value)
                    if parsed.tzinfo is None:
                        raise ValueError('Dates must include a timezone')
                    value = parsed.astimezone(timezone.utc).isoformat(timespec='seconds')
                columns[key] = value or None if key in ('next_follow_up', 'last_contact') else value
        for key in ('replied', 'opted_out', 'inactive'):
            if key in changes:
                if not isinstance(changes[key], bool):
                    raise ValueError('Invalid stop preference')
                columns[key] = int(changes[key])
        if 'revenue' in changes:
            value = changes['revenue']
            if value is not None and (type(value) not in (int, float) or not 0 <= value <= 1e12):
                raise ValueError('Invalid revenue amount')
            columns['revenue'] = value
        note = clean(changes.get('note', ''), 3000)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT id FROM leads WHERE id=?', (lead_id,)).fetchone()
            if row is None:
                raise KeyError('Lead not found')
            if columns:
                columns['updated_at'] = now()
                db.execute('UPDATE leads SET ' + ','.join(k+'=?' for k in columns) + ' WHERE id=?', (*columns.values(), lead_id))
                self.activity(db, lead_id, 'updated', json.dumps(columns))
            if note:
                self.activity(db, lead_id, 'note', note)
        return self.get(lead_id)

    def unsubscribe(self, token):
        with self.connect() as db:
            row = db.execute('SELECT id FROM leads WHERE unsubscribe_token=?', (token,)).fetchone()
            if not row:
                return False
            db.execute('UPDATE leads SET opted_out=1,updated_at=? WHERE id=?', (now(), row['id']))
            self.activity(db, row['id'], 'opted_out', 'Promotional follow-up stopped')
            return True

    def reporting(self):
        """Lifecycle facts from status history, including subsequently lost opportunities."""
        with self.connect() as db:
            rows = db.execute("SELECT lead_id,detail FROM activities WHERE kind='updated'").fetchall()
        proposed, qualified = set(), set()
        for row in rows:
            status = json.loads(row['detail']).get('status')
            if status in ('PROPOSAL_SENT','NEGOTIATION','WON'):
                proposed.add(row['lead_id'])
            if status in ('QUALIFIED','DISCOVERY','PROPOSAL_SENT','NEGOTIATION','WON'):
                qualified.add(row['lead_id'])
        leads = self.list()
        won = {lead['id'] for lead in leads if lead['status']=='WON'}
        return {'total_inquiries':len(leads),'ever_qualified':len(qualified),
                'ever_proposed':len(proposed),'currently_won':len(won),
                'proposal_to_won_percent':round(len(won & proposed)/len(proposed)*100,1) if proposed else None,
                'qualification_definition':'Ever entered qualified or a later pipeline stage',
                'proposal_definition':'Ever entered proposal, negotiation or won; manually skipped stages are inferred',
                'currency':'INR','revenue_recorded':sum(lead['revenue'] or 0 for lead in leads if lead['status']=='WON')}

    def backup(self, destination):
        with self.connect() as source, sqlite3.connect(destination) as target:
            source.backup(target)
        Path(destination).chmod(0o600)
