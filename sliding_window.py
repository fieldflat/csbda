# 必要なライブラリをインポート
import random
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.special import comb

mc_count_list = []
mm_count_list = []
binary_mm_list = []
binary_mc_list = []
mod_count4_list = []
mult_count4_list = []

# ###########################
# 以下，鍵生成に使用するメソッド
# ###########################

#
# 関数：generate_c
# 引数：a, b(どちらも整数値)
# 機能：aからbまでのランダムな整数値を返す
# 返り値：ランダム整数値(a .. b)
#
def generate_c(a, b):
    return random.randint(a, b)

#
# 関数：make_d
# 引数：鍵長length, 1の最上位ビット位置top_bit, 鍵のハミング重みweight
# 機能：鍵長length, 1の最上位ビット位置top_bit, 鍵のハミング重みweightを
#      満たす鍵をランダムに1つ作成する
# 返り値：秘密鍵の配列(配列長length)
#
# 20200410 make_dの返り値が全て奇数となるように変更！
def make_d(length, top_bit, weight):
    if length < top_bit + weight - 1:
        raise Exception

    # (length - top_bit)個の0を配列に追加する
    l = [0] * (length - top_bit - (weight - 1))  # 20200410 変更

    # (weight - 1)個の1を配列に追加する
    # l.extend([1]*(weight - 1))
    l.extend([1]*(weight - 2))  # 20200410 変更

    # 配列lをシャッフルする
    random.shuffle(l)

    # 配列return_listに，[0, 0, ..., 1]の形の配列を追加する(「1」は1個，「0」は(top_bit-1)個)
    return_list = [0] * (top_bit-1)
    return_list.extend([1])

    # return_listをlに結合する
    return_list.extend(l)

    return_list.extend([1])

    return return_list

#
# 関数：change_decimal
# 引数：2進数配列list
# 機能：2進数形式で格納されているlistの10進数値を返す
# 返り値：10進数値
#
def change_decimal(list):
    return int(''.join(map(str, list)), 2)


# ############################
# 以下，バイナリ法で使用するメソッド
# ############################

#
# 関数：multiply
# 引数：x, y, mult_count
# 機能：x * yを返す
# 返り値：x * y, mult_count+1
#
def multiply(x, y, mult_count):
    return x*y, mult_count+1

#
# 関数：modulo
# 引数：x, y, mod_count
# 機能：x % yを返す
# 返り値：x % y, mod_count+1
#
def modulo(x, y, mod_count):
    ans = x % y
    if x > y:
        return ans, mod_count+1
    else:
        return ans, mod_count

#
# 関数：binary_method
# 引数：暗号文c，秘密鍵d(2進数配列)，N, 鍵長d_length, 1の最上位ビット位置d_top_bit
# 機能：c^d (mod N)を計算し，それぞれ剰余演算回数と乗算回数と平文を返す
# 返り値：平文，剰余演算回数，乗算回数
#


def binary_method(args):

    mod_count = 0  # 剰余計算のカウント
    mult_count = 0  # 乗算計算のカウント
    m = args["c"]

    l = args["d_length"]  # 2進表現の長さを獲得.

    for i in range(args["d_top_bit"], l):
        #m = (m ** 2) % argsN
        m, mult_count = multiply(m, m, mult_count)  # m = m*mの実行
        m, mod_count = modulo(m, args["N"], mod_count)  # m % Nの実行
        binary_mm_list.append(m//(2**1010))
        if args["d"][i] == 1:
            #m = (m*argsc) % argsN
            m, mult_count = multiply(m, args["c"], mult_count)  # m = m*cの実行
            m, mod_count = modulo(m, args["N"], mod_count)  # m % Nの実行
            binary_mc_list.append(m//(2**1010))
    return m, mod_count, mult_count


# ############################
# 以下，ModBin法で使用するメソッド
# ############################

#
# 関数：mod_equal_minus_1
# 引数：N, R
# 機能：N*(N') mod R = -1となるN'を返す
# 返り値：N'
#
def mod_equal_minus_1(N, R):
    result = 0
    t = 0
    r = R
    i = 1

    while (r > 1):

        if (t % 2 == 0):
            t += N
            result += i

        t //= 2
        r //= 2
        i *= 2

    return result

#
# 関数：decimal_to_binary_len
# 引数：10進数整数n
# 機能：10進数nを2進数に直し，その桁数を返す．
# 返り値：2進数の桁数
#
def decimal_to_binary_len(n):
    return len(bin(n)[2:])


# #################################
# 以下，スライディングウィンドウ法で利用するメソッド
# #################################
def count_leading_zeros(list):
  ans = 0
  for item in list:
    if item == 0:
      ans += 1
    else:
      return ans
  return ans


def count_trailing_zeros(list):
  ans = 0
  for item in reversed(list):
    if item == 0:
      ans += 1
    else:
      return ans
  return ans


def sliding_window_method(args):
  mod_count = 0
  mult_count = 0
  square_mod = 0
  mult_mod = 0
  block_num = 0
  c_dict = {}
  c_dict[1] = args["c"]
  tmp, mult_count = multiply(args["c"], args["c"], mult_count)
  c_dict[2], mod_count = modulo(tmp, args["N"], mod_count)
  a = 1
  z = 0
  for i in range(1, 2**(args["w"]-1)):
    tmp, mult_count = multiply(c_dict[2*i-1], c_dict[2], mult_count)
    c_dict[2*i+1], mod_count = modulo(tmp, args["N"], mod_count)
  print('事前計算部分のmod_count = {0}'.format(mod_count))
  print('事前計算部分のmult_count = {0}'.format(mult_count))
  i = 0
  while i <= args["d_length"]-1:
    clz = count_leading_zeros(args["d"][i:])
    z = z + clz  # 先頭何ビットが0であるか
    i += clz  # 最初の1のビット位置
    s = min(args["d_length"]-i, args["w"])
    u = args["d"][i:i+s]  # ブロック幅
    t = count_trailing_zeros(u)  # 最後何ビットが0であるか
    if t != 0:
      u = u[:-t]
    for _ in range(0, z+s-t):
      tmp, mult_count = multiply(a, a, mult_count)
      check = mod_count
      a, mod_count = modulo(tmp, args["N"], mod_count)
      if(check != mod_count):
        square_mod += 1
    tmp, mult_count = multiply(a, c_dict[change_decimal(u)], mult_count)
    check = mod_count
    a, mod_count = modulo(tmp, args["N"], mod_count)
    if (check != mod_count):
      mult_mod += 1
    i += s
    z = t
    block_num += 1
  print('square_mod = {0}, mult_mod = {1}, ブロックの個数 = {2}'.format(
      square_mod, mult_mod, block_num))
  return a, mod_count, mult_count


# #################################
# 以下，ヒストグラム作成に使用するメソッド
# #################################
def plotting(list, title, execute):
    x = np.array(list)
    t = 1 if x.max()-x.min() == 0 else x.max()-x.min()+1
    freq_dist = plt.hist(x, bins=t)
    print(freq_dist)
    plt.title(title)
    if execute == 1:
        plt.show()

    bottom_count = round(freq_dist[1][0])
    index_list = []
    freq_list = []
    for i in range(0, len(freq_dist[0])):
        index_list.append(int(bottom_count + i))
        freq_list.append(int(freq_dist[0][i]))

    with open('{0}.csv'.format(title), 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(index_list)
        writer.writerow(freq_list)

#
# 関数：binary_d
# 引数：d
# 機能：10進数を2進数配列にして返す
# 返り値：2進数配列
#
def binary_d(d):
    array_d = []
    while(1):
        array_d.append(d % 2)
        d = d // 2
        if(d == 0):
            break
    array_d.reverse()
    return array_d

#
# メイン関数
#
if __name__ == '__main__':

    #
    # 定数
    #
    # p = 1683317
    # q = 6700417

    # # N > 2 ** 254の条件を満たす
    # p = 256745764655464715289043834762721676979
    # q = 200871874067534114215487430360232242973

    # N > 2 ** 1000の条件を満たす
    # p = 3273390607896141870013189696827599152216642046043064789483291368096133796404674554883270092325904157150886684127560071009217256545885393053328527593931
    # q = 3273390607896141870013189696827599152216642046043064789483291368096133796404674554883270092325904157150886684127560071009217256545885393053328527596429

    # N = 1024ビット
    # p = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006098247
    # q = 13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006106897

    # N = 768ビット
    # p = 39402006196394479212279040100143613805079739270465446667948293404245721771497295682005996489500781484458485932372897
    # q = 59103009294591718818418560150215420707619608905698170001922440106368582657245815917121399382327373461209941985469873

    # N = 512ビット
    # p = 115792089237316195423570985008687907853269984665640564039457584007913129663261
    # q = 117601340631649260977064281649448656413477328176041197852574108758036772347269

    # N = 256
    p = 340282366920938463463374607431768321829
    q = 425352958651173079329218259289710332611

    # N = 128ビット
    # p = 18446744073709625221
    # q = 23058430092137006111
    # p = 16610794955794715761
    # q = 15187572242927430539

    # N = 16ビット
    # p=251
    # q=229

    N = p * q
    phi_N = (p-1)*(q-1)  # Nのオイラー数
    Loop_times = 100  # ループ回数
    d_length = 256  # dの鍵長
    d_top_bit = 1  # dにおける1の最上位ビット
    d_weight = 128  # dの重み
    R = 2 ** decimal_to_binary_len(N)
    R_2 = R*R % N
    N_dash = mod_equal_minus_1(N, R)

    # sliding-window幅
    w = 5

    correct = 0
    sum_of_mod_count2 = 0
    sum_of_mod_count3 = 0
    sum_of_mod_count4 = 0
    incorrect = 0  # バイナリ法で剰余演算回数が理論値と違っていた場合にカウントする
    binary_mod_count_list = []
    modbin_mod_count_list = []
    modbin_z_count_list = []
    crt_modbin_mod_count_list = []
    sliding_window_method_list = []
    crt_with_sliding_window_method_list = []

    # 各高速化アルゴリズムの引数
    algo_args = {}

    for i in range(0, Loop_times):
        print('N = {0}'.format(N))
        print('R = {0}'.format(R))

        # 暗号文の生成
        c = generate_c(1, N-1)

        # 秘密鍵の作成(2進数)
        d = make_d(d_length, d_top_bit, d_weight)
        d_num = change_decimal(d)

        print('\n\n************* {0}回目 ***************'.format(i+1))
        print(
            '******** c = {0} , d = {1} ({2}bit)  ********\n'.format(c, d_num, len(d)))

        #
        # 各高速化アルゴリズムで使用する引数
        #
        algo_args["c"] = c
        algo_args["d"] = d
        algo_args["N"] = N
        algo_args["d_length"] = d_length

        #
        # sliding window 法
        #
        algo_args["w"] = w
        m4, mod_count4, mult_count4 = sliding_window_method(algo_args)
        print('m4={0}'.format(m4))
        print('mod_count4={0} | mult_count4={1}'.format(mod_count4, mult_count4))
        mod_count4_list.append(mod_count4)
        mult_count4_list.append(mult_count4)

    print('mod_coun4の平均: {0}'.format(sum(mod_count4_list)/len(mod_count4_list)))
    print('mult_coun4の平均: {0}'.format(sum(mult_count4_list)/len(mult_count4_list)))
