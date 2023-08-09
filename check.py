import os

def check_files(directory):
    # 遍历指定目录
    for filename in os.listdir(directory):
        # 获取完整文件路径
        file_path = os.path.join(directory, filename)

        # 打开并读取文件
        with open(file_path, 'r') as file:
            for line in file:
                # 如果行的开头不是'0'或'1'，打印文件名
                if not line.startswith(('0', '1')):
                    print(filename)
                    # break  # 找到一个就跳出，如果需要找到所有的行，就注释掉这一行

# 使用你想要检查的目录替换'your_directory'
check_files('./apex_model/labels/train')