CELLS = [
    ("markdown","# 文字表示与相似度实验\n全部句子和主题向量为原创教学设定。词向量手工指定，没有下载或训练语义模型。"),
    ("code","from examples.text_core import *\nimport numpy as np\ndata = load_data()\nprint(np.__version__)\nprint(data['dimensions'])"),
    ("code","text = data['sentences'][0]\nvector, tokens, ids = sentence_vector(text,data['vectors'])\nprint(text)\nprint(list(text))\nprint(tokens)\nprint(ids)\nprint(vector)"),
    ("code","rules,splits,alphabet = train_bpe(data['bpe_word_counts'])\nfor rule in rules: print(rule)\nprint(splits)\nprint('newlow',tokenize_bpe('newlow',rules,alphabet))"),
    ("code","chars,counts = character_vectors(data['sentences'])\nencoded = [sentence_vector(text,data['vectors'])[0] for text in data['sentences']]\nfor i,j,case in data['pairs']:\n    print(case,round(cosine(counts[i],counts[j]),6),round(cosine(encoded[i],encoded[j]),6))"),
    ("code","print(data['sentences'][6],data['sentences'][7])\nprint(cosine(encoded[6],encoded[7]))\nassert cosine(encoded[6],encoded[7]) == 1\nprint('高分没有检查否定关系')"),
    ("code","print('尺度变大而方向不变',cosine(np.array([1,2]),np.array([10,20])))\nprint('正交',cosine([1,0],[0,1]))\nprint('相反',cosine([1,0],[-1,0]))"),
    ("markdown","## 结果边界\n字符分数考察重合。人工向量只保留预设主题，丢掉词序和否定信息。若换成训练好的语义模型，应单独核对模型版本、许可和实测，不能沿用本章数值。"),
]
