import os
import subprocess
import time

# 1.事先准备的tag文件目录,它是自己准备的,编码为uft-8
path1 = "C:\\Users\\dell\\Desktop\\CM491\\491.txt"

# f1path = input('请输入地址:')


# 读文件方法
def fileRead(fileName):
    fread = open(fileName, 'r', encoding="utf-8")  # 读
    lines = fread.readlines()  # 按行读取内容
    fread.close()
    return lines


# 2.读取txt文件,遍历lines
linesList = fileRead(path1)
absPomList = []
# 3.读取pom,删除其中的SNAPSHOT标记
for p in linesList:
    if p.strip() != "":
        # print(p)
        p1 = os.path.dirname(p)  # 将字符串转换为路径
        dirName = os.listdir(p1)  # 下一层必然有pom,代码就是为了修改它
        for k in dirName:
            if (k == 'pom.xml'):  # 生成pom的绝对路径
                absPomList.append(os.path.join(p1, k))

# 对应3rd和parent的tag,单独处理,此外还有一些需要单独处理的模块
for pom in absPomList:
    newPOM = []
    lines = fileRead(pom)
    # newPOM=lines
    for line in lines:
        newPOM.append(line)
    # 对lines处理两遍,第一遍单独处理3rd及parent
    for line in lines:
        # 先判断SNAPSHOT
        if 'SNAPSHOT' in line:
            i = lines.index(line)
            line = line.replace('-SNAPSHOT', '')
            del newPOM[i]
            newPOM.insert(i, line)
            break
    # 跳过前15行,这其中包含本模块的gav
    for line in newPOM[15:]:
        if 'SNAPSHOT' in line:
            i = newPOM.index(line)
            line = line.replace('-SNAPSHOT', '')
            del lines[i]
            lines.insert(i, line)
    # 对两个list进行组合,得到最终结果
    lines = newPOM[:15] + lines[15:]
    # 对pom的修改
    fwrite = open(pom, 'w', encoding="utf-8")  # 一个写
    for line in lines:
        fwrite.write(line)
    fwrite.close()
    # 3.执行一次命令,删除文本内及lines内一条目录(关键)
    mvn3 = "mvn clean"
    mvnT1 = "mvn package"
    # str2 = "E: && cd " + f1path + " && dir && " + mvnT1
    # p = subprocess.Popen(str2, shell=True)
    # p.wait()
    # 对sonar进行修改
    # moduleName=f1path.split("\\")[-1]
    for index, line in enumerate(lines):
        if 'TEST' in line:
            k = ''.join(lines[index].split())
            version = k[9:-15]
            # print(version)
    # 生成sonar文件路径
    sonaFile = os.path.join(linesList[0][:-1], "sonar-project.properties")
    # print(sonaFile)
    # print(os.path.isfile(sonaFile))
    fread = open(sonaFile, 'r', encoding="utf-8")  # 读
    sonarLinesBE = fread.readlines()
    fread.close()
    sonarLinesAF = []
    for line in sonarLinesBE:
        sonarLinesAF.append(line)
    sonarLinesAF[5] = sonarLinesAF[5][:-6] + version + '\n'
    fwrite = open(sonaFile, "w", encoding="utf-8")
    for line in sonarLinesAF:
        fwrite.write(line)
    fwrite.close()
    fread = open(sonaFile, 'r', encoding="utf-8")  # 读
    sonarLinesAF = fread.readlines()
    print(sonarLinesAF)
    time.sleep(100)
    # 对txt的修改
    fwrite = open(path1, "w", encoding="utf-8")
    del linesList[0]
    for line in linesList:
        fwrite.write(line)
    fwrite.close()
    str1 = input("如果继续请输入\"1\"")
    if str1 != 1:
        quit()

# 3.执行一次命令,删除文本内及lines内一条目录(关键)
