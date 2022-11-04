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

['TESTBOOL', 'TESTTEXT', 'TESTDATE', 'TESTNUM', 'TESTFLOAT']
[('L', 1, 0), ('C', 10, 0), ('D', 10, 0), ('N', 10, 0), ('F', 10, 2)]
['T', 'test0     ', datetime.date(2018, 1, 1), 42, 42.01]
['F', 'test1     ', datetime.date(2018, 1, 2), 43, 43.02]
['T', 'test2     ', datetime.date(2018, 1, 3), 44, 44.03]
....................
TESTBOOL,TESTTEXT,TESTDATE,TESTNUM,TESTFLOAT
T,test0     ,2018-01-01,42,42.01
F,test1     ,2018-01-02,43,43.02
T,test2     ,2018-01-03,44,44.03
