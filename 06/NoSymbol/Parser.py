#!/usr/bin/env python
# coding: utf-8

# In[154]:


import re

class Parser:
    instructions = []
    pc = -1
    length = 0

    def __init__(self, path):
        f = open(path, "r")
        for line in f.readlines():
            line = line.strip()
            if (line == '' or re.match(r'^(\/\/)',line)):
                continue
            line = re.sub(r'(\/\/).*', '',line).strip()
            self.instructions.append(line)
            self.length = self.length + 1

    def hasMoreCommands(self):
        return self.pc < self.length - 1

    def advance(self):
        self.pc = self.pc + 1

    def commandType(self):
        if self.instructions[self.pc][0] == '@':
            return 'A_COMMAND'
        if self.instructions[self.pc][0] == '(':
            return 'L_COMMAND'

        return 'C_COMMAND'

    def symbol(self):
        return self.instructions[self.pc][1:]

    def dest(self):
        if '=' in self.instructions[self.pc]:
            return self.instructions[self.pc].split('=')[0].strip()
        return ''

    def comp(self):
        comp = self.instructions[self.pc]
        if '=' in comp:
            comp = comp.split('=')[1].strip()
        if ';' in comp:
            comp = comp.split(';')[0].strip()
        comp = ''.join(comp.split(' ')) # 删除空格
        return comp

    def jump(self):
        if ';' in self.instructions[self.pc]:
            return self.instructions[self.pc].split(';')[1].strip()
        return ''

