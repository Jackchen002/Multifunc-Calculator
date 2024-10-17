import tkinter as tk
from tkinter import messagebox
from tkinter.constants import SUNKEN

import numpy as np

is_topmost = False


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
        global is_topmost
        is_topmost = not is_topmost
        root.attributes("-topmost", is_topmost)
        btn_topmost.config(text="√置顶" if is_topmost else "置顶")

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
    play_gui2()
