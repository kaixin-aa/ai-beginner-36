from pathlib import Path
import sys
import tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from project_path import ROOT
from knowledge_app.storage import Store
from knowledge_app.embedding import Embedder
from knowledge_app.indexing import build_index,load_index
with tempfile.TemporaryDirectory()as folder:
    store=Store(folder);encoder=Embedder()
    store.import_document('guide.md',(ROOT/'data/documents/guide.md').read_bytes())
    build_index(store,encoder)
    store.import_document('equipment.pdf',(ROOT/'data/documents/equipment.pdf').read_bytes())
    load_index(store,encoder)
