import numpy as np
from sympy import randprime, isprime
import random
import math

#
# 拡張ユークリッド互除法
#
def gcd_ext(a, b):
  """
  # 拡張ユークリッドの互除法
  # a*x + b*y = gcd(a,b) となる (x,y) を求める.
  http://www.tbasic.org/reference/old/ExEuclid.html
  """
  x, y, lastx, lasty = 0, 1, 1, 0
  while b != 0:
    q = a // b
    a, b = b, a % b
    x, y, lastx, lasty = lastx - q * x, lasty - q * y, x, y
  return (lastx, lasty)

#
# 10進数 → 2進数リスト
#
def decimal_to_binary_list(x):
  return [int(i) for i in list(str(bin(x))[2:])]

#
# 2進数リスト → 10進数
#
def binary_list_to_decimal(b_list):
  str_list = [str(s) for s in b_list]
  return int(''.join(str_list), 2)

#
# 素数ランダム生成 (a ~ bの間で)
#
def generate_prime(a, b):
  return randprime(a, b)

#
# ハミング重みの小さい鍵を生成
#
def generate_small_haming_weight_d(e, pq_length):
  delta = 1
  i = 0

  while True:
    i += 1
    p = generate_prime(2**(pq_length), 2**(pq_length+1)-1)
    print('i = {1} | p = {0}'.format(p, i))
    p_dash = p-1
    for s0 in range(pq_length, pq_length-1, -1):
      for _ in range(e):
        s1 = s0//2
        tmp = random.randint(2**(s1-1), 2**s1)
        d0 = 2**s0 + tmp

        lmd = (e*d0-1)//p_dash
        mu = (e*d0-1) % p_dash

        d1 = mu // e
        delta = mu % e

        if (d1 < tmp):
          print('==========')
          print('d1 < tmp')
          print('d1 = {0}'.format(d1))
          print('tmp = {0}'.format(tmp))
          print('==========')

        if (delta == 0) and (d1 < tmp):
          return d0-d1, lmd, p

#
# main function
#
if __name__ == '__main__':
  e = 2**16+1
  # d_length = 64
  d_length = 76
  pq_length = (d_length // 2)-1

  while True:
    dp, lmdp, p = generate_small_haming_weight_d(e, pq_length)
    print('OK')
    dq, lmdq, q = generate_small_haming_weight_d(e, pq_length)
    print('OK')

    if math.gcd(e, (p-1)*(q-1)) != 1:
      raise Exception('gcd error')

    d, _ = gcd_ext(e, (p-1)*(q-1))
    if d < 0:
      d += (p-1)*(q-1)

    if ((lmdp-1)*(lmdq-1)%e) != (lmdp*lmdq*p*q)%e:
      raise Exception('((lmdp-1)*(lmdq-1) % e) != (lmdp*lmdq*p*q) % e')

    if (dp != d % (p-1)):
      raise Exception('dp != d % (p-1)')

    print('==========')
    print('d = {0}'.format(d))
    print('dの2進表現: {0}'.format(decimal_to_binary_list(d)))
    print('dの鍵長は: {0}'.format(len(decimal_to_binary_list(d))))
    print('e = {0}'.format(e))
    print('p = {0}'.format(p))
    print('pの鍵長は: {0}'.format(len(decimal_to_binary_list(p))))
    print('q = {0}'.format(q))
    print('qの鍵長は: {0}'.format(len(decimal_to_binary_list(q))))
    print('dp = {0}'.format(dp))
    print('dpの2進表現: {0}'.format(decimal_to_binary_list(dp)))
    print('dpの鍵長は: {0}'.format(len(decimal_to_binary_list(dp))))
    print('dq = {0}'.format(dq))
    print('dqの2進表現: {0}'.format(decimal_to_binary_list(dq)))
    print('dqの鍵長は: {0}'.format(len(decimal_to_binary_list(dq))))
    print('kp = {0}'.format(lmdp))
    print('kq = {0}'.format(lmdq))
    print('==========')

    break
