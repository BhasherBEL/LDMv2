import os

# inspired of https://stackoverflow.com/questions/44320329/converting-csv-to-html-table-in-python
def convert(path: str):
	if os.path.isfile(path) and path.endswith('.csv'):
		output_path = path.split('.csv')[0] + '.html'
		with open(path, 'r') as csv:
			with open(output_path, 'w') as html:
				html.write('<table>')
				html.write('<tr>')
				for el in csv.readline().split(','):
					html.write('<td>' + el + '</td>')
				html.write('</tr>')
				for line in csv.readlines():
					html.write('<tr>')
					for el in line.split(','):
						html.write('<td>' + el + '</td>')
				html.write('</tr>')
				html.write('</table>')

