import os
import os
import shutil


# 打印不在标注类别里的txt
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


# label 类别转换
def class_change():
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


# 首先，我要将txt中内容为空的文件删除，然后我需要将这两个文件夹的文件名做交集，确保每个txt与每个png相对应。
def check_label_image():
    # 定义labels和images文件夹路径
    labels_folder = './apex_model/save/labels/2023-08-12-16-13-09'
    images_folder = './apex_model/save/images/2023-08-12-16-13-09'

    # 获取labels文件夹中所有txt文件的文件名（不带后缀）
    labels_files = [os.path.splitext(filename)[0] for filename in os.listdir(labels_folder) if
                    filename.endswith('.txt')]

    # 删除labels文件夹中内容为空的txt文件
    for filename in labels_files:
        txt_file_path = os.path.join(labels_folder, filename + '.txt')
        if os.path.getsize(txt_file_path) == 0:
            os.remove(txt_file_path)
            labels_files.remove(filename)

    # 获取images文件夹中所有png文件的文件名（不带后缀）
    images_files = [os.path.splitext(filename)[0] for filename in os.listdir(images_folder) if
                    filename.endswith('.png')]

    # 找到labels和images文件名的交集
    common_files = set(labels_files) & set(images_files)

    # 删除labels文件夹中不在交集中的txt文件
    for filename in labels_files:
        if filename not in common_files and filename != 'classes':
            txt_file_path = os.path.join(labels_folder, filename + '.txt')
            os.remove(txt_file_path)
            print(f"remove label：{txt_file_path}")

    # 删除images文件夹中不在交集中的png文件
    for filename in images_files:
        if filename not in common_files:
            png_file_path = os.path.join(images_folder, filename + '.png')
            os.remove(png_file_path)
            print(f"remove image：{png_file_path}")

    # 确保每个txt与每个png相对应
    for filename in common_files:
        txt_file_path = os.path.join(labels_folder, filename + '.txt')
        png_file_path = os.path.join(images_folder, filename + '.png')
        # 在这里可以进行进一步的处理，例如将txt和png文件进行匹配操作
        print(f"Matched: {txt_file_path} - {png_file_path}")


check_label_image()
