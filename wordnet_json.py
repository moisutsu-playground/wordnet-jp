import json
from pathlib import Path

def load_words():
    json_path = Path("data/wordnet-jp.json")
    json_open = json_path.open()
    json_dict = json.load(json_open)
    for entry in json_dict["LexicalResource"]["Lexicon"]["LexicalEntry"]:
        yield entry["Lemma"]["writtenForm"]
