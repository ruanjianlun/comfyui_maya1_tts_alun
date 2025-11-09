# -*- coding: utf-8 -*-
# @Time    : 2025/11/8/周六 21:53
# @Author  : Administrator
# @File    : test.py
import torch

# 检查 PyTorch 版本
print(f"PyTorch Version: {torch.__version__}")

# 检查 CUDA 是否可用
is_cuda_available = torch.cuda.is_available()
print(f"CUDA Available: {is_cuda_available}")

if is_cuda_available:
    # 打印 PyTorch 使用的 CUDA 版本
    print(f"CUDA Version: {torch.version.cuda}")
    # 打印 GPU 数量
    print(f"Device Count: {torch.cuda.device_count()}")
    # 打印当前 GPU 的名称
    print(f"Current Device Name: {torch.cuda.get_device_name(torch.cuda.current_device())}")

