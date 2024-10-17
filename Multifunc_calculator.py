import math
import tkinter as tk
from tkinter import messagebox

# 分文件功能导入
from Determinant_func import play_gui2
from Linearp_func import play_gui3
from Quadratic_func import play_gui1

# 按钮集
buttons1 = [
    ('sin', 'cos', 'tan', '^2', 'e^x', '←'),
    ('7', '8', '9', '/', 'ln', '('),
    ('4', '5', '6', '*', '1/x', ')'),
    ('1', '2', '3', '-', '!', 'e'),
    ('0', 'C', '=', '+', '√', 'π'),
]

is_topmost = False


def play_gui():
    # GUI设置
    root = tk.Tk()
    root.title("多功能计算器")
    root.geometry("412x323")

    def toggle_topmost():  #实现窗口置顶
        global is_topmost
        is_topmost = not is_topmost
        root.attributes("-topmost", is_topmost)
        btn_topmost.config(text="√置顶" if is_topmost else "置顶")

    # 输入框设置
    entry = tk.Entry(root, width=24, font=('Arial', 18), borderwidth=5, relief="solid", justify='right')
    entry.grid(row=0, column=0, columnspan=5, pady=5)

    #窗口置顶
    btn_topmost = tk.Button(root, text="置顶", width=6, height=2, font=('黑体', 12), command=toggle_topmost)
    btn_topmost.grid(row=0, column=5, padx=2, pady=5)

    #菜单栏
    menu = tk.Menu(root)
    funcmenu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="功能", menu=funcmenu)
    funcmenu.add_command(label="一元二次方程", command=play_gui1)
    funcmenu.add_command(label="行列式(2-4阶)", command=play_gui2)
    funcmenu.add_command(label="一元线性规划", command=play_gui3)

    # 创建计算器按钮
    for row_idx, row in enumerate(buttons1):
        for col_idx, key in enumerate(row):
            if key in ('sin', 'cos', 'tan', '^2', 'e^x', 'ln', '1/x', '!', '√'):
                button = tk.Button(root, text=key, width=6, height=2, font=('Arial', 12),
                                   command=lambda func=key: calculate_function(func, entry))
            elif key == '=':
                button = tk.Button(root, text=key, width=6, height=2, font=('Arial', 12),
                                   command=lambda: press("=", entry))
            elif key == 'C':
                button = tk.Button(root, text=key, width=6, height=2, font=('Arial', 12),
                                   command=lambda: press("C", entry))
            elif key == '←':
                button = tk.Button(root, text=key, width=6, height=2, font=('Arial', 12),
                                   command=lambda: press("←", entry))
            else:
                button = tk.Button(root, text=key, width=6, height=2, font=('Arial', 12),
                                   command=lambda key=key: press(key, entry))
            button.grid(row=row_idx + 1, column=col_idx, padx=2, pady=2)
    # GUI运行
    root.config(menu=menu)
    root.mainloop()


# 特殊符
def press(key, entry):
    if key == "=":
        try:
            result = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception as e:
            messagebox.showerror("xx错误xx", "对不起，做不到！")
            entry.delete(0, tk.END)
    elif key == "C":
        entry.delete(0, tk.END)
    elif key == "←":
        entry.delete(len(entry.get()) - 1, tk.END)
    elif key == "e":
        entry.insert(tk.END, math.e)
    elif key == "π":
        entry.insert(tk.END, math.pi)
    else:
        entry.insert(tk.END, key)


# 运算符
def calculate_function(func, entry):
    try:
        num = float(entry.get())
        if func == 'sin':
            result = math.sin(math.radians(num))
        elif func == 'cos':
            result = math.cos(math.radians(num))
        elif func == 'tan':
            result = math.tan(math.radians(num))
        elif func == '^2':
            result = num ** 2
        elif func == 'e^x':
            result = math.e ** num
        elif func == 'ln':
            result = math.log(num)
        elif func == '1/x':
            result = 1 / num
        elif func == '√':
            result = math.sqrt(num)
        elif func == '!':
            result = math.factorial(int(num))
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
    except Exception as e:
        messagebox.showerror("xx错误xx", "对不起，做不到！")


if __name__ == '__main__':
    play_gui()
