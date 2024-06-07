---
title: Handling Trace Files in H5 Format
lang: zh
tags: ["Cpp", "H5"]
key: H5_FILE
---

 本文总结了用CPP处理侧信道波形文件（使用python scared库得到的`.ets`文件，实际为h5格式）的方法。

<!--more-->

---

## HDF5库的下载安装

- 在[下载地址](https://portal.hdfgroup.org/display/support/Downloads)找到最新版，再找到编译好的Ready to use Binaries，找到适合的版本
  - Visual Studio 2019（vs16）或Visual Studio 2022（vs17）
- 运行安装程序
- 设置环境变量：
  - include加到`INCLUDE`变量
  - lib加到`LIB`变量
  - bin（含dll文件）加到`PATH`变量

## 简单的读取例子

下面是一个使用HDF5库来读取H5格式文件中名为"traces"的数据集的C++程序示例，然后将前4行（每行包含1001个元素）打印在屏幕上。

```cpp
#include <iostream>
#include <string>
#include <H5Cpp.h>
using namespace H5;

int main() {
    H5File file("traces.ets", H5F_ACC_RDONLY);
    DataSet dataset = file.openDataSet("traces");
    DataSpace dataspace = dataset.getSpace();

    hsize_t dims_out[2];
    dataspace.getSimpleExtentDims(dims_out, NULL);
    std::cout << "dims_out " << dims_out[0] << " " << dims_out[1] << std::endl;

    const int numRows = 4;
    const int numCols = 1001;
    unsigned char data[numRows][numCols];

    hsize_t start[2] = {0, 0};
    hsize_t count[2] = {numRows, numCols};
    dataspace.selectHyperslab(H5S_SELECT_SET, count, start);

    DataSpace memspace(2, count);
    dataset.read(data, PredType::NATIVE_UINT8, memspace, dataspace);

    for (int i = 0; i < numRows; ++i) {
        std::cout << "Row " << i << ": ";
        for (int j = 0; j < numCols; ++j) {
            std::cout << static_cast<int>(data[i][j]) << " ";
        }
        std::cout << std::endl;
    }

    dataset.close();
    file.close();
    return 0;
}
```

- `dataspace`（数据空间）是用于描述数据集的维度和大小的对象。它用于定义数据集的形状，以及确定你想要读取或写入的数据集的部分。
  - 我们使用`dataset.getSpace()`获取数据集的数据空间。
  - 使用`dataspace.getSimpleExtentDims(dims_out, NULL)`获取数据集的维度和大小。`dims_out`数组包含数据集的维度信息。在示例中，`dims_out[0]`表示数据集的行数，`dims_out[1]`表示数据集的列数。
- 我们使用`dataspace.selectHyperslab()`来选择我们要读取的数据集的一部分。
- `memspace`（内存空间）是用于定义在内存中的数据的形状和大小的对象。它通常与数据集的数据空间（`dataspace`）一起使用，用于指定在读取或写入数据时，数据应该存储在内存中的哪个位置以及如何组织。
- 在Windows使用Microsoft Visual C++ Build Tools的参考编译命令：`cl.exe /D H5_BUILT_AS_DYNAMIC_LIB /EHsc h5test.cpp /link hdf5.lib hdf5_cpp.lib`

## 相关链接

- H5官网：([The HDF5® Library & File Format - The HDF Group](https://www.hdfgroup.org/solutions/hdf5/))
- H5文档：[HDF5: Main Page (hdfgroup.github.io)](https://hdfgroup.github.io/hdf5/)
