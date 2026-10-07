"""没有文件写入、任意网络请求或系统命令入口的两个工具。"""
import ast
import math
import operator
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"31-rag/examples"))
from embedding import Embedder
from retrieval import load_index,search

DEFINITIONS=[
    {"type":"function","function":{"name":"calculate","description":"对已确定的数字做加减乘除及括号运算。不能执行代码。",
     "parameters":{"type":"object","properties":{"expression":{"type":"string"}},"required":["expression"],"additionalProperties":False}}},
    {"type":"function","function":{"name":"search_documents","description":"只读搜索柳叶学习室教学资料，返回原文、文件名和行号。query用包含机构与所需事实的完整自然语言问题，一次合并相关事实，避免拆成短关键词。",
     "parameters":{"type":"object","properties":{"query":{"type":"string"}},"required":["query"],"additionalProperties":False}}},
]
OPS={ast.Add:operator.add,ast.Sub:operator.sub,ast.Mult:operator.mul,ast.Div:operator.truediv}


def calculate(expression):
    if not isinstance(expression,str) or not expression.strip() or len(expression)>80:
        raise ValueError("表达式必须为1至80字符")
    try:tree=ast.parse(expression,mode="eval")
    except SyntaxError:raise ValueError("表达式语法错误")from None
    if len(list(ast.walk(tree)))>25:raise ValueError("表达式节点过多")
    def evaluate(node):
        if isinstance(node,ast.Constant)and type(node.value)in(int,float):
            value=node.value
        elif isinstance(node,ast.UnaryOp)and isinstance(node.op,(ast.UAdd,ast.USub)):
            value=evaluate(node.operand)*(1 if isinstance(node.op,ast.UAdd)else -1)
        elif isinstance(node,ast.BinOp)and type(node.op)in OPS:
            try:value=OPS[type(node.op)](evaluate(node.left),evaluate(node.right))
            except ZeroDivisionError:raise ValueError("不能除以0")from None
        else:raise ValueError("只允许数值、括号和加减乘除")
        if not math.isfinite(value)or abs(value)>1e9:raise ValueError("计算值必须有限且绝对值不超过十亿")
        return value
    return {"value":evaluate(tree.body)}


class LocalSearch:
    def __init__(self):
        self.encoder=Embedder()
        root=Path(__file__).resolve().parents[2]/"31-rag"
        self.data,self.vectors=load_index(root/"results/index",root/"data/documents",self.encoder.revision)

    def __call__(self,query):
        if not isinstance(query,str)or not query.strip()or len(query)>200:raise ValueError("查询必须为1至200字符")
        hits=search(self.data,self.vectors,self.encoder.encode([query],query=True)[0])
        return {"hits":[{key:hit[key]for key in("chunk_id","source","line_start","line_end","text","score")}for hit in hits]}


def dispatch(name,arguments,local_search):
    if name not in("calculate","search_documents"):raise ValueError("工具未获授权")
    if not isinstance(arguments,dict):raise ValueError("工具参数必须是对象")
    key="expression"if name=="calculate"else"query"
    if set(arguments)!={key}:raise ValueError("工具参数字段不匹配")
    return calculate(arguments[key])if name=="calculate"else local_search(arguments[key])
