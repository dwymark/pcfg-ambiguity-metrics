#!python3
import grammar
from nltk.corpus import treebank
from nltk.treetransforms import chomsky_normal_form, collapse_unary
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader.bracket_parse import CategorizedBracketParseCorpusReader

import pickle

def trained_pcfg():
  try:
    with open("pcfgcache.pkl",'rb') as input:
      print("Loading the PCFG...")
      gram = pickle.load(input)
    print("Loaded!")
    return gram
  except FileNotFoundError:
    print("Training the PCFG...")
    ptb = LazyCorpusLoader( # Penn Treebank v3: WSJ 
    'ptb', CategorizedBracketParseCorpusReader, r'wsj/\d\d/wsj_\d\d\d\d.mrg',
    cat_file='allcats.txt', tagset='wsj')
    productions = []
    tb = treebank
    # Search for nltk_data/corpora/ptb and place all the wsj/XX/*.mrg files in 
    useFullTreeBank = True
    n = 0                   # check progress of training
    if useFullTreeBank:
      tb = ptb
    print("Counting Sentences...")
    numSentences = len(tb.parsed_sents())
    print("Done. Parsing corpus...")
    for t in tb.parsed_sents(): 
      if n % 200 == 0:
        print("{:.2f}% complete".format((n/numSentences)*100))
      collapse_unary(t,True)
      chomsky_normal_form(t,vertMarkov = 3)
      n = n + 1
      for p in t.productions():
        productions.append(p)
    print("Building grammar...")
    gram = grammar.induce_pcfg(grammar.Nonterminal('S'), productions)
    print("Built.")
    print("Writing the PCFG...")
    with open("pcfgcache.pkl",'wb') as output:
      pickle.dump(gram, output, -1)
    print("Write successful!")
    return gram

if __name__ == '__main__':
  tb_pcfg = trained_pcfg()
