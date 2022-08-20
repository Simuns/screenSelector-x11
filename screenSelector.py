#!/usr/bin/env python3
from sre_constants import MAX_REPEAT
import subprocess # Used for unix commmands
from subprocess import PIPE, STDOUT # Used for unix commmands
import os
from pathlib import Path
import sys
import json
import ast
import time
import re
##Testing
def get_fileTimestamp(file_path):
    import os.path, time
    lastModified_stamp = time.ctime(os.path.getmtime(file_path))
    creation_stamp = time.ctime(os.path.getctime(file_path))
    return lastModified_stamp, creation_stamp 




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
        path = ""
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
    pre_arandr = time.ctime()
    execute("arandr &")
    print("Create layout and save it.\n Press Exit Arandr when done")
    directory = os.path.expanduser('~/.screenlayout/')
    layout_file = execute(f"ls -t {directory}")[0].split("\n")[0]
    layout_name =layout_file.split(".")[0]
    post_arandr = time.ctime(os.path.getmtime(directory+layout_file))
    if pre_arandr < post_arandr:
        pass
        print(f"Preset {layout_name} was saved")
    else:
        print("You did not save a preset.\nExiting...")
        sys.exit()
    with open(directory+layout_name+".json", "w") as outfile:
        outfile.write(str(current_monitors))
    print("Layout created")

def automirror_layout():
    resline = False
    res = []
    screens = {}
    substring = " connected "
    raw_monitors = execute("xrandr")[0]
    for line in raw_monitors.splitlines():

        # if last line included header for connected monitor, then list highest monitor resolution, and all hz options into array
        if resline == True:
            resline = False
            
            pattern_resolution = re.compile(r'\d{3,5}x\d{3,5}')
            resolution_raw = pattern_resolution.findall(line)[0]
            resolution = resolution_raw.split('x')
            pattern_ghz = re.compile(r'\d{2,3}\.\d{2,3}')
            frequency = pattern_ghz.findall(line)
            sorted_frequency = frequency.sort()

            #append max resolution list to dictionary
            screens[monitor_name]['max_resolution'] = []
            for direction in resolution:
                screens[monitor_name]['max_resolution'].append(direction) 

            #append frequency list to dictionary            
            count = 0
            screens[monitor_name]['frequency'] = []
            for option in frequency:
                screens[monitor_name]['frequency'].append(frequency[count])
                count += 1
        
        # if line includes a connected monitor, then index the monitor into dictionary
        if substring in line:
            monitor_name = line.split(' ', 1)[0]
            screens[monitor_name] = {}
            screens[monitor_name]['primary'] = bool
            bool_primary = bool(re.search(" primary ", line))
            if bool_primary == False:
                screens[monitor_name]['primary'] = False
            else:
                screens[monitor_name]['primary'] = True
            resline = True

    # verify if monitors run same resolution
    for connected in screens:
        print(connected)
        #if screens[connected][max_]
        
    return screens


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
    if len(sys.argv) == 1:
        print("Options...\n --manual -m, --automated -a, --create -c")
        sys.exit()

    elif sys.argv[1] == "--manual" or sys.argv[1] == "-m" or sys.argv[1] == "--create" or sys.argv[1] == "-c":
        manual()

    elif sys.argv[1] == "--automated" or sys.argv[1] == "-a":
        automated()

    else:
        print("Options...\n --manual -m, --automated -a, --create -c")
        sys.exit()
    return

#main()
screens = automirror_layout()
print(json.dumps(screens, indent = 4))