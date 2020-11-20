from pathlib import Path
from argparse import ArgumentParser

from wordnet_json import load_words
from wordnet_db import getSynonym, getHypernym


def main(args):
    if args.mode == "synonym":
        with Path(args.output_path).open("w") as f:
            for word in load_words():
                synonym = getSynonym(word)
                if len(synonym) == 0:
                    continue
                f.write(f"{word}\t{' '.join(synonym)}\n")
    elif args.mode == "hypernym":
        with Path(args.output_path).open("w") as f:
            for word in load_words():
                hypernym = getHypernym(word)
                if len(hypernym) == 0:
                    continue
                f.write(f"{word}\t{' '.join(hypernym)}\n")
    else:
        raise ValueError(f"No such mode '{args.mode}''")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output_path", "-o", type=str)
    parser.add_argument("--mode", "-m", type=str)

    args = parser.parse_args()
    main(args)
