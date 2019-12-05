#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   svnCP.py
@Time    :   2019/12/03 08:52:36
@Author  :   imwednesday 
@Version :   1.1
'''

import os
import subprocess
import time
"""
dict的key是唯一的.不能有重复,不然会覆盖上一个value
"""


# 读文件方法
def fileRead(fileName):
    fread = open(fileName, 'r', encoding="utf-8")  # 读
    lines = ''
    try:
        lines = fread.readlines()  # 按行读取内容
    except UnicodeDecodeError:
        logName = f1path + '\\' + 'e.log'
        with open(logName, 'a+', encoding="utf-8") as fwlog:  # 追加
            fwlog.write(fileName + '不是uft-8编码' + '\n')
            fwlog.close()
    finally:
        fread.close()
    return lines


# 生成模块名和tag地址对应
def tagStr():
    tagDict = {}
    moduleName = ""
    fpath = "C:\\Users\\dell\\Desktop\\zidong\\tags\\P4.9.3tags.txt"
    lines = fileRead(fpath)
    for line in lines:
        moduleName = line.strip().split("/")[-1][:-6]
        tagDict[moduleName] = line
    return tagDict


# 将添加模块的svn地址和模块tag地址对应
def svnStr(tagDict):
    moduleDict = {}
    svnDict = {}
    branchAddr = input("请输入分支地址:")
    txtPath = "C:\\Users\\dell\\Desktop\\zidong\\Psvnadd.txt"
    lines = fileRead(txtPath)
    for line in lines:
        moduleAdd = line.strip()
        moduleDict[moduleAdd] = branchAddr + "/" + moduleAdd
    # 组合需要的dict
    for k in moduleDict:
        if k in tagDict:
            svnDict[tagDict[k]] = moduleDict.get(k)
    return svnDict


# 执行svn copy命令
def svnCopy(svnDict):
    svnCPstrList = []
    logStr = input("分支用途:")
    svnLog = " -m \"【分支类型】：开发分支【分支用途】：" + logStr.strip() + "\""
    for k in svnDict:
        svnCPstrList.append("svn cp " + k.strip() + "  " + svnDict[k] + svnLog)
    for svnCPstr in svnCPstrList:
        print(svnCPstr)
        # shell=True的作用是接收字符串作为指令
        p = subprocess.call(svnCPstr, shell=True)


def main():
    tagDict = tagStr()
    svnDict = svnStr(tagDict)
    svnCopy(svnDict)


if __name__ == "__main__":
    main()