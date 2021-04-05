
d, sumtime = map(int, input().split())
check = sumtime
schadule = [0 for i in range(d)]
newdays = []

for i in range(d):
    days = list(map(int, input().split()))
    newdays.append(days)
    if sumtime - days[0] >= 0:
        sumtime -= days[0]
        schadule[i] += days[0]


if sum(schadule) != check:
    j = 0
    for el in newdays:
        while el[1] >= el[0]:
            # print(el[1])
            # print(sumtime)
            if (sumtime + el[0]) - el[1] >= 0:
                sumtime += el[0]
                sumtime -= el[1]
                schadule[j] = el[1]
                j += 1
                break
            else:
                el[1] -= 1

# print(schadule)
# print(sumtime)
# print(sum(schadule))
if sum(schadule) == check:
    print("YES")
    for el in schadule:
        print(el, end=" ")
else:
    print("NO")