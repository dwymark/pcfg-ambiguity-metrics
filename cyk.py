from nltk.grammar import PCFG
from nltk.tree import Tree
import main

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
        for ii in range(len(chart[k][j])):
          for jj in range(len(chart[i-(k+1)][k+(j+1)])):
            for prod in pcfg.productions(rhs=chart[k][j][ii][0].lhs()):
              if chart[i-(k+1)][k+(j+1)][jj][0].lhs() == prod.rhs()[1]:
                li.append((prod,prod.prob() * chart[k][j][ii][1] * chart[i-(k+1)][k+(j+1)][jj][1],((k,j,ii),(i-(k+1),k+(j+1),jj))))
        chart[i][j].extend(li)
  return trees_from_chart(chart,numparses)

def trees_from_chart(chart, numparses):
  starting_nodes = sorted(chart[len(chart)-1][0], key=lambda x : x[1], reverse=True)
  trees = []
  for i in range(numparses):
    li = []
    buildtree(chart,li,starting_nodes[i])
    print("".join(li))
    trees.append(Tree.fromstring("".join(li)))
  return trees

def buildtree(chart,li,tup):
  if tup[2] != 0:
    li.append('(' + str(tup[0].lhs()))
    buildtree(chart,li,chart[tup[2][0][0]][tup[2][0][1]][tup[2][0][2]])
    li.append(' ')
    buildtree(chart,li,chart[tup[2][1][0]][tup[2][1][1]][tup[2][1][2]])
    li.append(')')
  else:
    li.append('(' + str(tup[0].lhs()) + ' ' + str(tup[0].rhs()[0]) + ')')

def test1(test_str):
  toy_pcfg = PCFG.fromstring("""
  S -> A A [0.8] | A B [.1] | A S [.1]
  A -> A A [.6] | A B [.2] | 'a' [.2]
  B -> B A [.3] | A B [.2] | 'b' [.5]
  """)
  for t in CYK(toy_pcfg,test_str.split(" "),5):
    t.draw()

def test2():
  pcfg = main.trained_pcfg()
  try:
    CYK(pcfg,"He crossed the road".split(" "))[0].draw()
  try:
    CYK(pcfg,"The man saw the boy with the telescope .".split(" "))[0].draw()

if __name__ == '__main__':
  test2()
