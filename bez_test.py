from celluloid import Camera  # 保存动图时用，pip install celluloid
import numpy as np
import matplotlib.pyplot as plt

P0 = np.array([0, 0])
P1 = np.array([15, 0])
P2 = np.array([15, 10])
P3 = np.array([30, 10])
fig = plt.figure(3)
camera = Camera(fig)

x_2 = []
y_2 = []
for t in np.arange(0, 1, 0.1):
    plt.cla()
    plt.plot([P0[0], P1[0]], [P0[1], P1[1]], 'k')
    plt.plot([P1[0], P2[0]], [P1[1], P2[1]], 'k')
    plt.plot([P2[0], P3[0]], [P2[1], P3[1]], 'k')
    p11_t = (1-t)*P0+t*P1
    p12_t = (1-t)*P1+t*P2
    p13_t = (1-t)*P2+t*P3
    p21_t = (1-t)*p11_t+t*p12_t
    p22_t = (1-t)*p12_t+t*p13_t
    p3_t = (1-t)*p21_t+t*p22_t

    x_2.append(p3_t[0])
    y_2.append(p3_t[1])
    plt.scatter(x_2, y_2, c='r')

    plt.plot([p11_t[0], p12_t[0]], [p11_t[1], p12_t[1]], 'b')
    plt.plot([p12_t[0], p13_t[0]], [p12_t[1], p13_t[1]], 'b')

    plt.plot([p21_t[0], p22_t[0]], [p21_t[1], p22_t[1]], 'r')
    plt.title("t="+str(t))
    plt.pause(0.1)
#     camera.snap()
# animation = camera.animate()
# animation.save('3阶贝塞尔.gif')
print()
