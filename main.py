#!python3
import nltk.grammar as grammar
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
    # Search for nltk_data/corpora/ptb and place all the wsj/XX/*.mrg files in 
    useFullTreeBank = True
    if useFullTreeBank:
      for t in ptb.parsed_sents(): 
        collapse_unary(t,True)
        chomsky_normal_form(t)
        #t.draw()
        for p in t.productions():
          productions.append(p)  
    else:
      for t in treebank.parsed_sents():
        collapse_unary(t,True)
        chomsky_normal_form(t)
        #t.draw()
        for p in t.productions():
          productions.append(p)
    gram = grammar.induce_pcfg(grammar.Nonterminal('S'), productions)
    print("Trained!")
    print("Writing the PCFG...")
    with open("pcfgcache.pkl",'wb') as output:
      pickle.dump(gram, output, -1)
    print("Write successful!")
    return gram

if __name__ == '__main__':
  tb_pcfg = trained_pcfg()
