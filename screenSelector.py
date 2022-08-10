#!/usr/bin/env python3
import subprocess # Used for unix commmands
from subprocess import PIPE, STDOUT # Used for unix commmands
import os
from pathlib import Path
import sys
import json
import ast


def execute(cmd):
    exec = subprocess.Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    output = exec.communicate()[0]
    exitcode = exec.returncode
    if exitcode > 2:
        print("Offending line:",cmd)
    return output.decode("utf-8").strip(), exitcode


def list_monitors():
    raw_monitors = execute('hwinfo --monitor --short')[0]
    monitors = []
    for monitor in raw_monitors.split('\n'):
        monitors.append(monitor.strip())
    del monitors[0]
    monitors.sort()
    return monitors


def find_layout(current_monitors):
    directory = os.path.expanduser('~/.screenlayout/')
    files = Path(directory).glob('*.json')
    print("cm:",current_monitors)
    layout_found = 0
    for file in files:
        with open(file, 'r') as f:
            layout_raw = list(f)[0]
            layout = ast.literal_eval(layout_raw)
            layout = [n.strip() for n in layout]
            layout.sort()
            if layout == current_monitors:
                layout_found += 1
                path = str(file)
                print("Layout is already used.")
            else: 
                pass


    if layout_found == 0:
        print("no matching layout found")
        layout_bool = False
    elif layout_found == 1:
        layout_bool = True
    elif layout_found > 1:
        print("Too many matching layout found, picking first one")
        path = path[0]
        layout_bool = False
    else:
        layout_bool = False

    return layout_bool, path


def create_layout(current_monitors):
    execute("arandr")
    directory = os.path.expanduser('~/.screenlayout/')
    layout_name = execute(f"ls -t {directory}")[0].split("\n")[0].split(".")[0]
    with open(directory+layout_name+".json", "w") as outfile:
        outfile.write(str(current_monitors))


def activate_layout(path_layout):
    full_fileName = path_layout.split("/")[-1]
    split_fileName = full_fileName.split(".")[0]
    path = path_layout.rsplit('/', 1)[0]+"/"
    print("Activating layout", split_fileName)
    execute(f"bash {path}{split_fileName}.sh")


def manual():
    current_monitors = list_monitors()
    check_layoutExsists = find_layout(current_monitors)
    if check_layoutExsists[0] == True:
        print("Layout already exsists:", check_layoutExsists[1])
        yes_no = input("do you want to activate layout? (y/n)")
        if yes_no == "y":
            activate_layout(check_layoutExsists[1])
        else:
            sys.exit()
    else:
        print("There is no layout present with your current monitors")
        yes_no = input("do you want to Create layout? (y/n)")
        print(current_monitors)
        if yes_no == "y":
            create_layout(current_monitors)
        else:
            sys.exit()


def automated():
    current_monitors = list_monitors()
    check_layoutExsists = find_layout(current_monitors)
    if check_layoutExsists[0] == True:
        activate_layout(check_layoutExsists[1])
    else:
        # Future notify user that the layout does not excists
        sys.exit()


def main():
    if len(sys.argv) < 2:
        automated()
    else:
        if sys.argv[1] == "--manual" or "-m" or "--create" or "-c":
            print("fuck")
            manual()
        elif sys.argv[1] == "--automated" or "-a":
            automated()
        else:
            print("screenSelector options are following")
            print("--manual -m, --automated -a, --create -c")
            sys.exit()


main()