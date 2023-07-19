# README for TreeView.py

## Description:

`treeview.py` is a Python script that provides a visual representation of the files and directories in a directory tree. It color-codes files and directories based on their status:

- Red: Not Started
- Yellow: In Progress
- Green: Completed

The script counts the number of files and directories at each status level and prints this information in a table format.

## Requirements:

- Python 3.x
- Anytree Python library

## Installation:

### Linux/MacOS

1. Install the required Python libraries, using pip:

```bash
pip3 install -r requirements.txt
```

2. Make the Python script executable:

```bash
chmod +x /path/to/treeview.py
```

3. Move the script to a directory in your PATH to run it from any location (optional):

```bash
sudo mv /path/to/treeview.py /usr/local/bin/treeview
```

## Usage:

Run the script in the terminal by typing 'treeview' (or './treeview.py' if you didn't move it to a directory in your PATH).

The script will display the directory tree for the current directory, color-coding each file and directory based on its status. It will then print a table showing the number of files and directories at each status level.

For example, to display the directory tree for the current directory, use:
```bash
treeview
```

Or, to display the directory tree for a specific directory, use:
```bash
treeview /path/to/directory
```

## Notes:
The status of a file is determined by its extension and by whether the words 'DONE' or 'PROG' appear in the first line of the file. 
The status of a directory is determined by the statuses of its contents.


