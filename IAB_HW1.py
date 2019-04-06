import pandas as pd
import numpy as np

Students = {"Choi" : [73, 66, 47, 83],
"Delao" : [82, 72, 93, 89] ,
"Henry" : [46, 74, 100, 48] ,
"Kim" : [59, 47, 65, 41] ,
"Parish" : [92, 42, 77, 62] ,
"Park" : [71, 41, 64, 59] ,
"Stamps" : [43, 57, 59, 78] ,
"Taylor" : [70 , 91 , 88, 54] }

Students = pd.DataFrame(Students).T

Departments = {'A' : [0.50 , 0.10 , 0.30 , 0.10], 
'B' : [0.05 , 0.55 , 0.20 , 0.20],
'C' : [0.10 , 0.10 , 0.70 , 0.10],
'D' : [0.15 , 0.18 , 0.22 , 0.45]}

Departments = pd.DataFrame(Departments).T

# 문제 1 각 부서가 절대평가로 지원자를 선별할 때,
def Solution(stu,dep):
    scores = np.dot(stu,dep.T)
    maxscores = scores.argmax(axis = 1 )
    result = {stu.index[i]:dep.index[j] for i,j in enumerate(maxscores)}
    return result
# 정답확인
result = Solution(Students, Departments)
print(result)
answer = {'Park': 'A', 'Choi': 'D', 'Kim': 'C', 'Delao': 'C', 'Parish': 'A', 'Taylor': 'C', 'Henry': 'C', 'Stamps': 'D'}

correct = True
for i in answer.items():
    if i not in result.items():
        correct = False
if correct: print('정답!')
else: print('어딘가 틀렸습니다.')

# 문제 2 각 부서가 상대평가로 지원자를 선발할 떄, 
def Solution(stu,dep):
    scores = np.dot(stu,dep.T)
    scores = pd.DataFrame(scores, index = stu.index, columns = dep.index)
    result = {}
    for i in list(scores):
        idx = scores[i].nlargest(2).index
        result[idx[0]] = i
        result[idx[1]] = i
        scores = scores.drop(index = idx)
    return result
## 정답확인.
result = Solution(Students, Departments)
print(result)
answer = {'Park': 'C', 'Henry': 'B', 'Parish': 'A', 'Choi': 'D', 'Stamps': 'D', 'Delao': 'A', 'Kim': 'C', 'Taylor': 'B'}
correct = True
for i in answer.items():
    if i not in result.items():
        correct = False
if correct: print('정답!')
else: print('어딘가 틀렸습니다.')