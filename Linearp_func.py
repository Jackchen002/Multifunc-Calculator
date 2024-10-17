import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
from pylab import mpl

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]

#窗口置顶变量
is_topmost = False

def play_gui3():
    # 设置主窗口
    root = tk.Tk()
    root.title("一元线性回归")
    root.geometry("824x646")

    def toggle_topmost():  #实现窗口置顶
        global is_topmost
        is_topmost = not is_topmost
        root.attributes("-topmost", is_topmost)
        btn_topmost.config(text="√置顶" if is_topmost else "置顶")
    # 窗口置顶
    btn_topmost = tk.Button(root, text="置顶", width=8, height=2, font=('黑体', 12), command=toggle_topmost)
    btn_topmost.place(x=740, y=10)

    # 标记是否将第一行作为数据标签
    header_var = tk.IntVar()

    def upload_file():
        nonlocal file_name, canvas, r_squared
        # 选择文件
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=(("Excel files", "*.xls *.xlsx"), ("All files", "*.*"))
        )

        if file_path:
            try:
                # 根据Checkbutton的选中状态设置header值
                header = 0 if header_var.get() else None

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
        root.clipboard_append(f"{label_equation.cget('text')} R^2 = {r_squared:.4f}")
        # 更新剪贴板内容
        root.update()

    # 提示信息
    label_info = tk.Label(root,
                          text="请上传包含回归数据的Excel文件。\n要求：文件至少包含两列数据，第一列为自变量X，第二列为因变量Y。",
                          font=("Arial", 12), fg="blue")
    label_info.pack(pady=10)

    # 文件上传按钮
    btn_upload = tk.Button(root, text="上传Excel文件", font=("Arial", 14), command=upload_file)
    btn_upload.pack(pady=(0, 20))  # 靠近提示文字

    # 选择是否将第一行作为数据标签
    header_check = tk.Checkbutton(root, text="第一行为数据标签", font=("Arial", 12), variable=header_var)
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

    root.mainloop()


if __name__ == "__main__":
    play_gui3()
