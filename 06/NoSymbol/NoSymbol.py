#!/usr/bin/env python
# coding: utf-8

# In[1]:


import import_ipynb
from Parser import Parser
from Code import Code


# In[2]:


def NoSymbol(filename):
    parser = Parser('../' + filename + '.asm')
    code = Code()
    mLanguage = ''

    while(parser.hasMoreCommands()):
        parser.advance()
        if parser.commandType() == 'A_COMMAND':
            mLanguage = mLanguage + code.symbol(parser.symbol()).zfill(16) + '\n'

        if parser.commandType() == 'C_COMMAND':
            mLanguage = mLanguage + '111' + code.comp(parser.comp()) + code.dest(parser.dest()) + code.jump(parser.jump()) + '\n'
    
    print(mLanguage)
    with open('../' + filename + '1.hack', 'w') as file_object:
        file_object.write(mLanguage)


# In[3]:


NoSymbol('pong/PongL')

