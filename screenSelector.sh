#!/bin/bash
cat /dev/null > ~/.screenlayout/.screenSetup_checksum.md5
for i in $(find /sys/devices -name "edid"); do
        cat $i >> ~/.screenlayout/.screenSetup_checksum.md5
done
before_md5=$(md5sum ~/.screenlayout/.screenSetup_checksum.md5 | cut -d " " -f 1)
after_md5=$before_md5
while true
do
echo "" > ~/.screenlayout/.screenSetup_checksum.md5


        for i in $(find /sys/devices -name "edid"); do
                md5sum $i | cut -d " " -f 1 >> ~/.screenlayout/.screenSetup_checksum.md5
        done

        if [ "$before_md5" = "$after_md5" ]
        then
                echo "Match, do nothing"
                before_md5=$(md5sum ~/.screenlayout/.screenSetup_checksum.md5 | cut -d " " -f 1)
        else
                echo "no match, start application"
                after_md5=$before_md5
                export DISPLAY=:0
                python3 ~/git/screenSelector-x11/screenSelector.py > ~/git/screenSelector-x11/screenSelector.log
        fi
        sleep 8


done
~              
