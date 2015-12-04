from nltk.grammar import PCFG
from nltk.tree import Tree
from nltk.draw import draw_trees
from nltk.treetransforms import un_chomsky_normal_form
import time
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
        slot1 = chart[k][j]
        slot2 = chart[i-(k+1)][k+(j+1)]
        for ii in range(len(slot1)):
          bp1 = (k,j,ii)
          slot1_prod = slot1[ii]
          for jj in range(len(slot2)):
            bp2 = (i-(k+1),k+(j+1),jj)
            slot2_prod = slot2[jj]
            slotProbMult = slot1_prod[1] * slot2_prod[1]
            for prod in pcfg.productions(rhs=slot1_prod[0].lhs()):
              if len(prod.rhs()) == 2 and slot2_prod[0].lhs() == prod.rhs()[1]:
                li.append((prod,prod.prob() * slotProbMult,(bp1, bp2)))
        chart[i][j].extend(li)
  return trees_from_chart(chart,numparses)

# Returns a list of tuples (TREE, PROBABILITY)
def trees_from_chart(chart, numparses):
  roots = sorted(chart[len(chart)-1][0], key=lambda x : x[1], reverse=True)
  trees = []

  if numparses > len(roots) or numparses < 1:
    numparses = len(roots)
  if len(roots) == 0:
    print("No parses found.")
    return 0

  for i in range(numparses):
    li = []
    buildtree(chart,li,roots[i])
    print("".join(li))
    trees.append((Tree.fromstring("".join(li)), roots[i][1]))
  return trees

def buildtree(chart,li,tup):
  t0 = tup[0]
  t2 = tup[2]
  if t2 != 0:
    li.append('(' + str(t0.lhs()))
    buildtree(chart,li,chart[t2[0][0]][t2[0][1]][t2[0][2]])
    li.append(' ')
    buildtree(chart,li,chart[t2[1][0]][t2[1][1]][t2[1][2]])
    li.append(')')
  else:
    li.append('(' + str(t0.lhs()) + ' ' + str(t0.rhs()[0]) + ')')

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
  return pcfg

def cykTimeTesting(sentence):
  t0 = time.time()
  CYK(pcfg, sentence.split(" "), 10)
  print(time.time() - t0)

def print_trees(li):
  # assumes list of tuples of form (TREE, PROBABILITY)
  n = 1
  for tup in li:
    print("Tree " + str(n) + ": " + str(tup[1]))
    n = n + 1
  draw_trees(*[x[0] for x in li])

if __name__ == '__main__':
  pcfg = test2()
