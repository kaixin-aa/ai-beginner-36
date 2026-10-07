"""只汇总已发生的真实请求、离线引用核对及新环境验收，不再请求模型。"""
import csv
from decimal import Decimal
import json
import statistics
from project_path import COURSE,ROOT
PRICE_URL='https://api-docs.deepseek.com/zh-cn/quick_start/pricing/?article_id=article_1779470751466_8'
def load(path):return json.loads(path.read_text(encoding='utf-8'))

def collect_usage():
    source=load(COURSE/'chapters/34-document-retrieval/results/live-project-20261004-022408-935901.json')
    rows=[]
    for item in source['records']:
        result=item['result'];response=result.get('response')
        if not response:continue
        assert response['kind']=='live_api'
        usage=response['usage'];assert usage['prompt_tokens']+usage['completion_tokens']==usage['total_tokens']
        rows.append({'source':'chapter34','case_id':item['case']['id'],'original_status':result['status'],**usage,'elapsed_seconds':result['elapsed_seconds']})
    browser=load(COURSE/'chapters/35-web-deployment/results/browser-checks.json')
    answer=browser['real_answer'];usage=answer['usage'];assert browser['real_api_requests']==1
    rows.append({'source':'chapter35-browser','case_id':'projector-return-web','original_status':answer['status'],**usage,'elapsed_seconds':answer['elapsed_seconds']})
    return rows

def write_csv(path,rows,fields):
    with path.open('w',encoding='utf-8-sig',newline='')as file:
        writer=csv.DictWriter(file,fieldnames=fields);writer.writeheader();writer.writerows(rows)

def run():
    results=ROOT/'results';results.mkdir(exist_ok=True);rows=collect_usage()
    write_csv(results/'request-costs.csv',rows,list(rows[0]))
    prompt=sum(r['prompt_tokens']for r in rows);completion=sum(r['completion_tokens']for r in rows)
    total=sum(r['total_tokens']for r in rows);assert(prompt+completion,total)==(5080,5080)
    lower=(Decimal(prompt)*Decimal('0.02')+Decimal(completion)*4)/1_000_000
    upper=(Decimal(prompt)+Decimal(completion)*4)/1_000_000
    cost={'price_checked_on':'2026-10-04','price_source':PRICE_URL,'model':'deepseek-flash','period':'空闲时段，执行日期为周日',
          'rates_cny_per_million':{'input_cache_hit':'0.02','input_cache_miss':'1','output':'4'},
          'requests':len(rows),'prompt_tokens':prompt,'completion_tokens':completion,'total_tokens':total,
          'estimated_cny_min':str(lower),'estimated_cny_max':str(upper),'actual_debit_known':False,
          'reason':'记录没有缓存命中拆分，也未读取账单；范围按查询时公开价目估算，不能当成实际扣款。',
          'latency_seconds':{'n':len(rows),'median':statistics.median(r['elapsed_seconds']for r in rows),'min':min(r['elapsed_seconds']for r in rows),'max':max(r['elapsed_seconds']for r in rows)},
          'new_api_requests_in_this_summary':0}
    (results/'cost-summary.json').write_text(json.dumps(cost,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    checked=load(COURSE/'chapters/34-document-retrieval/results/revalidated-answers.json')
    scores=[]
    for item in checked['records']:
        assert item['expected_matched']
        value=item['validated'];scores.append({'case_id':item['case_id'],'original_status':item['original_status'],'current_status':value['status'],
            'facts_match':1,'status_match':1,'citation_match':1 if value['citations']else'不适用',
            'note':'编写助手按保存文件核对，非用户亲自评分；修复后离线核对'if item['original_status']!=value['status']else'编写助手按保存文件核对，非用户亲自评分'})
    fields=list(scores[0]);write_csv(results/'editor-scores.csv',scores,fields)
    questions={item['id']:item['question']for item in load(COURSE/'chapters/34-document-retrieval/data/questions.json')}
    template=[{'case_id':r['case_id'],'question':questions[r['case_id']],'facts_score':'','citation_score':'','status_score':'','reviewer':'','notes':''}for r in scores]
    write_csv(results/'manual-score-template.csv',template,list(template[0]))
    fresh=load(COURSE/'chapters/35-web-deployment/results/fresh-environment.json')
    assert fresh['all_passed']and fresh['fresh_cli_server_started']['http_status']==200
    report={'fixed_questions':7,'current_expected_matches':7,'original_expected_matches':6,'backend_tests':15,'web_tests':7,'project_tests':22,
            'fresh_environment_passed':True,'browser_actions_checked':9,'real_api_requests':7,'total_tokens':5080,
            'online_deployment_performed':False,'container_built':False,'local_project_accepted':True,'new_api_requests':0}
    (results/'final-project-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(cost,ensure_ascii=False));print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':run()
