def my_gen(n):
    for i in range(n+1):
        if(i % 2 == 0):
            yield i
            if i != n: print(",", end=" ")


n = int(input())
for item in my_gen(n):
    print(item, end="")
