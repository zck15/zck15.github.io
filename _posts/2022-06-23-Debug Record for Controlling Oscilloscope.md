---
title: Debug Record for Controlling Oscilloscope
lang: zh
tags: ["Python", "Debug"]
key: Debug_Control_Osc
---

 本文记录了尝试修复与示波器通信脚本中Bug的调试过程与解决方法。

<!--more-->

---

在本实验中，我们用到了电脑、一台示波器、一块FPGA开发板，我们在电脑上通过python脚本控制开发板和示波器，用示波器采集开发板的波形，并在电脑上用python脚本读回示波器的波形。电脑与示波器通信使用的USB，通过NI-VISA通信。

在回传示波器波形的过程中，我们遇到了如下问题：经过若干次回传波形，某一次通信就会突然失败，然后就无法和示波器通信了。但是如果重启python内核（一开始我们用的jupytor notebook）或重新运行python脚本，通信就会恢复正常。

我们首先尝试在实验脚本内通过重启visa的相关对象来解决；然后通过启用日志，尝试定位错误出现的位置与原因；最后定位到错误原因在c底层或物理传输或设备问题，无法直接解决；最终通过修改python库，通过出错后重启visa的resource manager，使实验能够连续运行。

## 实验环境

- 电脑操作系统：Win 10
- Python 3.7
- 示波器：TELEDYNE LECROY WAVERUNNER 8404M
- 通信方式：USBTMC
- python通信库：[pyvisa](https://github.com/pyvisa/pyvisa)，[lecroydso](https://github.com/TeledyneLeCroy/lecroydso).

## 调试方法

### 阶段1: 尝试重启python中的通信对象

由于我们观察到，每次出现通信问题，重启jupyter的python内核后，就能恢复通信，因此通信本身并没有瘫痪，而应该是python或visa出现问题。因此，我们尝试在通信出错时，重启通信对象。然而，当时不了解通信中具体调用的层次结构，并没有能够全部重启，所以尝试失败了。

### 阶段2: 通过Logging尝试定位问题

我们随后尝试定位错误出现的位置并修复错误，因此打开了库的[logging](https://zck15.github.io/2022/06/21/Logging-in-Python.html)功能，将运行日志存储在文件中进行分析。

首先在分析日志时，我们发现出错时最后一次通信与开始时正好相距10秒，因此认为可能是数据太多，通信时间需要超过设置的timeout。通过[lecroydso](https://github.com/TeledyneLeCroy/lecroydso)的源码，发现LeCroyVISA类的实例`l`可以通过`l.timeout = 20.0`直接设置。然后发现，其实只有最后一次通信用了全部的timeout，平时通信一次只需几毫秒。

然后通过分析崩溃时读取到的数据，我们发现每次崩溃时，最后读到的字符都是`\n`，因此认为可能是读到`\n`导致出现的问题。通过阅读[pyvisa](https://github.com/pyvisa/pyvisa)的python源码以及[ni-visa文档](https://www.ni.com/docs/zh-CN/bundle/ni-visa/page/ni-visa/viread.html)，我们发现viRead默认每次读到`\n`就返回，因此不论出不出问题，每次读取的最后字符都是`\n`。顺带着我们发现了，可以在数据传输前设置visa的停止符无效，数据传输后再恢复，使我们数据传输的速度提升了越30%。

最后我们发现，产生报错的是ni-visa的c代码，原因可能是通信或设备原因，这些我们是无法简单的修复的。

### 阶段3: 尝试如何彻底重启

由于错误本身无法解决，我们重新尝试如何成功的重启，从而让实验能连续进行。由于前面通过logging debug的过程，我们对库的调用关系与结构更加熟悉了，通过log我们发现，每次出错后重启，visa的resource manager并没有被关闭和重启，而是在上层的类重启是被复用了。通过python源码，发现LeCroyVISA在调用resource manager后，没有保存，因此后面重启时也没有处理rm。由于该库的维护不算太及时（Issue回复很慢），所以只好fork一份自己修改。

### 阶段4: 可以连续运行后的意外之喜

通过失败后彻底重启，我们可以连续运行实验了。随后我们发现出错的频率有点太高了，结合之前分析认为，出错可能是在物理上传输真的有错，结合用的传输线是消费级的随便买的线，我猜测也许这根线传输会丢数据。更换为实验室之前采购的带有放大器的线后，原本每十几次实验就出错，变成了几百次实验还未出错。所以做实验还是不要随便用消费级的商品了。

## 解决方法

### 修改timeout的方法

```python
scope = LeCroyVISA(ip, maxLen)
scope.timeout = 10.0
```

### 加快传输速度的方法

读取较多字节数据时，pyvisa会不断调用viRead，直到读取够目标数量。viRead默认读取到`\n`就会返回，因为指令传输大多以`\n`结尾。然而数据传输时，常常也会碰到编码恰好是`\n`的数据，所以viRead会频繁返回。我们可以在传输数据前，取消此功能，并在传输后恢复，从而加快传输速度。

```python
scope = LeCroyVISA(ip, maxLen)
scope._visa.read_termination = None
scope._visa.read_bytes(len_data)
scope._visa.read_termination = "\n"
```

此外，如果未读到`\n`，viRead最多读取chunk_size字节数据就会返回，这个chunk_size可以通过以下方式设置。但是实验后发现，默认的20*1024就大概是传输最快的了（修改后时间大致不变或变慢）

```python
scope = LeCroyVISA(ip, maxLen)

scope._visa.read_bytes(len_data, chunk_size=20*1024)
```

### 解决出错后无法继续实验的方法

LeCroyVISA在使用后没有保存pyvisa的ResourceManager，因此也无法重启ResourceManager。我们fork了一份代码，具体修改可参见[此库](https://github.com/zck15/lecroydso)的`CHANGELOG.md`。

### 减少出错频率

不要用淘宝京东上随便购买的数据线做实验，可靠性不够好。
