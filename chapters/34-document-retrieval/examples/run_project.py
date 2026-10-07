"""固定文档和问题端到端验证，默认仅检索，--live才发出真实请求。"""
import argparse
from datetime import datetime
import json
from project_path import ROOT
from knowledge_app.storage import Store
from knowledge_app.embedding import Embedder
from knowledge_app.indexing import build_index,load_index,retrieve
from knowledge_app.qa import ask
from knowledge_app.chat import live_chat

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--live',action='store_true');args=parser.parse_args()
    store=Store(ROOT/'results/runtime');encoder=Embedder()
    imports=[store.import_document(file.name,file.read_bytes())for file in sorted((ROOT/'data/documents').iterdir())]
    indexed=build_index(store,encoder)
    metadata,vectors=load_index(store,encoder)
    cases=json.loads((ROOT/'data/questions.json').read_text(encoding='utf-8'))
    records=[]
    for case in cases:
        if args.live:
            result=ask(store,encoder,case['question'],lambda messages:live_chat()(messages))
            citations=result['citations']
            matched=result['status']==case['expected_status']and all(t in result['answer']for t in case['expected_terms'])
            if 'expected_filename'in case:matched=matched and any(c['filename']==case['expected_filename']and c['page']==case.get('expected_page')for c in citations)
        else:
            hits=retrieve(metadata,vectors,encoder.encode([case['question']],query=True)[0])
            result={'hits':hits,'model_called':False,'kind':'retrieval_only'};matched=None
        records.append({'case':case,'result':result,'expected_matched':matched})
    result={'kind':'live_api'if args.live else'retrieval_only','index':indexed,'imports':[{'filename':i['document']['filename'],'duplicate':i['duplicate']}for i in imports],
            'records':records,'request_count':sum(r['result'].get('request_attempted',False)for r in records),
            'total_tokens':sum((r['result'].get('usage')or{}).get('total_tokens',0)for r in records),
            'all_expected_matched':all(r['expected_matched']for r in records)if args.live else None}
    name=('live-project-'+datetime.now().strftime('%Y%m%d-%H%M%S-%f')if args.live else'retrieval-results')+'.json'
    output=ROOT/'results'/name;output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(indexed)
    print([(r['case']['id'],r['result'].get('status','retrieved'),r['expected_matched'])for r in records])
    print('实际请求',result['request_count'],'Token',result['total_tokens'],'文件',name)
    return 1 if args.live and not result['all_expected_matched']else 0

if __name__=='__main__':raise SystemExit(main())
