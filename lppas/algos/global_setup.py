import os
import hashlib
import random

from ecdsa.curves import SECP256k1

'''
算法: GlobalSetup (由可信第三方执行)
输入: k (K 越大系统则越安全)
输出: gpp (全局参数)
步骤: 
1. 选择素数和生成元
选择两个大素数 p 和 q, 其中 p 是一个 k 位素数，q 是一个小于 p 的素数，且 p 除以 q 的余数为 1. 
p 和 q 用于定义一个素数阶的有限字段 Fp
2. 定义哈希函数
定义一个哈希函数，用于将任意长输入映射到定长序列
3. 定义伪随机函数和伪随机置换
定义一个伪随机函数，它根据输入生成一个伪随机序列
定义一个伪随机置换，它根据输入选择 n + 1 个元素的一个子集并生成这些元素的一个随机排列
4. 发布全局公共参数 gpp
'''


def hash_function(input_data: bytes):
    """简单的哈希函数，使用SHA-256"""
    return hashlib.sha256(input_data).hexdigest()


def pseudo_random_function(seed, u):
    """伪随机函数，基于给定的种子生成随机数序列"""
    random.seed(seed)
    return [random.randint(1, 100) for _ in range(u)]


class GlobalSetup:
    def __init__(self, sec_param: int):
        self.sec_param = sec_param

    def setup(self) -> dict:
        """全局设置算法，生成全局公共参数"""
        # 生成大素数和生成元，这里使用ECDSA的SECP256k1曲线参数
        p = SECP256k1.order
        g = SECP256k1.generator
        # 使用随机数作为哈希函数的输入，生成哈希基元
        h = hash_function(os.urandom(32)).encode('utf-8')
        # 安全参数决定伪随机函数输出的数量
        rand = pseudo_random_function(hash_function(h), self.sec_param)
        return {'p': p, 'g': g, 'h': h, 'rand': rand}


if __name__ == '__main__':
    # 假设安全参数为10, 执行全局设置
    gpp = GlobalSetup(sec_param=10).setup()
    print("Global Public Parameters:", gpp)
