
Spoken answers api for wordnet


```python
d = WordnetSolver()
for sentence in d.spoken_answers("what is the definition of computer"):
    print(sentence)
    # a machine for performing calculations automatically

d = WordnetSolver()
for sentence in d.spoken_answers("qual é a definição de computador", lang="pt"):
    print(sentence)
    # uma máquina para realizar cálculos automaticamente
```
