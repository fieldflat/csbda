import math
import random
import yaml
from sympy import isprime

# ========================
# Constants
# ========================
E = 2**16 + 1

def generate_block_of_csbda(filename: str) -> (list, int):
  with open('./config/'+filename, 'r') as yml:
    config = yaml.load(yml, Loader=yaml.FullLoader)

  d_length = config['key_params']['d_length']
  padding_bits_num = d_length
  blocks = config['key_params']['blocks']

  block_d = []
  for b in blocks:
    content, quantity = blocks[b]['content'], blocks[b]['quantity']
    block_d += [content]*quantity
    padding_bits_num -= len(content)*quantity

  for _ in range(padding_bits_num):
    block_d += random.choice(['0', '1'])

  return block_d, d_length

def shuffle_block_d(block_d: list) -> list:
  random.shuffle(block_d)
  while ''.join(block_d)[-1] == '0':
    random.shuffle(block_d)
  return block_d

def generate_key_of_csbda(block_d: list) -> (int, list):
  block_d = shuffle_block_d(block_d)
  d_bits_string = '0b'+''.join(block_d)
  d = int(d_bits_string, 2)
  return d, block_d

def generate_primes(e: int, d: int) -> (int, int, bool):
  ok = False
  for k in range(1, e):
    if (e*d-1) % k == 0:
      p = (e*d-1)//k + 1
      if isprime(p):
        ok = True
        break

  return p, k, ok

def xgcd(a: int, b: int):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0

def modinv(a: int, m: int):
    g, x, y = xgcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def decryption_csbda(c: int, d_block: list, n: int) -> (int):
  # 結果格納用
  memory = {}

  m = 1
  for b in d_block:
    # memoryに存在する場合は、
    # (1) len(b)回 2倍算を行い，
    # (2) memory[b]を書ける(そしてmod nをとる)
    if b in memory:
      for _ in b:
        m *= m
        m %= n
      m *= memory[b]
      m %= n
    else:
      t = 1
      for i in b:
        i = int(i)
        t *= t
        t %= n
        if i == 1:
          t *= c
          t %= n
      memory[b] = t

      for _ in b:
        m *= m
        m %= n
      m *= memory[b]
      m %= n
  
  return m


if __name__ == '__main__':
  ok = False
  while not ok:
    block_dp, dp_length = generate_block_of_csbda('key_params256_1.yml')
    dp, block_dp = generate_key_of_csbda(block_dp)
    p, kp, ok = generate_primes(E, dp)

  ok = False
  while not ok:
    block_dq, dq_length = generate_block_of_csbda('key_params256_1.yml')
    dq, block_dq = generate_key_of_csbda(block_dq)
    q, kq, ok = generate_primes(E, dq)

  n = p*q
  phi_n = (p-1)*(q-1)
  d = modinv(E, phi_n)
  q_inv = modinv(q, p)

  print("============== parameters ==============")
  print("e \t= {0}".format(E))
  print("dp \t= {0}".format(dp))
  print("kp \t= {0}".format(kp))
  print("dq \t= {0}".format(dq))
  print("kq \t= {0}".format(kq))
  print("p \t= {0}".format(p))
  print("q \t= {0}".format(q))
  print("n \t= {0}".format(n))
  print("phi_n \t= {0}".format(phi_n))
  print("d \t= {0}".format(d))
  print("e*dp % (p-1)\t= {0}".format((E*dp) % (p-1)))
  print("e*dq % (q-1)\t= {0}".format((E*dq) % (q-1)))
  print("e*d % ((p-1)(q-1))\t= {0}".format((E*d) % phi_n))
  print("============== results ==============")

  c = random.randint(1, n)
  mp = decryption_csbda(c, block_dp, p)
  mq = decryption_csbda(c, block_dq, q)
  print("c \t= {0}".format(c))
  print("mp \t= {0}".format(mp))
  print("mq \t= {0}".format(mq))
  print("m (crt) \t= {0}".format(mq+q*(q_inv*(mp-mq)%p)))
  print("m (real) \t= {0}".format(pow(c, d, n)))
