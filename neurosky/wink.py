from Talk import Talk

class Wink:

    talk = Talk()

    def __init__(self):
        self.blink_start = 0
        self.t1 = 0
        self.t2 =0

    def detectWink(self, max):
        if( max > 400 and self.blink_start == 0):
            self.blink_start = 1
        if( max < 400 and self.blink_start != 0 ):
            self.blink_start=0;
            return 1
