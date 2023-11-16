l1 = [5, 4, 6, 2, 8, 8, 2, 7, 3, 9, 1, 10, 5]
sum_val = 10
dict_key_pair = {}

for i in range(len(l1)):
    for j in range(len(l1)-i):
        if l1[i] + l1[j] == sum_val:
            if l1[i] < l1[j]:
                dict_key_pair[l1[i]] = l1[j]
            else:
                dict_key_pair[l1[j]] = l1[i]


print(dict_key_pair)


