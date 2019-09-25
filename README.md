 ## 一、首先看看破解的效果图
    ![效果1](https://github.com/chushiyan/slide_captcha_cracking/blob/master/results/001.gif "效果1")
    ![效果2](https://github.com/chushiyan/slide_captcha_cracking/blob/master/results/002.gif "效果2")
    ![效果3](https://github.com/chushiyan/slide_captcha_cracking/blob/master/results/003.gif "效果3")
    ![效果4](https://github.com/chushiyan/slide_captcha_cracking/blob/master/results/004.gif "效果4")

## 二、滑块验证码的破解

       滑块验证码的破解的难点主要有两个：计算出滑块到缺口的距离和模拟人拖动滑块的轨迹。

       如何计算出滑块到缺口的距离？从网上的资料来看，主要有两种方式：自己使用Pillow库实现算法，使用OpenCV库提供的现成方法。本文就使用后者，简单而又强大、成功率高。

      本文主要参考https://juejin.im/post/5cf4cbd4f265da1b8e7089b4，但是由于它的注释太少，也未给出完整代码。所以，决定写这篇博客。
## 三、什么是OpenCV？什么是OpenCV-python？

      OpenCV（Open Source Computer Vision Library）是一个开源的计算机视觉库，提供了很多处理图片、视频的方法。虽然是C/C++开发的，但是提供了 Python、Java、MATLAB 等其他语言的接口。

      OpenCV-python库就是使用pthon操作OpenCV的一个库。
## 四、为什么要用OpenCV-python库？

      说白了，就是OpenCV库提供了一个方法（matchTemplate()）：从一张较大的图片中搜索一张较小图片，计算出这张大图上各个区域和小图相似度。调用这个方法后返回一个二维数组（numpy库中ndarray对象），从中就能拿到最佳匹配区域的坐标。换到滑块验证码上面，滑块背景图片是大图，滑块是小图。

      opencv-python参见官网：https://docs.opencv.org/4.0.0/index.html

     cv.matchTemplate()方法参见：

     https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matchin/py_template_matching.html

    今日头条PC端登录页面： https://sso.toutiao.com/
## 五、环境

    首先，selenium、谷歌浏览器、谷歌浏览器驱动等环境是必须的。

    安装OpenCV-python库

    pip install  opencv-python

    或者使用阿里源：

    pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com opencv-python

