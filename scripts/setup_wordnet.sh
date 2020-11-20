curl -L http://compling.hss.ntu.edu.sg/wnja/data/1.1/jpn_wn_lmf.xml.gz -o data/wordnet-jp.xml.gz
melt data/wordnet-jp.xml.gz
python -m xmljson -d yahoo data/wordnet-jp.xml > data/wordnet-jp.json
