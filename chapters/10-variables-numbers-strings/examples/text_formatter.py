def build_learning_card(raw_title, raw_author, raw_tag):
    title = raw_title.strip()
    author = raw_author.strip()
    tag = raw_tag.strip().upper()

    card = f"[{tag}] {title} | 作者 {author}"
    return card, len(title)


def main():
    raw_title = input("文章标题：")
    raw_author = input("作者名称：")
    raw_tag = input("英文标签：")

    card, title_length = build_learning_card(raw_title, raw_author, raw_tag)

    print()
    print(card)
    print(f"标题长度：{title_length} 个字符")
    print(card.replace(" | ", "\n"))


if __name__ == "__main__":
    main()
