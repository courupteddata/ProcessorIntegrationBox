#!/bin/bash
nohup /usr/sbin/sshd -D &
python3 /app/main.py
