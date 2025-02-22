def my_gen(n):
    for i in range(n):
        i = i**2
        yield i


n = int(input())
for item in my_gen(n):
    print(item, end=" ")
