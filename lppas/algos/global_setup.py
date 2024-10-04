from sympy import nextprime, isprime
import random
import hashlib


def find_p_of_q(q: int):
    """找到一个素数p，使得q|p-1"""
    k = 1
    while True:
        p = k * q + 1
        if isprime(p):
            return p
        k += 1


def generate_large_prime(bits: int, ith: int = 1):
    """生成一个大素数"""
    return nextprime(2**(bits-1), ith)


def hash_function(_in: str):
    """简单的哈希函数实现，使用SHA256"""
    return int(hashlib.sha256(_in.encode()).hexdigest(), 16)


def pseudo_random_function(t, u, q):
    """伪随机函数，生成从t开始的u个伪随机数"""
    random.seed(t)
    return [random.randint(1, q-1) for _ in range(u)]


def pseudo_random_permutation(u, n):
    """伪随机置换，从1到n中选择u个数字并随机排列"""
    return random.sample(range(1, n+1), u)


def global_setup(u=16, n=128, bits=512):
    """全局设置算法"""
    q = generate_large_prime(bits)
    p = find_p_of_q(q)
    g = 2
    while pow(g, q, p) != 1:
        g += 1
    t = 0
    random_sequence = pseudo_random_function(t, u, q)
    permutation = pseudo_random_permutation(u, n)
    return p, q, g, hash_function, random_sequence, permutation


if __name__ == '__main__':
    u = 16  # 伪随机数序列长度
    n = 128  # 伪随机置换集合大小
    public_params = global_setup(u, n, bits=64)
    print("Global public parameters(gpp):", public_params)
