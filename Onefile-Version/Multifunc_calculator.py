import math
import tkinter as tk
from email.quoprimime import header_check
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from pylab import mpl

from tkinter.constants import SUNKEN

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

#Quadratic_func 一元二次方程求解

is_topmost1 = False

def play_gui1():
    # 创建一元二次方程求解窗口
    root = tk.Tk()
    root.title("一元二次方程求解")
    root.geometry("400x300")

    # 输入提示标签
    tk.Label(root, text="请输入一元二次方程的系数:", font=('Arial', 14)).place(x=50, y=20)
    tk.Label(root, text="ax² + bx + c = 0", font=('Arial', 14)).place(x=140, y=50)

    # 系数输入框
    tk.Label(root, text="a:", font=('Arial', 12)).place(x=50, y=90)
    entry_a = tk.Entry(root, width=10, font=('Arial', 12))
    entry_a.place(x=100, y=90)



    tk.Label(root, text="b:", font=('Arial', 12)).place(x=50, y=130)
    entry_b = tk.Entry(root, width=10, font=('Arial', 12))
    entry_b.place(x=100, y=130)

    tk.Label(root, text="c:", font=('Arial', 12)).place(x=50, y=170)
    entry_c = tk.Entry(root, width=10, font=('Arial', 12))
    entry_c.place(x=100, y=170)

    # 结果显示标签
    result_label = tk.Label(root, text="", font=('Arial', 14), fg="blue")
    result_label.place(x=80, y=220)

    def toggle_topmost():  #实现窗口置顶
        global is_topmost1
        is_topmost1 = not is_topmost1
        root.attributes("-topmost", is_topmost1)
        btn_topmost.config(text="√置顶" if is_topmost1 else "置顶")

    # 计算函数
    def calculate_quadratic():
        try:
            # 获取输入的系数并转换为浮点数
            a = float(entry_a.get())
            b = float(entry_b.get())
            c = float(entry_c.get())

            # 判断a是否为0
            if a == 0:
                result_label.config(text="系数a不能为0。")
                return

            # 计算判别式
            discriminant = b ** 2 - 4 * a * c

            # 根据判别式判断解的情况
            if discriminant > 0:
                root1 = (-b + math.sqrt(discriminant)) / (2 * a)
                root2 = (-b - math.sqrt(discriminant)) / (2 * a)
                result_text = f"两个不同的解:\n x₁ = {root1:.2f}, x₂ = {root2:.2f}"
            elif discriminant == 0:
                root = -b / (2 * a)
                result_text = f"有两个相同的解:\n x = {root:.2f}"
            else:
                result_text = "无实数解。"

            result_label.config(text=result_text)
        except ValueError:
            result_label.config(text="请输入有效的数字。")

    # 计算按钮
    calculate_button = tk.Button(root, text="计算", command=calculate_quadratic, font=('Arial', 12), width=10)
    calculate_button.place(x=220, y=120)

    # 窗口置顶
    btn_topmost = tk.Button(root, text="置顶", width=6, height=2, font=('黑体', 12), command=toggle_topmost)
    btn_topmost.place(x=320, y=15)

    root.mainloop()

#Linearp_func 一元线性回归

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]

#窗口置顶变量
is_topmost2 = False

def play_gui3():
    # 设置主窗口
    root = tk.Tk()
    root.title("一元线性回归")
    root.geometry("824x646")

    def toggle_topmost():  #实现窗口置顶
        global is_topmost2
        is_topmost2 = not is_topmost2
        root.attributes("-topmost", is_topmost2)
        btn_topmost.config(text="√置顶" if is_topmost2 else "置顶")
    # 窗口置顶
    btn_topmost = tk.Button(root, text="置顶", width=8, height=2, font=('黑体', 12), command=toggle_topmost)
    btn_topmost.place(x=740, y=10)

    def upload_file():
        nonlocal file_name, canvas, r_squared, header
        # 选择文件
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=(("Excel files", "*.xls *.xlsx"), ("All files", "*.*"))
        )

        if file_path:
            try:
                # 获取文件名用于标题
                file_name = os.path.basename(file_path).split('.')[0]

                # 读取数据
                data = pd.read_excel(file_path, header=header)
                if data.shape[1] < 2:
                    messagebox.showerror("错误", "文件格式不正确，请确保有至少两列数据（x和y）。")
                    return

                # 取前两列为 x 和 y，并对x进行排序
                data = data.sort_values(by=data.columns[0])
                x = data.iloc[:, 0].values
                y = data.iloc[:, 1].values

                # 计算线性回归斜率和截距
                slope, intercept = np.polyfit(x, y, 1)
                equation = f"y = {slope:.2f}x + {intercept:.2f}"
                # 计算 R^2 值
                y_pred = slope * x + intercept
                ss_res = np.sum((y - y_pred) ** 2)
                ss_tot = np.sum((y - np.mean(y)) ** 2)
                r_squared = 1 - (ss_res / ss_tot)
                r_squared = '%.4f'% r_squared

                #展示解析式与R^2值
                label_equation.config(text="解析式: " + equation + "  R^2: " + str(r_squared))


                # 如果已存在canvas，先销毁它
                if canvas:
                    canvas.get_tk_widget().destroy()

                # 绘制数据点和回归线
                fig, ax = plt.subplots()
                ax.scatter(x, y, color="blue", label="数据点")
                ax.plot(x, slope * x + intercept, color="red", label="回归直线")
                ax.set_xlabel("X")
                ax.set_ylabel("Y")
                ax.set_title(f"一元线性回归 - 数据来源: {file_name}")
                ax.legend()

                # 在Tkinter窗口中嵌入图像
                canvas = FigureCanvasTkAgg(fig, master=root)
                canvas.draw()
                canvas.get_tk_widget().place(x=50, y=260, width=700, height=350)  # 调整位置和大小

                # 启用保存图像按钮和复制按钮
                btn_save_image.config(state="normal")
                copy_button.config(state="normal")

            except Exception as e:
                messagebox.showerror("错误", f"文件读取或处理失败: {e}")

    def save_image():
        # 保存当前图像
        save_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All Files", "*.*")],
            initialfile=f"{file_name}_回归图.png"
        )
        if save_path:
            plt.savefig(save_path)
            messagebox.showinfo("保存成功", f"图像已保存到 {save_path}")

    #复制功能
    def copy_result():
        # 清空剪贴板
        root.clipboard_clear()
        # 将结果添加到剪贴板
        root.clipboard_append(f"{label_equation.cget('text')}")
        # 更新剪贴板内容
        root.update()

    #设置header值
    def set_header():
        nonlocal header
        if header == 0:
            header = None
        else:
            header = 0


    # 提示信息
    label_info = tk.Label(root,
                          text="请上传包含回归数据的Excel文件。\n要求：文件至少包含两列数据，第一列为自变量X，第二列为因变量Y。",
                          font=("Arial", 12), fg="blue")
    label_info.pack(pady=10)

    # 文件上传按钮
    btn_upload = tk.Button(root, text="上传Excel文件", font=("Arial", 14), command=upload_file)
    btn_upload.pack(pady=(0, 20))  # 靠近提示文字

    # 选择是否将第一行作为数据标签
    # header_check = tk.Checkbutton(root, text="第一行是数据标签", font=("Arial", 12), variable=header_var, onvalue=0, offvalue=1)
    header_check = tk.Checkbutton(root,text="第一行是数据标签", font=("Arial", 12), command=set_header)
    header_check.place(x=500, y=78)

    # 回归方程显示标签
    label_equation = tk.Label(root, text="解析式与R^2值: ", font=("Arial", 12))
    label_equation.pack(pady=10)

    # 保存图像按钮 (初始禁用)
    btn_save_image = tk.Button(root, text="保存图像", font=("Arial", 12), command=save_image)
    btn_save_image.place(x=300, y=222)
    btn_save_image.config(state="disabled")

    #一键复制按钮 (初始禁用)
    copy_button = tk.Button(root, text="复制解析式与R^2值", font=("Arial", 12), command=copy_result)
    copy_button.place(x=420, y=222)
    copy_button.config(state="disabled")

    file_name = ""  # 用于保存文件名
    canvas = None  # 用于存储图像的canvas
    r_squared = None # R^2值
    header = None # 第一行是否为数据标签

    root.mainloop()

#Determinant_func 行列式计算

is_topmost3 = False

def play_gui2():
    root = tk.Tk()
    root.title("行列式(2-4阶)求解")
    root.geometry("400x400")

    # 创建输入框框架
    input_frame = tk.Frame(root, highlightbackground="black", highlightthickness=0.5)
    input_frame.place(x=50, y=100)
    input_frame.configure(relief=SUNKEN)#, bg="white")

    #更新输入框
    def press(value, var, input_frame, result_label):
        var.set(value)
        solve_determinant(var, input_frame, result_label)

    def toggle_topmost():  #实现窗口置顶
        global is_topmost3
        is_topmost3 = not is_topmost3
        root.attributes("-topmost", is_topmost3)
        btn_topmost.config(text="√置顶" if is_topmost3 else "置顶")

    #行列式计算函数
    def calculate_determinant(entries, size):
        try:
            matrix = []
            for i in range(size):
                row = []
                for j in range(size):
                    value = float(entries[i][j].get())  # 获取输入框中的值并转换为浮点数
                    row.append(value)
                matrix.append(row)
            matrix = np.array(matrix)
            determinant = np.linalg.det(matrix)  # 使用NumPy计算行列式
            return determinant
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字")
            return None

    def update_input_grid(frame, size):

        # 清除旧的输入框
        for widget in frame.winfo_children():
            widget.destroy()

        #根据阶数创建新的输入框
        entries = []
        for i in range(size):
            row_entries = []
            for j in range(size):
                entry = tk.Entry(frame, width=5, font=('Arial', 14), justify='center')
                entry.grid(row=i, column=j, padx=5, pady=5)
                row_entries.append(entry)
            entries.append(row_entries)

        return entries

    def solve_determinant(var, input_frame, result_label):
        size = int(var.get())
        entries = update_input_grid(input_frame, size)

        def calculate_and_display():
            det = calculate_determinant(entries, size)
            if det is not None:
                result_label.config(text=f"行列式结果：{det:.2f}")

        # 清除旧的计算按钮
        for widget in input_frame.grid_slaves(row=size, column=0):
            widget.destroy()

        # 添加新计算按钮
        calculate_btn = tk.Button(input_frame, text="计算行列式", command=calculate_and_display, font=('Arial', 14))
        calculate_btn.grid(row=size, column=0, columnspan=size, pady=10)

    # 创建选择框架
    var = tk.StringVar()
    tk.Radiobutton(root, text="2阶", variable=var, value="2", font=('Arial', 16),
                   command=lambda: press(2, var, input_frame, result_label)).place(x=50, y=5)
    tk.Radiobutton(root, text="3阶", variable=var, value="3", font=('Arial', 16),
                   command=lambda: press(3, var, input_frame, result_label)).place(x=150, y=5)
    tk.Radiobutton(root, text="4阶", variable=var, value="4", font=('Arial', 16),
                   command=lambda: press(4, var, input_frame, result_label)).place(x=250, y=5)

    # 窗口置顶
    btn_topmost = tk.Button(root, text="置顶", width=6, height=2, font=('黑体', 12), command=toggle_topmost)
    btn_topmost.place(x=320, y=5)

    # 初始化结果标签
    result_label = tk.Label(root, text="", font=('Arial', 14))
    result_label.place(x=50, y=350)

    #默认显示2阶输入框
    press(2, var, input_frame, result_label)

    root.mainloop()

if __name__ == '__main__':
    play_gui()
