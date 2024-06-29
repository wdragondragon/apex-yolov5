import hashlib
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
    labels_folder = 'D:/Desktop/模型/数据集/训练场沙漠/labels/'
    images_folder = 'D:/Desktop/模型/数据集/训练场沙漠/images/'

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


# 删除多余label
def delete_label():
    # 定义labels和images文件夹路径
    labels_folder = 'C:/Users/Administrator/Desktop/ow/labels/'
    images_folder = 'C:/Users/Administrator/Desktop/ow/images/'

    # 获取labels文件夹中所有txt文件的文件名（不带后缀）
    labels_files = [os.path.splitext(filename)[0] for filename in os.listdir(labels_folder) if
                    filename.endswith('.txt')]

    # 获取images文件夹中所有png文件的文件名（不带后缀）
    images_files = [os.path.splitext(filename)[0] for filename in os.listdir(images_folder) if
                    filename.endswith('.png')]

    # 删除labels文件夹中不在图片中的txt文件
    for filename in labels_files:
        if filename not in images_files and filename != 'classes':
            txt_file_path = os.path.join(labels_folder, filename + '.txt')
            os.remove(txt_file_path)
            print(f"remove label：{txt_file_path}")


# 切分
def split_label_image():
    # 定义labels和images文件夹路径
    folder = 'C:/Users/Administrator/Desktop/ow/5'
    labels_folder = folder + '/labels/'
    images_folder = folder + '/images/'

    new_folder = folder + '/all/'
    images_suffix = ".png"
    # 获取images文件夹中所有png文件的文件名（不带后缀）
    images_files = [os.path.splitext(filename)[0] for filename in os.listdir(images_folder) if
                    filename.endswith(images_suffix)]
    labels_files = [os.path.splitext(filename)[0] for filename in os.listdir(labels_folder) if
                    filename.endswith('.txt')]

    count = 0
    # 删除images文件夹中不在交集中的png文件
    for filename in images_files:
        count += 1
        png_file_path = os.path.join(images_folder, filename + images_suffix)
        labels_file_path = os.path.join(labels_folder, filename + ".txt")
        if count == 9:
            images_folder_new = new_folder + "images/test"
            labels_folder_new = new_folder + "labels/test"
        elif count == 10:
            images_folder_new = new_folder + "images/val"
            labels_folder_new = new_folder + "labels/val"
            count = 0
        else:
            images_folder_new = new_folder + "images/train"
            labels_folder_new = new_folder + "labels/train"

        os.makedirs(images_folder_new, exist_ok=True)
        os.makedirs(labels_folder_new, exist_ok=True)
        png_file_new_path = os.path.join(images_folder_new, filename + images_suffix)
        labels_file_new_path = os.path.join(labels_folder_new, filename + '.txt')
        shutil.copy(png_file_path, png_file_new_path)
        print(f"image path：{filename}")
        if filename in labels_files:
            shutil.copy(labels_file_path, labels_file_new_path)
            print(f"labels path：{filename}")


def class_change_1():
    # 源目录和目标目录
    src_dir = 'D:/dev/PycharmProjects/yolov5/apex_model/APEX/Data1/apex20000-单敌人/AL-YOLO-dataset-master/AL-YOLO-dataset-master/labels'
    # 遍历源目录中的所有文件
    src_folder = src_dir
    # for folder in ['test', 'train', 'val']:
    #     src_folder = os.path.join(src_dir, folder)
    max_label = 0
    for filename in os.listdir(src_folder):
        if filename.endswith('.txt'):
            src_file = os.path.join(src_folder, filename)
            # 读取源文件内容
            with open(src_file, 'r') as f_src:
                lines = f_src.readlines()

            for line in lines:
                line = line[:1]
                max_label = max(int(line), max_label)
    print(max_label)


def classification():
    folder = 'D:/dev/PycharmProjects/yolov5/apex_model/APEX/Data1/apex20000-单敌人/AL-YOLO-dataset-master/AL-YOLO-dataset-master'
    labels_folder = folder + '/labels/'
    images_folder = folder + '/images/'
    # 获取images文件夹中所有png文件的文件名（不带后缀）
    images_files = [filename for filename in os.listdir(folder) if
                    filename.endswith('.jpg')]
    labels_files = [filename for filename in os.listdir(folder) if
                    filename.endswith('.txt')]
    os.makedirs(labels_folder, exist_ok=True)
    os.makedirs(images_folder, exist_ok=True)
    for filename in images_files:
        file_path = os.path.join(folder, filename)
        file_new_path = os.path.join(images_folder, filename)
        shutil.move(file_path, file_new_path)
    for filename in labels_files:
        file_path = os.path.join(folder, filename)
        file_new_path = os.path.join(labels_folder, filename)
        shutil.move(file_path, file_new_path)


split_label_image()
