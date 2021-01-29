from itertools import groupby
from operator import itemgetter

tmp = [1,2,3,4,6,7,9,10]
tmp = [list(map(itemgetter(1), g)) for k, g in groupby(enumerate(tmp), lambda x: x[0]-x[1])]
print(enumerate(tmp))
print(groupby(enumerate(tmp), lambda x: x[0]-x[1]))
print(tmp)