def maxWater(height, n):
    maximum = 0

    # Check all possible pairs of buildings
    for i in range(n - 1):
        for j in range(i + 1, n):
            print("-> current index:{},{}".format(i,j))
            print("-> current value compare: {}, {}".format(height[i], height[j]))
            current = min(height[i],
                          height[j]) * (j - i - 1)
            print("-> current max values: {}".format(current))
            # Maximum so far
            maximum = max(maximum, current)
            print("-> max selected values: {}".format(maximum))

    return maximum


# Driver code
if __name__ == "__main__":
    height = [2, 1, 3, 4, 6, 5]

    n = len(height)
    print(maxWater(height, n))