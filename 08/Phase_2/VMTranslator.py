#!/usr/bin/env python
# coding: utf-8

# In[1]:


import import_ipynb
import os.path
from Parser import Parser
from CodeWriter import CodeWriter


# In[2]:


def main(path):
    inDir = [] # 输入文件名列表
    outPath = '' # 输出文件名
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                if os.path.splitext(file)[1] == '.vm':
                    inDir.append(os.path.join(root , file))
        outPath = path + '/' + path.split('/')[-1] + '.asm'
    if os.path.isfile(path):
        inDir.append(path)
        outPath = path.replace('.vm', '.asm')

    fileOut = open(outPath, 'w')
    codeWriter = CodeWriter(fileOut)
    command = 'C_INIT'
    fileOut.write('\n// ' + command + '\n')
    codeWriter.writeInit()
    print(command)
    functionName = ''
    for inPath in inDir:
        fileIn = open(inPath, 'r')
        parser = Parser(fileIn)
        while(parser.hasMoreCommands()):
            parser.advance()
            if parser.commandType() == 'C_ARITHMETIC':
                command = parser.commandType() + ' ' + parser.arg1()
                fileOut.write('\n// ' + command + '\n')
                codeWriter.writeArithmetic(parser.arg1())
            if parser.commandType() == 'C_PUSH' or parser.commandType() == 'C_POP':
                offset = parser.arg2()
                if parser.arg1() == 'static': # 如果是静态变量
                    offset = inPath.split('/')[-1].split('.')[0] + '.' + parser.arg2()
                command = parser.commandType() + ' ' + parser.arg1() + ' ' + offset
                fileOut.write('\n// ' + command + '\n')
                codeWriter.writePushPop(parser.commandType(), parser.arg1(), offset)
            if parser.commandType() == 'C_LABEL':
                functionName_label = functionName + '$' + parser.arg1()
                command = parser.commandType() + ' ' + functionName_label
                fileOut.write('\n// ' + command + '\n')
                codeWriter.writeLabel(functionName_label)
            if parser.commandType() == 'C_GOTO':
                functionName_label = functionName + '$' + parser.arg1()
                command = parser.commandType() + ' ' + functionName_label
                fileOut.write('\n// ' + command + '\n')
                codeWriter.writeGoto(functionName_label)
            if parser.commandType() == 'C_IF':
                functionName_label = functionName + '$' + parser.arg1()
                command = parser.commandType() + ' ' + functionName_label
                fileOut.write('\n// ' + command + '\n')
                codeWriter.writeIf(functionName_label)
            if parser.commandType() == 'C_CALL':
                command = parser.commandType() + ' ' + parser.arg1() + ' ' + parser.arg2()
                fileOut.write('\n// ' + command + '\n')
                codeWriter.writeCall(parser.arg1(), parser.arg2())
            if parser.commandType() == 'C_FUNCTION':
                command = parser.commandType() + ' ' + parser.arg1() + ' ' + parser.arg2()
                fileOut.write('\n// ' + command + '\n')
                codeWriter.writeFunction(parser.arg1(), parser.arg2())
                functionName = parser.arg1()
            if parser.commandType() == 'C_RETURN':
                command = parser.commandType()
                fileOut.write('\n// ' + command + '\n')
                codeWriter.writeReturn()
            print(command)

    codeWriter.close()


# In[3]:


path = '/Users/ceshi/Desktop/计算机系统要素/nand2tetris/projects/08/FunctionCalls/NestedCall'
main(path)

