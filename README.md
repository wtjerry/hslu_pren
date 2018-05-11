[![Build Status](https://travis-ci.org/wtjerry/hslu_pren.svg?branch=master)](https://travis-ci.org/wtjerry/hslu_pren)

# how to deploy to the raspberry PI
just copy all files within the repository to the pi (you may want to exclude .git/ and tests/ for performance reasons)
``` sh
rsync -rav -e ssh --exclude='.git/' --exclude='tests/'  . pi@PI_IP:/home/pi/pren/
```

# how to start the App
## startup
Either use the provided but experimental systemd service in ExampleScripts/
or start via:
``` sh
cd path_to_repository/; /usr/bin/python3 -u ./App.py | tee last_run.log &
```

It will create a logfile "last_run.log"

## start signal
Once started the App goes into waiting mode and you need to send it a start signal:

### Windows:
``` sh 
nc 127.0.0.1 12345
```
and then
``` sh
start
```

### Linux:
``` sh 
nc your_current_wlan_ip 12345
```
and then
``` sh
start
```


## install opencv
1. sudo pip3 install opencv-python
2. sudo apt install libhdf5-dev
3. sudo apt install libhdf5-serial-dev
4. sudo apt install libatlas-base-dev
5. sudo apt install libjasper-dev
6. sudo apt install libjpeg8-dev
7. sudo apt install libgtk2.0-dev
8. sudo apt install libqtgui4
9. sudo apt install libqt4-test


## Gui
It reads from a named pipe. It's path is specified in Gui.py
Make sure the pipe exists. Create it via:
``` sh
mkfifo pos_queue
```
To test it locally just write to the pipe, eg:
``` sh
echo "new position x: '135.21' z: '98.2323'" > pos_queue
```
To actually use it just pipe the output of nc to the pipe:
``` sh
nc IP 12345 > pos_queue
```


# Notes
As the Software is still under development and there are external hardware dependencies, some parts have dummy implementations.
You can configure whether to use the real or the dummy implementation in *Bindings.py*.
