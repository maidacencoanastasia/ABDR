# ABDR
read dbf file
From

v   � *                     TESTBOOL   L                   TESTTEXT   C    
               TESTDATE   D    
               TESTNUM    N    
               TESTFLOAT  F    
              
 Ttest0     20180101  42        42.010000  Ftest1     20180102  43        43.020000  Ttest2     20180103  44        44.030000 



To

['TESTBOOL', 'TESTTEXT', 'TESTDATE', 'TESTNUM', 'TESTFLOAT']<br>
[('L', 1, 0), ('C', 10, 0), ('D', 10, 0), ('N', 10, 0), ('F', 10, 2)]<br>
['T', 'test0     ', datetime.date(2018, 1, 1), 42, 42.01]<br>
['F', 'test1     ', datetime.date(2018, 1, 2), 43, 43.02]<br>
['T', 'test2     ', datetime.date(2018, 1, 3), 44, 44.03]<br>
....................<br>
TESTBOOL,TESTTEXT,TESTDATE,TESTNUM,TESTFLOAT<br>
T,test0     ,2018-01-01,42,42.01<br>
F,test1     ,2018-01-02,43,43.02<br>
T,test2     ,2018-01-03,44,44.03<br>

![dbf1](https://user-images.githubusercontent.com/42982928/199990784-5774560e-b3e6-4c02-9352-6f8d4be6d91a.png)

![encoded dbf](https://user-images.githubusercontent.com/42982928/199990798-3c8b5b9c-959e-4821-bbcd-7aefc9513dae.png)
