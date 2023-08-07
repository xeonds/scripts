import tkinter as tk
import mysql.connector as mc

root = tk.Tk()
root.title("MySQL管理工具")
root.geometry("600x400+300+100")

def connect_mysql():
    host = entry_host.get()
    user = entry_user.get()
    password = entry_password.get()
    database = entry_database.get()
    try:
        global conn 
        conn = mc.connect(host=host.split(":")[0] if ":" in host else host, user=user, password=password, database=database, port=host.split(":")[1] if ":" in host else 3306)
        text_log.insert(tk.END, "连接成功！\n")
        dialog.destroy()
    except Exception as e:
        text_log.insert(tk.END, "连接失败！\n")
        text_log.insert(tk.END, str(e) + "\n")

def open_dialog():
    global dialog 
    dialog = tk.Toplevel()
    dialog.title("连接MySQL")
    dialog.geometry("300x200+400+200")
    label_host = tk.Label(dialog, text="主机名（:端口）：")
    label_host.grid(row=0, column=0, padx=10, pady=10)
    label_user = tk.Label(dialog, text="用户名：")
    label_user.grid(row=1, column=0, padx=10, pady=10)
    label_password = tk.Label(dialog, text="密码：")
    label_password.grid(row=2, column=0, padx=10, pady=10)
    label_database = tk.Label(dialog, text="数据库名：")
    label_database.grid(row=3, column=0, padx=10, pady=10)
    global entry_host 
    entry_host = tk.Entry(dialog)
    entry_host.grid(row=0, column=1, padx=10, pady=10)
    global entry_user 
    entry_user = tk.Entry(dialog)
    entry_user.grid(row=1, column=1, padx=10, pady=10)
    global entry_password 
    entry_password = tk.Entry(dialog, show="*")
    entry_password.grid(row=2, column=1, padx=10, pady=10)
    global entry_database 
    entry_database = tk.Entry(dialog)
    entry_database.grid(row=3, column=1, padx=10, pady=10)
    button_connect = tk.Button(dialog, text="连接", command=connect_mysql)
    button_connect.grid(row=4, columnspan=2)
    
def execute_command():
    command = entry_command.get()
    try:
        cursor = conn.cursor() 
        cursor.execute(command) 
        results = cursor.fetchall() 
        cursor.close() 
        if results:
            for row in results:
                text_log.insert(tk.END, ",".join(map(str, row)) + "\n")
        else:
            text_log.insert(tk.END, "没有查询到数据！\n")
    except Exception as e:
        text_log.insert(tk.END, "执行失败！\n")
        text_log.insert(tk.END, str(e) + "\n")

menubar = tk.Menu(root)
menu_file = tk.Menu(menubar, tearoff=0)
menu_file.add_command(label="连接", command=open_dialog)
menu_file.add_command(label="退出", command=root.quit)
menubar.add_cascade(label="文件", menu=menu_file)
root.config(menu=menubar)
text_log = tk.Text(root)
text_log.place(x=10, y=10, width=580, height=300)
label_command = tk.Label(root, text="请输入指令：")
label_command.place(x=10, y=320, width=80, height=30)
entry_command = tk.Entry(root)
entry_command.place(x=100, y=320, width=400, height=30)
button_execute = tk.Button(root, text="执行", command=execute_command)
button_execute.place(x=510, y=320, width=80, height=30)
root.mainloop()
