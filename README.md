
# Installation Guide (Tested on arch)
#### Intended (but not tested) to work on following distros
|distro families|-|-|-|
|----|------|------|------|
|rhel|fedora|centos||
|debian|ubuntu|linuxmint|raspbian|
|arch(tested )||||

* Clone repo: `git clone https://github.com/Simuns/screenSelector-x11.git`
* `cd screenSelector-x11/`
* Install screenSelector: `sudo ./.configure`
* List manual command options with by simply running `screenSelector`
* If you wish screenSelector to run as an automated service, run following commands:
    - Start service: `sudo systemctl start screenSelector`
    - Verify status: `sudo systemctl status screenSelector`
    - Then enable: `sudo systemctl enable screenSelector`
### Usage
#### Commandline Options:
|Option|Long Command|Short Command|
|------|------------|-------------|
|Create layout|--create|-c|
|Manually change layout|--manual|-m|
|Automated run (No Confirmation needed)|--automated|-a|
##### Arandr
* Creating a news layout will automatically prompt Arandr.
1. Configure your Display settings.
2. Save layout:Layout -> Save as
3. Exit arandr

## todo

- [x] Make sure systemvars work in service
- [x] Separate script into smaller chunks
- [x] create arandr execution wait loop verifying based on filecreation timestamp
- [x] Create guide to layout creation section
- [x] Atomated run. Create function that will turn on all connected screens when no preset is picket. Screens will be mirrored from main display
- [ ] dunst notification integration
- [x] Write .configure script, that installs screenSelector (figure out if sh or py (python has jinjar2 templating support))
- [ ] Cleanup debug lines not needed
- [ ] Create propper log management
- [x] fix switchcases based on userinput (automated, manual, create ect..)
- [ ] Author a complete README including. sections(installation, requirements, how it works)
- [ ] test app on multiple distros
- [ ] make uninstallable
