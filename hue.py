import threading
import time
import argparse
from rgbxy import Converter
from rgbxy import GamutC
from phue import Bridge

def main():
    parser = argparse.ArgumentParser(description='Change my Hue Lights')
    parser.add_argument('ip', type=str, help='local IP for for Hue Bridge')
    parser.add_argument('group', type=str, help='name of Hue group')
    args = parser.parse_args()

    bridge = Bridge(args.ip)
    bridge.connect()
    print('Connected to bridge')
    lightId = getLight(bridge, args.group)
    print(f'lightId = {lightId}')

    lightLoop(bridge, lightId)

def getLight(bridge, groupName):
    groupIds = bridge.get_group()
    patioGroup = None
    for gid in groupIds:
        group = bridge.get_group(int(gid))
        if group['name'] == 'Patio':
            patioGroup = group
            break
    lightId = int(patioGroup['lights'][0])
    return lightId


def lightLoop(bridge, lightId):
    red = (255,0,0)
    white = (1,1,1) # rgbxy has a division by zero bug with (0,0,0)
    green = (0,255,0)
    transitionTime = 2
    holdTime = 5
    holdTime2 = 3
    while True:
        changeColor(bridge, lightId, red, seconds=transitionTime)
        time.sleep(transitionTime + holdTime)
        changeColor(bridge, lightId, white, seconds=transitionTime)
        time.sleep(transitionTime + holdTime2)
        changeColor(bridge, lightId, green, seconds=transitionTime)
        time.sleep(transitionTime + holdTime)
        changeColor(bridge, lightId, white, seconds=transitionTime)
        time.sleep(transitionTime + holdTime2)


def changeColor(bridge, lightId, rgb, seconds=0):
    converter = Converter(GamutC)
    xy = converter.rgb_to_xy(*rgb)
    # transition time is specified in multpiles of 100 ms
    transition = seconds * 10
    command = {
        'on': True,
        'bri': 254,
        'xy': xy,
        'transitiontime': transition
    }
    bridge.set_light(lightId, command)


if __name__ == "__main__":
    main()
    