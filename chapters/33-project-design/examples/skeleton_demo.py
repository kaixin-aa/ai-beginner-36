import json
from pathlib import Path
import sys
PROJECT=Path(__file__).resolve().parents[3]/'projects/knowledge-assistant'
sys.path.insert(0,str(PROJECT))
from knowledge_app.contracts import FilePolicy,AskRequest,Citation
from knowledge_app.plan import describe

def run():
    policy=FilePolicy()
    accepted=[policy.validate(name,size)for name,size in [('guide.txt',10),('notes.md',100),('rules.pdf',200)]]
    rejected=[]
    for name,size in [('empty.txt',0),('../secret.txt',10),('program.exe',10),('huge.pdf',1_000_001)]:
        try:policy.validate(name,size)
        except ValueError as error:rejected.append({'filename':name,'reason':str(error)})
        else:raise AssertionError('应拒绝的上传被接受')
    try:AskRequest('   ')
    except ValueError:empty_rejected=True
    else:raise AssertionError('空问题被接受')
    citation=Citation('a'*64,'guide.md',None,11,11,70,78,'借阅期限为14天')
    result={'stage':'design_skeleton','accepted_extensions':accepted,'rejected_inputs':rejected,
            'empty_question_rejected':empty_rejected,'citation_sample_is_author_constructed':True,
            'citation_filename':citation.filename,'plan':describe()}
    root=Path(__file__).resolve().parents[1]/'results';root.mkdir(exist_ok=True)
    (root/'skeleton-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('骨架参数检查',len(accepted),'种接收',len(rejected),'种拒绝；空问题拒绝；业务模块仍待实现')

if __name__=='__main__':run()
