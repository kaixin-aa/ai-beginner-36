import json
from pathlib import Path
import sys
from urllib.request import Request,urlopen
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from web_fixture import fixture
with fixture()as(base,service):
    request=Request(base+'/api/documents',data=json.dumps({'filename':'notes.txt','content_base64':'QQ=='}).encode(),headers={'Content-Type':'application/json'})
    urlopen(request)
