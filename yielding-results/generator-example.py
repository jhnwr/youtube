mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def add_10(value):
    return value + 10


for x in mylist:
    print(add_10(x))

res = [add_10(x) for x in mylist]
genres = (add_10(x) for x in mylist)

for g in genres:
    print(g)

print(list(genres))
