import time
import sys

# 定义两帧动画，模拟跳动感
frame1 = [
    "    \033[38;5;210m█████\033[0m    ",
    "\033[38;5;210m█ \033[30m█\033[38;5;210m█\033[30m█\033[38;5;210m █\033[0m",
    "    \033[38;5;210m█████\033[0m    ",
    "     \033[38;5;210m█ █\033[0m     "
]

frame2 = [
    "             ",  # 第一行留空，产生下落感
    "    \033[38;5;210m█████\033[0m    ",
    "\033[38;5;210m█ \033[30m█\033[38;5;210m█\033[30m█\033[38;5;210m █\033[0m",
    "    \033[38;5;210m█████\033[0m    ",
    "     \033[38;5;210m█ █\033[0m     "
]


def animate_robot():
    # 隐藏光标
    sys.stdout.write("\033[?25l")
    try:
        while True:
            for frame in [frame1, frame2]:
                # 清除之前的行并重置光标位置
                sys.stdout.write("\033[H")
                # 如果不想清屏，可以用 \033[F 回退行

                output = "\n".join(frame)
                sys.stdout.write(output + "\n")
                sys.stdout.flush()
                time.sleep(0.5)  # 控制跳动速度
    except KeyboardInterrupt:
        # 退出时恢复光标
        sys.stdout.write("\033[?25h")
        print("\n动画停止。")


if __name__ == "__main__":
    # 清屏
    sys.stdout.write("\033[2J")
    animate_robot()