import time


class Pid():
    def __init__(self, kp, ki, kd):
        self.KP = kp
        self.KI = ki
        self.KD = kd
        self.now_val = 0
        self.sum_err = 0
        self.now_err = 0
        self.last_err = 0

    def cmd_pid(self, exp_val):
        self.last_err = self.now_err
        self.now_err = exp_val - self.now_val
        self.sum_err += self.now_err

        # 使用 PID 控制算法
        control_output = self.KP * (exp_val - self.now_val) + self.KI * self.sum_err + self.KD * (
                self.now_err - self.last_err)

        # 更新当前值
        self.now_val += control_output

        return self.now_val


if __name__ == '__main__':
    # 假设你有人物运动轨迹数据
    trajectory_data = [(1, 2), (2, 4), (3, 6), (4, 8), (5, 10)]  # 格式为 (x, y)

    # 初始化 x 和 y 方向上的 PID 控制器
    pid_controller_x = Pid(kp=0.2, ki=0.03, kd=0.15)
    pid_controller_y = Pid(kp=0.1, ki=0.01, kd=0.1)
    for i in range(1, 1000):
        start = time.time()
        x = i
        y = 2 * i
        predicted_x = pid_controller_x.cmd_pid(x)
        predicted_y = pid_controller_y.cmd_pid(y)
        print(
            f"The {i}th prediction, cost {int((time.time() - start) * 1000)} ms,Actual Trajectory: ({x + 1}, {2 * (x + 1)}), Predicted Trajectory: ({predicted_x}, {predicted_y})")
