import ctypes
import random
import threading
import time
from threading import Lock, Timer


SendInput = ctypes.windll.user32.SendInput

global flag3
flag3 = True
lock = Lock()

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def anxia():
    global flag3
    while flag3:
        print('按下\'e\'键')
        PressKey(0x12)
    print('松开')
    flag3 = not (flag3)
    ReleaseKey(0x12)


def songkai():
    lock.acquire()
    global flag3
    while flag3:
        flag3 = not (flag3)
    lock.release()


# 传入的是长按时间
def changan(ltime):
    t1 = Timer(1, anxia)
    t2 = Timer(1, songkai)
    t1.start()
    time.sleep(int(ltime))
    t2.start()


def guaji(ltime):
    time.sleep(5)
    i = 0
    while True:
        # 从在车上的状态开始第一步,传入的是长按时间
        changanjianpan = threading.Thread(target=changan, args=(ltime))
        changanjianpan.start()
        changanjianpan.join()
        # 第二步,下车,随便使用一个技能,然后上车
        time.sleep(2)
        PressKey(0x21)
        time.sleep(0.1)
        ReleaseKey(0x21)
        print('下车')
        # 使用技能
        time.sleep(5)
        PressKey(0x2)
        time.sleep(0.1)
        ReleaseKey(0x2)
        print('使用技能')
        # 上车
        time.sleep(5)
        PressKey(0x21)
        time.sleep(0.1)
        ReleaseKey(0x21)
        print('上车')
        # 第三步,休息随机的时间10-30秒左右
        suiji = random.randint(10, 30)
        time.sleep(suiji)
        i = i + 20 + suiji
        if i > 3600:
            print("已挂机一个小时,换个地方继续")
            break


def main():
    ajtime = input("持续时间:").strip()
    guaji(ajtime)


if __name__ == "__main__":
    main()