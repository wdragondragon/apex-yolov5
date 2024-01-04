# apex gun

基于yolov5的apex英雄目标检测自动瞄准器

## 功能清单

- [x] ai自瞄，敌我识别
- [x] 识别枪械，自动开枪
- [x] 鼠标平滑移动
- [x] 可自定义鼠标单次移动像素，增加识别图像移动倍率
- [x] debug窗口，显示框人物位置
- [x] 基于socket双机：服务端运算，客户端移动鼠标
- [x] 多服务端支持，可同时运行多个服务端供单个客户端进行加速运算
- [x] [基于机器码的使用权限校验](https://github.com/wdragondragon/apex_vaildate.git)
- [x] [自动下载/更新](https://github.com/wdragondragon/ag_auto_update.git)
- [x] 识别到目标时，1秒频率的自动标注，供反喂数据优化学习
- [x] 支持保存配置，多配置切换
- [x] 识别帧数波动变换的可视化折线图
- [x] 漏枪
- [x] 适配kmbox A,罗技驱动,无涯键鼠盒子
- [X] 动态识别区域：解决了固定参数无法贴脸与抽远枪的问题，现支持根据敌人大小动态改变识别范围
- [X] 锁定敌人标记

## 使用说明

为提高作弊门槛，旨在技术分享，本项目不提供任何运行说明。

除权重文件外，其他项目文件完整，有能力可自行研究。

或参考文章[(yolov5从零开始，自动瞄准不再是天方夜谭)](https://www.jianshu.com/p/84ad94250172)

## 其他项目

[罗技抖枪宏大全](https://github.com/wdragondragon/apex-shake-gun.git)

[基于opencv的apex枪械识别宏框架](https://github.com/wdragondragon/ApexAutomaticGunSelection.git)


## 加入我们

欢迎加入我们，共同完善已有代码，优化模型或提供建议。我们将资源完全共享。

![wechat.png](wechat.png)
