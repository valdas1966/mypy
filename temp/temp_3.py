html = 'd:\\temp\\temp.html'

file = open(html, 'w')
file.write(f'<html>\n')
file.write(f'\t<body>\n')
for i in range(1000):
    file.write(f'\t\t<p> {i} </p>\n')
file.write(f'\t</body>\n')
file.write(f'</html>\n')
file.close()
