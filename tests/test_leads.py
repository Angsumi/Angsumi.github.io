import copy
import io
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from unittest.mock import patch
from wsgiref.util import setup_testing_defaults

from backend.lead_store import Store, validate, score
from backend.server import App, password_hash
from backend.notifications import deliver, schedule

ORIGIN='http://127.0.0.1:8765'
PAYLOAD={'name':'Synthetic Researcher','email':'test@example.invalid','phone':'','category':'research',
 'description':'Review a synthetic count matrix and experimental design before scoping a differential expression workflow.',
 'budget':'under_5000','details':{'stage':'data_ready','institution':'Synthetic Lab','deadline':'2026-12-01'},
 'landing_page':'/services/rna-seq-analysis/','source':'github','campaign':'research-checklist',
 'contact_consent':True,'marketing_consent':False,'website':''}

class SystemTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.password='synthetic-password-for-testing-only';cls.encoded=password_hash(cls.password)
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.store=Store(Path(self.tmp.name)/'leads.sqlite')
  self.app=App(self.store,[ORIGIN],self.encoded,development=True)
 def tearDown(self):self.tmp.cleanup()
 def request(self,path,method='GET',data=None,origin=ORIGIN,cookie='',csrf='',key='test-submission-key-0001'):
  env={};setup_testing_defaults(env)
  body=json.dumps(data).encode() if data is not None else b''
  env.update(PATH_INFO=path,REQUEST_METHOD=method,HTTP_ORIGIN=origin,HTTP_COOKIE=cookie,
   HTTP_X_CSRF_TOKEN=csrf,HTTP_IDEMPOTENCY_KEY=key,CONTENT_TYPE='application/json',
   CONTENT_LENGTH=str(len(body)),REMOTE_ADDR='127.0.0.1',**{'wsgi.input':io.BytesIO(body)})
  result={}
  def start(status,headers):result.update(status=int(status.split()[0]),headers=dict(headers))
  result['body']=b''.join(self.app(env,start));return result
 def login(self):
  result=self.request('/api/login','POST',{'password':self.password})
  self.assertEqual(result['status'],200)
  cookie=result['headers']['Set-Cookie'].split(';')[0]
  session=self.request('/api/admin/session',cookie=cookie)
  return cookie,json.loads(session['body'])['csrf']
 def test_all_pathways_persist_with_optional_fields(self):
  for i,category in enumerate(['research','digital','training']):
   payload={**PAYLOAD,'category':category,'details':{}}
   result=self.request('/api/leads','POST',payload,key='different-key-0000'+str(i))
   self.assertEqual(result['status'],201)
   self.assertTrue(json.loads(result['body'])['saved'])
  self.assertEqual(len(self.store.list()),3)
 def test_submission_durable_with_activity_and_outbox(self):
  lead_id,duplicate=self.store.create(PAYLOAD,'test-submission-key-0001')
  self.assertFalse(duplicate)
  lead=self.store.get(lead_id)
  self.assertEqual(len(lead['activities']),1);self.assertEqual(len(lead['notifications']),2)
  self.assertIsNotNone(lead['next_follow_up'])
  reopened=Store(self.store.path);self.assertEqual(reopened.get(lead_id)['id'],lead_id)
 def test_duplicate_same_key_and_same_payload(self):
  first=self.store.create(PAYLOAD,'test-submission-key-0001')
  second=self.store.create(PAYLOAD,'test-submission-key-0001')
  third=self.store.create(PAYLOAD,'test-submission-key-0002')
  self.assertEqual(first[0],second[0]);self.assertEqual(first[0],third[0]);self.assertTrue(third[1])
  self.assertEqual(len(self.store.get(first[0])['notifications']),2)
 def test_key_reuse_for_changed_payload_rejected(self):
  self.store.create(PAYLOAD,'test-submission-key-0001')
  with self.assertRaises(ValueError):self.store.create({**PAYLOAD,'description':'A distinct second research inquiry.'},'test-submission-key-0001')
 def test_parallel_duplicate_submissions(self):
  with ThreadPoolExecutor(max_workers=6) as pool:
   results=list(pool.map(lambda _:self.store.create(PAYLOAD,'parallel-submission-0001'),range(6)))
  self.assertEqual(len({r[0] for r in results}),1);self.assertEqual(len(self.store.list()),1)
 def test_no_save_on_validation_errors(self):
  for changes in [{'email':'invalid'},{'category':'unknown'},{'description':'short'},{'contact_consent':False},{'details':[]},{'name':'x'*121}]:
   result=self.request('/api/leads','POST',{**PAYLOAD,**changes});self.assertEqual(result['status'],400)
  self.assertEqual(self.store.list(),[])
 def test_honeypot_and_bad_origin(self):
  self.assertEqual(self.request('/api/leads','POST',{**PAYLOAD,'website':'bot'})['status'],400)
  self.assertEqual(self.request('/api/leads','POST',PAYLOAD,origin='https://evil.invalid')['status'],403)
  self.assertEqual(self.store.list(),[])
 def test_size_limit(self):
  self.assertEqual(self.request('/api/leads','POST',{**PAYLOAD,'unknown':'x'*20000})['status'],400)
 def test_request_rate_limit(self):
  for _ in range(10):self.request('/api/leads','POST',PAYLOAD)
  self.assertEqual(self.request('/api/leads','POST',PAYLOAD)['status'],429)
 def test_auth_and_csrf_required(self):
  self.assertEqual(self.request('/api/admin/leads')['status'],401)
  self.assertEqual(self.request('/api/admin/export')['status'],401)
  cookie,csrf=self.login();lead_id,_=self.store.create(PAYLOAD,'test-submission-key-0001')
  self.assertEqual(self.request('/api/admin/leads/'+lead_id,'PATCH',{'status':'QUALIFIED'},cookie=cookie)['status'],403)
  result=self.request('/api/admin/leads/'+lead_id,'PATCH',{'status':'QUALIFIED','note':'Reviewed scope'},cookie=cookie,csrf=csrf)
  self.assertEqual(result['status'],200);self.assertEqual(json.loads(result['body'])['status'],'QUALIFIED')
 def test_login_throttle_and_logout(self):
  cookie,csrf=self.login()
  self.assertEqual(self.request('/api/admin/logout','POST',{},cookie=cookie,csrf=csrf)['status'],200)
  self.assertEqual(self.request('/api/admin/leads',cookie=cookie)['status'],401)
  for _ in range(4):self.request('/api/login','POST',{'password':'wrong'})
  self.assertEqual(self.request('/api/login','POST',{'password':self.password})['status'],429)
 def test_status_revenue_and_dates_validated(self):
  lead_id,_=self.store.create(PAYLOAD,'test-submission-key-0001')
  for update in [{'status':'PAID_FAKE'},{'revenue':-1},{'revenue':'100'},{'revenue':float('nan')},{'next_follow_up':'2026-12-01T12:00'}]:
   with self.assertRaises(ValueError):self.store.update(lead_id,update)
  lead=self.store.update(lead_id,{'status':'WON','revenue':12000,'assigned_to':'Owner','next_follow_up':'2026-12-01T12:00:00+05:30','replied':True})
  self.assertEqual(lead['revenue'],12000);self.assertEqual(lead['next_follow_up'],'2026-12-01T06:30:00+00:00')
 def test_low_budget_is_not_rejected(self):
  data=validate(PAYLOAD);points,priority,reasons=score(data)
  self.assertGreater(points,0);self.assertIn('known_budget',reasons)
  lead_id,_=self.store.create(PAYLOAD,'test-submission-key-0001');self.assertEqual(self.store.get(lead_id)['status'],'NEW')
 def test_source_allowlist_and_pii_urls(self):
  data=validate({**PAYLOAD,'source':'test@example.invalid','campaign':'name=person','landing_page':'https://example.invalid/?email=test'})
  self.assertEqual(data['source'],'other');self.assertEqual(data['campaign'],'none');self.assertEqual(data['landing_page'],'/inquiry/')
 def test_static_server_never_exposes_private_paths(self):
  for path in ['/backend/lead_store.py','/docs/ANGSUMI_SECURITY_AUDIT.md','/.git/config','/scripts/build_growth.py','/assets/../backend/server.py','/tests/test_leads.py']:
   self.assertEqual(self.request(path)['status'],404,path)
  self.assertEqual(self.request('/inquiry/')['status'],200)
 def test_csv_formula_injection_neutralized(self):
  self.store.create({**PAYLOAD,'name':'=HYPERLINK("unsafe")'},'test-submission-key-0001')
  cookie,_=self.login();result=self.request('/api/admin/export',cookie=cookie)
  self.assertEqual(result['status'],200);self.assertIn(b"'=HYPERLINK",result['body'])
 def test_notifications_failure_keeps_saved_lead(self):
  lead_id,_=self.store.create(PAYLOAD,'test-submission-key-0001')
  def failing(*_):raise OSError('provider failure secret must not be logged')
  with patch.dict(os.environ,{'OWNER_EMAIL':'owner@example.invalid'}):result=deliver(self.store,failing)
  self.assertEqual(result['failed'],2);self.assertEqual(len(self.store.list()),1)
  self.assertNotIn('secret',json.dumps(self.store.get(lead_id)))
 def test_notifications_send_after_save_and_no_repeat(self):
  self.store.create(PAYLOAD,'test-submission-key-0001');sent=[]
  def fake(*args):
   self.assertEqual(len(self.store.list()),1);sent.append(args)
  with patch.dict(os.environ,{'OWNER_EMAIL':'owner@example.invalid'}):
   self.assertEqual(deliver(self.store,fake)['sent'],2)
   self.assertEqual(deliver(self.store,fake)['sent'],0)
  self.assertEqual(len(sent),2)
 def test_unsubscribe_stops_pending_marketing(self):
  lead_id,_=self.store.create({**PAYLOAD,'marketing_consent':True},'test-submission-key-0001')
  with self.store.connect() as db:
   token=db.execute('SELECT unsubscribe_token FROM leads WHERE id=?',(lead_id,)).fetchone()[0]
   db.execute("INSERT INTO outbox(lead_id,kind,due_at) VALUES(?, 'follow_up_1', '2020-01-01')",(lead_id,))
  self.assertTrue(self.store.unsubscribe(token))
  with patch.dict(os.environ,{'OWNER_EMAIL':'owner@example.invalid'}):result=deliver(self.store,lambda *_:None)
  self.assertEqual(result['cancelled'],1)
  self.assertTrue(self.store.get(lead_id)['opted_out'])
 def test_sequences_disabled_by_default(self):
  self.store.create({**PAYLOAD,'marketing_consent':True},'test-submission-key-0001')
  self.assertEqual(schedule(self.store),0)
 def test_reply_or_customer_stops_marketing(self):
  for changes in [{'replied':True},{'status':'WON'},{'inactive':True},{'status':'CONTACTED'}]:
   lead_id,_=self.store.create({**PAYLOAD,'description':str(changes)+' synthetic context','marketing_consent':True},'key-for-stop-'+str(len(self.store.list())).zfill(10))
   self.store.update(lead_id,changes)
   with self.store.connect() as db:db.execute("INSERT INTO outbox(lead_id,kind,due_at) VALUES(?, 'follow_up_1', '2020-01-01')",(lead_id,))
  with patch.dict(os.environ,{'OWNER_EMAIL':'owner@example.invalid'}):result=deliver(self.store,lambda *_:None)
  self.assertEqual(result['cancelled'],4)
 def test_backup_and_restore(self):
  lead_id,_=self.store.create(PAYLOAD,'test-submission-key-0001');backup=Path(self.tmp.name)/'backup.sqlite'
  self.store.backup(backup);self.assertEqual(Store(backup).get(lead_id)['id'],lead_id)
 def test_public_packaging_excludes_private_material(self):
  from scripts.build_public import build
  output=build(Path(self.tmp.name)/'public')
  self.assertTrue((output/'inquiry/index.html').is_file())
  for path in ['docs','backend','scripts','tests','.git','supabase']:
   self.assertFalse((output/path).exists())

if __name__=='__main__':unittest.main()

class ReportingTests(unittest.TestCase):
 def test_lost_proposals_remain_in_denominator(self):
  with tempfile.TemporaryDirectory() as temp:
   store=Store(Path(temp)/'leads.sqlite')
   first,_=store.create(PAYLOAD,'reporting-first-key-0001')
   second,_=store.create({**PAYLOAD,'email':'second@example.invalid'},'reporting-second-key-0001')
   for lead_id in (first,second):store.update(lead_id,{'status':'PROPOSAL_SENT'})
   store.update(first,{'status':'WON','revenue':15000});store.update(second,{'status':'LOST'})
   report=store.reporting()
   self.assertEqual(report['ever_proposed'],2);self.assertEqual(report['proposal_to_won_percent'],50)
   self.assertEqual(report['revenue_recorded'],15000)
