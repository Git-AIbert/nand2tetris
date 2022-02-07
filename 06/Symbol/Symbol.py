#!/usr/bin/env python
# coding: utf-8

# In[1]:


import import_ipynb
from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable


# In[2]:


def Symbol(filename):
    parser = Parser('../' + filename + '.asm')
    code = Code()
    symbolTable = SymbolTable()
    mLanguage = ''
    ROM_address = 0
    RAM_address = 16

    # 第一遍读取阶段
    while(parser.hasMoreCommands()):
        parser.advance()
        if parser.commandType() == 'A_COMMAND' or parser.commandType() == 'C_COMMAND':
            ROM_address = ROM_address + 1
        if parser.commandType() == 'L_COMMAND':
            symbolTable.addEntry(parser.symbol(), str(ROM_address))
    
    # 第二遍读取阶段
    while(parser.hasMoreCommands()):
        parser.advance() 
        if parser.commandType() == 'A_COMMAND':
            if parser.symbol()[0] >= '0' and parser.symbol()[0] <= '9': # 是数字
                mLanguage = mLanguage + code.symbol(parser.symbol()).zfill(16) + '\n'
            else: # 是符号
                if symbolTable.contains(parser.symbol()):
                    mLanguage = mLanguage + code.symbol(symbolTable.GetAddress(parser.symbol())).zfill(16) + '\n'
                else:
                    symbolTable.addEntry(parser.symbol(), str(RAM_address))
                    RAM_address = RAM_address + 1
                    mLanguage = mLanguage + code.symbol(symbolTable.GetAddress(parser.symbol())).zfill(16) + '\n'
                    
        if parser.commandType() == 'C_COMMAND':
            mLanguage = mLanguage + '111' + code.comp(parser.comp()) + code.dest(parser.dest()) + code.jump(parser.jump()) + '\n'
    
    print(mLanguage)
    with open('../' + filename + '1.hack', 'w') as file_object:
        file_object.write(mLanguage)


# In[3]:


Symbol('rect/Rect')

