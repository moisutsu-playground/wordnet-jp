bash scripts/conda_init.sh
bash scripts/setup_wordnet.sh

python main.py -o corpus/synonym.tsv -m synonym
python main.py -o corpus/hypernym.tsv -m hypernym
