import sys
import re

# #の数に応じて見出しのHTML文を作成する関数
def createHTMLheading(num, content, counter):
    if num <= 5:
        return "<h" + str(num) + " id=\"h" + str(num) + "-" + str(counter) + "\">" + content + "</h" + str(num) +">\n"
    else:
        return content

if sys.argv[1] != "markdown":
    print("ERROR: Invalid command.")
else:
    inputPath = sys.argv[2]
    outputPath = sys.argv[3]

    inFile = open(inputPath, 'r')
    outFile = open(outputPath, 'w')

    headingCounters = [0]*6
    tableBuffer = ""
    isList = False
    isNumList = False
    isTable = False
        
    while True:
        # ファイルを一行ずつ読み込む
        line = inFile.readline()
        htmlLine = ""

        if not line:
            break

        # リストの終了処理
        if not (line[0] == "-" and line[1] == " "):
            if isList is True:
                htmlLine += "</ul>\n"
                isList = False

        # 番号付きリストの終了処理
        if not (line.find(".") > 0 and line[:line.find(".")].isdigit()):
            if isNumList is True:
                htmlLine += "</ol>\n"
                isNumList = False

        # テーブルの終了処理
        if line[1:-2].find("|") <= 0:
            if isTable is True:
                htmlLine += "</table>\n"
                isTable = False

        # 見出しの変換
        if line[0] == '#':
            spaceLoc = line.find(' ')
            header = line[0:spaceLoc]
            content = line[spaceLoc+1:-1]

            if header == "#":
                headerNum = 1
            elif header == "##":
                headerNum = 2
            elif header == "###":
                headerNum = 3
            elif header == "####":
                headerNum = 4
            elif header == "#####":
                headerNum = 5
            else:
                #見出しにならない場合を６でひと括り
                headerNum = 6

            htmlLine += createHTMLheading(headerNum, content, headingCounters[headerNum-1])
            headingCounters[headerNum-1] += 1
        # 水平線の変換
        elif line[:-1] == "---":
            htmlLine += "<hr />\n"
        # 太字の変換
        elif line[0:2] == "**" and line[-3:-1] == "**":
            content = line[2:-3]
            htmlLine += "<p><strong>" + content + "</strong></p>\n"
        # リストの変換
        elif line[0] == "-" and line[1] == " ":
            content = line[2:-1]
            if isList is False:
                htmlLine += "<ul>\n"
                isList = True

            htmlLine +=  " <li>" + content + "</li>\n"
        # 番号付きリストの変換
        # lineに"."が含まれており，それより前が自然数になっていること
        elif line.find(".") > 0 and line[:line.find(".")].isdigit():
            if isNumList is False:
                listNo = int(line[:line.find(".")])
                isNumList = True
                htmlLine += "<ol start = \"" + str(listNo) + "\">\n"

            content = line[line.find(".")+1:-1]
            htmlLine += " <li>" + content + "</li>\n"
            listNo += 1
        # テーブルの変換
        elif line[1:-2].find("|") > 0:
            if isTable is False:
                #テーブルのヘッダを内容を取得
                thContents = line[:-1].split("|")
                #ヘッダの種類数を取得
                numOfElem = len(thContents)

                subLine = inFile.readline() #tableのheaderの1行下を読み込む
                subThContents = subLine[:-1].split("|")

                pattern = re.compile(r"[^-]")
                isNotTableHeader = False

                for subContent in subThContents:
                    if pattern.search(subContent):
                        isNotTableHeader = True

                # tableのheaderの下の行に"|"が含まれない場合
                if subLine[:-2].find("|") < 1:
                    htmlLine += line
                    htmlLine += subLine
                # tableのheaderの下の行に"-"以外の文字が含まれる場合
                elif isNotTableHeader is True:
                    htmlLine += line
                    htmlLine += subLine
                #tableのheaderとして成立している場合
                else:
                    htmlLine += "<table>\n"
                    htmlLine += " <tr>\n"
                    for thContent in thContents:
                        htmlLine += "  <th>" + thContent + "</th>\n"
                    htmlLine += " </tr>\n"

                    isTable = True
            else:
                contentsCounter = 0 #列の数
                tdContents = line[:-1].split("|")
                htmlLine += " <tr>\n"

                for tdContent in tdContents:
                    if contentsCounter >= numOfElem:
                        break
                    htmlLine += "  <td>" + tdContent + "</td>\n"
                    contentsCounter += 1

                htmlLine += " </tr>\n"
        else:
            htmlLine += line

        outFile.write(htmlLine)

    # 読み取りファイルが最後に達している段階の処理
    # リストの終了処理
    htmlLine = ""

    if isList is True:
        htmlLine += "</ul>\n"
        isList = False

    if isNumList is True:
        htmlLine += "</ol>\n"
        isNumList = False

    if isTable is True:
        htmlLine += "</table>\n"
        isTable = False

    outFile.write(htmlLine)

    inFile.close()
    outFile.close()
        
