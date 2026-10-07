from contextlib import contextmanager
import tempfile
import threading
from project_path import ROOT
from knowledge_app.web_service import Service,make_server
@contextmanager
def fixture():
    with tempfile.TemporaryDirectory(prefix='ai36-http-demo-')as folder:
        service=Service(folder);server=make_server(service,0);thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:yield f'http://127.0.0.1:{server.server_port}',service
        finally:server.shutdown();server.server_close();thread.join()
