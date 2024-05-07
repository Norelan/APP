from random import randint
n = int(input())
a = randint(1,100)
while(n==a):
  if n == a:
    print("победа")
  else:
    if n > a:
      print("мое число меньше")
    else:
      print(" мое число больше")
