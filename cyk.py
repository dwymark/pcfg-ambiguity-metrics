from nltk.grammar import PCFG

# PCFG : nltk.grammar.pcfg
# words : list(strings)
def CYK(pcfg, words, numparses=1):
  numwords = len(words)
  chart = [[]]
  for w in words:
    prods = pcfg.productions(rhs=w)
    li = []
    for p in prods:
      # Tuples go into every slot in chart with (production, probability, backpointer)
      li.append((p,p.prob(),0))
    chart[0].append(li)
  
  for i in range(1,numwords):
    chart.append([])
    for j in range(numwords):
      for k in range(i):
        li = []
        for t1 in chart[k][0]:
          for t2 in chart[i-(k+1)][k+1]:
            for prod in pcfg.productions(rhs=t1[0].lhs()):
              if t2[0].lhs() in prod.rhs():
                  li.append((prod,prod.prob() * t1[1] * t2[1],((k,j),(i-k,j+1+k))))
        chart[i].append(li)
  
  return chart[numwords-1][0]

if __name__ == '__main__':
  toy_pcfg = PCFG.fromstring("""
  S -> A A [0.8] | A B [.1] | A S [.1]
  A -> A A [.6] | A B [.2] | 'a' [.2]
  B -> B A [.3] | A B [.2] | 'b' [.5]
  """)
  for top in sorted(CYK(toy_pcfg,['a','b','a']), key=lambda x : x[1], reverse=True):
    print(top)