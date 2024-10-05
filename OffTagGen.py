# File:OffTagGen.py
# Author:网安2302-03-李谢兴
from sympy import nextprime, mod_inverse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import random
def sample_Zq(q):
    return random.randint(1, q-1)
# 假设的加密函数
def encrypt_with_private_key(private_key, message):
    # 使用 RSA 私钥加密
    public_key = private_key.public_key()
    encrypted = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted
# 假设的 psi 函数
def psi(eta, n):
    # 这里我们只是简单地返回一个密钥列表，实际应用中需要根据具体需求定义
    return [eta + i for i in range(n+1)]
def Algorithm1(g, p, s, k_U, psi, encrypt):
    eta=sample_Zq(p-1)
    #随机选择eta从Zq
    u=[]
    #创建u数组
    alpha=[]
    #创建alpha数组
    for j in range(1,s+1):
        alpha_j=sample_Zq(p-1)
        #从Zq中获取随机alpha_j
        u_j=pow(g,alpha_j,p)
        #计算u_j
        u.append(u_j)
        #将u_j添加到u数组里面
        alpha.append(alpha_j)
    t_c=encrypt(k_U,''.join(map(str,alpha+[eta])))
    #生成t_c
    k_list=psi(eta,s-1)
    #生成k列表
    r=[]
    #生成r列表
    for i in k_list:
        r_i=pow(g,i,p)
        r.append(r_i)
    pv={
        'u':u,
        'r':r,
        't_c':t_c
    }
    return pv




