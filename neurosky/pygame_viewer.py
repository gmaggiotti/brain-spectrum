import pygame, sys
from numpy import *
from pygame import *
import scipy
from neurosky.connector.NeuroskyConnector import NeuroskyConnector
from bluetooth.btcommon import BluetoothError
from parser import  ThinkGearParser, TimeSeriesRecorder
from pyeeg import bin_power
import math

description = """Pygame Example
"""


conn = NeuroskyConnector()
socket = conn.getConnectionInstance()
recorder = TimeSeriesRecorder()
parser = ThinkGearParser(recorders= [recorder])

screen_with = 1280
screen_height = 720

def normalize( value, weight ):
    return weight*value/screen_height

def buildSignals():
    return {'raw': 0, 'med': 0, 'attention' : 0, 'delta' : 0, 'theta' : 0, 'alpha' : 0, 'beta' : 0, 'gamma' : 0}

def main():
    pygame.init()

    fpsClock= pygame.time.Clock()

    screen = pygame.display.set_mode((screen_with,screen_height))
    pygame.display.set_caption("Mindwave Viewer")


    blackColor = pygame.Color(0,0,0)
    redColor = pygame.Color(255,0,0)
    greenColor = pygame.Color(0,255,0)
    deltaColor = pygame.Color(0,0,128)
    thetaColor = pygame.Color(238,130,238)
    alphaColor = greenColor
    betaColor = pygame.Color(255,255,0)
    gammaColor = redColor


    background_img = pygame.image.load("pygame_background.png")


    font = pygame.font.Font("freesansbold.ttf", 20)
    raw_eeg = True
    spectra = []



    record_baseline = False
    quit = False
    i = 0

    signal = buildSignals()

    rawy= medy = 0
    prevsigy = sigy = 0
    while quit is False and socket is not None:
        try:
            data = socket.recv(1000)
            parser.feed(data)

            signal['raw'] = recorder.raw[-10:].mean()
            signal['med'] = recorder.attention[-10:].max()

            #FIXme: iterate hashmap to set 0 when is nan
            if math.isnan(signal['raw']) :
                signal['raw'] = 0
            if math.isnan(signal['med']) :
                signal['med'] = 0
            if i == screen_with :
                i = 0
                screen.fill((0,0,0))

            prev_raw = rawy
            prev_med = medy
            rawy = normalize(signal['raw'], 200)
            pygame.draw.line(screen, redColor, [i, screen_height-10 -prev_raw], [i+2,screen_height-10 -rawy], 3)

            medy = normalize(signal['med'], 500)
            pygame.draw.line(screen, greenColor, [i, screen_height-100-prev_med], [i+2,screen_height-100 -medy], 3)



            flen = 50
            if len(recorder.raw)>=500:
                spectrum, relative_spectrum = bin_power(recorder.raw[-512*3:], range(flen),512)
                spectra.append(array(relative_spectrum))
                if len(spectra)>30:
                    spectra.pop(0)

                factor = 200
                spectrum = mean(array(spectra),axis=0)
                for x in range (flen-1):
                    value = float(spectrum[x]*1000)
                    if x<3:
                        color = deltaColor  #blue
                        line = 200
                        sig_name = "delta"
                    elif x<8:
                        color = thetaColor  #violet
                        line = 300
                        sig_name = "theta"
                    elif x<13:
                        color = alphaColor  #green
                        line = 400
                        factor = 400
                        sig_name = "alpha"
                    elif x<30:
                        color = betaColor  #yellow
                        line = 500
                        factor = 1000
                        sig_name = "beta"
                    else:
                        color = gammaColor  #red
                        line = 600
                        factor =1000
                        sig_name = "gamma"

                    prevsigy = sigy
                    sigy = normalize(value, factor)
                    pygame.draw.line(screen, color, [i, screen_height-line-prevsigy], [i+10,screen_height-line -sigy], 3)


            #print med
            i+= 10
            pygame.display.flip()



        except BluetoothError:
            pass


        for event in pygame.event.get():
                if event.type==QUIT:
                    quit = True
                if event.type==KEYDOWN:
                    if event.key==K_ESCAPE:
                        quit = True
        pygame.display.update()
        fpsClock.tick(12)

if __name__ == '__main__':
    try:
        main()
    finally:
        pygame.quit()
