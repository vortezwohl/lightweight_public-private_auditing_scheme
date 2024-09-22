from ecdsa.keys import SigningKey
from ecdsa.curves import SECP256k1

'''
算法: UserSetup
输入: gpp (全局参数)
输出: sk, pk (私钥，公钥)
步骤: 
1. 生成私钥
用户利用 gpp 中的信息生成一个随机的私钥
2. 计算公钥
使用私钥和椭圆曲线的生成元，通过特定的椭圆曲线算法计算出对应的公钥，公钥是私钥在曲线上的一个点
3. 返回密钥对
私钥严格包密，公钥则公开用于后续验证
'''


def user_setup(gpp: dict):
    """
    用户设置算法，生成用户的密钥对
    :param gpp: 全局公共参数
    :return: 用户的私钥和公钥
    """
    # 生成随机的私钥
    sk = SigningKey.generate(curve=SECP256k1)

    # 计算对应的公钥
    vk = sk.get_verifying_key()

    # 返回用户的私钥和公钥
    return sk, vk


# 示例：执行用户设置
gpp = {}  # 假设全局公共参数已经由可信权威生成并提供给用户
user_private_key, user_public_key = user_setup(gpp)
print("User's Private Key:", user_private_key.to_string().hex())
print("User's Public Key:", user_public_key.to_string().hex())