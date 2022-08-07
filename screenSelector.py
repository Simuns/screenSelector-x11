#!/usr/bin/env python3
import subprocess # Used for unix commmands
from subprocess import PIPE, STDOUT # Used for unix commmands
import os
from pathlib import Path
import os
import json
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
    return monitors


def find_layout(current_monitors):
    # assign directory
    directory = os.path.expanduser('~/.screenlayout/')
    # iterate over files in
    # that directory
    files = Path(directory).glob('*.json')
    if len(list(files)) == 0:
        print("no prefixes")
    else:
        for file in files:
            print(file)
            with open(file, 'r') as f:
                json_object = json.load(f)
            if json_object != current_monitors:
                print("Layout does not exist")
            else:
                print("layout exsists")
    return


def create_layout(current_monitors):
    layout_name = input("Enter current layout name:")
    with open(directory+layout_name+".json", "w") as outfile:
        outfile.write(json.dumps(current_monitors, indent=4))


def main():
    current_monitors = list_monitors()
    find_layout(current_monitors)
    
main()