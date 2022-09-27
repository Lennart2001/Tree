import os
from anytree import Node, RenderTree


def get_all_files(path: str):
    file_memory = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if "venv" not in root and "idea" not in root:
                file_memory.append(os.path.join(root, file))
    return file_memory


def get_dir_list(path: str, rm_list: list):
    temp_list = os.listdir(path)
    for rm in rm_list:
        if rm in temp_list:
            temp_list.remove(rm)
    return temp_list


def is_file_done(path: str) -> bool:
    for ext in [".mp3", "mp4", ".jpeg", ".jpg", ".png", ".tex", ".db"]:
        if path.endswith(ext):
            return True

    with open(path, "r") as f:
        line = f.readline()
        if "DONE" in line.upper():
            return True
        else:
            return False


def is_directory_done(path: str) -> bool:
    all_files = get_all_files(path)
    for file in all_files:
        if not is_file_done(file):
            return False
    return True


def print_red_green(path: str, file: str):
    done = False
    new_path = os.path.join(path, file)
    if os.path.isdir(new_path):
        done = is_directory_done(new_path)
    else:
        done = is_file_done(new_path)
    if done:
        return "\x1b[1;32;40m" + file + "\x1b[0m"
    else:
        return "\x1b[1;31;40m" + file + "\x1b[0m"


directory_path = os.getcwd()
temp = "/"
for x in directory_path.split("/")[:-2]:
    temp = os.path.join(temp, x)

directory_path = temp


banking = Node(print_red_green(directory_path, "Banking"))


def createNodeTree(path, file, parent):
    new_path = os.path.join(path, file)
    if os.path.isdir(new_path):
        dir_contents = get_dir_list(new_path, ["venv", ".idea"])
        dir_node = Node(print_red_green(path, file), parent=parent)
        for element in dir_contents:
            createNodeTree(new_path, element, dir_node)
    else:
        Node(print_red_green(path, file), parent)


createNodeTree(directory_path, "Banking", banking)


for pre, fill, node in RenderTree(banking):
    print("\x1b[0;32;40m%s\x1b[0m%s" % (pre, node.name))

