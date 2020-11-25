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


# Key: 下位語(str), value: 上位語(List[str])
to_hypernym_dict = None


def init_to_hypernym_dict():
    global to_hypernym_dict
    to_hypernym_dict = {}
    cur = conn.execute("select synset1,synset2 from synlink where link='hypo'")
    for row in cur:
        n_term = row[0]
        b_term = row[1]

        if b_term not in to_hypernym_dict:
            to_hypernym_dict[b_term] = []

        to_hypernym_dict[b_term].append(n_term)


# Key: 上位語(str), value: 下位語(List[str])
to_hyponym_dict = None


def init_to_hyponym_dict():
    global to_hyponym_dict
    to_hyponym_dict = {}
    cur = conn.execute("select synset1,synset2 from synlink where link='hypo'")
    for row in cur:
        b_term = row[0]
        n_term = row[1]

        if b_term not in to_hyponym_dict:
            to_hyponym_dict[b_term] = []

        to_hyponym_dict[b_term].append(n_term)


def getHypernym(word):
    if to_hypernym_dict is None:
        init_to_hypernym_dict()
    hypernym = []
    words = getWords(word)
    if words:
        for w in words:
            senses = getSenses(w)
            for sense in senses:
                if not sense.synset in to_hypernym_dict:
                    return []
                hypersynsets = to_hypernym_dict[sense.synset]
                for hypersynset in hypersynsets:
                    hyper_words = getWordsFromSynset(hypersynset, "jpn")
                    hypernym.extend(
                        [
                            hyper_word.lemma
                            for hyper_word in hyper_words
                            if hyper_word.lemma != word
                        ]
                    )
    hypernym = list(set(hypernym))
    return hypernym


def getCohyponym(word):
    if to_hypernym_dict is None:
        init_to_hypernym_dict()
    if to_hyponym_dict is None:
        init_to_hyponym_dict()

    cohyponym = []

    words = getWords(word)
    if words:
        for w in words:
            senses = getSenses(w)
            hyponym_synsets = []
            for sense in senses:
                if not sense.synset in to_hypernym_dict:
                    return []
                hyper_synsets = to_hypernym_dict[sense.synset]

                for hyper_synset in hyper_synsets:
                    hyponym_synsets.extend(to_hyponym_dict[hyper_synset])

            hyponym_synsets = list(
                set(
                    [
                        hyponym_synset
                        for hyponym_synset in hyponym_synsets
                        if not hyponym_synset in [sense.synset for sense in senses]
                    ]
                )
            )
            for hyponym_synset in hyponym_synsets:
                cohypo_words = getWordsFromSynset(hyponym_synset, "jpn")
                cohyponym.extend(
                    cohypo_word.lemma
                    for cohypo_word in cohypo_words
                    if cohypo_word.lemma != word
                )

    cohyponym = list(set(cohyponym))
    return cohyponym
