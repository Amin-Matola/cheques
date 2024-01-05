from PIL import Image, ImageFilter
import os, re
import textract

class Imager:

	def __init__(self, file = ""):
		self.file = file
		self.home = "static"
		self.text = ""
		self.repl = [(" ", ""), (":", ""), ("\'", ""), ("\"", ""), (".", "")]
		self.info = []
		self.more = []
		self.cust = ""

		self.saveFile()
		self.readText()

	def getFilePath(self):
		return os.path.join(self.home, "checks", str(self.file))

	def saveFile(self, source = ""):

		if source:
			self.file = source

		fp 	= self.getFilePath()

		if not self.hasFile() or os.path.isfile(fp):
			return ""

		with open(fp, "wb") as d:
			for chunk in self.file.chunks():
				d.write(chunk)

		return str(self.file)

	def process(self):
		if not self.hasFile():
			return

		# image = Image.open(self.getFilePath())
		# blur = image.filter(ImageFilter.GaussianBlur)

		# image.paste(blur, (0, 0))
		# image.save("output.png")

	def readText(self):
		if not len(self.text.strip()):
			self.text = textract.process(
				self.getFilePath(),
				method='tesseract',
			    language='eng',
			    ).decode("utf-8")

		self.replaceAll()
		#print(self.text)

		return self.text

	def readLines(self):
		
		text = self.readText()

		lines = text.splitlines()
		

		return lines

	def replaceAll(self):
		replacer = re.findall(r"(\w+)\s?_", self.text)
		open("o.txt", "w").write(self.text)

		# for i in replacer:
		# 	#print(i)
		# 	if (len(i.strip("_"))):
		# 		self.text = self.text.replace(i.strip("_"), "%s:" % i.strip("_"))



	def jsonify( self, lines = [] ):

		self.info.clear()

		if not len(lines):
			lines = self.readLines()

		for line in lines[1:]:

			line = line.replace(r"\w+\S?_", ":")
				
			if line.__contains__("DOLLARS"):
				line = "DOLLARS: " + line.strip("DOLLARS")
			if line.__contains__("MEMO"):
				line = line.replace("MEMO", "MEMO:")

			if self.isnum(line):

				line = self.replace(line, [("\"", ""), (":", " "), (".", ""), (" ", ":")])

				inner = "ROUTING NUMBER:%s\nACCOUNT NUMBER: %s\nCHECK NUMBER: %s" % tuple(line.split(":")[:3])

				inner = inner.splitlines()
				if len(inner) > 1:
					for l in inner:
						self.processLine(l)
					continue

				
			if line.__contains__('$') or line.__contains__("DATE:"):

				inner = line.replace("$", "\nAMOUNT:").replace("DATE:", "\nDATE:").splitlines()

				if len(inner) > 1:
					for l in inner:
						self.processLine(l)
					continue

			self.processLine(line)

		self.info.append({"key": "Customer Details", "value": self.cust.strip(",")})
		return self.info

	def isnum(self, line, repl = []):
		return self.replace(line, repl).isnumeric()

	def processLine(self, line):
		json = {}
		data = line.split(":")

		if len(data) > 1:
			try:
				_key  = data[0].strip("_")
				val   = data[1].strip("_")
				json = {"key": _key, "value": val}
			except:
				pass

		if len(json) > 1:
			self.info.append(json)
		elif len(data) == 1:
			if len(self.info) < 1:
				self.cust += line + ","
			else:
				self.more.append(line)
		return json

	def getTitle(self):
		return self.readLines()[0]

	def replace(self, text, repl = []):

		if not len(repl):
			repl = self.repl

		[text := text.replace(a, b) for a, b in repl]

		return text

	def hasFile(self):
		return self.file
