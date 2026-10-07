from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from project_path import ROOT
from knowledge_app.ingestion import parse_document
units=parse_document('equipment.pdf',(ROOT/'data/documents/equipment.pdf').read_bytes())
print('可提取文字页数',len(units),'页码',[u['page']for u in units])
