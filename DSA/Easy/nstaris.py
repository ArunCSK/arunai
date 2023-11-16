from os import *
from sys import *
from collections import *
from math import *

def countDistinctWays(nStairs: int) -> int:
    # one,two = 1,1
    #
    # for n in range(nStairs -1):
    #     temp = one
    #     one = one + two
    #     two = temp
    # n = nStairs[0]
    # no_stairs_list = []
    # for i in range(1, len(nStairs)):
    #     no_stairs_list.append((nStairs[i]))
    #
    # slen = len(no_stairs_list)
    # result = 0
    # for i in range(slen):
    #     val = no_stairs_list[i]
    #     result += 1
    #     if val % 2 == 0:
    #         result += 1
    #
    # print(no_stairs_list)
    #
    # return None
    N = nStairs[0]
    if N <= 1:
        return 1

    a, b = 1, 1
    for _ in range(N):
        a, b = b, a + b

    return a



nStairs = [2, 4, 5]
print(countDistinctWays(nStairs))
