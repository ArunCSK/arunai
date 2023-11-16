# Reading input
# input_path = "input.txt"
Q = int(input())
queries = []
for _ in range(Q):
    A, B, K = map(int, input().split())
    queries.append((A, B, K))

# for q in queries:
#     print(q)

# val = open(input_path, 'r')
# raw = val.read()
# # set = map(int, raw.split())
# set = raw.split('\n')
# Q = set[0]
# queries = []
# for i in range(1, len(set)):
#     A, B, K = map(int, set[i].split())
#     # print(A, B, K)
#     queries.append((A ,B, K))

# print("-> no of questions:", Q)
# print("-> input set:", queries)

prime_sets = []
for q in queries:
    A, B, K = q
    temp_list = []
    start_num, end_num = A, B
    for i in range(start_num, end_num+1):
        if start_num % 2 == 0 and start_num != 2:
            start_num += 1
        else:
            temp_list.append(start_num)
            start_num += 1
    print("-> temp list:", temp_list)
    if len(temp_list) != 0 and K <= len(temp_list)+1:
        if temp_list[K-1] - A == 0:
            prime_sets.append(temp_list[K - 1])
        elif temp_list[K-1] - A < B - temp_list[K-1] or temp_list[K-1] - A == B - temp_list[K-1]:
            prime_sets.append(temp_list[K-1])
        else:
            prime_sets.append(-1)
    else:
        prime_sets.append(-1)

for p in prime_sets:
    print(p)


