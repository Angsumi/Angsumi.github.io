"""Lead API WSGI application; run behind TLS reverse proxy for production."""
import csv
import hashlib
import hmac
import io
import ipaddress
import json
import mimetypes
import os
import re
import secrets
import threading
import time
from pathlib import Path
from urllib.parse import parse_qs
from wsgiref.simple_server import WSGIRequestHandler, make_server

from .lead_store import Store, STATUSES

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_DIRS = {'assets', 'about', 'business', 'cv', 'learning', 'locations', 'privacy-policy',
               'services', 'terms', 'tools', 'inquiry', 'resources', 'portfolio', 'training', 'owner', 'unsubscribe'}
PUBLIC_FILES = {'index.html', '404.html', 'CNAME', 'robots.txt', 'sitemap.xml', 'favicon.ico',
                'favicon-32x32.png', 'apple-touch-icon.png', 'logo.png', 'og-icon.png',
                'hero-illustration.jpg', 'hero-illustration.webp', 'ads.txt', 'google98f2be4e341a535a.html',
                '6c3d5fd49dcb41b5ac4b7e3a74b7c048.txt'}


def password_hash(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 600000).hex()
    return f'pbkdf2_sha256${salt}${digest}'


def password_matches(password, encoded):
    try:
        algorithm, salt, digest = encoded.split('$')
        return algorithm == 'pbkdf2_sha256' and hmac.compare_digest(password_hash(password, salt), encoded)
    except (ValueError, AttributeError):
        return False


class App:
    def __init__(self, store, origins, admin_hash='', development=False, trusted_proxies=()):
        self.store = store
        self.origins = set(origins)
        self.admin_hash = admin_hash
        self.development = development
        self.trusted_proxies = set(trusted_proxies)
        self.sessions = {}
        self.rates = {}
        self.lock = threading.Lock()

    def limited(self, key, maximum, period=3600):
        with self.lock:
            current = time.monotonic()
            if len(self.rates) > 10000:
                self.rates = {k: v for k, v in self.rates.items() if current-v[0] < 3600}
                if len(self.rates) > 10000:
                    return True
            start, count = self.rates.get(key, (current, 0))
            if current-start >= period:
                start, count = current, 0
            self.rates[key] = (start, count+1)
            return count >= maximum

    def session(self, env):
        cookie = env.get('HTTP_COOKIE', '')
        match = re.search(r'(?:^|;\s*)angsumi_session=([A-Za-z0-9_-]+)', cookie)
        token = match.group(1) if match else ''
        with self.lock:
            self.sessions = {k: v for k, v in self.sessions.items() if v['expires'] > time.monotonic()}
            return token, self.sessions.get(token)

    @staticmethod
    def body(env):
        try:
            length = int(env.get('CONTENT_LENGTH') or 0)
        except ValueError:
            raise ValueError('Invalid request length')
        if not 0 < length <= 16384:
            raise ValueError('Request must be under 16 KB')
        if env.get('CONTENT_TYPE', '').split(';')[0] != 'application/json':
            raise ValueError('Use JSON')
        return json.loads(env['wsgi.input'].read(length))

    def __call__(self, env, start_response):
        method, path = env['REQUEST_METHOD'], env.get('PATH_INFO', '/')
        origin = env.get('HTTP_ORIGIN', '')
        headers = [('X-Content-Type-Options', 'nosniff'), ('Referrer-Policy', 'no-referrer'),
                   ('X-Frame-Options', 'DENY'), ('Cache-Control', 'no-store')]
        if origin in self.origins:
            headers += [('Access-Control-Allow-Origin', origin), ('Vary', 'Origin')]

        def respond(status, body, kind='application/json; charset=utf-8', extra=()):
            if not isinstance(body, bytes):
                body = json.dumps(body).encode() if kind.startswith('application/json') else body.encode()
            start_response(str(status)+' '+{200:'OK',201:'Created',204:'No Content',400:'Bad Request',401:'Unauthorized',403:'Forbidden',404:'Not Found',413:'Payload Too Large',429:'Too Many Requests',503:'Service Unavailable',500:'Internal Server Error'}[status],
                           headers+[('Content-Type',kind), ('Content-Length',str(len(body)))]+list(extra))
            return [b'' if method == 'HEAD' else body]

        try:
            if method == 'OPTIONS':
                if origin not in self.origins:
                    return respond(403, {'error':'Origin not allowed'})
                return respond(204, b'', extra=[('Access-Control-Allow-Methods','GET,POST,PATCH,OPTIONS'),
                    ('Access-Control-Allow-Headers','Content-Type,Idempotency-Key,X-CSRF-Token')])
            if method in ('POST','PATCH') and origin not in self.origins:
                return respond(403, {'error':'Origin not allowed'})
            address = env.get('REMOTE_ADDR','unknown')  # Never trust arbitrary X-Forwarded-For.
            if address in self.trusted_proxies:
                # The configured proxy MUST overwrite this header with the immediate client IP.
                try:
                    address = str(ipaddress.ip_address(env.get('HTTP_X_REAL_IP','')))
                except ValueError:
                    return respond(400, {'error':'Proxy client address missing'})
            if path == '/api/health' and method == 'GET':
                return respond(200, {'ready':True,'storage':'configured'})
            if path == '/api/leads' and method == 'POST':
                if self.limited(('intake',address), 10):
                    return respond(429, {'error':'Too many requests. Please contact us directly.'})
                payload = self.body(env)
                if not isinstance(payload, dict):
                    raise ValueError('Expected an inquiry object')
                if payload.get('website'):
                    raise ValueError('Unable to accept this inquiry')
                lead_id, duplicate = self.store.create(payload, env.get('HTTP_IDEMPOTENCY_KEY',''))
                return respond(200 if duplicate else 201, {'id':lead_id,'saved':True,'duplicate':duplicate})
            if path == '/api/login' and method == 'POST':
                if self.limited(('login',address), 5, 900):
                    return respond(429, {'error':'Wait before trying again'})
                payload = self.body(env)
                if not isinstance(payload,dict) or not self.admin_hash:
                    return respond(503, {'error':'Owner access is not configured'})
                password = payload.get('password','')
                if not isinstance(password,str) or len(password)>512 or not password_matches(password,self.admin_hash):
                    return respond(401, {'error':'Invalid sign-in'})
                token = secrets.token_urlsafe(32)
                with self.lock:
                    self.sessions[token] = {'csrf':secrets.token_urlsafe(32),'expires':time.monotonic()+28800}
                cookie = f'angsumi_session={token}; HttpOnly; SameSite=Strict; Path=/; Max-Age=28800'
                if not self.development:
                    cookie += '; Secure'
                return respond(200, {'signed_in':True}, extra=[('Set-Cookie',cookie)])
            if path.startswith('/unsubscribe/') and method in ('GET','POST'):
                token = path.rsplit('/',1)[-1]
                if not re.fullmatch(r'[A-Za-z0-9_-]{40,60}',token):
                    return respond(404,'Link not found','text/plain')
                if method == 'GET':
                    return respond(200,'<!doctype html><html lang="en"><meta name="viewport" content="width=device-width"><title>Stop follow-ups</title><h1>Stop promotional follow-ups</h1><p>Your inquiry and project-related communication remain available.</p><form method="post"><button>Unsubscribe</button></form></html>','text/html')
            if path.startswith('/api/admin') or path.startswith('/admin') or path.startswith('/unsubscribe/'):
                if path.startswith('/unsubscribe/'):
                    # A standard form POST has an Origin but no JSON body; token is the sole capability.
                    self.store.unsubscribe(token)
                    return respond(200,'Promotional follow-ups stopped.','text/plain')
                session_token, session = self.session(env)
                if not session:
                    return respond(401, {'error':'Sign in at /login/'}) if path.startswith('/api/') else self.static('backend/login.html', respond, private=True)
                if method in ('POST','PATCH') and not hmac.compare_digest(env.get('HTTP_X_CSRF_TOKEN',''),session['csrf']):
                    return respond(403, {'error':'Invalid session token'})
                if path == '/api/admin/session' and method == 'GET':
                    return respond(200, {'csrf':session['csrf'],'statuses':STATUSES})
                if path == '/api/admin/logout' and method == 'POST':
                    with self.lock:
                        self.sessions.pop(session_token, None)
                    return respond(200, {'signed_out':True},extra=[('Set-Cookie','angsumi_session=; HttpOnly; SameSite=Strict; Path=/; Max-Age=0'+('' if self.development else '; Secure'))])
                if path == '/api/admin/leads' and method == 'GET':
                    return respond(200, {'leads':self.store.list()})
                if path == '/api/admin/reporting' and method == 'GET':
                    return respond(200, self.store.reporting())
                if path == '/api/admin/export' and method == 'GET':
                    output=io.StringIO(); writer=csv.writer(output)
                    writer.writerow(['id','received','category','name','email','source','status','priority','budget','revenue_inr'])
                    for lead in self.store.list():
                        data=lead['data']
                        cells=[lead['id'],lead['created_at'],data['category'],data['name'],data['email'],data['source'],lead['status'],lead['priority'],data['budget'],lead['revenue']]
                        writer.writerow(["'"+str(v) if str(v).lstrip().startswith(('=','+','-','@')) else v for v in cells])
                    return respond(200,output.getvalue(),'text/csv; charset=utf-8',extra=[('Content-Disposition','attachment; filename="angsumi-leads.csv"')])
                match = re.fullmatch(r'/api/admin/leads/(ANG-[A-F0-9]{16})',path)
                if match and method in ('GET','PATCH'):
                    return respond(200, self.store.get(match[1]) if method=='GET' else self.store.update(match[1],self.body(env)))
                if path in ('/admin','/admin/') and method in ('GET','HEAD'):
                    return self.static('backend/admin.html',respond,private=True)
                return respond(404, {'error':'Not found'})
            if path in ('/login','/login/') and method in ('GET','HEAD'):
                return self.static('backend/login.html',respond,private=True)
            if method not in ('GET','HEAD'):
                return respond(404, {'error':'Not found'})
            return self.static(path.lstrip('/') or 'index.html',respond)
        except (ValueError, TypeError, UnicodeError):
            return respond(400, {'error':'Check required fields, email, consent and submission details.'})
        except KeyError:
            return respond(404, {'error':'Lead not found'})
        except Exception:
            return respond(500, {'error':'Request failed. Please retry or contact us directly.'})

    @staticmethod
    def static(path, respond, private=False):
        parts=Path(path).parts
        if not private and (not parts or (parts[0] not in PUBLIC_DIRS and path not in PUBLIC_FILES)):
            return respond(404, {'error':'Not found'})
        target=(ROOT/path).resolve()
        if not target.is_relative_to(ROOT) or '..' in parts or any(p.startswith('.') for p in parts):
            return respond(404, {'error':'Not found'})
        if not private and target.relative_to(ROOT).parts[0] not in PUBLIC_DIRS and path not in PUBLIC_FILES:
            return respond(404, {'error':'Not found'})
        if target.is_dir():
            target=target/'index.html'
        if not target.is_file():
            return respond(404, {'error':'Not found'})
        return respond(200,target.read_bytes(),mimetypes.guess_type(str(target))[0] or 'application/octet-stream')


def from_environment():
    development=os.getenv('ANGSUMI_DEVELOPMENT')=='1'
    location=os.getenv('LEAD_DB_PATH','')
    if not location:
        raise RuntimeError('Set LEAD_DB_PATH to a private durable volume outside the public checkout')
    resolved=Path(location).resolve()
    if resolved.is_relative_to(ROOT):
        raise RuntimeError('Database must be outside the public checkout')
    origins=[o.strip() for o in os.environ.get('ALLOWED_ORIGINS','').split(',') if o.strip()]
    if not origins or any(not o.startswith('https://') for o in origins) and not development:
        raise RuntimeError('Configure exact HTTPS ALLOWED_ORIGINS')
    proxies=[ip.strip() for ip in os.getenv('TRUSTED_PROXY_IPS','').split(',') if ip.strip()]
    for ip in proxies:
        ipaddress.ip_address(ip)
    return App(Store(resolved),origins,os.getenv('ADMIN_PASSWORD_HASH',''),development,proxies)


class QuietHandler(WSGIRequestHandler):
    def log_message(self, *args):
        pass  # Do not log unsubscribe tokens, query strings, or intake fields.


if __name__=='__main__':
    port=int(os.getenv('PORT','8765'))
    app=from_environment()
    print(f'Local preview: http://127.0.0.1:{port}',flush=True)
    with make_server('127.0.0.1',port,app,handler_class=QuietHandler) as server:
        server.serve_forever()
