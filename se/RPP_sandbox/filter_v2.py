import traceback
final = open("finalRRP.csv",'r')
key = open('key.csv', 'r')
output = open('output.txt', 'w')
keys = {}
for line in key:
    templine = line.replace('\n', '').split(',')
    keys.update({templine[1]: templine[0]})

for i in final:
    temp = i.split(',')
    try:
        output.write(keys[temp[0].strip('"')] + ', ' + temp[1])
    except KeyError:
        print(traceback.format_exc())
        continue

output.close()
