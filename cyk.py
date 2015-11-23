from nltk.grammar import PCFG

# PCFG : nltk.grammar.pcfg
# words : list(strings)
def CYK(pcfg, words, numparses=1):
  numwords = len(words)
  chart = [[]]                # each [row][col] is a list of production tuples
  #[ row0:[ col0:[(prod1),(prod2),(prod3)] , col1:[(prod4),(prod5),(prod6)] ], row1:[ col0:[(p1),(p2)] , col1:[(p3)] ] ]
  i = 0
  for w in words:
    chart[0].append([])       # create the new column
    prods = pcfg.productions(rhs=w)
    li = []
    for p in prods:
      # Tuples go into every slot in chart with (production, probability, backpointer)
      li.append((p,p.prob(),0))
    chart[0][i].extend(li)
    i += 1
  
  for i in range(1,numwords):   # length of the span and level of chart
    chart.append([])            # create the new row
    for j in range(numwords-i): # current slot [i,j] in the chart we are evaluating
      chart[i].append([])       # create the new column
      for k in range(i):        # used to increment through all sub-lengths when comparing previous slots of productions
        li = []
        # iterate through all productions in each slot of [k,j] and those in [i-(k+1),j+k+1]
        for ii in range(len(chart[k][0])):
          for jj in range(len(chart[i-(k+1)][k+(j+1)])):
            for prod in pcfg.productions(rhs=chart[k][0][ii][0].lhs()):
              if chart[i-(k+1)][k+(j+1)][jj][0].lhs() == prod.rhs()[1]:
                li.append((prod,prod.prob() * chart[k][0][ii][1] * chart[i-(k+1)][k+(j+1)][jj][1],((k,0,ii),(i-(k+1),k+(j+1),jj))))
        chart[i][j].extend(li)
  
  return chart[numwords-1][0]

if __name__ == '__main__':
  toy_pcfg = PCFG.fromstring("""
  S -> A A [0.8] | A B [.1] | A S [.1]
  A -> A A [.6] | A B [.2] | 'a' [.2]
  B -> B A [.3] | A B [.2] | 'b' [.5]
  """)
  for top in sorted(CYK(toy_pcfg,['a','b','a']), key=lambda x : x[1], reverse=True):
    print(top)
