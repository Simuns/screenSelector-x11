#!/usr/bin/env python3
from screenSelector import execute

def check_linuxFlvor():

def list_missingDependencies


def install_dependencies():
    dependencies = ['xrandr','arandr','hwinfo']
    for dependency in dependencies:
        current_dependency = execute(f"which {dependency}")[1]
        if current_dependency == 0:
            pass
        else:
            try:
                execute(f"pacman -Syu {dependency} --noconfirm")
            except:
                pass
    for dependency in dependencies:
        current_dependency = execute(f"which {dependency}")[1]
        if current_dependency == 0:
            pass
        else:
            print(f"There were issues installing dependencies. \nTry to manually install package {current_dependency} and run installer again.")
install_dependencies()

#def setup_service():

#def setup_executable():
