import requests
from bs4 import BeautifulSoup
import urllib
import json

class Parser():
	API_BASE_URL = "https://angular.io/docs/ts/latest/api/"

	def __init__(self):
		self.API_LIST = ""
		with open('download/api-list.json', 'r') as data_file:
			self.API_LIST = data_file.read()

	def fetchApiHtml(self, apiName, apiPath):
		apiUrl = self.API_BASE_URL + apiPath
		# print apiUrl
		fileName = apiPath
		fileName = fileName.replace("/", ";")
		urllib.urlretrieve(apiUrl, "download/" + fileName)
		print 'Successfully saved ' + fileName

	def parseBarrel(self, barrelName, barrelApiList):
		print barrelName
		for api in barrelApiList:
			print '-'+api['title']
			self.fetchApiHtml(api['title'], api['path'])

	def parse(self):
		parsedList = json.loads(self.API_LIST)
		for barrel in parsedList.keys():
			self.parseBarrel(barrel, parsedList[barrel])

if __name__ == "__main__":
	parser = Parser()
	parser.parse()