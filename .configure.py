#!/usr/bin/env python3

import subprocess # Used for unix commmands
from subprocess import PIPE, STDOUT # 

import sys
import platform
import os
from os import path # Check if file exsists
import shutil # Copy files

def execute(cmd):
    exec = subprocess.Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True)
    output = exec.communicate()[0]
    exitcode = exec.returncode
    if exitcode > 2:
        print("Offending line:",cmd)
    return output.decode("utf-8").strip(), exitcode

def get_privelege():
    if os.geteuid() == 0:
        pass
    else:
        print("Installation requires sudo\nExiting")
        sys.exit()
    return 


def check_linuxFlavor():
    info = platform.freedesktop_os_release()
    distro = [info["ID"]]
    if "ID_LIKE" in info:
        # distro are space separated and ordered by precedence
        distro.extend(info["ID_LIKE"].split())
    return distro[0]


def list_missingDependencies():
    dependencies = ['xrandr','arandr','hwinfo']
    missing_Dependencies = []
    for dependency in dependencies:
        current_dependency = execute(f"which {dependency}")[1]
        if current_dependency == 0:
            pass
        else:
            if len(missing_Dependencies) == 0:
                print("Following Dependencies are missing:")
            missing_Dependencies.append(dependency)
            print(dependency)
    return (missing_Dependencies)

def install_dependencies(distro, missing_Dependencies):
    print("Checking for missing Dependencies")
    if distro == "arch":
        pkg_manager = "pacman -Syu --noconfirm"
    elif distro == "ubuntu" or raspbian or linuxmint:
        pkg_manager = "apt-get install -y"
    elif distro == "centos" or "fedora" or "rhel" or "oracle":
        pkg_manager = "yum install -y"
    else:
        print(f"Your distro {distro} is not supported. Please manually install the missing dependencies")
        sys.exit()

    for dependency in missing_Dependencies:
        installation = execute(f"{pkg_manager} {dependency}")
        if installation[1] == 0:
            pass
        else:
            print(f"installing package {dependency} failed.\nTry manually installing it and run me again.")
            sys.exit()


def install_bin(install_dest, exe_path):
    print("Creating installation directory...")
    execute(f"mkdir -p {install_dest}/screenSelector-x11")
    print("Installing...")
    shutil.copy2("./screenSelector.py", f"{install_dest}/screenSelector-x11/")
    try:
        os.symlink(f"{install_dest}/screenSelector-x11/screenSelector.py", f"{exe_path}/screenSelector")
    except:
        pass

def main():
    get_privelege()
    missing_Dependencies = list_missingDependencies()
    distro = check_linuxFlavor()
    install_dependencies(distro, missing_Dependencies)

    install_dest = ("/usr/share/pyshared")
    exe_path = ("/usr/local/bin")
    install_bin(install_dest, exe_path)
    print("Installation complete")

    return

main()
