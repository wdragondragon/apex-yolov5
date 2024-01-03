# import time
#
# import numpy as np
# from sklearn.linear_model import LinearRegression
#
# # 假设你有过去的坐标数据
# past_coordinates = np.array(
#     [[0, 0, 0], [1, 1, 1], [2, 3, 2], [3, 5, 3], [4, 6, 5], [5, 7, 7], [6, 8, 9], [7, 10, 11], [8, 12, 12], [9, 13, 15],
#      [10, 16, 16], [11, 17, 17], [12, 18, 18]])  # 时间, x, y
# # # 提取时间和坐标
# time_values = past_coordinates[:, 0].reshape(-1, 1)
# x_values = past_coordinates[:, 1]
# y_values = past_coordinates[:, 2]
# start = time.time() * 1000
# # 创建线性回归模型
# model_x = LinearRegression(n_jobs=-1)
# model_y = LinearRegression(n_jobs=-1)
# model_x.fit(time_values, x_values)
# model_y.fit(time_values, y_values)
#
# # 预测未来的时间点
# future_time = 13
# future_x = model_x.predict([[future_time]])[0]
# future_y = model_y.predict([[future_time]])[0]
# print(time.time() * 1000)
# print(f"cost {int(time.time() * 1000 - start)}ms,Predicted Coordinates at time {future_time}: ({future_x}, {future_y})")
