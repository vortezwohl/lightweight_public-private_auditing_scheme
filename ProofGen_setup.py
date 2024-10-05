# File:ProofGen_setup.py
# Author:网安2302-03-李谢兴
def(chal,gpp,m,tags):
    u,e=chal
    s = gpp['s']
    q = gpp['q']
    g = gpp['g']
    h = gpp['h']
    #第1步：这里我们假设L是一个列表，用于存储证明的各个部分
    L = []
    #第2步：使用e作为种子生成伪随机数序列
    random_sequence = pseudo_random_function(e, s, q)
    #第3-5步：计算beta_j
    for j in range(1,s+1):
        # 假设m[u-1]是第u块的内容，可以进一步分割为节
        mij=m[u-1][j-1]# 获取第u块的第j节
        vi = pow(g, random_sequence[j - 1], q)# 计算v_i
        beta_j = (int(mij, 16) * vi % q)#疑似缺少累加环节，请注意！！！！！！！！！
        L.append(beta_j)
    # Step 6: 将计算得到的β_j和其他信息结合起来生成最终的响应
    resp = []
    for j, beta_j in enumerate(L):
        r_i = tags['r'][u - 1]
        sigma_i = tags['sigma'][u - 1]

        # 假设我们需要结合r_i, sigma_i和β_j来生成响应的一部分
        response_part = (r_i, sigma_i, beta_j)
        resp.append(response_part)

    # 返回响应
    return resp
