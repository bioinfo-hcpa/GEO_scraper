from bs4 import BeautifulSoup
import requests

#Input file
html_path = 'input/Data.html'
verbose = True	
output_name = 'output/Results.csv'

def getAccession(file):
	accessionCodes = []
	with open(file,'r') as texto:
		html_doc = texto
		soup = BeautifulSoup(html_doc,'lxml')
		lista = soup.find_all('dd')
		for value in lista:
			if '<dd>GSE' in str(value):
				accessionCodes.append(str(value).replace('<dd>','').replace('</dd>',''))
	return accessionCodes
'''
def check_for_problems():
	Solve this: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE214730	
'''

def experimentTyper(target):
	experiment = 'Two or more types'
	for line in target:
		if "<td>Expression profiling by MPSS<br></td>" in line:
			experiment="Expression profiling by MPSS"
		elif "<td>Expression profiling by RT-PCR<br></td>" in line:
			experiment="Expression profiling by RT-PCR"
		elif "<td>Expression profiling by SAGE<br></td>" in line:
			experiment="Expression profiling by SAGE"
		elif "<td>Expression profiling by SNP array<br></td>" in line:
			experiment="Expression profiling by SNP array"
		elif "<td>Expression profiling by array<br></td>" in line:
			experiment="Expression profiling by array"
		elif "<td>Expression profiling by genome tiling array<br></td>" in line:
			experiment="Expression profiling by genome tiling array"
		elif "<td>Expression profiling by high throughput sequencing<br></td>" in line:
			experiment="Expression profiling by high throughput sequencing"
		elif "<td>Genome binding/occupancy profiling by SNP array<br></td>" in line:
			experiment="Genome binding/occupancy profiling by SNP array"
		elif "<td>Genome binding/occupancy profiling by array<br></td>" in line:
			experiment="Genome binding/occupancy profiling by array"
		elif "<td>Genome binding/occupancy profiling by genome tiling array<br></td>" in line:
			experiment="Genome binding/occupancy profiling by genome tiling array"
		elif "<td>Genome binding/occupancy profiling by high throughput sequencing<br></td>" in line:
			experiment="Genome binding/occupancy profiling by high throughput sequencing"
		elif "<td>Genome variation profiling by SNP array<br></td>" in line:
			experiment="Genome variation profiling by SNP array"
		elif "<td>Genome variation profiling by array<br></td>" in line:
			experiment="Genome variation profiling by array"
		elif "<td>Genome variation profiling by genome tiling array<br></td>" in line:
			experiment="Genome variation profiling by genome tiling array"
		elif "<td>Genome variation profiling by high throughput sequencing<br></td>" in line:
			experiment="Genome variation profiling by high throughput sequencing"
		elif "<td>Methylation profiling by SNP array<br></td>" in line:
			experiment="Methylation profiling by SNP array"
		elif "<td>Methylation profiling by array<br></td>" in line:
			experiment="Methylation profiling by array"
		elif "<td>Methylation profiling by genome tiling array<br></td>" in line:
			experiment="Methylation profiling by genome tiling array"
		elif "<td>Methylation profiling by high throughput sequencing<br></td>" in line:
			experiment="Methylation profiling by high throughput sequencing"
		elif "<td>Non-coding RNA profiling by array<br></td>" in line:
			experiment="Non-coding RNA profiling by array"
		elif "<td>Non-coding RNA profiling by genome tiling array<br></td>" in line:
			experiment="Non-coding RNA profiling by genome tiling array"
		elif "<td>Non-coding RNA profiling by high throughput sequencing<br></td>" in line:
			experiment="Non-coding RNA profiling by high throughput sequencing"
		elif "<td>Other<br></td>" in line:
			experiment="Other"
		elif "<td>Protein profiling by Mass Spec<br></td>" in line:
			experiment="Protein profiling by Mass Spec"
		elif "<td>Protein profiling by protein array<br></td>" in line:
			experiment="Protein profiling by protein array"
		elif "<td>SNP genotyping by SNP array<br></td>" in line:
			experiment="SNP genotyping by SNP array"
		elif "<td>Third-party reanalysis<br></td>" in line:
			experiment="Third-party reanalysis"
	if verbose == True:
		print('Experiment type: ' + experiment)		
	return experiment

def platformFinder(target):
	last_line = False
	platform = "Not found"
	for line in target:
		if last_line == True:
			linha = line.replace('</a>',' ').replace('</td>',' ').replace('>',' ')
			linha = linha.split()
			platform = linha[-1]
			last_line = False
		if 'Platforms (' in line:
			last_line = True
	if verbose == True:
		print('Platform = ' + platform)
	return platform
	
def organismFinder(target):
	last_line = False
	organism = 'Two or more organisms'
	for line in target:
		if last_line == True:
			linha = line.replace('</a>',' ').replace('</td>',' ').replace('>',' ')
			linha = linha.split()
			organism = linha[-2] + ' ' + linha[-1]
			last_line = False
		if 'nowrap>Organism</' in line:
			last_line = True
	if verbose == True:
		print('Organism = ' + organism + '\n')
	return organism	


#Get accession codes from input file	
codes = getAccession(html_path)	
data_for_studies = {}

for code in codes:
	data_for_studies[code] = {}
	

#Parse html pages for accession codes	
n_studies = 0

		
for value in codes:
	if n_studies == 6:
		break
	geo_path = 'https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=' + value
	html_page = requests.get(geo_path)
	data_for_studies[value]['Link'] = geo_path	
	if html_page.status_code==200:
		html_content=html_page.text
		print('Parsing ' + value + '... \n')
		with open('page_html/Page.html','w',encoding='utf-8') as file:
			file.write(html_content)
		with open('page_html/Page.html','r') as texto:
			experiment = experimentTyper(texto) #Encontra o tipo de estudo
		data_for_studies[value]['Experiment_Type'] = experiment
		with open('page_html/Page.html','r') as texto:
			data_for_studies[value]['Platform'] = platformFinder(texto)
		with open('page_html/Page.html','r') as texto:
			data_for_studies[value]['Organism'] = organismFinder(texto)
		
		
		n_studies += 1
		print('Done: ' + value + ' (' + str(n_studies) + '/' + str(len(codes))+ ')\n---------')
	else:
		print(f'Failed to download HTML. Status code: {html_page.status_code}')
	
	
		
with open(output_name,'w') as texto:
	texto.write('Accession code , Link, Experiment Type , Platform , Organism \n')
	for key, value in data_for_studies.items():
		if 'Experiment_Type' in value.keys():
			texto.write(key + ' , ' + value['Link'] + ' , ' + value['Experiment_Type'] + ' , ' + value['Platform'] + ' , ' + value['Organism'] + '\n')
		
		
	
	
	
	
	
	
	
	
	
	
	
	
	
	
