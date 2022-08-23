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

def notify(messageType, message):
    # verify user has notify installed
    fact_installed = execute("which notify-send")[1]
    if fact_installed > 0:
        pass
    else:
        if messageType == "layout":
            execute(f"notify-send --urgency=normal \"Screen layout:\" {message}")
        elif messageType == "mirror":
            execute('notify-send --urgency=normal "Mirroring displays" "No layout found"')
    return

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

def get_screens():
    resline = False # resline switches between true and false dependent on line type for command "xrandr"
    screens = {} # define as dictionary
    pattern_commected = " connected " # String to catch connected screens

    raw_monitors = execute("xrandr")[0]
    for line in raw_monitors.splitlines():

        # if last line included header for connected monitor, then list highest monitor resolution, and all hz options into array
        if resline == True:
            bool_resline = bool(re.search('^\s{3}', line))
            if bool_resline == True:
                pattern_resolution = re.compile(r'\d{3,5}x\d{3,5}')
                resolution_raw = pattern_resolution.findall(line)[0]
                resolution = resolution_raw.split('x')
                pattern_ghz = re.compile(r'\d{2,3}\.\d{2,3}')
                frequency = pattern_ghz.findall(line)
                float_frequency = [float(x) for x in frequency]
                sorted_frequency = sorted(float_frequency,reverse=True)
                
                #append max resolution list to dictionary
                screens[monitor_name]["monitor_option"][resolution_raw] = {}
                screens[monitor_name]["monitor_option"][resolution_raw]['resolution'] = []
                screens[monitor_name]["monitor_option"][resolution_raw]['frequency'] = []


                for direction in resolution:
                    screens[monitor_name]["monitor_option"][resolution_raw]['resolution'].append(int(direction))
                #append frequency list to dictionary            
                count = 0
                for option in frequency:
                    screens[monitor_name]["monitor_option"][resolution_raw]['frequency'].append(float(frequency[count]))
                    count += 1
            else:
                resline = False
        
        # if line includes a connected monitor, then index the monitor into dictionary
        if pattern_commected in line:
            monitor_name = line.split(' ', 1)[0]
            screens[monitor_name] = {}
            screens[monitor_name]['primary'] = bool
            screens[monitor_name]["monitor_option"] = {}
            bool_primary = bool(re.search(" primary ", line))
            if bool_primary == False:
                screens[monitor_name]['primary'] = False
            else:
                screens[monitor_name]['primary'] = True
                primary_screen = monitor_name
            resline = True
            
            if screens[monitor_name]['primary'] == True:
                pattern_resolution = re.compile(r'\d{3,5}x\d{3,5}')
                resolution_raw = pattern_resolution.findall(line)[0]
                screens[monitor_name]['active_resolution'] = resolution_raw

    return screens


def auto_mirror(screens):
    # Find Main display
    for display in screens:
        if screens[display]['primary'] == True:
            primary_display = display
            mirror_resolution = screens[primary_display]['active_resolution']
        else:
            pass

    # Generate xrandr command
    command_xrandrMirror = f"xrandr --output {primary_display} --mode {mirror_resolution} "
    for display in screens:
        if screens[display]['primary'] == False:
            for option in screens[display]['monitor_option']:
                if option == mirror_resolution:
                    print(f"Display: {display} CAN display at res:{mirror_resolution}")
                    command_xrandrMirror = command_xrandrMirror+str(f"--output {display} --same-as {primary_display} --mode {mirror_resolution} ")
                else:
                    pass
        else:
            pass

    #execute xrandr command
    execute(command_xrandrMirror)
    notify('mirror',"")
    return

def activate_layout(path_layout):
    full_fileName = path_layout.split("/")[-1]
    split_fileName = full_fileName.split(".")[0]
    path = path_layout.rsplit('/', 1)[0]+"/"
    print("Activating layout", split_fileName)
    execute(f"bash {path}{split_fileName}.sh")
    notify("layout",split_fileName)

def manual():
    current_monitors = list_monitors()
    check_layoutExsists = find_layout(current_monitors)
    if check_layoutExsists[0] == True:
        print("Layout already exsists:", check_layoutExsists[1])
        yes_no = input("\nEnter:\na) To activate layout\nm) To mirror all screens\nq) To quit\nChoise: ")
        if yes_no == "a":
            activate_layout(check_layoutExsists[1])
        elif yes_no == "m":
            screens = get_screens()
            auto_mirror(screens)            
        else:
            print("Exiting...")
            sys.exit()
    else:
        print("There is no layout present with your current monitors")
        yes_no = input("\nEnter:\nc) To create a new layout\nm) To mirror all screens\nq) To quit\nChoise:")
        print(current_monitors)
        if yes_no == "c":
            create_layout(current_monitors)
        elif yes_no == "m":
            screens = get_screens()
            auto_mirror(screens)
        else:
            print("Exiting...")
            sys.exit()


def automated():
    current_monitors = list_monitors()
    check_layoutExsists = find_layout(current_monitors)
    if check_layoutExsists[0] == True:
        activate_layout(check_layoutExsists[1])
    else:
        # Attempt to mirror the displays
        screens = get_screens()
        auto_mirror(screens)
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


main()