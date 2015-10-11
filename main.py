import nltk.grammar as grammar
from nltk.corpus import treebank

def trained_pcfg():
  productions = []
  for t in treebank.parsed_sents():
    for p in t.productions():
      productions.append(p)
  return grammar.induce_pcfg(grammar.Nonterminal('S'), productions)

if __name__ == '__main__':
  tb_pcfg = trained_pcfg()
