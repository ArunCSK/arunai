# Python3 program for weighted job scheduling using
# Naive Recursive Method

# Importing the following module to sort array
# based on our custom comparison function
from functools import cmp_to_key


# A job has start time, finish time and profit
class Job:

    def __init__(self, start, finish, profit):
        self.start = start
        self.finish = finish
        self.profit = profit
        self.job_execution_time = 0

    def jobExecutionTimeWithProfit(self):
        self.job_execution_time = self.finish - self.start
        return self.job_execution_time, self.profit


values = [(3, 10, 20), (1, 2, 50), (6, 19, 100), (2, 100, 200)]
arr = []

for i in values:
    obj = Job(i[0], i[1], i[2])
    arr.append([(i[0], i[1], i[2]), (obj.jobExecutionTimeWithProfit())])

for i in range(len(arr)-1):
    for j in range(0,len(arr)-i-1):
        if arr[j][1][0] > arr[j + 1][1][0]:
            arr[j], arr[j+1] = arr[j+1], arr[j]

print(arr)
# obj = Job(0, 0, 0)
