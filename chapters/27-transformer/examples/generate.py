import argparse
import json
from toy_transformer import ROOT,load_model,generate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("--max-new-tokens",type=int,default=12)
    args = parser.parse_args()
    try:
        model,tokenizer = load_model(ROOT/"results/tiny-transformer.pt")
        result = generate(model,tokenizer,args.prompt,max_new_tokens=args.max_new_tokens)
    except ValueError as error:
        parser.error(str(error))
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == "__main__": main()
