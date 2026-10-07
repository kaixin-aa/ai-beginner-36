import sys
from pathlib import Path
COURSE=Path(__file__).resolve().parents[3];PROJECT=COURSE/'projects/knowledge-assistant';ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(PROJECT))
