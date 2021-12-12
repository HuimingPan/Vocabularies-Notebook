
# 1. Introduction
最近在准备二刷CET-6，贫瘠的单词积累和差劲的英语听力让我没啥信心。在知乎上看到一个介绍提高英语听力的帖子[1]，便照此方法训练。但听力材料里面的生词又是我不可避免的困难。我从网易有道整理单词效率很低，受知乎贴[2]的启发，就写了一个用LaTeX和Python结合的笔记本脚本。

# 2. Script
我写的程序主要有三个`.py`文件：

 - `get_word.py` ——获取单词并储存；
 - `write_latex.py`——形成LaTeX文本；
 - `main.py` ——主程序，在这里输入要查阅的单词.

## 2.1 get_word.py 
我这个单词本的数据都是从网易有道网页版里的柯林斯(Collins)词典里爬取的。

这个`.py`文件里的函数的基本内容是借鉴[3]，我的程序里有关爬虫的基本介绍可以去帖子[3]看看。除了几个函数，我还创建了`word_class`、`explanation_class`、`example_class`三个类，分别是表示单词、解释和例句的类。三种类的属性的命名很直接。在这里只需解释一下`explanation_class`的`kind`属性。

在Collins词典里，有几种类别解释：分别是单词的一种含义、同根词以及联想词等。因为开始想用`kind`属性来表示这种区别，但后来发现没必要，但还是没有删除。

## 2.2 write_latex.py
基本的LaTeX语法请读者自行去查阅有关资料，推荐《一份部太短的LaTeX》。

我将每一个单词的有关信息形成一个字符串，在替换点模板里的字符串`"contents"`，将替换后的模板字符串写入我们的文件。

需要特别说明的是，为了能够在`.tex`文本里表示单词音标，引用了`tipa`库，参见[4].

## 2.3 main.py
在这个脚本里输入我们要查的单词，我们输入的需要是一个列表，列表的每一个元素都是一个单词字符串。我们也可以用一个字符串用split函数形成我们需要的列表。

# 3. Results
如图，左边是形成的LaTeX文本，右边是编译后的pdf文件
![左边是形成的LaTeX文本，右边是编译后的pf文件](https://img-blog.csdnimg.cn/20210602214816742.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3dlaXhpbl80NjE5MTAzMw==,size_16,color_FFFFFF,t_70)
# 4.Reference
[1] 六级听力如何上二百？ https://www.zhihu.com/question/361688103/answer/1872761175

[2] 如何利用Python + Latex完成每日实验记录？https://zhuanlan.zhihu.com/p/364018866

[3] 利用PYTHON 爬虫爬出自己的英语单词库.https://www.jianshu.com/p/8a93198316ed

[4] 使用LaTeX编辑英文国际音标.https://zhuanlan.zhihu.com/p/199284523