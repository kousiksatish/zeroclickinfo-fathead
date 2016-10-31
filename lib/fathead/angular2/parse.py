import requests
from bs4 import BeautifulSoup
import json

class Parser():
	API_BASE_URL = "https://angular.io/docs/ts/latest/api/"
	def __init__(self):
		self.API_LIST = ""
		with open('download/api-list.json', 'r') as data_file:
			self.API_LIST = data_file.read()
		

	def printSource(self):
		print self.API_LIST

	def fetchApiContent(self, apiName, apiPath):
		apiUrl = self.API_BASE_URL + apiPath
		fileName = apiPath.replace("/", ";")
		with open('download/'+fileName, 'r') as data_file:
			content = data_file.read()
		return content

	def parseApiContent(self, apiName, apiDocType, apiHtmlContent):
		apiSoup = BeautifulSoup(apiHtmlContent, 'html.parser')
		rows = apiSoup.findAll("div", {"layout": "row"})
		if apiDocType=='directive':
			mainContent = "<section class='prog__container'>"
			description = ""
			code = ""
			for row in rows:
				childRows = row.findAll("div")
				if childRows[0].text == "What it does":
					description = childRows[1].text 
				if childRows[0].text == "How to use":
					code = childRows[1].text
			print description, code
			mainContent = mainContent + "<p>"
			mainContent = mainContent + description
			mainContent = mainContent + "</p>"
			mainContent = mainContent + "<pre><code>"
			mainContent = mainContent + code
			mainContent = mainContent + "</pre></code></section>"
			mainContent = mainContent.replace("\n", "\\n")
			return mainContent
			
			
			
			
		if apiDocType == 'let':
			mainContent = "<section class='prog__container'>"
			description = ""
			code = ""
			for row in rows:
				childRows = row.findAll("div")
				if childRows[0].text == "Variable Export":
					descriptionDiv = childRows[1]
			description = "\n".join([x.text for x in descriptionDiv.findAll("p")])
			code = descriptionDiv.find("code-example").text
			mainContent = mainContent + "<p>"
			mainContent = mainContent + description
			mainContent = mainContent + "</p>"
			mainContent = mainContent + "<pre><code>"
			mainContent = mainContent + code
			mainContent = mainContent + "</pre></code></section>"
			mainContent = mainContent.replace("\n", "\\n")
			return mainContent
		
		
	
	def output(self, apiName, apiDocType, parserApiContent, apiPath):
		apiUrl = self.API_BASE_URL + apiPath
		outputList = [
			apiName,				#unique name
			'A',				#type is article
			'',					#no redirect data
			'',					#ignore
			'',					#no categories
			'',					#ignore
			'',					#no related topics
			'',					#ignore
			self.API_BASE_URL,		#add an external link back to BeautifulSoup Home
			'',					#no disambiguation
			'',					#images
			parsedApiContent,	#abstract
			apiUrl				#url to the relevant tag doc
		]
		with open('output.txt', 'w+') as output_file:
			output_file.write('{}\n'.format('\t'.join(outputList)))
	
	def parseBarrel(self, barrelName, barrelApiList):
		print barrelName
		for api in barrelApiList:
			print '-'+api['title']
			apiHtmlContent = self.fetchApiContent(api['title'], api['path'])
			parsedApiContent = self.parseApiContent(api['title'], api['docType'], apiHtmlContent)

	def parse(self):
		parsedList = json.loads(self.API_LIST)
		for barrel in parsedList.keys():
			self.parseBarrel(barrel, parsedList[barrel])

if __name__ == "__main__":
	parser = Parser()
	# parser.parse()'
# 	apiHtmlContent = parser.fetchApiContent("NgClass", "common/index/NgClass-directive.html")
# 	parsedApiContent = parser.parseApiContent("NgClass", "directive", apiHtmlContent)
# 	parser.output("NgClass", "directive", parsedApiContent, "common/index/NgClass-directive.html")
	apiHtmlContent = parser.fetchApiContent("APP_BASE_HREF", "common/index/APP_BASE_HREF-let.html")
	parsedApiContent = parser.parseApiContent("APP_BASE_HREF", "let", apiHtmlContent)
	print parsedApiContent
# 	parser.output("APP_BASE_HREF", "let", parsedApiContent, "common/index/APP_BASE_HREF-let.html")