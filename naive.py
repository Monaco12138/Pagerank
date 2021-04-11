import random
import ReadWrite
import time
'''
C = [index for index in range(N)]
M = []
for index in range(N):
    d = random.randint(6,15)    #网页的出度
    data = random.sample(C , d)
    M.append(data)
'''

#print(M)                   #M=[C1,C2,C3,...,Cn]Ci表示出度

N = 10000000
Beta = 0.8
M = ReadWrite.Read(N)

'''
N = 3
Beta = 0.8
M = [[0,1],[0,2],[2]]
'''
def normalOne(X , Y):
    answer = 0.0
    Z = [ X[i]-Y[i] for i in range(len(X)) ]
    for data in Z:
        answer += abs(data)
    return answer




rankOld = [1/N]*N
#print(Rank)
epoches  = 0
degree = 0
destination = 0
rankNew = [(1-Beta)/N]*N


start = time.time()

while True:
#for epoch in range(epoches):
    epoches += 1
    rankNew = [(1-Beta)/N]*N
    for i in range(N):
        degree = len(M[i])  #source i的出度个数

        for j in range(degree):
            
            destination = M[i][j]

            rankNew[destination] +=  (Beta * rankOld[i] ) *  (1.0/ degree)

    #print(normalOne(rankOld,rankNew))

    if normalOne(rankOld,rankNew) < 1e-3:
        break
    #print(rankNew)
    rankOld = rankNew
    #print(normalOne(rankOld,rankNew))
    
#print(rankNew)
end = time.time()
print(sum(rankNew))
print(epoches)
print(end - start)
rankId = sorted(range(len(rankNew)), key=lambda k: rankNew[k], reverse=True)

#rankNew.sort(reverse=True)
print(rankId[0:10])
#print(normalOne(rankNew,rankOld))
