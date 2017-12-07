import subprocess

p = subprocess.Popen(['ps', '-aux'], stdout=subprocess.PIPE)
out, err = p.communicate()
for l in out.splitlines():
    if b"networking" in l:
        splitter = l.decode('utf8').split()
        print(splitter[-2], splitter[1])

        # kill $(ps -aux | grep -v grep | grep App.py | head -n 1 | awk '{print $2 $12}')
