import math


# Function to check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True


# Function to find the closest prime number to A
def closest_prime(A):
    if A <= 2:
        return 2
    prime = A
    while not is_prime(prime):
        prime += 1
    return prime


# Function to solve the problem for each query
def find_minimum_P(Q, queries):
    for query in queries:
        A, B, K = query
        closest = closest_prime(A)
        count_primes = 0

        # Count prime numbers between A and closest
        for num in range(A, closest + 1):
            if is_prime(num):
                count_primes += 1

        # If count of primes is at least K, print the minimum possible P
        if count_primes >= K:
            print(closest)
        else:
            print(-1)


# Reading input
Q = int(input())
queries = []
for _ in range(Q):
    A, B, K = map(int, input().split())
    queries.append((A, B, K))

find_minimum_P(Q, queries)
