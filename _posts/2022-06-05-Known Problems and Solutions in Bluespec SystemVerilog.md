---
title: Known Problems and Solutions in Bluespec SystemVerilog
lang: zh
tags: ["BSV", "Issues"]
key: Known_Problems_and_Solutions_in_Bluespec_SystemVerilog
---

 本文总结了在硬件描述语言**Bluespec SystemVerilog (BSV)** 中的一些已知问题和解决方法。

<!--more-->

---

**Bluespec SystemVerilog (BSV)** 是一门用于硬件描述设计的高级语言，可被用来FPGA和ASIC的设计和验证。

相比于Verilog来说，BSV具有以下几个特点，使其在设计大型复杂电路时更加得心应手：

- 使用**原子行为**来描述电路功能。每个原子行为都是同时发生的、不可再分的一个单元。一方面，我们可以将电路的每个功能、每种状态变换用独立的一个行为来描述，具有更好地可读性和可维护性；另一方面，原子行为是不可再分的，只要保证该行为是正确的，在和外部众多电路组合起来后，就仍然是正确的，这大大简化了设计和debug的难度。
- 更高的**抽象等级**。提供了更多的数据类型，可以专类型专用，提高了可读性，大大减少因误用出错的情况。将模块的接口抽象出来，并按功能定义不同的方法，更有利于复用。
- 提供了大量的**官方库**，其中包含了大量的常用模块、接口。熟悉了这些官方库后，可以大大加快开发速度。

由于BSV开源的时间较短，使用的人数较少，因此相关的问题讨论的资源较少。官方汇总了一些[已知问题的解决办法(KPNS)](https://web.ece.ucsb.edu/its/bluespec/doc/BSV/kpns.pdf)，本文不是复述其中的问题，而是主要讨论笔者实际遇到的一些问题及解决方法。

## 方法 (Method) 与规则 (rule) 的紧急程度 (urgency)

- **问题描述：** **规则**可以通过**调度属性 (Scheduling attributes)** 来规定紧急程度的区别，从而规定冲突时优先执行哪个规则。而**方法**是无法定义紧急程度的，调度器默认**方法**永远比**规则**更加紧急，即方法和规则冲突时，永远执行方法而非规则（对应编译时的警告`method a shadows the effects of rule b`）。

- **解决方法：**本问题在[官方KPNS](https://web.ece.ucsb.edu/its/bluespec/doc/BSV/kpns.pdf)的Problem #5中讨论了，原文如下：

  > - Problem: Methods are forced to be more urgent than rules.
  >   The scheduler considers methods to be the most urgent things in a module and allows them to block rules whenever they are enabled (as part of implementing the standard interface contract - if a method that is ready is enabled, it will be executed). Sometimes it is desirable to provide a method that is less urgent than an internal rule.
  > - Solution:
  >   Change the ready signal of the method so that it does not overlap with the enable condition of the desired more urgent rule. This can usually be achieved by anding !p (where p is the explicit condition of the relevant rule) with the rest of the method’s ready signal.

  意为：若想让**规则**比**方法**更紧急，即**方法**无法阻塞**规则**运行，可以在**方法**的条件中加上**规则**不执行的条件。即，若规则执行的条件为p，方法原本的调用条件为o，则将方法调用的条件更改为o&&p。

## 规则的命名

- **问题描述：**在规定**调度属性**时，需要用到**规则的名称**。本模块定义的规则r，其名称就是`r`。而**子模块中的规则**、**用for批量定义的规则**、**`mkConnection`对应的规则**，其命名规则是怎样的呢？与报错信息中的规则名称是否相同？
- **解决方法：**我们可以从报错信息提示的规则名称中获得一些启示，然而报错中的名字与书写调度属性时用的名字不尽相同。
  - **子模块的规则命名**：如果在当前模块中实例化了一个子模块，获得的对应接口赋值给了接口变量m（如：`SomeModuleIfc m <- mkSomeModule();`）。那么子模块中的规则r，在本模块中对应的名称为`m.r`，而非报错信息中的`m_r`。
  - **用for批量定义的规则**：如果用for定义了多个规则r（如：`for (Integer i=0; i<n; i=i+1) rule r; ... endrule`）。那么在调度属性中对应的名字分别为`r`, `r_1`, `r_2`, ...。
  - **`mkConnection`对应的规则**：`mkConnection`返回的接口是一个空接口，可以通过显式声明出这个接口来得到对应规则的命名。如声明`Empty e <- mkConnection(aGet, bPut);`，这样对应的规则名称为`e.mkConnectionGetPut`。

## 相关链接

- [BSV中文教程](https://github.com/WangXuan95/BSV_Tutorial_cn) by [Xuan Wang](https://github.com/WangXuan95).
- [BSV官方提供的编译器&仿真器](https://github.com/B-Lang-org/bsc).
- [BSV官方库的文档](https://github.com/B-Lang-org/bsc/releases) (见最新release版本中的`bsc_libraries_ref_guide.pdf`)
- [一些官方文档](https://web.ece.ucsb.edu/its/bluespec/index.html).
