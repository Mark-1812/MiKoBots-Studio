from backend.xbox.xbox import XBox

xbox = XBox()

def xbox_on():
    xbox.XBoxOn()


def close_xbox():
    xbox.xbox_on = False