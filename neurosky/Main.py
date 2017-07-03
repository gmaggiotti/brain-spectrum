from neurosky.connector.NeuroskyConnector import NeuroskyConnector
from bluetooth.btcommon import BluetoothError
from parser import  ThinkGearParser, TimeSeriesRecorder
import wink, states
from Talk import Talk

conn = NeuroskyConnector()
socket = conn.getConnectionInstance()
recorder = TimeSeriesRecorder()
parser = ThinkGearParser(recorders= [recorder])



w = wink.Wink()
s = states.States()
t = Talk()

while socket is not None:
    try:
        data = socket.recv(1000)
        parser.feed(data)

        m = recorder.meditation[-100:].max()
        a = recorder.attention[-100:].max()
        #e = recorder.poor_signal.mean()
        max = recorder.raw[-100:].max()

        # if not(math.isnan(m) and math.isnan(a) and math.isnan(b)) :
        #     print( str(int(m))  + " - "+ str(int(a)) + " - "+ str(b) + " - " + str(max) )
        print( str(m)  + " - "+ str(a) + " - " + str(max) )

        # if( w.detectWink(max) ):
        #     s.addWink()
        # count = s.getWinkWithinDelta()
        # if( count == 1 ):
        #     t.sayYes()
        # elif( count == 2 ):
        #     t.sayNo()
        # elif( count == 3 ):
        #     t.sayHelp()


    except BluetoothError:
        pass


