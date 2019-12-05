#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   getVersion.py
@Time    :   2019/12/04 10:19:35
@Author  :   imwednesday 
@Version :   1.0
'''
import os
import subprocess
import time


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


# 读取文件 获得模块名和版本号相互对应的dict
def getDict():
    dictV = {}
    txtPath = "C:\\Users\\dell\\Desktop\\zidong\\tags\\svncopy.txt"
    pomList = fileRead(txtPath)
    for k in pomList:
        pomk = k.strip() + "\\pom.xml"
        # 生成模块名 thinkwin-ETB
        moduleName = (k.strip().split("\\"))[-1]
        pomVersion = moduleName + getVersion(pomk)
        # 生成这样的字符串 source/thinkwin-cr/trunk/thinkwin-ETB
        moduleStr = k[3:].split()[0].replace("\\", "/")
        dictV[pomVersion] = moduleStr
    return dictV


def getVersion(pom):
    pversion = ""
    lines = fileRead(pom)
    for line in lines:
        if "SNAPSHOT" in line:
            pversion = line.strip()[9:-19]
            break
    pversions = pversion[0] + pversion[2] + pversion[4]
    if pversions == "100":
        return pversion
    pInt = int(pversions) - 1
    pStr = str(pInt)
    tagV = pStr[0] + "." + pStr[1] + "." + pStr[2]
    return tagV


# 根据模块和版本号,组合需要的tag地址,存入list
def tagStr(dictPom):
    tagDict = {}
    svnAddr = ""
    moduleName = ""
    for k in dictPom:
        svnAddr = "https://sv-svn2017.chavage.com/svn/maven/" + dictPom[
            k].replace("trunk", "tags") + "-" + k[-5:]
        moduleName = dictPom[k].split("/")[-1]
        tagDict[moduleName] = svnAddr
    fpath = "C:\\Users\\dell\\Desktop\\zidong\\tags\\P4.9.3tags.txt"
    with open(fpath, 'a+', encoding="utf-8") as fv:  # 写入
        for line in tagDict.values():
            fv.write(line + '\n')
    return tagDict


def main():
    dict = getDict()
    tagDict = tagStr(dict)


if __name__ == "__main__":
    main()