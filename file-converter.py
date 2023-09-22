import sys

# #の数に応じて見出しのHTML文を作成する関数
def createHTMLheading(num, content, counter):
    if num <= 5:
        return "<h" + str(num) + " id=\"h" + str(num) + "-" + str(counter) + "\">" + content + "</h" + str(num) +">\n"
    else:
        return content

if sys.argv[1] != "markdown":
    print("Invalid command.")
else:
    inputPath = sys.argv[2]
    outputPath = sys.argv[3]

    inFile = open(inputPath, 'r')
    outFile = open(outputPath, 'w')

    headingCounters = [0]*6
    isList = False
        
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

            htmlLine += "<li>" + content + "</li>\n"
        else:
            htmlLine += line

        outFile.write(htmlLine)

    # 読み取りファイルが最後に達している段階の処理
    # リストの終了処理
    htmlLine = ""

    if isList is True:
        htmlLine += "</ul>\n"
        isList = False

    outFile.write(htmlLine)

    inFile.close()
    outFile.close()
        
