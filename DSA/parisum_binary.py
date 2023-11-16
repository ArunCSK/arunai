# Python code to implement the approach
import bisect


# Function to find the count of pairs


def getPairsCount(arr, n, k):
    arr.sort()
    x, c = 0, 0
    for i in range(n - 1):
        x = k - arr[i]

        # Lower bound from i+1
        y = bisect.bisect_left(arr, x, i + 1, n)
        print("-> y: {}".format(y))

        # Upper bound from i+1
        z = bisect.bisect(arr, x, i + 1, n)
        print("-> z: {}".format(z))
        c = c + z - y
        print("-> c: {}".format(c))
    return c


# Driver function
arr =  [5, 4, 6, 2, 8, 8, 2, 7, 3, 9, 1, 10, 5]
n = len(arr)
k = 6

# Function call
print("Count of pairs is", getPairsCount(arr, n, k))

# This code is contributed by Pushpesh Raj
