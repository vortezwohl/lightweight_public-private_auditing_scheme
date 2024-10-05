# File:OnTagGen_setup.py
# Author:网安2302-03-李谢兴
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import random

# 假设的解密函数
def decrypt_with_private_key(private_key, ciphertext):
    # 使用 RSA 私钥解密
    decrypted = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode()
# 假设的哈希函数
def hash_function(data):
    return hashes.Hash(hashes.SHA256(), backend=default_backend()).update(data.encode()).digest()
def psi(eta, n):
    return [eta * (i+1) % (q-1) for i in range(n+1)]
# 假设的 h 函数
def h(data):
    return hash_function(data).hex()
# 从有限域中随机选择一个元素
def sample_Zq(q):
    return random.randint(1, q-1)
def OnTagGen(gpp,sk_U,k_U,m,pv,q):
    #第1步：Splits m into n blocks
    sF=len(m) # 假设文件大小为文件内容的长度
    sB=1024 # 假设块大小为1024字节
    n=sF//sB #计算块数

    #第2-4步：Split each block into s sections
    sS=sB//4 #假设块被分为4节
    blocks=[m[i*sB:(i+1)*sB] for i in range(n)]
    section= [[block[i*sS:(i+1)*sS] for i in range(len(block)//sS)] for block in blocks]

    #第5步：解密t_c
    t_c=decrypt_with_private_key(k_U,pv['t_c'])
    alpha=t_c.split('||')[0:-1]
    #将解密后的字符串 t_c 按照 || 分割成多个部分。取分割后列表的前 s 个元素（不包括最后一个元素），这些元素组成 alpha 列表。
    eta=t_c.split('||')[-1]
    #取分割后列表的最后一个元素，即 eta
    alpha=list(map(int,alpha))
    #将 alpha 列表中的每个字符串元素转换为整数。

    #第6步：选取文件名字
    name=sample_Zq(q)

    #第7步：从eta中获取key
    k_list = psi(int(eta),n)

    #第8步：创建波浪字符t
    u_list=[pow(gpp['g'], gpp['alpha'][j], gpp['p']) for j in range(gpp['s'])]
    titlde_t=f"{name}||{n}||{'|'.join(u_list)}||{t_c}"

    #第9步：计算西格玛0
    r_0=gpp['r'][0]
    sigma_0=(sk_U*int(h(titlde_t+'||'+r_0),16))-k_list[0]*int(r_0,16)%q

    #第10步：创建t_0
    t_0=f"{titlde_t}||{r_0}||{sigma_0}"

    #第11-13步：每个区块计算sigma_0
    tags=[t_0]
    for i,section in enumerate(section):
        r_i=gpp['r'][i]
        sum_alpha_m = sum(alpha[j-1] * int(section[j], 16) for j in range(len(section)))
        sigma_i=(sk_U*int(h(f"{name}||{i+1}||{r_i}"),16)+sum_alpha_m-k_list[i]*int(r_i,16))%q
        t_i=f"{r_i}||{sigma_i}"
        tags.append(t_i)
    return tags