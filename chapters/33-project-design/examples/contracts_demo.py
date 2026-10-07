from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[3]/'projects/knowledge-assistant'))
from knowledge_app.contracts import FilePolicy,AskRequest,Citation
from knowledge_app.plan import describe
