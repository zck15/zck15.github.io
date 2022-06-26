---
title: Run KAT for LWC
lang: zh
tags: ["LWC", "Tutorial"]
key: Run_KAT_for_LWC
---

本文介绍了如何对轻量级密码算法 (LWC) 硬件代码进行已知答案测试 (KAT) 的方法步骤。

<!--more-->

---

## 准备

- 下载GMU提供的[**LWC开发包**](https://github.com/GMUCERG/LWC/releases)，其中路径`hardware\dummy_lwc\scripts\`下包含了**测试脚本**
- 安装好**Modelsim**，可从[Intel网站](https://www.intel.com/content/www/us/en/software/programmable/quartus-prime/model-sim.html)点击下载，选择Intel Quartus blabla，选择版本21.2，选择Individual Files，下载ModelSim相关的文件并安装，参考[博客](https://blog.csdn.net/qq_39021670/article/details/124967506)
- 准备好**RTL代码**和**KAT文件**
  - 如果是测试别人的实现，别人提供的库中应该有对应的KAT。
    - [LWC硬件防护实现列表](https://cryptography.gmu.edu/athena/LWC/LWC_Finalists_protected_HW_implementations.html)
    - [LWC硬件未防护实现列表](https://cryptography.gmu.edu/athena/LWC/LWC_Finalists_unprotected_HW_implementations.html)
  - 如果是自己的实现，可以用开发包中`software\cryptotvgen\`中的测试向量生成器cryptotvgen生成KAT文件

## 测试环境

建议新建文件夹，并按以下的文件结构准备测试环境

- `src_rtl\`：rtl源代码
- `KAT\v1\`：KAT文件，**两级文件夹**是因为官方tb文件中按这个路径读的
  - 路径下应包含`do.txt`、`pdi.txt`、`rdi.txt`、`sdi.txt`
  - **如果没有`rdi.txt`**：请先随便从别的库里找一个，然后根据`src_rtl\LWC_config.vhd`文件（或类似名称）中`RW`的定义，修改`rdi.txt`的每行长度（`RW`是每行bit数，`rdi.txt`中是16进制表示，因此每行应有`RW/4`个数字）
- `scripts\`：测试脚本
  - `modelsim.tcl`，拷贝自`LWC开发包\hardware\dummy_lwc\scripts\modelsim.tcl`，稍后会对内容进行修改
- `LWC_rtl\`：LWC的接口源代码，拷贝自`LWC开发包\hardware\LWC_rtl\`
- `LWC_tb\`：LWC的testbench代码，拷贝自`LWC开发包\hardware\LWC_tb\`

## 修改测试脚本

修改`scripts\modelsim.tcl`

- 原接口库路径设置`set INTERFACE_REPO "../../LWCsrc"`修改为：

  ```
  set INTERFACE_REPO "../LWC_rtl"
  ```

- 顶层名称设置`set TOP_LEVEL_NAME LWC_TB`不要修改

- 修改rtl文件列表，可以参考原库中`.toml`文件中`[rtl]`的`sources`列表

  - vhdl文件放在`src_vhdl`的列表中，例如

    ```tcl
    set src_vhdl [subst {
        "../src_rtl/CryptoCore_SCA.vhd"
        "../src_rtl/design_pkg.vhd"
        "../src_rtl/LWC_config_32.vhd"
        "../src_rtl/xoodoo_globals.vhd"
        "$INTERFACE_REPO/data_piso.vhd"
        "$INTERFACE_REPO/data_sipo.vhd"
	      "$INTERFACE_REPO/FIFO.vhd"
        "$INTERFACE_REPO/key_piso.vhd"
        "$INTERFACE_REPO/NIST_LWAPI_pkg.vhd"
        "$INTERFACE_REPO/PreProcessor.vhd"
        "$INTERFACE_REPO/PostProcessor.vhd"
        "$INTERFACE_REPO/LWC_SCA.vhd"
    }]
    ```
  
  - verilog文件，参考`src_vhdl`格式，新建一个`src_verilog`列表，例如
  
    ```tcl
    set src_verilog [subst {
        "../src_rtl/xoodoo_n_rounds_SCA.v"
        "../src_rtl/xoodoo_register_SCA.v"
        "../src_rtl/xoodoo_round_SCA.v"
        "../src_rtl/xoodoo_SCA.v"
    }]
    ```
  
  - tb文件列表，修改为：
  
    ```tcl
    set tb_vhdl [subst {
        "../LWC_tb/LWC_TB_SCA.vhd"
    }]
    ```

- 修改编译实现部分（注释`# Compile implementation files`后），增加对verilog文件的编译命令：

  ```tcl
  alias imp_com {
      echo "imp_com"
      foreach f $src_vhdl {vcom -quiet -work work $f}
      foreach f $src_verilog {vlog -quiet -work work $f}
  }
  ```

- 修改波形列表设置（注释`# Add wave form and run`后）

  - 如果只想通过KAT验证是否正确，可以把该列表中除第一行外的命令全部注释（一行不留会报错`invalid command name "#"`），得到：

    ```tcl
    alias run_wave {
        echo "\[exec\] run_wave"
    }
    ```

  - 如果想观察某些波形，推荐新建文件`wave.do`，将添加波形命令写到该文件中。语法可用搜索引擎搜索“Modelsim do”或“Modelsim tcl”

## 使用Modelsim仿真

1. 启动Modelsim，在`Transcript`窗口中通过`cd "path/to/test"`命令进入测试文件夹，注意用`/`而非`\`。

2. 进入脚本路径：`cd scripts`

3. 读取tcl文件：`source modelsim.tcl`，注意，每次修改tcl文件后，都需要先运行此命令重新读取，再运行后面的命令

4. 编译，通过报错信息修改文件列表的顺序

   1. 运行`ldd`命令
   2. 根据报错信息`编译文件A：无法找到名称B`，在tcl的`src_vhdl`或`src_verilog`列表中，将文件B置于文件A之前
   3. 重新进行第三步，读取tcl文件；再进行第四步；直到仿真能够开始

5. 如果仿真出错，可用`quit -sim`命令退出仿真

6. 如果没有问题，应该只输出类似这种结果

   ```
   # ** Note: Testcase #33 MsgID:33 Op:HASH
   #    Time: 20340 ns  Iteration: 1  Instance: /lwc_tb
   ```

   如果**只有个别测试出错**，大部分测试通过，有可能是用的LWC接口版本不同。有的实现使用了较老的版本，用新版本测试会有个别测试出错，可以查看实现的相关说明，找到对应版本进行测试。

## 相关链接

- [NIST LWC项目](https://csrc.nist.gov/projects/lightweight-cryptography)
- [GMU LWC资源与汇总](https://cryptography.gmu.edu/athena/index.php?id=LWC)
- [Modelsim Intel版下载](https://www.intel.com/content/www/us/en/software-kit/670232/intel-quartus-prime-pro-edition-design-software-version-21-2-for-windows.html)
- [清华大学HWSec实验室的LWC侧信道防护实现](https://github.com/ybhphoenix/THU_HWSec_LWC)
