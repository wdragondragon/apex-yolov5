import os


# def check_files(directory):
#     # 遍历指定目录
#     for filename in os.listdir(directory):
#         # 获取完整文件路径
#         file_path = os.path.join(directory, filename)
#
#         # 打开并读取文件
#         with open(file_path, 'r') as file:
#             for line in file:
#                 # 如果行的开头不是'0'或'1'，打印文件名
#                 if not line.startswith(('0', '1')):
#                     print(filename)
#                     # break  # 找到一个就跳出，如果需要找到所有的行，就注释掉这一行
#
#
# # 使用你想要检查的目录替换'your_directory'
# check_files('./apex_model/labels/train')

import os
import shutil

# 源目录和目标目录
src_dir = '.\\apex_model\\1w2\\labels'
dst_dir = '.\\apex_model\\1w2\\labels1'

# 遍历源目录中的所有文件
for folder in ['test', 'train', 'val']:
    src_folder = os.path.join(src_dir, folder)
    dst_folder = os.path.join(dst_dir, folder)

    # 创建目标文件夹
    os.makedirs(dst_folder, exist_ok=True)

    for filename in os.listdir(src_folder):
        if filename.endswith('.txt'):
            src_file = os.path.join(src_folder, filename)
            dst_file = os.path.join(dst_folder, filename)

            # 读取源文件内容
            with open(src_file, 'r') as f_src:
                lines = f_src.readlines()

            # 修改内容
            new_lines = []
            for line in lines:
                if line.startswith('0'):
                    new_line = '1' + line[1:]
                elif line.startswith('1'):
                    new_line = '0' + line[1:]
                else:
                    new_line = line
                new_lines.append(new_line)

            # 写入新文件
            with open(dst_file, 'w') as f_dst:
                f_dst.writelines(new_lines)
