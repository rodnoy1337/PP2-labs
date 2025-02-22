def my_gen(a, b):
   for i in range(a, b):
      i = i**2
      yield i

a, b = int(input()), int(input())
for item in my_gen(a, b):
   print(item)