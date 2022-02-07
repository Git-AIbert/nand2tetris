#!/usr/bin/env python
# coding: utf-8

# In[1]:


class CodeWriter:
    index = 0
    callIndex = -1
    segment_to_symbol = { # 动态段
        'local': 'LCL',
        'argument': 'ARG',
        'this': 'THIS',
        'that': 'THAT',
    }
    segment_to_number = { # 固定段
        'pointer': '3',
        'temp': '5',
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
    
    def writeInit(self):
        code = '''
@256
D = A
@SP
M = D
'''
        self.file.write(code)
        self.writeCall('Sys.init', '0')
        return

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
            if segment in self.segment_to_symbol:
                code = ('\n@' + index + '''
D = A
@''' + self.segment_to_symbol[segment] + '''
A = M
A = A + D
D = M
@SP
A = M
M = D
@SP
M = M + 1
''')
                self.file.write(code)
                return
            if segment in self.segment_to_number:
                code = ('\n@' + index + '''
D = A
@''' + self.segment_to_number[segment] + '''
A = D + A
D = M
@SP
A = M
M = D
@SP
M = M + 1
''')
                self.file.write(code)
                return
            if segment == 'static':
                code = '\n@' + index + '''
D = M
@SP
A = M
M = D
@SP
M = M + 1
'''
                self.file.write(code)
                return
        else: # C_POP
            if segment in self.segment_to_symbol:
                code = ('\n@' + index + '''
D = A
@''' + self.segment_to_symbol[segment] + '''
D = M + D
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
''')
                self.file.write(code)
                return
            if segment in self.segment_to_number:
                code = ('\n@' + index + '''
D = A
@''' + self.segment_to_number[segment] + '''
D = D + A
@R13
M = D
@SP
AM = M - 1
D = M
@R13
A = M
M = D
''')
                self.file.write(code)
                return
            if segment == 'static': # 靠汇编编译器分配从地址16开始的RAM单元
                code = '''
@SP
AM = M - 1
D = M
'''+ '@' + index + '''
M = D
'''
                self.file.write(code)
                return
    
    def writeLabel(self, label):
        code = '\n(' + label + ')\n'
        self.file.write(code)
        return
    
    def writeGoto(self, label):
        code = '\n@' + label + '''
0;JMP
'''
        self.file.write(code)
        return
    
    def writeIf(self, label):
        code = '''\n@SP
AM = M - 1
D = M
@''' + label + '''
D;JNE
'''
        self.file.write(code)
        return
    
    def writeCall(self, functionName, numArgs):
        self.callIndex = self.callIndex + 1
        # 保存返回地址
        code = '\n@' + functionName + '$return_address' + str(self.callIndex) + '''
D = A
@SP
A = M
M = D
@SP
M = M + 1
'''
        # 保存LCL、ARG、THIS、THAT段指针
        for symbol in ['LCL', 'ARG', 'THIS', 'THAT']:
            code = code + '\n@' + symbol + '''
D = M
@SP
A = M
M = D
@SP
M = M + 1
'''
        # 重置ARG和LCL
        code = code + '\n@' + numArgs + '''
D = A
@5
D = D + A
@SP 
D = M - D
@ARG
M = D
@SP
D = M
@LCL
M = D
'''
        # 跳转至functionName
        code = code + '\n@' + functionName + '''
0;JMP
''' 
        # 为返回地址声明一个标签
        code = code + '\n(' + functionName + '$return_address' + str(self.callIndex) + ')\n'
        self.file.write(code)
        return
    
    def writeReturn(self):
        # 将LCL保存在临时变量R13
        code = '''
@LCL
D = M
@R13
M = D
'''
        # 将返回地址保存在临时变量R14
        code = code + '''
@5
A = D - A
D = M
@R14
M = D
'''
        # 重置调用者的返回值
        code = code + '''
@SP
AM = M - 1
D = M
@ARG
A = M
M = D
'''
        # 恢复调用者的SP
        code = code + '''
@ARG
D = M + 1
@SP
M = D
'''
        # 恢复调用者的THAT、THIS、ARG、LCL段指针
        for symbol in ['THAT', 'THIS', 'ARG', 'LCL']:
            code = code + '''
@R13
AM = M - 1
D = M
''' + '@' + symbol + '''
M = D
'''
        # 跳转到返回地址
        code = code + '''
@R14
A = M
0;JMP
'''
        self.file.write(code)
        return
    
    def writeFunction(self, functionName, numLocals):
        code = '\n(' + functionName + ')\n'
        self.file.write(code)
        for i in range(int(numLocals)): # 为numLocals个局部变量分配空间
            self.writePushPop('C_PUSH', 'constant', '0')
        return
    
    def close(self):
        self.file.close()
        return

