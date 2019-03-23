x = open("zip5_to_CBSA.txt")
key = open("key.csv", "w")
dictionaire = {}

for line in x:
    linetemp = line.replace('"', '').replace('\n', '').split(',')

    if linetemp[1] not in dictionaire and linetemp[1] != '':
        dictionaire.update({linetemp[1]:linetemp[0]})
        key.write(linetemp[0] + "," + linetemp[1] + "\n")

x.close()
print(dictionaire)
key.close()

