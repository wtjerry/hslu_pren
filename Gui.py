from appJar import gui

pipe_path = "/home/jerry/coding/git/pren/hslu_pren/pos_queue"

def extract_x_and_z(s):
    index_x_start = s.find("'") + 1
    index_x_end = s.find("'", index_x_start)
    x = s[index_x_start:index_x_end]
    
    index_z_start = s.find("'", index_x_end+1) + 1
    index_z_end = s.find("'", index_z_start)
    z = s[index_z_start:index_z_end]

    return (x, z)


def update_label():
    while True:
        with open(pipe_path, "r") as f:
            l = f.readline().rstrip()
            if "new position" in l:
                x, z = extract_x_and_z(l)
                x = int(float(x))
                z = int(float(z))
                app.queueFunction(app.setLabel, "pos_x_value", x) 
                app.queueFunction(app.setLabel, "pos_z_value", z) 


app = gui()
app.setFont(18)

app.addLabel("pos_x_label", "x position:   ", 0, 0)
app.addLabel("pos_x_value", "", 0, 1)
app.addLabel("pos_z_label", "z position:   ", 1, 0)
app.addLabel("pos_z_value", "", 1, 1)

app.setLabel("pos_x_value", "650")
app.setLabel("pos_z_value", "0")

app.thread(update_label)

app.go()

