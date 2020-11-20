from pathlib import Path
from argparse import ArgumentParser

from wordnet_json import load_words
from wordnet_db import getSynonym


def main(args):
    if args.mode == "synonym":
        with Path(args.output_path).open("w") as f:
            for word in load_words():
                synonym = getSynonym(word)
                if len(synonym) == 0:
                    continue
                f.write(f"{word}\t{' '.join(synonym)}\n")
    else:
        raise ValueError(f"No such mode '{args.mode}''")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--output_path", "-o", type=str)
    parser.add_argument("--mode", "-m", type=str)

    args = parser.parse_args()
    main(args)
