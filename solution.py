def esh(a, b):
    if (a[0] < b[0]):
        if a[1] >= b[0]:
            return True
        return False
    elif a[0] > b[0]:
        if b[1] >= a[0]:
            return True
        return False
    else:
        return True

lst = []
count = 0
n = int(input())
for i in range(n):
    lst.append(list(input().split()))

lst.sort(key=lambda x : x[0])
print(lst)

for i in range(n-1):
    for j in range(i+1, n):
        if esh(lst[i], lst[j]):
            count += 1
if n - count <= 0:
    print(1)
else:
    print(n - count)