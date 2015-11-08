#!python3
import nltk.grammar as grammar
from nltk.corpus import treebank
from nltk.treetransforms import chomsky_normal_form

def trained_pcfg():
  productions = []
  for t in treebank.parsed_sents():
    tr = t
    chomsky_normal_form(tr)
    for p in t.productions():
      productions.append(p)
  return grammar.induce_pcfg(grammar.Nonterminal('S'), productions)

if __name__ == '__main__':
  tb_pcfg = trained_pcfg()
  print(tb_pcfg.productions(lhs=grammar.Nonterminal('S')))
