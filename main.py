#!python3
import nltk.grammar as grammar
from nltk.corpus import treebank
from nltk.treetransforms import chomsky_normal_form

def trained_pcfg():
  try:
    f = open("pcfgcache.txt",'r')
    gram = PCFG.from_string(f.read())
    f.close()
    return gram
  except FileNotFoundError:
    f = open("pcfgcache.txt",'w')
    print("Training the PCFG...")
    productions = []
    for t in treebank.parsed_sents():
      tr = t
      chomsky_normal_form(tr)
      for p in t.productions():
        productions.append(p)
        f.write("{0}\n".format(p.__str__()))
    print("Trained!")
    f.close()
    return grammar.induce_pcfg(grammar.Nonterminal('S'), productions)

if __name__ == '__main__':
  tb_pcfg = trained_pcfg()
  print(tb_pcfg.productions(lhs=grammar.Nonterminal('S')))
