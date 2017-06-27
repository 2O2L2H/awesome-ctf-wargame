footer: radare2 © 2O2L2H Seminar, 2017
slidenumbers: true

# [fit] radare2

[radare/radare2: unix-like reverse engineering framework and commandline tools](https://github.com/radare/radare2)

---

## Installation

```bash
$ sys/install.sh
```

## Basic usage

```bash
$ radare2
Usage: r2 [-ACdfLMnNqStuvwzX] [-P patch] [-p prj] [-a arch] [-b bits] [-i file]
          [-s addr] [-B baddr] [-M maddr] [-c cmd] [-e k=v] file|pid|-|--|=

$ r2
Usage: r2 [-ACdfLMnNqStuvwzX] [-P patch] [-p prj] [-a arch] [-b bits] [-i file]
          [-s addr] [-B baddr] [-M maddr] [-c cmd] [-e k=v] file|pid|-|--|=
```

---

# Usage


```bash
$ r2 executable
$ r2 -d executable
```

