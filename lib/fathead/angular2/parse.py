import requests
from bs4 import BeautifulSoup
import json

def encodeHtml(s):
	htmlCodes = (
		("'", '&#39;'),
		('"', '&quot;'),
		('>', '&gt;'),
		('<', '&lt;'),
		('&', '&amp;')
	)
	for code in htmlCodes:
		s = s.replace(code[1], code[0])
	print s
	return s

def htmlContentFormer(description, code1 = "None", code2 = "None"):
	mainContent = "<section class='prog__container'>"
	mainContent = mainContent + "<p>"
	mainContent = mainContent + description
	mainContent = mainContent + "</p>"
	if code1 != "None":
		mainContent = mainContent + "<pre><code>"
		mainContent = mainContent + code1
		mainContent = mainContent + "</pre></code>"
	if code2 != "None":
		mainContent = mainContent + "<pre><code>"
		mainContent = mainContent + code1
		mainContent = mainContent + "</pre></code>"
	mainContent = mainContent + "</section>"
	mainContent = mainContent.replace("\n", "\\n")
	return mainContent

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
			description = ""
			code = ""
			for row in rows:
				childRows = row.findAll("div")
				if childRows[0].text == "What it does":
					description = childRows[1].text 
				if childRows[0].text == "How to use":
					code = childRows[1].text
			return htmlContentFormer(description, code)
			
		if apiDocType == 'let':
			description = ""
			code = ""
			for row in rows:
				childRows = row.findAll("div")
				if childRows[0].text == "Variable Export":
					descriptionDiv = childRows[1]
			description = "\n".join([x.text for x in descriptionDiv.findAll("p")])
			code = descriptionDiv.find("code-example")
			if code:
				code = code.text
				return htmlContentFormer(description, code)
			else:
				return htmlContentFormer(description)
		
		if apiDocType == 'pipe':
			description = ""
			code = ""
			for row in rows:
				childRows = row.findAll("div")
				if childRows[0].text == "What it does":
					description = childRows[1].text
				if childRows[0].text == "Description":
					if childRows[1].find("p"):
						description = description + "\n" + childRows[1].find("p").text
				if childRows[0].text == "How to use":
					code = childRows[1].text
			return htmlContentFormer(description, code)
		
		if apiDocType == 'class':
			description = ""
			code = ""
			for row in rows:
				childRows = row.findAll("div")
				if childRows[0].text == "Class Description":
					descriptionDiv = childRows[1]
			description = "\n".join([x.text for x in descriptionDiv.findAll("p")])
			code = descriptionDiv.find("code-example")
			if code:
				code = code.text
				return htmlContentFormer(description, code)
			else:
				return htmlContentFormer(description)
		
		else:
			return "NONE"
		
	
	def output(self, apiName, apiDocType, parsedApiContent, apiPath):
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
			'',					#add an external link back to Home
			'',					#no disambiguation
			'',					#images
			parsedApiContent,	#abstract
			apiUrl				#url to the relevant tag doc
		]
		with open('output.txt', 'a') as output_file:
			output_file.write('{}\n'.format('\t'.join(outputList)))
	
	def parseBarrel(self, barrelName, barrelApiList):
		print barrelName
		for api in barrelApiList:
			print '-'+api['title']
			apiHtmlContent = self.fetchApiContent(api['title'], api['path'])
			parsedApiContent = self.parseApiContent(api['title'], api['docType'], apiHtmlContent)
			if parsedApiContent != "NONE":
				print api['title'], api['docType']
				self.output(api['title'], api['docType'], parsedApiContent, api['path'])
			

	def parse(self):
		parsedList = json.loads(self.API_LIST)
		for barrel in parsedList.keys():
			self.parseBarrel(barrel, parsedList[barrel])

if __name__ == "__main__":
	open('output.txt', 'w').close()
	parser = Parser()
	parser.parse()
# 	apiHtmlContent = parser.fetchApiContent("NgClass", "common/index/NgClass-directive.html")
# 	parsedApiContent = parser.parseApiContent("NgClass", "directive", apiHtmlContent)
# 	parser.output("NgClass", "directive", parsedApiContent, "common/index/NgClass-directive.html")
# 	apiHtmlContent = parser.fetchApiContent("APP_BASE_HREF", "common/index/APP_BASE_HREF-let.html")
# 	parsedApiContent = parser.parseApiContent("APP_BASE_HREF", "let", apiHtmlContent)
# 	parser.output("APP_BASE_HREF", "let", parsedApiContent, "common/index/APP_BASE_HREF-let.html")
# 	apiHtmlContent = parser.fetchApiContent("AsyncPipe", "common/index/AsyncPipe-pipe.html")
# 	parsedApiContent = parser.parseApiContent("AsyncPipe", "pipe", apiHtmlContent)
# 	parser.output("AsyncPipe", "pipe", parsedApiContent, "common/index/AsyncPipe-pipe.html")
# 	apiHtmlContent = parser.fetchApiContent("Location", "common/index/Location-class.html")
# 	parsedApiContent = parser.parseApiContent("Location", "class", apiHtmlContent)
# 	parser.output("Location", "class", parsedApiContent, "common/index/Location-class.html")
# 	print parsedApiContent