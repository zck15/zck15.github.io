---
title: Rime Configuration
lang: zh
tags: ["Rime", "Tutorial"]
key: Rime_Configuration
---

 中文输入法RIME的配置方法。本文为笔者配置RIME的笔记，主要关于双拼的配置以及在双拼中输入符号的配置。

<!--more-->

---

笔者在厌烦了搜狗输入法不断的弹窗广告后，开始使用开源的[RIME输入法](https://rime.im/)。该输入法支持多种输入方案，可配置性很高。由于配置一次输入法后很久都不会再次重新配置，为了放置遗忘，在配置新电脑时能尽快完成输入法配置，特写此笔记。

## 下载安装

[下载地址](https://rime.im/download/)

### 基本配置

在状态栏右下角输入法处右击，在**输入法设定**中可以取消勾选不使用的方案。注意，按`中`按钮确认。

然后可以选择配色方案，我偏好的方案为luna，同样按`中`确认。

## 双拼方案安装

在状态栏右下角输入法处右击，在**输入法设定**中，点击获取更多输入方案。

 在打开的窗口中输入`double-pinyin`，然后回车，输出中有`Everything is OK`表示安装成功。

## 双拼方案中的特殊符号配置

在状态栏右下角输入法处右击，在**用户文件夹**中`double_pinyin.schema.yaml`中，将

```yaml
punctuator:
  import_preset: default
  
key_binder:
  import_preset: default

recognizer:
  import_preset: default
  patterns:
    reverse_lookup: "`[a-z]*'?$"
```

修改为

```yaml
punctuator:
  import_preset: symbols

key_binder:
  import_preset: paging

recognizer:
  import_preset: default
  patterns:
    punct: '^/([0-9]0?|[A-Za-z]+)$'
    reverse_lookup: "`[a-z]*'?$"
```

在用户文件夹中，新建文件`paging.yaml`:

```yaml
key_binder:
  bindings:
    # commonly used paging keys
    - { when: composing, accept: ISO_Left_Tab, send: Page_Up }
    - { when: composing, accept: Shift+Tab, send: Page_Up }
    - { when: composing, accept: Tab, send: Page_Down }
    - { when: has_menu, accept: minus, send: Page_Up }
    - { when: has_menu, accept: equal, send: Page_Down }
    - { when: paging, accept: comma, send: Page_Up }
    - { when: has_menu, accept: period, send: Page_Down }
    - { when: paging, accept: bracketleft, send: Page_Up }
    - { when: has_menu, accept: bracketright, send: Page_Down }
```

在状态栏右下角输入法处右击，在**程序文件夹**的data子文件夹中，在文件`symbols.yaml`的结尾添加:

```yaml
    "/alpha":   [ "α", "Α" ]
    "/beta":    [ "β", "Β" ]
    "/gamma":   [ "γ", "Γ" ]
    "/delta":   [ "δ", "Δ" ]
    "/epsilon": [ "ε", "Ε" ]
    "/zeta":    [ "ζ", "Ζ" ]
    "/eta":     [ "η", "Η" ]
    "/theta":   [ "θ", "Θ" ]
    "/iota":    [ "ι", "Ι" ]
    "/kappa":   [ "κ", "Κ" ]
    "/lambda":  [ "λ", "Λ" ]
    "/mu":      [ "μ", "Μ" ]
    "/nu":      [ "ν", "Ν" ]
    "/xi":      [ "ξ", "Ξ" ]
    "/omicron": [ "ο", "Ο" ]
    "/pi":      [ "π", "Π" ]
    "/rho":     [ "ρ", "Ρ" ]
    "/sigma":   [ "σ", "Σ", "ς" ]
    "/tau":     [ "τ", "Τ" ]
    "/upsilon": [ "υ", "Υ" ]
    "/phi":     [ "φ", "Φ" ]
    "/chi":     [ "χ", "Χ" ]
    "/psi":     [ "ψ", "Ψ" ]
    "/omega":   [ "ω", "Ω" ]
```

在状态栏右下角输入法处右击，点击重新部署

## 参考资料

- [官方指南](https://github.com/rime/home/wiki/UserGuide)
