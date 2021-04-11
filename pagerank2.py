import os
import time
import tqdm

blocks = int(1e4)
N = int(1e5)
K = N // blocks
Beta = 0.8

filePath = './M_100000.txt'
localNew = './data2/rankNew.txt'
localOld = './data2/rankOld.txt'

'''
#-------------------先清空一下缓存数据-------------
for i in range(K):
    localMblock = './data/Mblock_{}.txt'.format(i)
    fileMblock = open(localMblock , 'w')
    fileMblock.close()
    
#------------------------处理数据，改写成矩阵分块形式--------------------

for k in range(K):

    file = open(filePath , 'r')
    row = file.readlines()[k*blocks:(k+1)*blocks]   #一次读取blocks行
    M = []
    for line in row:
        line = list(line.strip().split(' '))
        s = []
        for i in line:
            s.append(int(i))
        M.append(s)
    #print(M)       #   M size is one blocks   


    Mblock = [None]*K       #将M分成K个小Mblock

    destination = -1

    destList = []

    #print(len(M))
    #----------------------------生成Mblock-----------------

    for i in range(blocks):     # 对于M 的每一行(blocks行)

        degree = len(M[i])  #source i的出度个数

        bottom = [None]*K

        src = i + k * blocks    #找到源

        for j in range(degree):
            destination = M[i][j]           #找到目的
            index = destination//blocks     #确定要放到哪一块

            if not isinstance(bottom[index],list):
                bottom[index] = []
                bottom[index].append([src,degree])
                bottom[index].append([])

            bottom[index][1].append(destination)
        
        for j in range(K):                  #将其放进Mblock中存储
            if isinstance(bottom[j] , list):
                if not isinstance(Mblock[j] , list):
                    Mblock[j] = []

                Mblock[j].append(bottom[j])
    

    #-----------------------将Mblock写回文件中-----------------
    for i in range(K):
        
        localMblock = './data/Mblock_{}.txt'.format(i)
        fileMblock = open(localMblock , 'a')

        blockCrows = len(Mblock[i])

        for crow in range(blockCrows):
            list1 = Mblock[i][crow][0]
            destList = Mblock[i][crow][1]

            for j in range( len(list1) ):
                fileMblock.write(str(list1[j]))
                fileMblock.write(' ')
            for j in range( len(destList) ):
                fileMblock.write(str(destList[j]))
                fileMblock.write(' ')

            fileMblock.write('\n')

        fileMblock.close()

    file.close()
'''



#----------------------------求一范数----------------
def normalOne(X , Y):
    answer = 0.0
    Z = [ X[i]-Y[i] for i in range(len(X)) ]
    for data in Z:
        answer += abs(data)
    return answer



def NormalOne(count):    #对rankNew 和rankOld文件中的值逐个比对求一范数

    one = 0.0
    for i in range(K):
        New = []
        Old = []
        #------------------deal with rankNew----
        file = open(localNew , 'r')
        row = file.readlines()[i*blocks : (i+1)*blocks]

        for line in row:
            New.append(float(line))
        
        file.close()

        #-----------------deal with rankOld--------
        if(count <= 1):
            Old = [1/N] * blocks
        else:
            file = open(localOld , 'r')
            row = file.readlines()[i*blocks:(i+1)*blocks]

            for line in row:
                Old.append(float(line))
            file.close()
        one += normalOne(New , Old)

    return one


#------------------------------读取Mblocks-----------------
def ReadMblocks(index):
    local = './data2/Mblock_{}.txt'.format(index)
    file = open(local , 'r')
    row = file.readlines()
    Mblock = []

    for line in row:
        line = list(line.strip().split(' '))
        s = []
        tmp = []
        for (i,data) in enumerate(line):

            s.append(int(data))
            if(i == 1):
                tmp.append(s)
                s = []
        tmp.append(s)
        Mblock.append(tmp)
    file.close()
    return Mblock


#--------------------------------读取Rold-------------------
def ReadrOld(rankOld):
    
        file = open(localOld , 'r')
        row = file.readlines()
        rankOld.clear()
        for line in row:
            rankOld.append( float(line) )
        file.close()

#--------------------------------写回Rnew-------------------
def WriteNew(rankNew):
    file = open(localNew , 'a')
    crows = len(rankNew)

    for i in range(crows):
        file.write(str(rankNew[i]))
        file.write('\n')

    file.close()

#------------------------------------将rankNew 写回 rankOld------------------------
def writeNewToOld():
    if os.path.exists(localOld):    #如果old存在，直接删掉
        os.remove(localOld)

    os.rename(localNew,localOld)    #直接将new 改名为 old来避免拷贝一次

#------------------------------迭代流程------------------


#rankNew = [(1-Beta)/N]*blocks
#rankOld = [1/N] * blocks
roldIndex = -1               #标记现在是第几块rankOld,如果相等就不用重新读取rOld
count = 0
os.remove(localNew)
os.remove(localOld)

start = time.time()
rankOld = [1/N] * N
#while True:
for kk in tqdm.tqdm(range(5)):
    count += 1

    for epoch in tqdm.tqdm(range(K)):  #对于每一块分块矩阵

        rankNew = [(1-Beta)/N]*blocks   #初始化rankNew

        roldIndex = -1
        Mblock = ReadMblocks(epoch)     #读取Mblock_epoch in K

        blockCrow = len(Mblock)


        for i in tqdm.tqdm(range(blockCrow)):
            #print(Mblock)
            destList = Mblock[i][1]
            degree  = Mblock[i][0][1]
            src = Mblock[i][0][0]

            #tpIndex = src // blocks

            cols = len(destList)

            for j in range(cols):

                destination = destList[j]

                rankNew[ destination%blocks ] +=  (Beta * rankOld[ src  ] ) *  (1.0/ degree)


        WriteNew(rankNew)


    #if NormalOne(count) < 1e-3:
    #    break

    
    #rankOld = rankNew
    writeNewToOld()     #把rankNew 信息写入rankOld里
    ReadrOld(rankOld)

end = time.time()
print(count)
print(end - start)
