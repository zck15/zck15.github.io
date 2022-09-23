---
title: Cyclist Mode in Xoodyak
lang: zh
tags: ["Xoodyak", "LWC", "Notes"]
key: Cyclist_Mode_in_Xoodyak
---

 本文介绍了轻量级密码算法Xoodyak中的Cyclist模式的运行方式，以及Xoodyak在AEAD和Hash模式下的工作方式

<!--more-->

---

[Xoodyak](https://keccak.team/xoodyak.html)是[NIST](https://www.nist.gov/)举办的[LWC标准化](https://csrc.nist.gov/Projects/lightweight-cryptography/)进程中的[最终候选者](https://csrc.nist.gov/Projects/lightweight-cryptography/finalists)之一，可以用来哈希、加密、计算MAC、认证加密AE、AEAD。它的构造是与SHA-3中使用的[海绵结构 (Sponge Construction)](https://keccak.team/sponge_duplex.html) 类似的姊妹结构——[双工结构 (Duplex construction)](https://keccak.team/sponge_duplex.html)。

## 海绵结构与双工结构

- 海绵结构：

![海绵结构](https://keccak.team/images/Sponge-150.png)

- 双工结构：

![双工结构](https://keccak.team/images/Duplex-150.png)

海绵结构和双工结构的示意图如上所示，他们均有一个宽度 (Width)为$b$比特的状态空间 (State)，其中$r$比特可以与外界交互，称为比特率 (Bitrate)，剩下的$c$比特是对外界隐藏的，称为容量 (Capacity)；此外，它们都使用了一个输入b比特输出b比特的置换函数 (Permutation) $f$。

海绵结构允许输入任意长度的输入，并产生任意长度的输出。他的工作过程分为吸收 (Absorb) 和挤压 (Squeeze) 两个阶段，先分块吸收输入，在分块挤压输出。

双工结构则允许反复的吸收和挤压，且后面的挤压输出结果依赖于前面的所有输入。

更多说明请参考Keccak团队[网站](https://keccak.team/sponge_duplex.html)上的说明。

## Cyclist Mode in Xoodyak

在海绵结构中，吸收、挤压和置换函数的操作顺序非常的简单——吸够了就置换，置换完接着吸，直到吸完了并置换一次，开始挤压。而在Xoodyak的双工结构中，Spec文档中定义了一层又一层的函数，层层调用，也没给实际运行的例子，看了我好半天才弄清啥时候吸收、啥时候挤压、啥时候置换函数。本文尝试讲清楚这个问题，帮助大家（和以后的我）看懂Spec。

Cyclist mode，骑车人模式，意思是在Xoodyak的双工结构中，操作像是骑车蹬脚踏板一样，一下一上、一下一上，参见上面双工结构的示意图。往下蹬就对应着吸收输入，往上就对应着挤压输出，所以在Xoodyak的Spec中，定义了两个底层的函数Up()和Down()。

然而，在Spec中，置换函数并**没有**被单拉出来作为和Up(), Down()同一级的函数，而是被包含在了Up()函数中。即，在Spec定义中，Up()函数会先执行一次置换函数，再挤压出数据；而Down()函数仅仅会吸收，即把输入异或到状态上，不会执行置换函数。

再上一级，Spec又定义了几个函数：Absorb()，Encrypt()，Decrypt()，Squeeze()。他们的行为描述如下：

- Absorb：如果上一次操作不是Up，就先执行一次Up（先置换再挤出），然后执行Down吸收输入
- Encrypt：把明文分成很多块，对于每块执行：
  - 先Up（先置换再挤出），然后把挤出的数与明文异或，作为密文
  - 然后用Down把明文吸收
- Decrypt：与Encrypt类似，先Up（先置换再挤出），把挤出的数与密文异或，得到明文；然后用Down吸收明文
- Squeeze：直接Up（先置换再挤出），如果输出不够，Down吸收一个空的，再Up（先置换再挤出）

这里忽略了一些中间函数，忽略了padding，是为了获得更直观的理解，具体实现细节还要看Spec。另外，实际的Up在置换前，还要先在状态最后一个byte异或一个名叫color的东西，用来标志当前是什么操作。

## AEAD in Xoodyak

现在应该可以尝试看懂Spec最后说明的AEAD流程了，除了第一行代码**Xoodyak(K, nonce)**,这里的Xoodyak的意思并不是执行一次Xoodyak算法，而是**实例化**一个Xoodyak对象（并用K, nonce初始化），类似软件语言中的实例化一个类。（另外，初始化不会运行置换函数）

- 加密：

  ```
  Xoodyak(Key,nonce)
  Absorb(AD)
  CphTxt <- Encrypt(PlnTxt)
  Tag <- Squeeze(t)
  return (CphTxt,Tag)
  ```

- 解密：

  ```
  Xoodyak(Key,nonce)
  Absorb(AD)
  PlnTxt <- Decrypt(CphTxt)
  Tag' <- Squeeze(t)
  if Tag == Tag' then
  	return P
  else
  	return 空
  ```

加密的主要操作：

1. 先用密钥key和nonce初始化（将key和nonce填充进state）
2. 运行置换函数
3. 吸收相关数据AD（将AD与state异或）（若未吸收完，运行置换函数后继续吸收）
4. 运行置换函数
5. 使用挤出的数据加密明文（与明文异或），再将明文吸收（若未加密完，运行置换函数后继续加密、吸收）
6. 运行置换函数
7. 挤出Tag

解密操作：

1. 用Key和nonce初始化
2. 运行置换函数
3. 吸收AD
4. 运行置换函数
5. 使用挤出的数据解密密文（与密文异或），再将**明文**吸收
6. 运行置换函数
7. 挤出Tag并比较

## Hash in Xoodyak

```
Xoodyak(空)
Absorb(x)
Squeeze(n)
```

说明：

1. 初始化状态（什么都不做）
2. 吸收数据X（若未吸收完，运行置换函数后继续吸收）
3. 运行置换函数
4. 挤出哈希值（若一次不够，运行置换函数后继续挤出）
