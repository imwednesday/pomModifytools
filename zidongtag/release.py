#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   release.py
@Time    :   2019/10/31 17:21:05
@Author  :   imwednesday 
@Version :   1.0
'''

import os
import subprocess
import time


# 获取记录了模块路径的文本 path
def getPath():
    global txtPath
    # txtPath=input('请输入文本绝对路径')
    txtPath = "C:\\Users\\dell\\Desktop\\zidong\\Pdict.txt"
    global linesList
    linesList = fileRead(txtPath)
    global versionList
    versionList = []
    # 3.读取pom,删除其中的SNAPSHOT标记
    global absPomList
    absPomList = []  # 一个包含了所有需要执行MS命令的pom的绝对路径list
    for p in linesList:
        if p.strip() != "":
            p1 = os.path.dirname(p)  # 将字符串转换为路径
            dirName = os.listdir(p1)  # 下一层必然有pom,代码就是为了修改它
            for k in dirName:
                if (k == 'pom.xml'):  # 生成pom的绝对路径
                    absPomList.append(os.path.join(p1, k))


# 读文件方法
def fileRead(fileName):
    # 字符串消除空行
    # line=line.strip()
    fread = open(fileName, 'r', encoding="utf-8")  # 一个读
    lines = fread.readlines()  # 按行读取内容
    strSonar = fileName.split(".")[1]
    if strSonar == "properties":
        fread.close()
        return lines
    lines = popIndexList(lines)
    fread.close()
    return lines


# 写文件方法1
def fileWrite(fileName, lines):
    fwrite = open(fileName, 'w', encoding="utf-8")  # 一个写
    for line in lines:
        fwrite.write(line)
        time.sleep(0.001)
    time.sleep(0.1)
    fwrite.close()

# 写文件方法2
def fileWrite2(fileName, lines):
    fwrite2 = open(fileName, 'w', encoding="utf-8")  # 一个写
    for line in lines:
        fwrite2.write(line)
        time.sleep(0.001)
    time.sleep(0.1)
    fwrite2.close()


def fileWritea(fileName, strv):
    fwrite = open(fileName, 'a', encoding="utf-8")  # 追加写
    fwrite.write(strv)
    fwrite.close()


# 对应3rd和parent的tag,单独处理,这个循环只进行一次,此外还有一些需要单独处理的模块
def is3RD(lines, newPOM):
    for line in lines:
        # 先判断SNAPSHOT
        if 'SNAPSHOT' in line:
            i = lines.index(line)
            line = line.replace('-SNAPSHOT', '')
            del newPOM[i]
            newPOM.insert(i, line)
            break
    return newPOM


# 如果此次不包含3rd,则除本模块外,去掉pom中的SNAPSHOT
def isNot3RD(lines, newPOM):
    # 跳过前15行,这其中包含本模块的gav
    for line in newPOM[15:]:
        if 'SNAPSHOT' in line:
            i = newPOM.index(line)
            line = line.replace('-SNAPSHOT', '')
            del lines[i]
            lines.insert(i, line)
    return lines


# sonar文件的修改
def sonarEdit(lines):
    version = ""
    for index, line in enumerate(lines):
        if 'SNAPSHOT' in line:
            k = ''.join(lines[index].split())
            version = k[9:-19]
            v = (linesList[0][:-1].split("\\"))[-2] + '     ' + version + '\n'
            fileWritea("C:\\Users\\dell\\Desktop\\zidong\\Pversion.txt", v)
    # 为保证文件对应关系不出错,需要对txt文本进行修改,每完成一次MS就删除一行,txt的第一行必然是正在修改的pom
    sonaFile = os.path.join(linesList[0][:-1], "sonar-project.properties")
    sonarLines = fileRead(sonaFile)
    sonarLines[5] = sonarLines[5][:-6] + version + '\n'
    fileWrite2(sonaFile, sonarLines)


def mavenAndsvn(pomDir):
    p = os.path.dirname(pomDir)  # 将字符串转换为路径

    cdE = "E: && cd " + p
    addition = " && "
    mvn1 = "mvn release:prepare -Darguments=\"-DskipTests\""
    mvn2 = "mvn release:perform -Darguments=\"-Dmaven.javadoc.skip=true\""
    mvn3 = "mvn clean"
    svnUptade = "svn update"
    svnCommit = "svn ci -m " + "\"【问题单号】：无 【简要描述】：修改依赖版本号(CM493)\""
    str1 = cdE + addition + svnUptade + addition + "dir" + addition + mvn3
    str2 = cdE + addition + "dir" + addition + svnUptade + addition + svnCommit + addition + mvn1 + addition + mvn2 + addition + mvn3
    # shell=True的作用是接收字符串作为指令
    # p = subprocess.Popen(str1, shell=True)
    p = subprocess.call(str2, shell=True)
    # p.wait()


# 文件空行处理
def popIndexList(lines):
    newPOMindex = []
    for index, line in enumerate(lines):
        if line.expandtabs().replace(' ', '') == '\n':
            newPOMindex.append(index)
    newLines = []
    for line in lines:
        newLines.append(line)
    # 对pom的修改
    for k in newPOMindex:
        newLines.pop(k - newPOMindex.index(k))  # 元素错行处理
    return newLines


def doMS():
    # 如果本次模块包含3rd,需要先进行一次处理
    str3rd = input('本次是否包含3rd及parent模块,如果是请输入\'1\',如果不包含,请输入\'0\':')
    for pom in absPomList:
        lines = fileRead(pom)
        newPOM = []
        for line in lines:
            newPOM.append(line)
        if str3rd == '1':
            newPOM = is3RD(lines, newPOM)
        lines = isNot3RD(lines, newPOM)
        # 对两个list进行组合,得到最终结果
        lines = newPOM[:15] + lines[15:]
        # 对pom的修改
        fileWrite(pom, lines)
        time.sleep(0.1)
        # 对sonar文件的修改
        sonarEdit(lines)
        # 执行MS命令
        time.sleep(1)

        mavenAndsvn(linesList[0])
        # 对txt的修改
        del linesList[0]
        # del absPomList[0]
        fileWrite(txtPath, linesList)

        str1 = input("如果继续请输入\'1\',如果需要终止,请输入\'0\':")
        if str1 != '1':
            quit()


def zidong():
    # 获取记录了模块路径的文本 return path
    getPath()
    # 对pomlist循环处理,即执行mvn及svn相关命令
    doMS()


zidong()
