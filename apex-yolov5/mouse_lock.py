
import pynput,win32con
#import pydirectinput
import win32api
from .mouse import mouse_xy
from math import atan

lock_tag = '0'
def mouse_To1(des_X,des_Y,current_mouse_x=0,current_mouse_y=0):
    up = des_X - current_mouse_x
    down = des_Y - current_mouse_y
    up = int(up)
    down = int(down)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, up, down)
def mouse_To(des_X,des_Y,current_mouse_x=0,current_mouse_y=0):
    #效果不好
    up = des_X - current_mouse_x
    down = des_Y - current_mouse_y
    if up ==0 and down ==0:
        return
    up = int(up)
    down = int(down)
    movingUp = up // 2
    movingDown = down // 2
    abs_up = up if up > 0 else -up
    abs_down = down if down > 0 else -down
    Max = max(abs_down,abs_up)
    ite = Max
    for i in range(ite):
        if (2**i)>Max:
            break
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, movingUp, movingDown)
        movingUp = movingUp //2
        movingDown = movingDown //2

    #mouse_xy(int(up),int(down))
    # des_Y = int(des_Y)
    # des_X = int(des_X)
    #pydirectinput.moveTo(int(des_X),int(des_Y))

def lock(aims,mouse,screen_width,screen_height,shot_width,shot_height):
    # shot_width 截图高度，shot_height 截图区域高度
    # x,y 是分辨率
    #mouse_x,mouse_y = mouse.position

    current_mouse_x = screen_width/2    #当前鼠标坐标，为屏幕中心
    current_mouse_y = screen_height/2   #同上
    current_mouse_x,current_mouse_y = mouse.position
    dist_list = []
    aims_copy = aims.copy()
    #print(aims_copy)
    aims_copy = [x for x in aims_copy if x[0] == lock_tag]
    if(len(aims_copy) ==0):
        return
    for det in aims_copy:
        _, x_c, y_c, _, _ = det
        dist = (shot_width * float(x_c) - current_mouse_x) ** 2 + (shot_height * float(y_c) - current_mouse_y) ** 2
        dist_list.append(dist)
    det = aims_copy[dist_list.index(min(dist_list))]
    #print('当前鼠标坐标',mouse.position)
    tag,target_x,target_y,target_width,target_height=det
    #将坐标及高度转变,转变为屏幕的坐标
    targetRealHeight = shot_height * float(target_height)
    targetShotX = shot_width * float(target_x)  #目标在截图范围内的坐标
    targetShotY = shot_height * float(target_y)
    screenCenterX = screen_width//2
    screenCenterY = screen_height//2
    left_top_x , left_top_y = screenCenterX - shot_width//2, screenCenterY - shot_height//2  #截图框的左上角坐标
    targetRealX = left_top_x + targetShotX  #目标在屏幕的坐标
    targetRealY = left_top_y + targetShotY

    #print("tag:%s,target_x:%s,target_y:%s,height:%s,width:%s"%(tag,target_x,target_y,target_width,target_height))
    #print("current mouse pos:",current_mouse_x," and ",current_mouse_y)
    #dist = (x*float(x_c)-mouse_x)**2 + (y*float(y_c) - mouse_y)**2
    dist = (targetRealX - current_mouse_x)**2 + (targetRealY - current_mouse_y)**2
    #print("dist:",dist)
    if(dist < 20000):
        #print("locking")
        #targetRealY += targetRealHeight/8   #将y轴移下面一点，可以防止枪械挡到模型
        #mouse.move(0,100)
        mouse_To1(des_X=targetRealX,des_Y=targetRealY,current_mouse_x=current_mouse_x,current_mouse_y=current_mouse_y)
        #mouse_To2(des_X=targetRealX,des_Y=targetRealY,current_mouse_x=current_mouse_x,current_mouse_y=current_mouse_y,height=targetRealHeight,x_center=targetRealX,y_center=targetRealY)
        #mouse_xy(round(int(x_cc)-mouse_x),round(int(y_cc)-mouse_y)//10)
        #mouse_xy(round(pid_movex),round(pid_movey))
        #win32api.mouse_event(win32con.MOUSEEVENTF_MOVE,round(targetRealX-current_mouse_x),round(targetRealY-current_mouse_y))
        #win32api.SetCursorPos((int(targetRealX),int(targetRealY)))
        #pydirectinput.moveTo(int(x_cc),int(y_cc),duration=100,tween=10,relative=False)
        #mouse.position = x_cc,y_cc
        # hwnd = 527818
        # hwnd = win32gui.FindWindow(None, "Apex Legends")
        # temp = win32api.MAKELONG(int(targetRealX)-1000, int(targetRealY))
        # win32api.SendMessage(hwnd, win32con.WM_MOUSEMOVE, 0, temp)