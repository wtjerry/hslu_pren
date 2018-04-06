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
cd path_to_repository/; /usr/bin/python3 -u ./App.py &
```

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


# Notes
As the Software is still under development and there are external hardware dependencies, some parts have dummy implementations.
You can configure whether to use the real or the dummy implementation in *Bindings.py*.
