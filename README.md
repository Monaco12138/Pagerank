Pagerank report

本次实现Pagerank经历了四次流程迭代:

    直接实现->分块(每块均放在内存里)->分块(放在磁盘里)->多线程并行化
    不妨记四次实现依次为naive->blockMemory->blockDisk->blockParallel

&nbsp;&nbsp;  
#### N=1e5  , Epsilon = 1e-3 , blocks=1e4
  |实现方式| 迭代时间 | 迭代次数 | 
  |----   |     ----|       ----|
  |naive  |3.596s   | 5     |
  |blockMemory| 9.021s|      5|
  |blockDisk|   35.992s|   5|
  |bolckParallel|   52.351s| 5|

  answer:
 
 |\range | 1  |2  |3  |4  |5  |6  |7  |8  |9  |10 |
 |------|------|------|------|------|------|------|------|------|------|------|
 |__index__|56168&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|30838&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|83722&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|88133&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|19912&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|30428&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|82276&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|57147&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|7673&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|53967&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
 |__Pagerank__|2.274e-05 |2.253e-05|2.243e-05|2.238e-05|2.236e-05|2.223e-05|2.217e-05|2.200e-05|2.199e-05|2.181e-05|


&nbsp;&nbsp;    


#### N=1e6 , Epsilon = 1e-3, blocks=1e5
|实现方式| 迭代时间 | 迭代次数 | 执行内存消耗|
  |----   |     ----|       ----|----|
  |naive  |66.312s   | 5     |  557MB|
  |blockMemory| 132.389s|      5|   2367MB|
  |blockDisk|   765.876s|   5|       387MB|
  |bolckParallel|   385.402s| 5| 1479MB|

answer:
 
|\range | 1  |2  |3  |4  |5  |6  |7  |8  |9  |10 |
 |------|------|------|------|------|------|------|------|------|------|------|
 |__index__|968073&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|800585&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|665180&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|547777&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|150783&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|172543&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|165312&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|407516&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|948539&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|944303&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
 |__Pagerank__|2.559e-06 |2.539e-06|2.511e-06|2.487e-06|2.456e-06|2.426e-06|2.419e-06|2.418e-06|2.406e-06|2.398e-06|
&nbsp;&nbsp;  

#### N=1e7 , Epsilon = 1e-3, blocks=1e5
|实现方式| 迭代时间 | 迭代次数 | 执行内存消耗|
  |----   |     ----|       ----|----|
  |naive  |353.239s   | 5     |  5797MB|
  |blockMemory| XXX|      X|   Segmentation fault|
  |blockDisk|   5479.446s|   5|       885MB|
  |bolckParallel|   4492.942s| 5| 2457MB|

answer:


|\range | 1  |2  |3  |4  |5  |6  |7  |8  |9  |10 |
 |------|------|------|------|------|------|------|------|------|------|------|
 |__index__|9458235&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|8656701&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|8966829&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|5473618&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|6316243&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|9860641&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|6620540&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|8967713&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|3687314&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|6882558&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
 |__Pagerank__|2.81e-07 |2.77e-07|2.684e-07|2.680e-07|2.666e-07|2.646e-07|2.618e-07|2.617e-07| 2.612e-07|2.610e-07|
&nbsp;&nbsp;  
    
