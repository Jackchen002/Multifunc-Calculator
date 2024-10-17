import tkinter as tk
import math

is_topmost = False

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
        global is_topmost
        is_topmost = not is_topmost
        root.attributes("-topmost", is_topmost)
        btn_topmost.config(text="√置顶" if is_topmost else "置顶")

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


if __name__ == '__main__':
    play_gui1()