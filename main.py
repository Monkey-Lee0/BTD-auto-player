import _thread,pickle,pynput,time,ctypes,pygame
PROCESS_PER_MONITOR_DPI_AWARE = 2
ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

def print_hi(name):
    print(f'Hi, {name}')

if __name__ == '__main__':
    print_hi('PyCharm')

pygame.init()
pygame.mixer.init()

res=[]
target="*"
press=False

def on_move(x, y):
    res.append(["move",time.time(),x,y])
def on_click(x, y, button, pressed):
    res.append(["click",time.time(),pressed,int(x),int(y),button])
def on_scroll(x, y, dx, dy):
    res.append(["scroll",time.time(),x,y,dx,dy])
def on_press(key):
    if key != pynput.keyboard.Key.f7 and key != pynput.keyboard.Key.f8 and key != pynput.keyboard.Key.f4:
        res.append(["press",time.time(),key])
def on_release(key):
    if key != pynput.keyboard.Key.f7 and key != pynput.keyboard.Key.f8 and key != pynput.keyboard.Key.f8:
        res.append(["release",time.time(),key])
def on_press_special(key):
    global press
    if(key == pynput.keyboard.Key.f7):
        press = True
mouse_listener, keyboard_listener = None, None

def start():
    pygame.mixer.music.load('./alpha.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    print("listening")
    global mouse_listener,keyboard_listener,res
    res.clear()
    mouse_listener=pynput.mouse.Listener(on_move=on_move,on_click=on_click,on_scroll=on_scroll)
    mouse_listener.start()
    keyboard_listener=pynput.keyboard.Listener(on_press=on_press,on_release=on_release)
    keyboard_listener.start()

def stop():
    global res,target
    pygame.mixer.music.stop()
    global mouse_listener,keyboard_listener
    mouse_listener.stop()
    keyboard_listener.stop()
    mouse_listener,keyboard_listener=None,None
    print("res:",res)
    if target!="*":
        with open("data/"+str(target)+'.pickle','wb') as file:
            # noinspection PyTypeChecker
            pickle.dump(res,file)

def execute():
    global res,target,press
    special_listener=pynput.keyboard.Listener(on_press=on_press_special)
    special_listener.start()
    if target!="*":
        with open("data/"+str(target)+'.pickle','rb') as file:
            # noinspection PyTypeChecker
            res=pickle.load(file)
    pygame.mixer.music.load('./Firebugs.mp3')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(-1)
    print("executing")
    if len(res):
        mouse_ctr=pynput.mouse.Controller()
        keyboard_ctr=pynput.keyboard.Controller()
        delta_time=time.time()-float(res[0][1])
        for command in res:
            time.sleep(max(0.0,float(command[1])-time.time()+delta_time))
            if command[0]=="move":
                mouse_ctr.position=[command[2],command[3]]
            elif command[0] == "click":
                mouse_ctr.position=[command[3],command[4]]
                if command[2]:
                    mouse_ctr.press(pynput.mouse.Button.left)
                else:
                    mouse_ctr.release(pynput.mouse.Button.left)
            elif command[0] == "scroll":
                mouse_ctr.position=[command[2],command[3]]
                mouse_ctr.scroll(command[4],command[5])
            elif command[0] == 'press':
                keyboard_ctr.press(command[2])
            elif command[0] == 'release':
                keyboard_ctr.release(command[2])
            if press:
                break
    pygame.mixer.music.stop()
    special_listener.stop()
    target="*"
    press=False

def set_target():
    global target
    target=input("enter your filename:")

def control(key):
    global mouse_listener,keyboard_listener
    if key == pynput.keyboard.Key.f8:
        if mouse_listener is not None:
            stop()
        else:
            start()
    elif key==pynput.keyboard.Key.f7:
        if mouse_listener is None:
            execute()
    elif key==pynput.keyboard.Key.f4:
        if mouse_listener is None:
            set_target()

with pynput.keyboard.Listener(on_press=control) as control_listener:
    control_listener.join()