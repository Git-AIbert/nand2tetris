#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re

class Parser:
    instructions = []
    pc = -1
    length = 0
    Type = ''

    def __init__(self, file):
        for line in file.readlines():
            line = line.strip() # 移除每行首尾的空格
            if (line == '' or re.match(r'^(\/\/)',line)): # 忽略以//开头的行
                continue
            line = re.sub(r'(\/\/).*', '',line).strip() # 移除//之后的部分
            self.instructions.append(line)
            self.length = self.length + 1

    def hasMoreCommands(self):
        return self.pc < self.length - 1

    def advance(self):
        self.pc = self.pc + 1

    def commandType(self):
        self.Type = ''
        if self.instructions[self.pc].split(' ')[0] == 'pop':
            self.Type = 'C_POP'
        if self.instructions[self.pc].split(' ')[0] == 'push':
            self.Type = 'C_PUSH'
        if self.instructions[self.pc].split(' ')[0] == 'label':
            self.Type = 'C_LABEL'
        if self.instructions[self.pc].split(' ')[0] == 'goto':
            self.Type = 'C_GOTO'
        if self.instructions[self.pc].split(' ')[0] == 'if-goto':
            self.Type = 'C_IF'
        if self.Type == '':
            self.Type = 'C_ARITHMETIC'
        return self.Type
    
    def arg1(self):
        if self.Type == 'C_ARITHMETIC': # 如果是计算类型，则返回命令本身，否则返回命令的第一个参数
            return self.instructions[self.pc]
        return self.instructions[self.pc].split(' ')[1]
    
    def arg2(self):
        return self.instructions[self.pc].split(' ')[2]

