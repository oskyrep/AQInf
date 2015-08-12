import pandas as pd;
from collections import OrderedDict;

labeledList = ['v1','v2','v3'];
unlabeledList = ['u1','u2','u3','u4','u5'];
timeStampList = ['t1','t2','t3'];
labeledAQITable = pd.DataFrame([[200,250,225],
                                [250,300,275],
                                [300,350,325]],
                                index = timeStampList,
                                columns = labeledList,
                                dtype = float);
numToBeRecommend = 3;
                                       
labeledFeatureDictListUponTimeStamp = OrderedDict( [
                                      ('t1',
                                            [
                                                OrderedDict([('v1',100),('v2',150),('v3',125)]),
                                                OrderedDict([('v1',150),('v2',200),('v3',175)]),
                                                OrderedDict([('v1',75),('v2',125),('v3',100)])
                                            ]),
                                      ('t2',
                                            [
                                                OrderedDict([('v1',150),('v2',200),('v3',175)]),
                                                OrderedDict([('v1',250),('v2',300),('v3',275)]),
                                                OrderedDict([('v1',50),('v2',100),('v3',75)])
                                            ]),
                                      ('t3',
                                            [
                                                OrderedDict([('v1',125),('v2',175),('v3',150)]),
                                                OrderedDict([('v1',200),('v2',250),('v3',225)]),
                                                OrderedDict([('v1',100),('v2',150),('v3',125)])
                                            ]) ]);

unlabeledFeatureDictListUponTimeStamp = OrderedDict(
                                        [('t1',
                                              [
                                                  OrderedDict([('u1',125),('u2',50),('u3',500),('u4',300),('u5',400)]),
                                                  OrderedDict([('u1',200),('u2',150),('u3',550),('u4',350),('u5',450)]),
                                                  OrderedDict([('u1',325),('u2',200),('u3',600),('u4',450),('u5',600)])
                                              ]),
                                         ('t2',
                                              [
                                                  OrderedDict([('u1',175),('u2',75),('u3',550),('u4',350),('u5',450)]),
                                                  OrderedDict([('u1',250),('u2',200),('u3',600),('u4',400),('u5',500)]),
                                                  OrderedDict([('u1',350),('u2',250),('u3',650),('u4',500),('u5',650)])
                                              ]),
                                         ('t3',
                                              [ 
                                                  OrderedDict([('u1',150),('u2',50),('u3',525),('u4',325),('u5',425)]),
                                                  OrderedDict([('u1',225),('u2',175),('u3',575),('u4',375),('u5',475)]),
                                                  OrderedDict([('u1',300),('u2',225),('u3',625),('u4',475),('u5',625)])
                                              ]) ]);
