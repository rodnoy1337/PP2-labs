def my_gen(n):
    for i in range(n, -1, -1):
        yield i


n = int(input())
for item in my_gen(n):
    print(item, end=" ")
