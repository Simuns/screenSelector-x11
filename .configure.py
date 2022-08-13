#!/usr/bin/env python3

import subprocess # Used for unix commmands
from subprocess import PIPE, STDOUT # 

import sys
import platform
import os
from os import path # Check if file exsists
import shutil # Copy files

import getpass # Used to retrieve username
import pwd # Used to retrieve username


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
    try:
        info = platform.freedesktop_os_release()
        myDistro = [info["ID"]]
        if "ID_LIKE" in info:
            # distro are space separated and ordered by precedence
            myDistro.extend(info["ID_LIKE"].split())
    except:
        try:
            import distro
            myDistro = distro.linux_distribution(full_distribution_name=False)
        except:
            print("could not determine distribution")
            sys.exit()
    return myDistro[0]


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
    elif distro == "ubuntu" or "raspbian" or "linuxmint":
        pkg_manager = "apt-get install -y"
    elif distro == "centos" or "fedora" or "rhel" or "oracle":
        pkg_manager = "yum install -y"
    else:
        print(f"Your distro {distro} is not supported. Please manually install the missing dependencies")
        sys.exit()
# special package names
    if distro == "raspbian":
        for i in range(len(missing_Dependencies)):
        
            # replace hardik with shardul
            if missing_Dependencies[i] == 'arandr':
                missing_Dependencies[i] = 'x11-xserver-utils'
            if missing_Dependencies[i] == 'xrandr':
                missing_Dependencies[i] = 'x11-xserver-utils'
        else:
            pass


    for dependency in missing_Dependencies:
        print(f"Installing {dependency}")
        installation = execute(f"{pkg_manager} {dependency}")
        if installation[1] == 0:
            pass
        else:
            print(f"installing package {dependency} failed.\nTry manually installing it and run me again.")
            sys.exit()


def get_user():
    """Try to find the user who called sudo/pkexec."""
    try:
        return os.getlogin()
    except OSError:
        # failed in some ubuntu installations and in systemd services
        pass

    try:
        user = os.environ['USER']
    except KeyError:
        # possibly a systemd service. no sudo was used
        return getpass.getuser()

    if user == 'root':
        try:
            return os.environ['SUDO_USER']
        except KeyError:
            # no sudo was used
            pass

        try:
            pkexec_uid = int(os.environ['PKEXEC_UID'])
            return pwd.getpwuid(pkexec_uid).pw_name
        except KeyError:
            # no pkexec was used
            pass

    return user

def prepare_service():
    print("Preparing service file")
    user = get_user()

    fin = open("screenSelector.service.template", "rt")
    #output file to write the result to
    fout = open("screenSelector.service", "wt")
    #for each line in the input file
    for line in fin:
    	#read replace the string and write to output file
    	fout.write(line.replace('USER', user))
    #close input and output files
    fin.close()
    fout.close()
    return

def install_bin(install_dest, exe_path):
    print(f"creating installation directory: {install_dest}/screenSelector-x11")
    execute(f"mkdir -p {install_dest}/screenSelector-x11")
    print("Setup...")
    shutil.copy2("./screenSelector.py", f"{install_dest}/screenSelector-x11/")
    shutil.copy2("./screenSelector.sh", f"{install_dest}/screenSelector-x11/")
    shutil.copy2("./screenSelector.service", "/etc/systemd/system/")
    try:
        os.symlink(f"{install_dest}/screenSelector-x11/screenSelector.py", f"{exe_path}/screenSelector")
    except:
        pass
    execute("systemctl daemon-reload")

def main():
    get_privelege()
    missing_Dependencies = list_missingDependencies()
    distro = check_linuxFlavor()
    install_dependencies(distro, missing_Dependencies)
    prepare_service()
    install_dest = ("/usr/share/pyshared")
    exe_path = ("/usr/local/bin")
    install_bin(install_dest, exe_path)
    print("Installation complete")

    return

main()

