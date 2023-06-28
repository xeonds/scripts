# 导入所需的库
import win32api
import win32con
import ctypes
import time
import threading

# 定义一个处理输入的函数
def handle_input():
    global recording # 声明recording为全局变量
    while recording: # 当录制状态为真时，循环执行
        if input("Press 'q' to quit recording: ") == 'q': # 如果输入为'q'，就设置录制状态为假
            recording = False

# 定义一个获取鼠标位置的函数
def get_pos():
    # 返回鼠标的横坐标和纵坐标
    return win32api.GetCursorPos()

# 定义一个模拟鼠标点击的函数
def click(x, y):
    # 移动鼠标到指定位置
    ctypes.windll.user32.SetCursorPos(x, y)
    # 按下左键
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    # 释放左键
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

# 定义一个存储鼠标事件的字符串
clicks = ""

while True:
    option = input("Menu: (l)oad, (r)ecord, (p[n])lay n times, (s)ave, (q)uit: ")
    
    if option == 'l':
        print("Loading...")
        f = open("clicks.txt", "r")
        clicks = f.read()
        f.close()
        print("Loaded")
    elif option == 'r':
        clicks = ""
        recording = True # 设置录制状态为真
        input_thread = threading.Thread(target=handle_input) # 创建一个线程来处理输入
        last_state = win32api.GetKeyState(win32con.VK_LBUTTON) # 记录上一次的鼠标状态
        input_thread.start() # 启动线程
        print("Recording...Press 'q' to quit recording")
        start_time = time.time() # 记录开始时间
        while recording:
            x, y = get_pos() # 获取鼠标位置
            state = win32api.GetKeyState(win32con.VK_LBUTTON) # 获取鼠标左键状态
            if state == -127 or state == -128: # 如果鼠标左键被按下
                state = 1
            else:
                state = 0
            elapsed_time = time.time() - start_time # 计算已经过去的时间
            if state != last_state: # 如果状态发生变化，就记录下这次的动作
                clicks += f"{x}, {y}, {state}, {elapsed_time}\n" # 把鼠标位置、状态和时间添加到字符串中
                print(f"Click event recorded: ({x}, {y}), state:{state}, elapsed_time:{elapsed_time}")
                last_state = state # 更新上一次的鼠标状态
        print("Recorded")
    elif option[0] == 'p':
        print("Playing...")
        if option[1:] == '':
            n = 1
        else:
            n = int(option[1:])
        for i in range(n):
            for c in clicks.split("\n"):
                time.sleep(1)
                if c == '':
                    continue
                x, y, state, elapsed_time = c.split(", ") # 解析字符串中的鼠标位置、状态和时间
                print(f"Playing: ({x}, {y}), state:{state}, elapsed_time:{elapsed_time}")
                x = int(x) # 转换为整数类型
                y = int(y) # 转换为整数类型
                state = int(state) # 转换为整数类型
                elapsed_time = float(elapsed_time) # 转换为浮点数类型
                if state == 0: # 如果是移动事件，就移动鼠标到指定位置
                    ctypes.windll.user32.SetCursorPos(x, y)
                elif state == 1: # 如果是左键按下事件，就按下左键
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                elif state == 2: # 如果是左键释放事件，就释放左键
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                elif state == 3: # 如果是右键按下事件，就按下右键
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                elif state == 4: # 如果是右键释放事件，就释放右键
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
    elif option == 's':
        print("Saving...")
        f = open("clicks.txt", "w")
        f.write(clicks)
        f.close()
        print("Saved")
    elif option == 'q':
        print("Quitting...")
        break
    else:
        print("Invalid input")
        continue


