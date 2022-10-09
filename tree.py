#!/usr/bin/env python3
import os
import sys
import warnings
from anytree import Node, RenderTree


class Tree:
    def __init__(self):
        if len(sys.argv) < 2:
            warnings.warn("\n\n*********\n\nNO FILE INPUT\n\n*********\n")
            sys.exit(4)
        if not os.path.exists(sys.argv[1]):
            warnings.warn("FILE PATH NOT FOUND")
            sys.exit(5)
        self.directory_path = "/"
        for x in sys.argv[1].split("/")[:-1]:
            self.directory_path = os.path.join(self.directory_path, x)
        self.tree_name = sys.argv[1].split("/")[-1]
        self.files_prog = 0
        self.files_total = 0
        self.files_done = 0
        self.directories_prog = 0
        self.directories_total = 0
        self.directories_done = 0
        self.root = Node

    def get_all_files(self, path: str):
        file_memory = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if "venv" not in root and "idea" not in root:
                    file_memory.append(os.path.join(root, file))
        return file_memory

    def get_dir_list(self, path: str, rm_list: list):
        temp_list = os.listdir(path)
        for rm in rm_list:
            if rm in temp_list:
                temp_list.remove(rm)
        return temp_list

    def is_file_done(self, path: str) -> int:
        for ext in [".mp3", "mp4", ".jpeg", ".jpg", ".png", ".tex", ".db"]:
            if path.endswith(ext):
                return 2
        """
        ***** CONVENTION *****
        0 - Not Started
        1 - In Progress
        2 - Finished
        """
        with open(path, "r") as f:
            line = f.readline()
            if "DONE" in line.upper():
                return 2
            elif "PROG" in line.upper():
                return 1
            else:
                return 0

    def is_directory_done(self, path: str) -> int:
        all_files = self.get_all_files(path)
        dir_prog = 0
        for file in all_files:
            temp = self.is_file_done(file)
            if temp == 0:
                return 0
            if dir_prog == 0 and temp == 1:
                dir_prog = 1
        if dir_prog == 1:
            return 1
        return 2

    def print_red_green(self, path: str, file: str):
        new_path = os.path.join(path, file)
        if os.path.isdir(new_path):
            file = file.upper()
            color = self.is_directory_done(new_path)
            self.directories_total += 1
            if color == 1:
                self.directories_prog += 1
            elif color == 2:
                self.directories_done += 1
        else:
            file = file.lower()
            color = self.is_file_done(new_path)
            self.files_total += 1
            if color == 1:
                self.files_prog += 1
            elif color == 2:
                self.files_done += 1
        if color == 0:
            return "\x1b[1;31;40m" + file + "\x1b[0m"
        elif color == 1:
            return "\x1b[1;33;40m" + file + "\x1b[0m"
        else:
            return "\x1b[1;32;40m" + file + "\x1b[0m"

    def print_files_dirs(self):

        files_prog = 6 - len(str(self.files_prog))
        files_done = 6 - len(str(self.files_done))
        files_total = 6 - len(str(self.files_total))

        dirs_prog = 6 - len(str(self.directories_prog))
        dirs_done = 6 - len(str(self.directories_done))
        dirs_total = 6 - len(str(self.directories_total))

        print("\n\n  In Prog  |  Finished  |  Total")
        files_in_prog = "     %d" % self.files_prog + " " * files_prog + "|"
        files_in_done = "      %d" % self.files_done + " " * files_done + "|"
        files_in_total = "    %d" % self.files_total + " " * files_total + "   Files\n"
        files = files_in_prog + files_in_done + files_in_total

        dirs_in_prog = "     %d" % self.directories_prog + " " * dirs_prog + "|"
        dirs_in_done = "      %d" % self.directories_done + " " * dirs_done + "|"
        dirs_in_total = "    %d" % self.directories_total + " " * dirs_total + "   Directories\n"
        dirs = dirs_in_prog + dirs_in_done + dirs_in_total
        print(files + dirs)

    def create_node_tree(self, path, file, parent):
        new_path = os.path.join(path, file)
        if os.path.isdir(new_path):
            dir_contents = self.get_dir_list(new_path, ["venv", ".idea"])
            dir_node = Node(self.print_red_green(path, file), parent=parent)
            for element in dir_contents:
                self.create_node_tree(new_path, element, dir_node)
        else:
            Node(self.print_red_green(path, file), parent)

    def build_tree(self):
        self.root = Node(self.print_red_green(self.directory_path, self.tree_name))
        self.create_node_tree(self.directory_path, self.tree_name, self.root)

    def print_tree(self):
        for pre, fill, node in RenderTree(self.root):
            print("\x1b[1;32;40m%s\x1b[0m%s" % (pre, node.name))
        self.print_files_dirs()


tree = Tree()
tree.build_tree()
tree.print_tree()
