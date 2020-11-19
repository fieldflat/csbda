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
# 鍵生成
#
def generate_dp(e, dp_length):
  loop_times = 1000
  for j in range(loop_times):
    dp = [1] + [0]*dp_length + [random.randint(0, 1) for _ in range(dp_length-2)] + [1]
    dp_decimal = binary_list_to_decimal(dp)

    for kp in range(1, e):
      if (e*dp_decimal-1) % kp != 0:
        continue
      p = ((e*dp_decimal-1) // kp) + 1
      if isprime(p):
        print('=======================')
        print('j = {0}'.format(j+1))
        print('=======================')
        return dp, dp_decimal, kp, p

#
# RSA鍵チェック
#
def rsa_key_check(e, n, p, dp_decimal, kp, q, dq_decimal, kq, d):
  if ((e*d) % ((p-1)*(q-1))) != 1:
    print('miss: 1')
    return False
  if ((e*dp_decimal) % (p-1)) != 1:
    print('miss: 2')
    return False
  if ((e*dq_decimal) % (q-1)) != 1:
    print('miss: 3')
    return False
  if (0 >= kp or kp >= e) or (0 >= kq or kq >= e):
    print('miss: 4')
    return False
  if (((kp-1)*(kq-1)) % e) != ((kp*kq*n) % e):
    print('miss: 5')
    return False
  if (d <= 0):
    print('miss: 6')
    return False
  return True


#
# main function
#
if __name__ == '__main__':
  e = 2**16 + 1
  dp_length = 512

  dp, dp_decimal, kp, p = generate_dp(e, dp_length)
  dq, dq_decimal, kq, q = generate_dp(e, dp_length)

  if math.gcd(e, (p-1)*(q-1)) != 1:
    raise Exception('e % ((p-1)*(q-1)) != 1')
  
  d, _ = gcd_ext(e, (p-1)*(q-1))
  n = p*q

  if d < 0:
    print('************* d < 0 *****************')
    d += (p-1)*(q-1)

  #
  # RSA条件チェック
  #
  if rsa_key_check(e, n, p, dp_decimal, kp, q, dq_decimal, kq, d):
    print('======= 結果発表 ======')
    print('p = {0}'.format(p))
    print('dp = {0}'.format(dp))
    print('dp_decimal = {0}'.format(dp_decimal))
    print('q = {0}'.format(q))
    print('dq = {0}'.format(dq))
    print('dq_decimal = {0}'.format(dq_decimal))
    print('d = {0}'.format(d))
    print('n = {0}'.format(p*q))
    print('e = {0}'.format(e))
  else:
    print('条件不一致')
