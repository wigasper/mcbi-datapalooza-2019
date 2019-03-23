x = open('output.txt', 'r')

y = open('zip_latlon.csv', 'r')

out = open('RRP_latlon.csv', 'w')

lista = []

for i in y:
   lista.append(i)

for line in x:
    for thing in lista:
        print(line + thing)
        if line.split(',')[0] == thing.split(',')[0]:
            out.write(line.replace('\n', '') + ',' + thing)
            break 

out.close()
