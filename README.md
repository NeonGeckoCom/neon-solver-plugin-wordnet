
Spoken answers api for wordnet


```python
from neon_solver_wordnet_plugin import WordnetSolver

d = WordnetSolver()
sentence = d.spoken_answer("what is the definition of computer")
print(sentence)
# a machine for performing calculations automatically

d = WordnetSolver()
sentence = d.spoken_answer("qual é a definição de computador", lang="pt")
print(sentence)
# uma máquina para realizar cálculos automaticamente
```
