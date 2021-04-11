import ReadWrite
import time

block = 100000        #一个Block大小

N = 1000000
Beta = 0.8
M = ReadWrite.Read(N)
#M = [[0,1,3,5],[0,5],[3,4],[0,3,2],[3,2],[4,5]]

K = N // block          #共K组，每组有一个Block大

Mblock = [None]*K       #将M分成K个小Mblock

destination = -1

destList = []

for i in range(N):

    degree = len(M[i])  #source i的出度个数

    bottom = [None]*K

    for j in range(degree):
        destination = M[i][j]
        index = destination//block

        if not isinstance(bottom[index],list):
            bottom[index] = []
            bottom[index].append([i,degree])
            bottom[index].append([])

        bottom[index][1].append(destination)
    
    for j in range(K):
        if isinstance(bottom[j] , list):
            if not isinstance(Mblock[j] , list):
                Mblock[j] = []

            Mblock[j].append(bottom[j])

#print(len(Mblock[0]))
'''
for i in range(len(Mblock[0])):
    if(i > 65550):
        print(Mblock[0][i])
'''
rankNew = [(1-Beta)/N]*N
rankOld = [1/N] * N



#----------------------------求一范数----------------
def normalOne(X , Y):
    answer = 0.0
    Z = [ X[i]-Y[i] for i in range(len(X)) ]
    for data in Z:
        answer += abs(data)
    return answer

#------------------------------------------------
count = 0

start = time.time()
while True:
    count += 1
    rankNew = [(1-Beta)/N]*N

    for epoch in range(K):

        blockCrow = len(Mblock[epoch])

        for i in range(blockCrow):

            destList = Mblock[epoch][i][1]
            degree  = Mblock[epoch][i][0][1]
            src = Mblock[epoch][i][0][0]

            cols = len(destList)

            for j in range(cols):
                destination = destList[j]

                rankNew[destination] +=  (Beta * rankOld[src] ) *  (1.0/ degree)

    if normalOne(rankOld,rankNew) < 1e-3:
        break

    rankOld = rankNew

end = time.time()
print(count)
print(end - start)
rankId = sorted(range(len(rankNew)), key=lambda k: rankNew[k], reverse=True)

#rankNew.sort(reverse=True)
print(rankId[0:10])

