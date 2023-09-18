import random

n = int(input('input the minimum number:'))
m = int(input('input the maximum number:'))

num = 0
ans = random.randint(n,m)

for i in range(0,5):
	num = int(input('guess the number:'))

	while num < n or num > m:
		num = int(input('Invalid number. please input again:'))

	if num == ans:
		print('congraturations! the answer is ' + str(ans))
		break
	else:
		print('guess again...')
