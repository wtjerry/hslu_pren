[![Build Status](https://travis-ci.org/wtjerry/hslu_pren.svg?branch=master)](https://travis-ci.org/wtjerry/hslu_pren)

# how to start the App
## startup
Either use the provided but experimental systemd service in ExampleScripts/
or start via:
``` sh
cd /path_to_repository/prenNetworkConnection; /usr/bin/python3 -u ./App.py &
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

### Windows:
``` sh 
nc your_current_wlan_ip 12345
```
and then
``` sh
start
```