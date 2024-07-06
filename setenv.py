import os

print("配置cuda环境变量：CUDA_MODULE_LOADING=LAZY")
os.environ["CUDA_MODULE_LOADING"] = "LAZY"
os.environ["VALIDATE_TYPE"] = "ai"
