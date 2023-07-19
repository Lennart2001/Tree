#!/usr/bin/env python3

import os
import sys
from anytree import Node, RenderTree

IGNORE_DIRECTORIES = {"venv", ".idea", ".DS_Store", "__pycache__", ".git"}
IGNORE_FILES = [".mp3", ".mp4", ".jpeg", ".jpg", ".png", ".tex", ".db", ".txt", ".DS_Store"]

class Tree:
    def __init__(self):
        if len(sys.argv) < 2:
            self.directory_path = os.getcwd()
        else:   
            self.directory_path = sys.argv[1]
        if not os.path.exists(self.directory_path):
            print("\n\nFILE PATH NOT FOUND\n\n")
            sys.exit(5)
        self.tree_name = os.path.basename(self.directory_path)
        self.counts = {
            'files': {'not_started': 0, 'in_progress': 0, 'completed': 0},
            'directories': {'not_started': 0, 'in_progress': 0, 'completed': 0}
        }
        self.status_cache = {}

    def get_status(self, path: str) -> int:
        if path in self.status_cache:
            return self.status_cache[path]

        if os.path.isfile(path):
            if path.endswith(tuple(IGNORE_FILES)):
                status = 2
            else:
                with open(path, "r") as f:
                    line = f.readline()
                    if "DONE" in line.upper():
                        status = 2
                    elif "PROG" in line.upper():
                        status = 1
                    else:
                        status = 0
            self.counts['files']['completed' if status == 2 else 'in_progress' if status == 1 else 'not_started'] += 1
        else:  # directory
            dir_contents = [os.path.join(path, x) for x in os.listdir(path) if x not in IGNORE_DIRECTORIES]
            statuses = [self.get_status(x) for x in dir_contents]
            if all(s == 2 for s in statuses):
                status = 2
            elif any(s in {1, 2} for s in statuses):
                status = 1
            else:
                status = 0
            self.counts['directories']['completed' if status == 2 else 'in_progress' if status == 1 else 'not_started'] += 1

        self.status_cache[path] = status
        return status

    def print_red_green(self, path: str) -> str:
        status = self.get_status(path)
        file_name = os.path.basename(path).upper() if os.path.isdir(path) else os.path.basename(path).lower()
        color_code = {
            0: "\x1b[1;31;40m",  # Red
            1: "\x1b[1;33;40m",  # Yellow
            2: "\x1b[1;32;40m",  # Green
        }.get(status, "\x1b[1;32;40m")  # Default to green
        return f"{color_code}{file_name}\x1b[0m"

    def create_node_tree(self, path: str, parent):
        for item in os.listdir(path):
            new_path = os.path.join(path, item)
            if item not in IGNORE_DIRECTORIES:
                node = Node(self.print_red_green(new_path), parent)
                if os.path.isdir(new_path):
                    self.create_node_tree(new_path, node)

    def build_tree(self):
        self.root = Node(self.print_red_green(self.directory_path))
        self.create_node_tree(self.directory_path, self.root)

    def print_tree(self):
        for pre, fill, node in RenderTree(self.root):
            print("\x1b[1;32;40m%s\x1b[0m%s" % (pre, node.name))
        self.print_files_dirs()

    def print_files_dirs(self):
        print(f'{"":<15} | {"Not Started":<12} | {"In Progress":<12} | {"Completed":<10} | {"Total":<10}')
        print('-' * 63)
        for category in ['files', 'directories']:
            category_counts = self.counts[category]
            total = sum(category_counts.values())
            print(f'{category.capitalize():<15} | {category_counts["not_started"]:<12} | {category_counts["in_progress"]:<12} | {category_counts["completed"]:<10} | {total:<10}')
        print('-' * 63)


tree = Tree()
tree.build_tree()
tree.print_tree()
