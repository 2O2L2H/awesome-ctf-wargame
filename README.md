# awesome-ctf-wargame

**Writeup oriented CTF skill improvement**

The corresponding ctf problem and wargame will be curated based on each required skill. 

:exclamation:  You may need the login account for browsing each wargame properly.

## :pencil:  Wargames on system hacking

| Difficulty | Wargames | 
|------------|----------|
| Easy | [(Exploit-exercise) Protostar](https://exploit-exercises.com/protostar/) |
| Medium | [(Root-me) App System](https://www.root-me.org/en/Challenges/App-System/), [(PwnerRank) Binary Exploitation](https://www.pwnerrank.com/categories/binary-exploitation/) |
| High | [Pwnable.kr](http://pwnable.kr/) |

### (0) TIP  :+1: 

- Generate and search pattern string for exploit development : [exploit-pattern @github](https://github.com/Svenito/exploit-pattern)
- Multi-Architecture GDB Enhanced Features for Exploiters & Reverse-Engineers : [gef @github](https://github.com/hugsy/gef)


### (1) BoF (Buffer Overflow)

#### 1. Overwrite local variable


| Difficulty | Platform | Exercise |
|------------|----------|----------|
| Easy | x86 |  [(Protostar) Stack0](https://exploit-exercises.com/protostar/stack0/), [(Protostar) Stack1](https://exploit-exercises.com/protostar/stack1/), [(root-me) x86 BoF basic1](https://www.root-me.org/en/Challenges/App-System/ELF-x86-Stack-buffer-overflow-basic-1) |

#### 2. Environment variable usage

| Difficulty | Platform | Exercise |
|------------|----------|----------|
| Easy | x86 |  [(Protostar) Stack2](https://exploit-exercises.com/protostar/stack2/) |


#### 3. Overwrite LR (to be other function like flag printing)

| Difficulty | Platform | Exercise |
|------------|----------|----------|
| Easy | x86 | [(Protostar) Stack3](https://exploit-exercises.com/protostar/stack3/), [(Protostar) Stack4](https://exploit-exercises.com/protostar/stack4/), [(root-me) x86 BoF basic2](https://www.root-me.org/en/Challenges/App-System/) |
|  | x64 |  [(root-me) x64 BoF basic](https://www.root-me.org/en/Challenges/App-System/ELF-x64-Stack-buffer-overflow-basic) |


#### 4. Overwrite LR + shellCode injection

| Difficulty | Platform | Exercise |
|------------|----------|----------|
| Easy | x86 | [(Protostar) Stack5](https://exploit-exercises.com/protostar/stack5/) |

#### 5. Ret2Libc (Return-to-Libc)


### (2) Format String

#### 1. Arbitrary memory read

#### 2. Direct Parameter Access (`n$`)

#### 3. Arbitrary memory write using `%n`

| Difficulty | Platform | Exercise |
|------------|----------|----------|
| Easy       | x86      | Easy - [Protostar: Format1](https://exploit-exercises.com/protostar/format1/) |


### (3) ROP (Return Oriented Programming)


### (4) Heap exploitation


### (5) ASLR bypassing



## Cryptography

### (1) Caesar cryptography

### (2) AES

### (3) RSA


## Forensics


## Web

### (1) SQL Injection

### (2) XSS (Cross-site Scripting)




