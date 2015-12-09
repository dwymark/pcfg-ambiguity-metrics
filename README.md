# pcfg-ambiguity-metrics
A program for training NLTK's PCFG on the Penn Treebank and passing sentences to it afterwards to check the top n parses. The goal of this project is to test if PCFGs can be a good tool for detecting sentence ambiguity based on the size of the margin between the probabilities of the top two returned parses. The claim is that the top two parses of ambiguous sentences should return probabilities that fall within a much closer margin than those for unambiguous sentences. 
In the current version, sentences must be less than 7 words to finish in a reasonable amount of time. This is an ongoing project that is always being improved. 
It can be run as follows:

```python
python -i ./cyk.py 
>>> #Pass in your sentence you wish to test with n, the number of parses you want
>>> # Note that adding a period to the end of the sentence as well capitalization affect the outputted parse
>>> li = CYK(pcfg, "Sentence goes here".split(" "), n) 
>>> print_trees(li)
```
