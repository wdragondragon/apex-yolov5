class Pid():
    """这里定义了一个关于PID的类"""

    def __init__(self, exp_val, kp, ki, kd):
        self.KP = kp
        self.KI = ki
        self.KD = kd
        self.exp_val = exp_val
        self.now_val = 0
        self.sum_err = 0
        self.now_err = 0
        self.last_err = 0

    def cmd_pid(self):
        self.last_err = self.now_err
        self.now_err = self.exp_val - self.now_val
        self.sum_err += self.now_err
        # 这一块是严格按照公式来写的
        self.now_val = self.KP * (self.exp_val - self.now_val) \
                       + self.KI * self.sum_err + self.KD * (self.now_err - self.last_err)
        return self.now_val


if __name__ == '__main__':
    pid_val = []
    # 对pid进行初始化，目标值是1000 ，p=0.1 ，i=0.15, d=0.1
    my_Pid = Pid(1000, 0.1, 0.01, 0.1)
    # 然后循环100次把数存进数组中去
    for i in range(0, 100):
        pid_val.append(my_Pid.cmd_pid())
    print(pid_val)
