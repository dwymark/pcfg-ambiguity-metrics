#!python3
import nltk.grammar as grammar
from nltk.corpus import treebank
from nltk.treetransforms import chomsky_normal_form, collapse_unary

def trained_pcfg():
#  try:
#    f = open("pcfgcache.txt",'r')
#    gram = PCFG.from_string(f.read())
#    f.close()
#    return gram
#  except FileNotFoundError:
    #f = open("pcfgcache.txt",'w')
    print("Training the PCFG...")
    productions = []
    for t in treebank.parsed_sents():
      collapse_unary(t,True)
      chomsky_normal_form(t)
      print(t)
      t.draw()
      for p in t.productions():
        productions.append(p)
    gram = grammar.induce_pcfg(grammar.Nonterminal('S'), productions)
    print("Trained!")
    #f.close()
    return gram

if __name__ == '__main__':
  tb_pcfg = trained_pcfg()
