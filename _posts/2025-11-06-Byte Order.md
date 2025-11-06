---
title: Byte Order
lang: zh
tags: ["Python"]
key: BO
---

字节序太容易混乱了

<!--more-->

---

## 分析对象

### (A) 单个无符号整数（uint）

- 出现场景：硬件变量（寄存器、线、端口等）、程序变量、数学计算
- 特点：
  - 用连续的多比特表示
  - 内部比特顺序通常没有争议（MSB/LSB固定）
- 注意：
  - 当 uint 转换成 **多字节存储/传输** 时，才会涉及字节序问题
    - 存储在Memory、文本文件

### (B) Bytes / Hex

- 出现场景：文本格式、网络传输、内存表示

- 特点：

  - 是 **字节序列**，顺序显式

- 字节序问题：

  1. **uint ↔ bytes**

     - 一个多字节整数如何拆成 bytes？大端/小端会不同

     - 例：`0x1234` → `b'\x12\x34'`（大端）或 `b'\x34\x12'`（小端）

       ```python
       0x1234.to_bytes(2, byteorder='big')    # get b'\x12\x34'
       0x1234.to_bytes(2, byteorder='little') # get b'\x34\x12'
       int.from_bytes(b'\x12\x34', byteorder='big') # get 0x1234 (4660)
       int.from_bytes(b'\x12\x34', byteorder='little') # get 0x3412 (13330)
       ```

  2. **bytes ↔ 文本显示(hex)**

     - Bytes和Hex之间的转换通常没有异议，Hex显示在前面的，对应Bytes[0]

       ```python
       b'\x12\x34'.hex()     # get '1234'
       bytes.fromhex('1234') # get b'\x12\x34'
       ```

  3. **bytes ↔ 传输顺序**

     - Bytes到以字节为单位的传输顺序通常没有异议，例如python串口，读和写就是先发bytes[0]

       ```python
       import serial
       ser = serial.Serial('/dev/ttyUSB0', 115200)  # 端口和波特率
       ser.write(b'\x12\x34')                       # 先发送 0x12 再 0x34
       ```

  4. **bytes ↔ 内存存放顺序**

     - bytes到内存映射的顺序通常没有异议，bytes[0]存放在addr，bytes[1]存放在addr+1

## 如何理解

- 对于一个变量，按他原本的面貌理解他，他就是一个uint或者list
- 当需要**文件中存储、传输、内存中存储**时，需要把原本的变量转换为bytes
  - 在python软件中，要**注意区分当前的这个bytes是干啥用的：**
    - 测试向量存储所用bytes；串口传输所用bytes；内存存储所用bytes；
    - 不同用途的bytes和原始变量对应的关系可能不同（有的大端有的小端）
    - 直接把一个用途的bytes，挪作他用是危险的（不同用途的字节序可能不同）
