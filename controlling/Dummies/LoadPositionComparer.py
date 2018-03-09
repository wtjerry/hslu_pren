import time
class LoadPositionComparer:
    def __init__(self, dummy_x):
        self._check_for_load= True
        self._dummy_x_position = dummy_x

        #Load position in mm
        self._load_position = 650

    def check_until_reached(self):
        while(self._check_for_load):
            position = self._dummy_x_position.get_position()
            if(position >= self._load_position):
                print("Load Reached!")
                self._check_for_load = False
            else:
                print("goal not yet reached, position: ", position)

            time.sleep(0.5)
