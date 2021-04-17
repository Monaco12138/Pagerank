# PageRank实验报告

### 算法设计思路

我们组Pagerank经历了四次不同的流程迭代:

    直接实现->分块(每块均放在内存里)->分块(放在磁盘里)->多线程并行化
    不妨记四次实现依次为naive->blockMemory->blockDisk->blockParallel

&nbsp;&nbsp;

整体而言思路采用课件上的实现形式，先随机生成数据，再进行Pagerank迭代。
我们生成的数据直接采用邻接表的方式存储，生成数据形式如下：
```C
    1 51 68 26 99 9 61 28 17 74 //第0行源为0，出度为10，分别指向1，51，68...
    60 85 57 46 66 6    //第1行源为1，出度为6，分别指向60,85...
    63 57 41 83 62 56 43 89 96 12 85 15 
    97 47 77 72 42 5 30 41 52 32 6 14 48 24 22 
```  

后面改进后使用分块存储形式如下:
```C
    0 14 78345 95734    //第一个数表示源为0 ， 第二个数表示出度为14，
    3 7 46788           //后面表示对应的出度节点(仅包含位于这一块里)
    6 12 45419 
    7 15 57821 79223 66425 
    10 9 53356 66701 99254 28083 
```

其中迭代的关键部分算法如下：
```python
    For each page i(of out-degree di):
        Initialize r_new = (1-beta)/N
        Read into memory: i , di , desti
        for j = i ... di:
            r_new(destj) += beta*r_old(i) / d(i)

```


之后我们就对rankNew 和rankOld文件中的值逐个比对求一范数，当求出的值小于给定的Epsilon的时候，就不再继续迭代，然后输出相应的时间、迭代次数、rankId，实验结束





### 关键代码描述

__naive算法__
```python
while True:
    epoches += 1            #记录迭代次数
    rankNew = [(1-Beta)/N]*N
    for i in range(N):
        degree = len(M[i])  #source i的出度个数

        for j in range(degree):
            
            destination = M[i][j]   #对每一个目的节点

            rankNew[destination] +=  (Beta * rankOld[i] ) *  (1.0/ degree)  #更新表达式


    if normalOne(rankOld,rankNew) < Epsilon:   #结束判断
        break
    rankOld = rankNew

```
&nbsp;&nbsp;

__blockMemory算法__
```python
#这里主要展示将矩阵分块存储的部分
K = N // block          #共K组，每组有一个Block大

Mblock = [None]*K       #将原始数据M分成K个小Mblock

destination = -1

destList = []
for i in range(N):

    degree = len(M[i])  #source i的出度个数

    bottom = [None]*K   #桶用来存放每一个destination条目

    for j in range(degree):
        destination = M[i][j]   #对i的每一个目的destination
        index = destination//block  #确定这一条目要分到的桶的序号

        if not isinstance(bottom[index],list):  #将这一条目插入桶中
            bottom[index] = []
            bottom[index].append([i,degree])
            bottom[index].append([])

        bottom[index][1].append(destination)
    
    for j in range(K):      #对i的每一个destination遍历完后，将整个i放入Mblock
        if isinstance(bottom[j] , list):
            if not isinstance(Mblock[j] , list):
                Mblock[j] = []

            Mblock[j].append(bottom[j])
```

&nbsp;&nbsp;

__blockDisk算法__
```python
    相比blockMemory操作多了文件读写的内容，将存放在内存中的东西写入文件来减少内存消耗
```

&nbsp; &nbsp;
__bolckParallel算法__
```python
#主要展示多线程实现部分
class pageThread(threading.Thread):
    def __init__(self , index , rankOld):   #index是线程标号， rankOld是旧的排名向量
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


            for i in range(blockCrow):  #对每一个分块矩阵Mblock作迭代更新表达式
                destList = Mblock[i][1]
                degree  = Mblock[i][0][1]
                src = Mblock[i][0][0]

                cols = len(destList)

                for j in range(cols):

                    destination = destList[j]

                    rankNew[ destination%blocks ] +=  (Beta * self.rankOld[ src ] ) *  (1.0/ degree)


            WriteNew(rankNew , self.index)


```


### 实验结果

    这里展示四种不同算法在Epsilon=1e-3时用时和内存开销的对比
    我们组这里做到了N=1e5,1e6,1e7 因为1e5时内存消耗太小故不作展示

&nbsp;&nbsp;  

#### N=1e5  , Epsilon = 1e-3 , blocks=1e4

| 实现方式      | 迭代时间 | 迭代次数 |
| ------------- | -------- | -------- |
| naive         | 3.596s   | 5        |
| blockMemory   | 9.021s   | 5        |
| blockDisk     | 35.992s  | 5        |
| bolckParallel | 52.351s  | 5        |

  answer:

| \range       | 1                                                     | 2                                                     | 3                                                     | 4                                                     | 5                                                     | 6                                                     | 7                                                     | 8                                                     | 9                                        | 10                                                    |
| ------------ | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ----------------------------------------------------- | ---------------------------------------- | ----------------------------------------------------- |
| __index__    | 56168&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 30838&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 83722&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 88133&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 19912&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 30428&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 82276&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 57147&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 7673&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 53967&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |
| __Pagerank__ | 2.274e-05                                             | 2.253e-05                                             | 2.243e-05                                             | 2.238e-05                                             | 2.236e-05                                             | 2.223e-05                                             | 2.217e-05                                             | 2.200e-05                                             | 2.199e-05                                | 2.181e-05                                             |


&nbsp;&nbsp;    


#### N=1e6 , Epsilon = 1e-3, blocks=1e5

| 实现方式      | 迭代时间 | 迭代次数 | 执行内存消耗 |
| ------------- | -------- | -------- | ------------ |
| naive         | 66.312s  | 5        | 557MB        |
| blockMemory   | 132.389s | 5        | 2367MB       |
| blockDisk     | 765.876s | 5        | 387MB        |
| bolckParallel | 385.402s | 5        | 1479MB       |

answer:

| \range       | 1                                                      | 2                                                      | 3                                                      | 4                                                      | 5                                                      | 6                                                      | 7                                                      | 8                                                      | 9                                    | 10                                                     |
| ------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------ | ------------------------------------------------------ |
| __index__    | 968073&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 800585&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 665180&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 547777&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 150783&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 172543&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 165312&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 407516&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 948539&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 944303&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |
| __Pagerank__ | 2.559e-06                                              | 2.539e-06                                              | 2.511e-06                                              | 2.487e-06                                              | 2.456e-06                                              | 2.426e-06                                              | 2.419e-06                                              | 2.418e-06                                              | 2.406e-06                            | 2.398e-06                                              |

&nbsp;&nbsp;  

#### N=1e7 , Epsilon = 1e-3, blocks=1e5

| 实现方式      | 迭代时间  | 迭代次数 | 执行内存消耗       |
| ------------- | --------- | -------- | ------------------ |
| naive         | 353.239s  | 5        | 5797MB             |
| blockMemory   | XXX       | X        | Segmentation fault |
| blockDisk     | 5479.446s | 5        | 885MB              |
| bolckParallel | 4492.942s | 5        | 2457MB             |

answer:


| \range       | 1                                                       | 2                                                       | 3                                                       | 4                                                       | 5                                                       | 6                                                       | 7                                                       | 8                                                       | 9                                     | 10                                                      |
| ------------ | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------- |
| __index__    | 9458235&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 8656701&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 8966829&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 5473618&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 6316243&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 9860641&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 6620540&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 8967713&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 3687314&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; | 6882558&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; |
| __Pagerank__ | 2.81e-07                                                | 2.77e-07                                                | 2.684e-07                                               | 2.680e-07                                               | 2.666e-07                                               | 2.646e-07                                               | 2.618e-07                                               | 2.617e-07                                               | 2.612e-07                             | 2.610e-07                                               |

&nbsp;&nbsp;  
    
#####这里再补充一个老师要求的添加多个Epsilon的结果(采用Naive算法)
    (迭代次数，收敛用时)
|Epsilon\N| 1000 | 10000 | 100000|
|---|   ----     | ----   |    ----|
|__1e-2__|   (4 , 0.0148s)      |  (5,0.15s)        | (4 , 2.315s)    |
|__1e-5__|  (10, 0.031s)        |  (8 , 0.366s)        | (9 , 4.40s)      |
|__1e-8__|  (14 , 0.043s)   | (13 , 0.59s)      |（15 , 7.28s) |
&nbsp;&nbsp;
|(N,Epsilon)       | index | pagerank|
|----   |   ----|   ----   |
|(1000,1e-2) |[229, 20, 201, 912, 98, 826, 812, 356, 575, 433]|[0.00227, 0.001813, 0.00181, 0.001807, 0.00173, 0.001726, 0.001708, 0.0017001, 0.001678, 0.001673]|
|(1000,1e-5) |[229, 201, 20, 912, 98, 826, 812, 356, 575, 433]|pagerank值近似这里不展示|
|(1000,1e-8) |[229, 201, 20, 912, 98, 826, 812, 356, 575, 433]|~|
|(1e4,1e-2) |[394, 3235, 7366, 8991, 8852, 299, 2479, 6690, 8910, 3809]|[0.000237, 0.000204, 0.000200, 0.000198, 0.000196, 0.0001932, 0.0001931, 0.0001922, 0.0001920, 0.0001915]|
|(1e4,1e-3)  |[394, 3235, 7366, 8991, 8852, 2479, 299, 6690, 8910, 3809]|pagerank值近似这里不展示|
|(1e4,1e-8)  |[394, 3235, 7366, 8991, 8852, 2479, 299, 6690, 8910, 3809]|~|
|(1e5 , 1e-2)|[56168, 30838, 83722, 88133, 19912, 30428, 82276, 57147, 7673, 53967]|[2.27e-05, 2.25e-05, 2.24e-05, 2.238e-05, 2.234e-05, 2.22e-05, 2.21e-05, 2.1995e-05, 2.1993e-05, 2.18e-05]|
|(1e5 , 1e-5)|[56168, 30838, 83722, 88133, 19912, 30428, 82276, 57147, 7673, 53967]|pagerank值近似这里不展示|
|(1e5, 1e-8) |[56168, 30838, 83722, 88133, 19912, 30428, 82276, 57147, 7673, 53967]|~|

### 实验分析

- ___由四种不同算法的四种实验结果可知___：
    -  __naive__ 算法将计算迭代时所运用的所有数据全部存储在内存中，故运算速度最快。但随着数据规模增大，明显当N=1e7时，内存中存放的数据接近6G。且N每增加10倍，内存所需存放的数据量增加10倍左右。过大的内存开销使得对于大量数据Pagerank变得不可能或需要大量内存成本
    &nbsp;&nbsp;
    - 需要指出 __blockMemory__ 算法只是过渡态的，将开始的邻接表存储的信息分块，后放入内存中，故其内存开销与时间开销都偏大，同时可以看出邻接表分块后的总容量会大于未分块的容量，因为存储了更多与分块有关的信息
    &nbsp;&nbsp;
    - __blockDisk__ 算法为了减少内存消耗，将分块后的信息放入文件中，每次只读取一块进入内存操作，故随着N增大，内存消耗增大速度趋于一块的大小。此方法减少了内存的消耗，使得N很大时执行Pagerank成为可能，我们也用此方法执行了N=1e7的pagerank。但此方法的缺点是分块后增加了文件I/O的时间，导致与 __naive__ 方法相比，执行用时大概增加了10倍多
    &nbsp;&nbsp;
    - __blockParallel__ 算法在 __blockDisk__ 基础上，为了减少运行时间，我们想到了使用多线程加速，因为每块每块之间的迭代互不影响，故不存在依赖关系，可以比较方便的并行化。需要说明的是，并行化的效果没有想象的理想，我们采用了5个线程并行化，一次读入5个块。内存消耗与 __blockDisk__ 相比增加了3 ~ 5倍，但是用时减少大概只有1~2倍。此外当N比较小时如1e5并行化的提升速度反而没有抵消其开销，导致用时更多。当N大一点时并行化的效果才可以体现出来
    &nbsp;&nbsp;
-  ___由补充实验结果可知___：
    - 对于同一Epsilon，收敛的迭代次数随N变化的不明显

    - 对于同一个N ,结果在Epsilon为1e-5左右收敛，后面随Epsilon增大对结果影响不大

####加分项
- 分块实现，用文件模拟磁盘操作减少执行内存开销，并成功执行N=1e7的Pagerank
- 进一步对分块实现的并行化
