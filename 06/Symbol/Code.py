#!/usr/bin/env python
# coding: utf-8

# In[1]:


class Code:
    cSet = {
        '0': '0101010',
        '1': '0111111',
        '-1': '0111010',
        'D': '0001100',
        'A': '0110000',
        'M': '1110000',
        '!D': '0001101',
        '!A': '0110001',
        '!M': '1110001',
        '-D': '0001111',
        '-A': '0110011',
        '-M': '1110011',
        'D+1': '0011111',
        'A+1': '0110111',
        'M+1': '1110111',
        'D-1': '0001110',
        'A-1': '0110010',
        'M-1': '1110010',
        'D+A': '0000010',
        'D+M': '1000010',
        'D-A': '0010011',
        'D-M': '1010011',
        'A-D': '0000111',
        'M-D': '1000111',
        'D&A': '0000000',
        'D&M': '1000000',
        'D|A': '0010101',
        'D|M': '1010101',
    }
    jSet = {
        'JGT': '001',
        'JEQ': '010',
        'JGE': '011',
        'JLT': '100',
        'JNE': '101',
        'JLE': '110',
        'JMP': '111',
    }
    
    def symbol(self, symbol):
        binary = bin(int(symbol))[2:]
        return binary
    
    def dest(self, dest):
        temp = ['0', '0', '0']
        if 'A' in dest:
            temp[0] = '1'
        if 'D' in dest:
            temp[1] = '1'
        if 'M' in dest:
            temp[2] = '1'
        return ''.join(temp)

    def comp(self, comp):
        if comp in self.cSet:
            return self.cSet[comp]
        if '+' in comp or '|' in comp or '&' in comp:
            comp = comp[::-1] # 字符串逆序
            if comp in self.cSet:
                return self.cSet[comp]
        raise Exception("无效指令")

    def jump(self, jump):
        if jump != '':
            if jump in self.jSet:
                return self.jSet[jump]
            else:
                raise Exception("无效指令")
        return '000'

