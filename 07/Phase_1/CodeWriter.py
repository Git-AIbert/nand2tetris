#!/usr/bin/env python
# coding: utf-8

# In[1]:


class CodeWriter:
    index = 0
    segment_to_sign = {
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
    }
    SP_minus_1 = '''@SP
AM = M - 1
'''
    SP_add_1 = '''@SP
AM = M + 1
'''
    Binary_Oper = '''@SP
AM = M - 1
D = M
A = A - 1
'''
    
    def __init__(self):
        return
    
    def __init__(self, file):
        self.file = file
    
    def setFileName(self, filename):
        self.file = open(filename, w)
        
    def createJudgementCode(self, judge):
        code = ('''
@SP
AM = M - 1
D = M
@SP
AM = M - 1
A = M
D = A - D
@YES''' + str(self.index) + '''
D; ''' + judge + '''
@SP
A = M
M = 0
@SP
M = M + 1
@CONTINUE''' + str(self.index) + '''
0; JMP
(YES''' + str(self.index) + ''')
@SP
A = M
M = -1
@SP
M = M + 1
(CONTINUE''' + str(self.index) + ''')
''')
        self.index = self.index + 1
        return code

    def writeArithmetic(self, Command):
        if Command == 'add':
            code = self.Binary_Oper + 'M = M + D\n'
            self.file.write(code)
            return
        if Command == 'sub':
            code = self.Binary_Oper + 'M = M - D\n'
            self.file.write(code)
            return
        if Command == 'neg':
            code = self.SP_minus_1 + 'M = - M\n' + self.SP_add_1
            self.file.write(code)
            return
        if Command == 'eq':
            self.file.write(self.createJudgementCode('JEQ'))
            return
        if Command == 'gt':
            self.file.write(self.createJudgementCode('JGT'))
            return
        if Command == 'lt':
            self.file.write(self.createJudgementCode('JLT'))
            return
        if Command == 'and':
            code = self.Binary_Oper + 'M = M & D\n'
            self.file.write(code)
            return
        if Command == 'or':
            code = self.Binary_Oper + 'M = M | D\n'
            self.file.write(code)
            return
        if Command == 'not':
            code = self.SP_minus_1 + 'M = ! M\n' + self.SP_add_1
            self.file.write(code)
            return
        return
        
    def writePushPop(self, Command, segment, index):
        if Command == 'C_PUSH':
            if segment == 'constant':
                code = ('\n@' + index + '''
D = A
@SP
A = M
M = D
@SP
M = M + 1
''')
                self.file.write(code)
                return
        return
        
    def close(self):
        self.file.close()
        return

