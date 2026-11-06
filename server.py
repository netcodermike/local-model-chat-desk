import argparse,json,unittest
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
from core import validate,request
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**k):super().__init__(*a,directory=str(Path(__file__).parent),**k)
 def reply(self,code,data):
  body=json.dumps(data).encode();self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
 def do_GET(self):
  if self.path=='/api/models':
   try:self.reply(200,request('tags'))
   except Exception:self.reply(503,{'error':'Ollama unavailable. Start it locally and install a model.'})
  elif self.path.startswith('/api/'):self.reply(404,{'error':'Unknown API route'})
  else:super().do_GET()
 def do_POST(self):
  if self.path!='/api/chat':return self.reply(404,{'error':'Unknown route'})
  if self.headers.get('Host')not in('127.0.0.1:8080','localhost:8080'):return self.reply(403,{'error':'Loopback host required'})
  origin=self.headers.get('Origin')
  if origin and origin not in('http://127.0.0.1:8080','http://localhost:8080'):return self.reply(403,{'error':'Same-origin request required'})
  try:
   size=int(self.headers.get('Content-Length','0'))
   if size<1 or size>100000:raise ValueError('Request must be 1–100000 bytes')
   self.reply(200,request('chat',validate(json.loads(self.rfile.read(size)))))
  except(ValueError,TypeError,KeyError)as e:self.reply(400,{'error':str(e)})
  except Exception:self.reply(503,{'error':'Local model request failed. Check Ollama and the selected model.'})
class Tests(unittest.TestCase):
 def test_requests(self):
  self.assertFalse(validate({'model':'demo','messages':[{'role':'user','content':'x'}]})['stream']);self.assertRaises(ValueError,validate,{'model':'','messages':[]});self.assertRaises(ValueError,validate,{'model':'x','messages':[{'role':'tool','content':'x'}]})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--self-test',action='store_true');a=p.parse_args()
 if a.self_test:unittest.main(argv=['chat'])
 else:print('Open http://127.0.0.1:8080 · localhost Ollama only',flush=True);ThreadingHTTPServer(('127.0.0.1',8080),Handler).serve_forever()
