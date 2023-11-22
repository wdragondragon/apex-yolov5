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

## 使用说明
本项目的权重文件并未开源，可以参考文章[(yolov5从零开始，自动瞄准不再是天方夜谭)](https://www.jianshu.com/p/84ad94250172)去训练自己的模型。

## 其他项目

[罗技抖枪宏大全](https://github.com/wdragondragon/apex-shake-gun.git)

[基于opencv的apex枪械识别宏框架](https://github.com/wdragondragon/ApexAutomaticGunSelection.git)
