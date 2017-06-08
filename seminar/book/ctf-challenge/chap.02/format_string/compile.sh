gcc -m32 -fno-stack-protector -z execstack -no-pie -O2 -o $1 $1.c

