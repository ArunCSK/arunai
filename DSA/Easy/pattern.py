lst = [ base**power for base in range(1, 5) for power in range(1,4)]
print(lst)

# Pattern = [1, 1, 1, 2, 4, 8, 3, 9, 27, 4, 16, 64]


for i in range(1,5):
    for j in range(1, 4):
        print(i**j)