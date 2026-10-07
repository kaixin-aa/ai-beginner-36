"""教学用英文词频统计，使用 Python 标准库。"""
import re


def tokenize(text):
    """只提取英文字母，保留词中间的直撇号，统一为小写。"""
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def count_words(text):
    """返回统计字典，不读写文件，也不打印。"""
    words = tokenize(text)
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    frequencies = []
    for word, count in ordered:
        frequencies.append({"word": word, "count": count})
    return {
        "total_words": len(words),
        "unique_words": len(counts),
        "frequencies": frequencies,
    }
