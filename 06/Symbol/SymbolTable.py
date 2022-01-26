#!/usr/bin/env python
# coding: utf-8

# In[11]:


class SymbolTable:
    table = {
        'SP': '0',
        'LCL': '1',
        'ARG': '2',
        'THIS': '3',
        'THAT': '4',
        'SCREEN': '16384',
        'KBD': '24576',
    }
    
    def __init__(self):
        for i in range(16):
            self.table['R' + str(i)] = str(i)
    
    def addEntry(self, symbol, address):
        self.table[symbol] = address
    
    def contains(self, symbol):
        return symbol in self.table
    
    def GetAddress(self, symbol):
        return self.table[symbol]

