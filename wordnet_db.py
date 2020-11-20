import sqlite3
from collections import namedtuple

conn = sqlite3.connect("./data/wordnet-jp.db")

Word = namedtuple("Word", "wordid lang lemma pron pos")


def getWords(lemma):
    cur = conn.execute("select * from word where lemma=?", (lemma,))
    return [Word(*row) for row in cur]


Sense = namedtuple("Sense", "synset wordid lang rank lexid freq src")


def getSenses(word):
    cur = conn.execute("select * from sense where wordid=?", (word.wordid,))
    return [Sense(*row) for row in cur]


Synset = namedtuple("Synset", "synset pos name src")


def getSynset(synset):
    cur = conn.execute("select * from synset where synset=?", (synset,))
    return Synset(*cur.fetchone())


def getWordsFromSynset(synset, lang):
    cur = conn.execute(
        "select word.* from sense, word where synset=? and word.lang=? and sense.wordid = word.wordid;",
        (synset, lang),
    )
    return [Word(*row) for row in cur]


def getWordsFromSenses(sense, lang="jpn"):
    synonym = {}
    for s in sense:
        lemmas = []
        syns = getWordsFromSynset(s.synset, lang)
        for sy in syns:
            lemmas.append(sy.lemma)
        synonym[getSynset(s.synset).name] = lemmas
    return synonym


def getSynonym(word):
    synonym = {}
    words = getWords(word)
    if words:
        for w in words:
            sense = getSenses(w)
            s = getWordsFromSenses(sense)
            synonym = dict(list(synonym.items()) + list(s.items()))
    synonym = sorted({x for v in synonym.values() for x in v if x != word})
    return synonym

def getHypernym(word):
    hypernym = {}
    words = getWords(word)
    if words:
        for w in words:
            pass
    return hypernym
