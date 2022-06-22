---
title: Logging in Python
lang: zh
tags: ["Python", "Tutorial"]
key: Logging_in_Python
---

 本文为笔者学习Python中logging功能的笔记。主要内容翻译摘自[Logging in Python by Abhinav Ajitsaria](https://realpython.com/python-logging/)

<!--more-->

---

Logging是调试程序的一个非常强大的工具。使用logging而非直接print有以下几点原因：

- 使用logging不必像使用print时反复删除或注释，来调整是否输出调试信息。
- 大部分python库都使用logging，想要调试相关库，可以直接用logging观察运行状况。

## 开始使用

Logging模块是Python中可直接引入使用的库。直接这样引入：

```python
import logging
```

默认有5个标准的等级，来描述事件的紧急程度：

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

本模块提供了一个默认的logger，可以直接使用而不用太多配置。可以直接这样记录各个等级的信息：

```python
import logging

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')
```

对应的输出为：

```
WARNING:root:This is a warning message
ERROR:root:This is an error message
CRITICAL:root:This is a critical message
```

输出信息的默认格式为：等级:logger名称:信息。其中默认logger的名称为root。此外，还可以通过配置，让输出信息包含时间戳、行数以及其他细节。

另外，默认输出的等级为WARNING及以上。可以通过配置来改变输出等级。

## 基本配置

可以通过`basicConfig()`来进行配置，一些基础的参数为：

- level: 输出等级
- filename: 输出文件名
- filemode: 文件打开方式，默认为`a`，即append
- format: log信息的格式

可以改变输出等级，记录所有DEBUG等级以上的信息：

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug('This will get logged')
```

```
DEBUG:root:This will get logged
```

可以将日志输出至文件，并通过format改变格式：

```python
import logging

logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logging.warning('This will get logged to a file')
```

```
root - ERROR - This will get logged to a file
```

更多基础配置的参数可以参考[此文档](https://docs.python.org/3/library/logging.html#logging.basicConfig)。

注意：`basicConfig()`只能被调用一次，且必须在`debug()`, `info()`等之前配置。

## 输出格式

虽然你可以在调用记录时，将任何字符串传到message中，但是其实每条记录本身有一些基础元素可以添加到记录中。

比如可以将进程ID添加到记录中：

```python
import logging

logging.basicConfig(format='%(process)d-%(levelname)s-%(message)s')
logging.warning('This is a Warning')
```

```
18472-WARNING-This is a Warning
```

可以将记录创建的日期时间添加到记录中：

```python
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Admin logged in')
```

```
2018-07-11 20:12:06,288 - Admin logged in
```

日期时间的格式可以通过`datefmt`参数调整：

```python
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.warning('Admin logged out')
```

```
12-Jul-18 20:53:19 - Admin logged out
```

记录中可用的其他参数参见[此文档](https://docs.python.org/3/library/logging.html#logrecord-attributes)，调整日期格式参见[此文档](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior)。

### 记录可变的信息

大多数情况下，希望记录的信息不是固定的字符串，而是与程序运行相关的可变的信息。可以类似print来使用：

```python
import logging

name = 'John'

logging.error('%s raised an error', name)
```

也可以使用Python 3.6后引入的f字符串方法，这种方法更直观易读：

```python
import logging

name = 'John'

logging.error(f'{name} raised an error')
```

### 记录函数调用信息（Stack Traces）

在记录时，使用参数`exc_info=True`可以记录完整的调用信息：

```python
import logging

a = 5
b = 0

try:
  c = a / b
except Exception as e:
  logging.error('Exception occurred', exc_info=True)
```

```
ERROR:root:Exception occurred
Traceback (most recent call last):
  File ".\logtest.py", line 7, in <module>
    c = a / b
ZeroDivisionError: division by zero
```

如果不将`exc_info`置为`True`，输出将只有：

```
ERROR:root:Exception occurred
```

一种简洁的方法，可以直接使用`logging.exception()`，相当于`logging.error(exc_info=True)`：

```python
import logging

a = 5
b = 0

try:
  c = a / b
except Exception as e:
  logging.exception('Exception occurred')
```

```
ERROR:root:Exception occurred
Traceback (most recent call last):
  File ".\logtest.py", line 7, in <module>
    c = a / b
ZeroDivisionError: division by zero
```

## 自定义Logger

前面我们使用的都是默认的名为`root`的logger，这个默认logger可以通过`logging`中的函数`logging.debug()`等直接调用。实际中，我们更常使用自定义的logger，尤其是应用中有较多模块时。为了使用自定义的logger，我们需要实例化一个Logger类的对象，这可以通过函数`getLogger(name)`来得到：

```python
import logging

logger = logging.getLogger('example_logger')
logger.warning('This is a warning')
```

```
This is a warning
```

多次调用`getLogger()`函数并使用相同的名称，将会得到相同的一个logger，这样我们就可以在任意一处得到一个想要的logger。

### logging库中的类

为了配置自定义的logger，我们需要了解logging库中常用的几个类，和他们工作的方式：

- **Logger**: 日志记录器，在记录日志时，我们直接调用的就是这个类的对象
- **LogRecord**: 记录，在我们调用日志记录器进行记录时，会自动生成一个此类的对象，包含该记录对应的相关信息（logger名称、message、行数、时间等）
- **Handler**: 记录处理器，Handler将一个LogRecord发送到目标输出的地方，比如控制台或一个文件
- **Formatter**: 输出格式，在这里定义输出的格式，即最终的输出记录用什么样的格式包含LogRecord中的那些信息

和默认的`root`不同，自定义的logger不能通过`basicConfig()`来配置，而需要通过Handler和Formatter来配置。

### 使用Handler和Formatter

Handler用来将产生的记录发送到不同的地方，比如发送到标准输出（屏幕控制台），比如写入文件，比如通过SMTP发送到邮箱。一个logger可以有多个handler，即可以发送到多个地方。

此外，handler也可以设置等级，比如你想将WARNING以上记录在文件中，同时ERROR以上通过邮件发送到邮箱，就可以将两个handler设置不同等级。

设置的例子：

```python
import logging

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.warning('This is a warning')
logger.error('This is an error')
```

在屏幕的输出为

```
__main__ - WARNING - This is a warning
__main__ - ERROR - This is an error
```

在文件的输出为

```
2018-08-03 16:12:21,723 - __main__ - ERROR - This is an error
```

其中`__main__`为默认模块的名称，如果上述代码在`logging_example.py`文件中，下面的代码导入该文件，则对应的`__name__`变量就对应`logging_example`：

```python
import logging_example
```

屏幕输出

```
logging_example - WARNING - This is a warning
logging_example - ERROR - This is an error
```

### 其他配置方法

除了以上直接配置的方法，还可以通过配置文件加载配置或者通过字典加载配置（字典可以从其他类型的配置文件中读出，如YAML或TOML等），分别使用`logging.config.fileConfig()`及`logging.config.dictConfig()`。其中字典的格式参考[这里](https://docs.python.org/3/library/logging.config.html#logging-config-dictschema)。

#### 配置文件

配置文件的例子：

```
[loggers]
keys=root,sampleLogger

[handlers]
keys=consoleHandler

[formatters]
keys=sampleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_sampleLogger]
level=DEBUG
handlers=consoleHandler
qualname=sampleLogger
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=sampleFormatter
args=(sys.stdout,)

[formatter_sampleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

使用配置文件配置的方法：

```python
import logging
import logging.config

logging.config.fileConfig(fname='file.conf', disable_existing_loggers=False)

# Get the logger specified in the file
logger = logging.getLogger('sampleLogger')
```

#### YAML文件

文件内容：

```yaml
version: 1
formatters:
  simple:
    format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
handlers:
  console:
    class: logging.StreamHandler
    level: DEBUG
    formatter: simple
    stream: ext://sys.stdout
loggers:
  sampleLogger:
    level: DEBUG
    handlers: [console]
    propagate: 0
root:
  level: DEBUG
  handlers: [console]
```

读取方法：

```python
import logging
import logging.config
import yaml

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)

logger = logging.getLogger(sampleLogger)
```

#### TOML文件

文件内容：

```toml
version   = 1
[formatters.fmt1]
format    = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
[handlers.hdl1]
class     = 'logging.StreamHandler'
level     = 'DEBUG'
formatter = 'fmt1'
[loggers.logger1]
level     = 'DEBUG'
handlers  = ['hdl1']
propagate = 0
[root]
level     = 'DEBUG'
handlers  = ['hdl1']
```

读取方法：

```python
import logging
import logging.config
import rtoml

with open('config.toml', 'r') as f:
    config = rtoml.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger('logger1')
```

## 实例及技巧

### 编写库时的日志

如果你正在编写一个将会在别处调用的库，最好为其使用单独的自定义logger，这样调用该库的人可以更方便的控制开启哪一部分的日志。

如果是单文件的库，可以用`__name__`来作为logger的名字，即`logger = logging.getLogger(__name__)`。如果该库的文件名为`filea.py`，调用时`import filea`，对应的logger的名字就是`filea`。

如果是多文件的库，最好用库的名称作为logger的名字。

### 等级控制

在自定义logger时，logger以及handler均可以设置输出等级。可以将这种设置看作过滤器或滤波器，结合一条日志的处理过程：
$$
logger\to handler\to files/stream
$$
可以知道，logger只会将高于`l_logger`的LogRecord发给handler，handler只会处理高于`l_handler`的LogRecord，其中`l_logger`, `l_handler`分别指logger和handler设置的等级。

因此，对于一个logger和一个handler，只有等级高于等于两者的等级的日志记录才会被输出。

### 一个例子

本例中，我们在编写一个测试程序`test.py`，调用了自己编写的一个库`mypackage.py`，调用了一个第三方库`pyvisa`。现在我们希望将日志打印到文件中，用于debug。

通过查看`pyvisa`库的源文件，可以知道该库中的logger名称为`pyvisa`。自己的库`mypackage.py`的logger名称为`mypackage`。测试程序`test.py`中的logger名称为`test`。

在配置文件`log_config.toml`中，配置三个logger：

```toml
version   = 1
[formatters.simple]
format    = '%(name)s - %(levelname)s - %(message)s'
[formatters.time]
format    = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
[handlers.console]
class     = 'logging.StreamHandler'
level     = 'INFO'
formatter = 'simple'
[handlers.file]
class     = 'logging.FileHandler'
level     = 'DEBUG'
formatter = 'time'
filename  = 'testlog.log'
mode      = 'w'
[loggers.mypackage]
level     = 'INFO'
handlers  = ['console', 'file']
propagate = 0
[loggers.test]
level     = 'INFO'
handlers  = ['console']
propagate = 0
[loggers.pyvisa]
level     = 'DEBUG'
handlers  = ['file']
propagate = 0
```

其中，设置了两种formatter，区别是是否包含时间信息；设置了两个handler，分别输出至控制台和文件中，因为控制台想用来观察实验进程是否正常，文件用来具体debug，因此等级分别设置为了`INFO`和`DEBUG`；对三个logger分别进行了配置，本例主要想观察pyvisa为何工作不正常，因此将pyvisa的logger的等级设置为了`DEBUG`，其余设置为了`INFO`。

部分测试脚本文件`test.py`：

```python
import pyvisa
import mypackage
import logging
import logging.config
import rtoml

with open('log_config.toml', 'r') as f:
    config = rtoml.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger('test')

# test
logger.info('example info')
```

