---
title: Composing Masked Gadgets
lang: zh
tags: ["SCA", "Masking", "Summary"]
---

本文总结了如何用Gadgets安全地构建整体电路。

主要介绍了t-probing secure、t-NI、t-SNI、t-PINI、robust probing model。

<!--more-->

---

**传统密码分析**通常假设攻击者根据**正常信道**（根据密文、明文等）的信息来进行分析与攻击。**侧信道攻击（SCA）**指攻击者利用**密码设备运算时的物理信道**（实时功耗、电磁辐射、运算时间等）的侧信息来进行分析与攻击。侧信道攻击对密码设备的安全造成了严重的威胁。为了抵抗侧信道攻击，目前最流行和有效的一种方法为**掩码（Masking）**。掩码通过将秘密信息分为多个share，通过随机数让每个share都与秘密信息独立，从而切断<u>与运算数据相关的侧信息</u>和<u>秘密信息</u>的关系。由于从零开始构造一个复杂的侧信道安全的电路是非常困难的，因此学术界首先对简单的电路进行了大量的研究，提出了各种侧信道保护的门的结构。这些小组件称为**Gadget**，为了构造复杂的电路，需要将Gadget进行组合。然而，本身是侧信道安全的Gadget，并不能保证组合而成的整体电路是侧信道安全的。本文总结和介绍了目前关于**如何用Gadget安全地组合构建整体电路**的模型与方法。

## 探针模型（Probing Model）[^ISW03]

为了检验电路是否是侧信道安全的，Ishai等研究者提出了探针模型，用于描述一种很强的攻击者的能力。探针模型指，攻击者可以将t根探针放置于电路的内部，可以同时获得t个中间运算结果。对应着，如果电路允许t根探针的攻击，仍能保证安全（可以保证t根探针的值与敏感信息无关），那么就称这个电路是t阶探针安全的（t-probing secure）。

然而，t阶探针安全的gadget，并不能保证组合成复杂电路时仍然是t阶探针安全的。若想要整体电路安全，仍然需要对整体电路进行复杂的分析。因此，为了研究如何更加方便的组合Gadget，研究者们提出了更多的模型与构造方法。

## NI与SNI（Non-Interference & Strong Non-Interference）[^BBP16]

为了说明NI和SNI的定义，首先介绍一下**可仿真性**。

### 可仿真性（Simulatability）

在描述可仿真性时，同时存在一个真正的攻击者，可以利用探针获得电路内的实际值的分布，和一个仿真器，**试图**在没有实际探针的情况下去产生一个和实际分布相同的分布。如果真正的攻击者得到的实际分布，与仿真器模拟产生的分布，是不可区分的，那么就称为具有可仿真性，或是可仿真的。

另外，在有些讨论场景下，仿真器可以已知一部分输入。在极端情况下，如果仿真器不知任何输入也能够仿真，说明中间结果的值与任何输入无关。如果仿真器已知所有输入，那么它一定是可以仿真的。

例如：一个AND门，输入两个数，输出一个数。如果仅已知一个输入，那么仿真器是不能仿真的。

再例如：一个实现$(r\oplus a)\oplus b$的电路，r是独立均匀随机数。不需知道a或b，仿真器也是可以仿真的（将异或视作不可拆分基础元件的情况下）。

### NI与SNI定义

原始NI与SNI仅讨论有一个输出的情况（可以有多个share）。

NI：如果在电路中任意放$t_0\le t$个探针，如果这些探针的分布，可以在已知每个输入的$t_0$个share的情况下被仿真，那么称其为t-NI的。

SNI：如果在电路中放置$t_1$个探针，并在输出放置$t_2$个探针，满足$t_1+t_2\le t$，如果这些探针的分布，可以在已知每个输入的$t_1$个share的情况下被仿真，那么称其为t-SNI的。

NI的电路必定是t-probing安全的，而probing安全的未必是NI的。SNI切断了输出与输入的联系，常常需要更多随机数消耗。

SNI刷新组件：输入一个变量，输出相同的变量，输出的share是使用随机数重新掩码后的，满足SNI的要求。如输入$s_1$, $s_2$，输出$s_1\oplus r$, $s_2\oplus r$，这是个1-SNI的刷新组件。

### 安全组合方法

构造一个t-NI的复杂电路的一个方法：所有组件都是t-NI的，且满足所有组件的输出以及所有输入只能连接一个非SNI刷新组件的输入。换句话，如果一个组件的输出需要在多个组件使用，只有一个可以直接用，其他的都需要经过SNI刷新组件reshare再使用。

### 探针传播方法（Probe Propagation Framework）[^BBP16] [^CasSta20]

NI与SNI还可以使用传播探针的方法来定义和理解。

传播探针：我们在某个位置放置一个探针，那么仿真这个探针所需要已知的前一步的输入，我们把探针也放在上面。这样反复迭代，将探针不断向前传播，直至输入。

NI的传播探针定义：我们在电路上放置$t_0\le t$个传播探针，那么每个输入(的shares中)至多有$t_0$个传播探针。

SNI的传播探针定义：我们在电路中放置$t_1$个探针，并在输出放置$t_2$个探针，满足$t_1+t_2\le t$，那么每个输入(的shares中)至多有$t_1$个传播探针。

用传播探针描述的安全条件：

1. 对于参数t<d，所有组成组件都是t-NI的
2. 对于连接组件的连线（每个连线指携带一个变量的所有shares的集合），每个连线上至多t个传播探针
3. 对于所有SNI组件，其上的中间探针加输出探针数之和小于等于t

## PINI（Probe Isolating Non-Interference）[^CasSta20]

提出PINI的目的在于让安全组合电路的方法变得更加简单直接。在NI和SNI中，重要的是探针的数量，而在PINI中，重要的是探针的位置（即探针所在share的index）。如果电路可以被分为d个独立的部分，那么对于t<d，敌手只能得知t个电路部分内的信息，无法获得其他部分的信息。那么如果一个电路满足，对于每个输出上的探针，其传播到输入时，对应的只是相同index的share；每个中间的探针，都只对应一个额外的电路部分，那么称为PINI的。

更严格的定义：对于$t_1$个index的集合A，和$t_2$个中间探针，满足$t_1+t_2\le t$，如果存在$t_2$个index的集合B，可以在已知index为A和B的输入share的情况下，仿真所有index为A的输出探针和前面提到的中间探针，那么称其为t-PINI的。

t-PINI的电路是t-probing安全的

将t-PINI的电路直接组合起来，其组合电路仍是t-PINI的

## MIMO-SNI

 [^CasSta20]文中还提出了MIMO-SNI的定义，该定义比PINI还要强（要求更严），t-MIMO-SNI的均满足t-PINI，详情见原文。

## 参考文献

[^ISW03]: Y. Ishai, A. Sahai, and D. A. Wagner, “Private circuits: Securing hardware against probing attacks,” in Proc. CRYPTO, 2003, pp. 463–481.
[^BBP16]: S. Belaïd, F. Benhamouda, A. Passelègue, E. Prouff, A. Thillard, and D. Vergnaud, “Randomness complexity of private circuits for multiplication,” in Proc. EUROCRYPT, 2016, pp. 616–648.
[^CasSta20]: Gaëtan Cassiers and François-Xavier Standaert. 2020. Trivially and efficiently composing masked gadgets with probe isolating non-interference. IEEE Transactions on Information Forensics and Security 15 (2020), 2542–25
