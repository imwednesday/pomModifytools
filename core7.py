# !/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
# 对函数进行优化,提取重复部分,待处理
# 增加对空行处理,提高可用性 √
# 可根据原标记长度自动截取,不限制原标记及新标记长度 √
# 如果修改3rd 优化修改在本模块的tab长度 √
# 删除模块时,将'-'改为':'
# 对文本内容非utf-8编码的文件,不支持


def getPath():
    global strTag
    strTag = input('请输入标记:')
    global f1path
    f1path = input('请输入地址:')

    # 将path路径下的所有文件名存入列表moduleDirList
    global moduleDirList
    moduleDirList = os.listdir(f1path)
    # 注释此处即可修改3rd版本,
    if 'thinkwin-3rd-parent' in moduleDirList:
        moduleDirList.remove('thinkwin-3rd-parent')
    # 将每个模块加上artifactId标签,以保证字符串对比准确
    global artifactIdList
    artifactIdList = []

    for k in moduleDirList:
        artifactIdList.append('<artifactId>' + k + '</artifactId>')


# 获取所有pom绝对路径 list
def getAbsPom(path):
    scpath = os.path.abspath(path)  # 获取目录的绝对路径,这是进行判断所必须的
    absPomList = []  # 将路径存储到list

    for fileName in moduleDirList:
        fileAbsName = os.path.join(scpath, fileName)  # 转换为路径
        if os.path.isdir(fileAbsName):  # 如果当前仍然是目录
            dirName = os.listdir(fileAbsName)  # 遍历目录 fileAbsName,我知道下一层就有pom
            for k in dirName:
                if (k == 'pom.xml'):  # 生成pom的绝对路径
                    absPomList.append(os.path.join(fileAbsName, k))

    return absPomList


# 获取模块与版本号对应dict
def getRightVersionStr(absPomList):
    versionDict = {}

    for fileAbsPom in absPomList:
        fread = open(fileAbsPom, 'r', encoding="utf-8")  # 读写方式打开
        print(fileAbsPom)
        lines = fread.readlines()  # 按行读取内容

        for moduleName in moduleDirList:
            if moduleName in fileAbsPom.split('\\'):  # 读取自身pom,获取版本号
                for index, line in enumerate(lines):
                    if '<artifactId>' + moduleName + '</artifactId>' in line:
                        # 可以在这里添加标记
                        k = ''.join(lines[index + 1].split())
                        if '-' in k:  # 区分对新增模块与已有模块的处理
                            # 如果是已有模块,已经有了标记,需判断标记的长度
                            versionL = len(k[:-10].split('-')[1])
                            version = k[:-(10 + versionL)] + strTag + '</version>'
                            versionDict[moduleName] = version  # 添加元素到dict
                        elif ':' in k:  # 删除模块准备
                            version = k.split(':')[0] + '</version>'
                            versionDict[moduleName] = version  # 添加元素到dict
                        else:
                            version = k[:-10] + '-' + strTag + '</version>'
                            versionDict[moduleName] = version  # 添加元素到dict

        fread.close()

    return versionDict


# 修改pom
def goEditPom(absPomList, versionDict):

    for fileAbsPom in absPomList:  # 依次修改pom
        pageListR = []
        fread = open(fileAbsPom, 'r', encoding="utf-8")  # 一个读

        lines = fread.readlines()  # 按行读取内容记录到list
        for currentLine in lines:
            pageListR.append(currentLine)
        fread.close()

        popIndexList = []  # 元素错行处理

        for index, line in enumerate(lines):
            if line.expandtabs().replace(' ', '') == '\n':
                popIndexList.append(index)
                print(fileAbsPom, ':', index + 1, '是空行,已删除!')
            elif line.split()[0] in artifactIdList:  # 如果是目标行,进行修改
                moduleName = line.split()[0][12:-13]  # 字符串截取模块名
                version = versionDict[moduleName]  # 根据dict取出版本号
                # 分情况修改指定行,即list内容
                if moduleName in fileAbsPom.split('\\'):  # 自身模块 处理
                    pageListR[index + 1] = '\t' + version + '\n'
                elif moduleName == 'thinkwin-3rd-parent' or moduleName == 'thinkwin-parent':
                    pageListR[index + 1] = '\t\t' + version + '\n'
                else:  # 依赖模块处理
                    pageListR[index + 1] = '\t\t\t' + version + '\n'

        for k in popIndexList:
            pageListR.pop(k - popIndexList.index(k))  # 元素错行处理

        fwrite = open(fileAbsPom, 'w', encoding="utf-8")  # 一个写
        for line in pageListR:
            fwrite.write(line)
        time.sleep(0.001)
        fwrite.close()


# 顺序执行
def doWorkPom():
    # 获取路径及标记
    getPath()
    # 获取所有pom绝对路径 list
    absPomList = getAbsPom(f1path)
    # 获取模块与版本号相互对应的dict
    versionDict = getRightVersionStr(absPomList)
    # 修改pom
    goEditPom(absPomList, versionDict)
    print('POM HAS MODIFY SUCCESSFULLY!')
    time.sleep(7)


doWorkPom()
