#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   depend.py
@Time    :   2019/11/14 14:56:13
@Author  :   imwednesday 
@Version :   1.0
'''
# 辅助完成依赖表
import os


# 获取所有pom绝对路径 list
def getAbsPom(path):
    scpath = os.path.abspath(path)  # 获取目录的绝对路径,这是进行判断所必须的
    absPomList = []  # 将路径存储到list

    for fileName in moduleDirList:
        fileAbsName = os.path.join(scpath, fileName)  # 转换为路径
        if os.path.isdir(fileAbsName):  # 如果当前仍然是目录
            dirName = os.listdir(fileAbsName)  # 下一层必然有pom,代码就是为了修改它
            for k in dirName:
                if (k == 'pom.xml'):  # 生成pom的绝对路径
                    absPomList.append(os.path.join(fileAbsName, k))
    return absPomList


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
    finally:
        fread.close()
    return lines


# 追加写
def fileWritea(fileName, strvList):
    fwrite = open(fileName, 'a', encoding="utf-8")  # 追加写
    for s in strvList:
        fwrite.write(s + '\n')
    fwrite.close()


# 获取需要的行
def getDependency(absPomList):
    dependencyList = []
    for fileAbsPom in absPomList:
        dependencyList1 = []
        dependencyList1.append(fileAbsPom)
        # 按行读取内容
        lines = fileRead(fileAbsPom)[12:]
        for index, line in enumerate(lines):
            if strTag in line:
                k = ''.join(lines[index - 1].split())
                moduleName = k[:-13].split('<artifactId>')[1]
                if moduleName not in dependencyList1:
                    dependencyList1.append(moduleName)
        dependencyList1.append(str(len(dependencyList1) - 1))
        fileWritea(f1path + "\\dependency.txt", dependencyList1)


def getPath():
    global strTag
    strTag = input('请输入标记:')
    global f1path
    f1path = input('请输入地址:')
    global moduleDirList
    moduleDirList = os.listdir(f1path)

    absPomList = getAbsPom(f1path)
    getDependency(absPomList)
    print("Congratulations")


getPath()