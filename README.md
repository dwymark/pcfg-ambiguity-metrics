# pcfg-ambiguity-metrics
TODO:
+ Get backpointers set up correctly. Right now they are pointing to the position in the chart where the next production is, but they don't identify the specific production itself. This won't be sufficient for building the parsing trees because every space in the chart is likely to have multiple productions.
+ Make a function for building the top n parse trees from the chart.
+ Test both functions against known-correct parsing algorithms (like nltk.ViterbiParser) and by hand.
