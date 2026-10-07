"""用修复后的校验器核对原始真实响应，不重新请求模型。"""
import json
from project_path import ROOT
from knowledge_app.storage import Store
from knowledge_app.qa import validate_answer

def recheck():
    files=sorted((ROOT/'results').glob('live-project-*.json'))
    if not files:raise ValueError('尚无真实请求记录')
    file=files[-1];original=json.loads(file.read_text(encoding='utf-8'));store=Store(ROOT/'results/runtime')
    records=[]
    for item in original['records']:
        case=item['case'];old=item['result']
        if old.get('response'):
            response=old['response']
            if not response['complete']:raise ValueError('原响应被截断')
            validated=validate_answer(response['answer'],old['hits'],store)
        else:validated={key:old[key]for key in('status','answer','citations')}
        matched=validated['status']==case['expected_status']and all(t in validated['answer']for t in case['expected_terms'])
        if 'expected_filename'in case:matched=matched and any(c['filename']==case['expected_filename']and c['page']==case.get('expected_page')for c in validated['citations'])
        records.append({'case_id':case['id'],'original_status':old['status'],'validated':validated,'expected_matched':matched})
    result={'kind':'offline_revalidation','original_file':file.name,'new_api_requests':0,'original_request_count':original['request_count'],
            'original_total_tokens':original['total_tokens'],'all_expected_matched':all(r['expected_matched']for r in records),'records':records}
    (ROOT/'results/revalidated-answers.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('修复后离线验证',[(r['case_id'],r['expected_matched'])for r in records])
    assert result['all_expected_matched']

if __name__=='__main__':recheck()
