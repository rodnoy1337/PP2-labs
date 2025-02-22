from datetime import datetime
d1 = input().split()
d2 = input().split()
first_date = datetime(int(d1[0]), int(d1[1]), int(d1[2]), int(d1[3]), int(d1[4]), int(d1[5]))
second_date = datetime(int(d2[0]), int(d2[1]), int(d2[2]), int(d2[3]), int(d2[4]), int(d2[5]))
diff = first_date - second_date
print(diff.total_seconds())
