from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from project_path import ROOT
from knowledge_app.ingestion import parse_document
parse_document('image-only.pdf',(ROOT/'data/invalid/image-only.pdf').read_bytes())
