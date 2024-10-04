import random
from lppas.algos.global_setup import global_setup, pseudo_random_function


def user_setup(global_public_params):
    """用户设置算法"""
    p, q, g, h, _, _ = global_setup()
    # 1. 用户U选择一个随机数skU∈Z_q作为他的秘密钥
    skU = random.randint(1, q - 1)
    # 2. 计算pkU=g^skUmodp作为他的公钥
    pkU = pow(g, skU, p)
    # 3. 选择对称加密和解密算法，这里我们假设使用AES算法的密钥为kU
    # 由于我们不实现具体的加密算法，我们只是生成一个随机的密钥
    kU = h(f'secret_key_{skU}')  # 使用哈希函数生成一个密钥
    # 4. 选择一个伪随机函数ct,u(·):Z_q→(Z*_q)^u，其中t表示从第t个开始的随机数
    # 这里我们使用全局公共参数中的伪随机函数，传入skU作为种子
    t = skU  # 使用skU作为种子
    u = 16  # 假设我们需要生成16个伪随机数
    prf_output = pseudo_random_function(t, u, q)

    # 用户发布他的公钥pkU，并保留他的秘密密钥skU;kU
    # 参数(EkU(·),DkU(·),ct,u(·))可以由用户自行决定保密或公开
    return pkU, skU, kU, prf_output
