import os
import threading
import time
blocks = int(1e5)
N = int(1e7)
K = N // blocks
Beta = 0.8
threads = 5

filePath = './M_10000000.txt'
localNew = './data/rankNew.txt'
localOld = './data/rankOld.txt'



#_-------------------------清空rankNew文件中缓存--------------
def RemoverankNew():
    filedir = './rankNew'
    #获取当前文件夹中的文件名称列表  
    filenames=os.listdir(filedir)

    for filename in filenames:
        filepath = filedir+'/'+filename
            #遍历单个文件，读取行数
        os.remove(filepath)


class pageThread(threading.Thread):
    def __init__(self , index , rankOld):
        threading.Thread.__init__(self)
        self.index = index
        self.rankOld = rankOld

    def run(self):
        epoches = K // threads

        for epoch in range( self.index*epoches , (self.index+1)*epoches ):  #对于每一块分块矩阵

            #print(self.index*epoches , (self.index+1)*epoches)
            rankNew = [(1-Beta)/N]*blocks   #初始化rankNew
            #rankOld = [1/N]*blocks

            Mblock = ReadMblocks(epoch)     #读取Mblock_epoch in K

            blockCrow = len(Mblock)


            for i in range(blockCrow):
                #print(Mblock)
                destList = Mblock[i][1]
                degree  = Mblock[i][0][1]
                src = Mblock[i][0][0]

                #tpIndex = src // blocks

                #self.roldIndex = ReadrOld(self.count , tpIndex , self.roldIndex , rankOld)     #根据相应的tpIndex号读取rankOld

                cols = len(destList)

                for j in range(cols):

                    destination = destList[j]

                    rankNew[ destination%blocks ] +=  (Beta * self.rankOld[ src ] ) *  (1.0/ degree)


            WriteNew(rankNew , self.index)

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
    local = './data/Mblock_{}.txt'.format(index)
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
            #line = list(line.strip().split(' '))
            rankOld.append( float(line) )

        file.close()

#--------------------------------写回Rnew-------------------
def WriteNew(rankNew , index):
    rankPath = './rankNew/rankNew_{}.txt'.format(index)

    file = open(rankPath , 'a')
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


#------------------------------------将多个rankNew_0~4合并成一个rankNew
def Merge():
    filedir = './rankNew'
    #获取当前文件夹中的文件名称列表  
    filenames=os.listdir(filedir)
    #打开当前目录下的result.txt文件，如果没有则创建
    f=open('./data/rankNew.txt','w')
    #先遍历文件名
    for filename in filenames:
        filepath = filedir+'/'+filename
        #遍历单个文件，读取行数
        for line in open(filepath):
            f.writelines(line)
        #f.write('\n')
    #关闭文件
    f.close()
#------------------------------迭代流程------------------


#rankNew = [(1-Beta)/N]*blocks
#rankOld = [1/N] * blocks
#roldIndex = -1               #标记现在是第几块rankOld,如果相等就不用重新读取rOld
count = 0

threadList = [None]*threads


RemoverankNew()
#os.remove(localNew)
#os.remove(localOld)


start = time.time()
rankOld = [1/N]*N

while True:
    count += 1
    for i in range(threads):
        threadList[i] = pageThread(i , rankOld)

    for i in range(threads):
        threadList[i].start()
    
    for i in range(threads):
        threadList[i].join()

    Merge()

    if NormalOne(count) < 1e-3:
        break

    
    #rankOld = rankNew
    writeNewToOld()     #把rankNew 信息写入rankOld里
    ReadrOld(rankOld)
    RemoverankNew()

end = time.time()
print(count)
print(end-start)