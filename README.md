# pcfg-ambiguity-metrics
A program for training NLTK's PCFG on the Penn Treebank and passing sentences to it afterwards to check the top n parses. The goal of this project is to test the claim that the top two parses of "clearly" ambiguous sentences should return probabilities that fall within a much closer margin than those for seemingly unambiguous sentences. 
In the current version, sentences must be less than 7 words to finish in a reasonable amount of time. This is an ongoing project.
It can be run as follows:

```python
python -i ./cyk.py 
>>> #Pass in your sentence you wish to test with n, the number of parses you want
>>> # Note that adding a period to the end of the sentence as well capitalization affect the outputted parse
>>> li = CYK(pcfg, "Sentence goes here".split(" "), n) 
>>> print_trees(li)
```
