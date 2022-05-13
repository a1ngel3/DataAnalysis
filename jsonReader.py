import json


def openJSON(fileName, writeFile):
    with open(fileName) as fp:
        with open(writeFile, 'w') as g:
            g.write("")
            with open(writeFile, 'a+') as f:
                jsonObject = json.load(fp)
                for i in jsonObject:
                    for x in i:
                        printingValues = list(x.values())
                        for item in printingValues:
                            f.write("%s; " % item)
                        f.write("\n")
        g.close()


openJSON("topData.json", 'top1Data.txt')
openJSON("jgData.json", 'jgData.txt')
openJSON("midData.json", "midData.txt")
openJSON("top2Data.json", "top2Data.txt")
openJSON("suppData.json", "suppData.txt")
openJSON("adcData.json", "adcData.txt")
