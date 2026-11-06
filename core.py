import json,urllib.request
def validate(body):
 if not isinstance(body,dict)or not isinstance(body.get('model'),str)or not body['model'].strip():raise ValueError('Choose an installed model')
 messages=body.get('messages')
 if not isinstance(messages,list)or not 1<=len(messages)<=100:raise ValueError('Use 1–100 messages')
 if any(not isinstance(m,dict)or m.get('role')not in('user','assistant','system')or not isinstance(m.get('content'),str)or len(m['content'])>20000 for m in messages):raise ValueError('Invalid message')
 return {'model':body['model'],'messages':messages,'stream':False}
def request(path,payload=None):
 req=urllib.request.Request('http://127.0.0.1:11434/api/'+path,data=None if payload is None else json.dumps(payload).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=180)as response:return json.load(response)
