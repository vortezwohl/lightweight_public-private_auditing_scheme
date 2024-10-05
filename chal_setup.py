# File:chal_setup.py
# Author:网安2302-03-李谢兴
def chal(n,u,e):
    # n - - 文件m的块数。
    # u - - 用户选择的块数，范围在1到n（包含）。
    # e - - 随机数e，用作伪随机函数和伪随机置换的种子。
    if 1 <= u < n:
        chal = (u, e)
        return chal
    else:
        raise ValueError("u must be in the range of [1, n).")

