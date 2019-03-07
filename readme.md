# 一笔画完辅助

## 写在前头

近年来微信小游戏的流行，出现了很多有趣的小游戏，比如跳一跳，再比如现在的这个**一笔画完**。一笔画完，是一个挺有意思的游戏，但是有的时候，我们会卡在一些关卡，久久不能过关。又或者想要解放大脑，解放双手，让它自己玩。于是，闲暇之时，参照着之前看到的微信[跳一跳辅助](!https://github.com/wangshub/wechat_jump_game)的思路，模仿写了一个辅助。

![xkg5j-cbee1](xkg5j-cbee1.gif)



## 原理说明

1. 将手机点击到《一笔画完》的某一关界面

2. 用adb工具获取当前手机截图，并用adb将截图pull上来

   ```
   adb shell screencap -p /sdcard/shot.png
   adb pull /sdcard/shot.png .
   ```

3. 计算路径，截取必要部分，然后根据颜色来识别方格，然后使用深度搜索树去找到一个解

4. 自动一笔画完

   - 模拟点击：一个一个格子的点击，速度不快

     ```
     adb shell input tap x y
     ```

   - 发送事件(待完成)：往对应设备中直接写滑动数据，丝般顺滑

     ```
     adb shell cat operating_data > /dev/input/event1
     ```


## 使用教程

```
python autowalk.py [options]
options:
	-s --stage 当前游戏关卡数
	-c --count 自动通关次数，默认1
	-s --sum   总关卡数
	-h --human 手动通关模式（默认是自动通关）
	-l --list  通关方案输出模式，1数字版(默认)，2文字版，3箭头版
	
```

