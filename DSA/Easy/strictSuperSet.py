def is_strict_superset(a, other_sets):
    for other_set in other_sets:
        if not a.issuperset(other_set):
            return False
    return True

# Read input
set_a = set(map(int, input().split()))
num_other_sets = int(input())
other_sets = [set(map(int, input().split())) for _ in range(num_other_sets)]

# Check if set_a is a strict superset of each other set
result = is_strict_superset(set_a, other_sets)

# Print the result
print(result)


#Sample Input
# 1 2 3 4 5 6 7 8 9 10 11 12 23 45 84 78
# 2
# 1 2 3 4 5
# 100 11 12