#/afs/nd.edu/user14/csesoft/new/bin/python
from tweepy import StreamListener
import json, time, sys, os, pwd
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import datetime
from mood import mood

class parser():
	def __init__(self):
		self.track_array = []
		self.do_write = None
		self.interval = None
		self.company = None
		self.graph = None

	def help(self):
		print "usage listen.py options and arguments"
		print "Options -short (--long) [arguments] explanation"
		print "-c --company [name of company] company to track"
		print "-f --filename [name of file containing track words]"
		print "-g --graph [line/pie/all] which graph to create **OBSOLETE**"
		print "-i --interval [value in seconds] interval between data dumps"
		print "-h --help displays helpful information on options available"
		print "-t --track [word1 word2 ... wordN] list of words to track"
		print "-w --write writes tweets to a file named <company name>.txt"

	def parse_args(self):
		if len(sys.argv) == 1: #gave no arguments
			self.help()
			return 0

		optargs = sys.argv[1:] #get arguments to program
		mode = None
		atleastoneword = 0 #checks that at least one word is passed

		for item in optargs:
			if item == '-f' or item == '--filename':
				mode = '-f'
			elif item == '-i' or item == '--interval':
				mode = '-i'
			elif item == '-h' or item == '--help':
				self.help()
			elif item == '-t' or item == '--track':
				mode = '-t'
			elif item == '-w' or item == '--write':
				self.do_write = 1 #set for web mode
			elif item == '-c' or item == '--company': #adding company name
				mode = '-c'
			elif item == '-g' or item == '--graph': #asking for graph feature
				mode = '-g'
			else: #process based on modes
				if mode == '-f':
					try:
						f = open(item)
					except IOError:
						print "No such file %s"%(item)
						return 0
					for line in f:
						self.track_array.append(line.rstrip()) #add word to tracker
					atleastoneword = 1
				elif mode == '-i':
					self.interval = int(item) #set interval
				elif mode == '-t':
					self.track_array.append(item.rstrip())
					atleastoneword = 1
				elif mode == '-c':
					self.company = item.rstrip()
				elif mode == '-g':
					self.graph = item.rstrip()
				else:
					print "Unexpected input"
					self.help()
					return 0

		if atleastoneword == 0:
			print "No words were passed in to listen for"
			return 0
		if self.company == None:
			print "No company name was passed to track"
			return 0

		return 1 #everything went well

class CustomStreamListener(tweepy.StreamListener): #listens for incomming tweets
	def __init__(self,myparser=None):
		super(CustomStreamListener, self).__init__()

		p = myparser
		self.count = 0 #count tweet
		self.do_write = None
		self.impression = None
		self.companyname = None
		self.companynameforfile = None #when formatting for files
		self.graph = None
		self.username = pwd.getpwuid(os.getuid()).pw_name
		self.url = "http://www.cse.nd.edu/~"+self.username+"/"
		self.mainpath = os.getcwd()
		self.path = os.path.expanduser("~/") #os.path.expanduser() expands ~ if needed
		self.path += "/www/"
		self.db = "it"
		self.dbpath = self.path + self.db
		self.date = datetime.datetime.now().strftime("%Y-%m-%d") #get current date
		self.time = datetime.datetime.now().strftime("%H:%M:%S") #get current time
		self.filepath = None
		self.f = None #used to write to the file containing company tweets

		if p != None: #valid parser object
			if p.do_write != None: #automatically true if != None
				self.do_write = 1 #the value of p.do_write doesn't matter
			if p.interval != None:
				self.impression = mood(p.interval)
			else:
				self.impression = mood(20)

			if p.company != None:
				self.companyname = p.company

			if p.graph != None:
				self.graph = p.graph

		self.impression.load('text_files/positive-words.txt','text_files/negative-words.txt')

		self.setup() #self.path will be ~/www/it/company_name and self.filepath will be updated
		if self.do_write == 1: #open file for writing tweets
			self.f = open(self.filepath+self.companyname+".txt","a") #append mode

		print "Database Link:\n%s"%(self.url+self.db)

	def on_data(self, data):
		outString = data.encode('utf-8')

		result = self.impression.add(outString)
		if result == 1: #show dumped data
			if self.graph == None or 1: #TODO: Change if other graphs exist
				self.companynameforfile = self.companyname.lower()+"_graph.html"
				self.impression.graph(self.companyname,self.companynameforfile) #show second line
				self.put("graph")
				print self.url+self.companynameforfile

		if self.do_write == 1: #want to print data
			self.f.write(outString) #check if it has newlines in it (if not, add \n)
		
		return True

	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream
	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True # Don't kill the stream

	def setup(self): #checks for the database and company name dir and creates them if needed
		if not os.path.exists(self.dbpath):
			os.mkdir(self.dbpath)
		else: #path exists, ensure it is a directory
			if not os.path.isdir(self.dbpath): #not a directory
				os.system("rm "+self.dbpath) #remove it and make it a directory
				os.mkdir(self.dbpath)

		self.filepath = self.dbpath+"/"+self.companyname #~/www/it/company_name
		if not os.path.exists(self.filepath):
			os.mkdir(self.filepath)
		else: #path exists, ensure it is a directory
			if not os.path.isdir(self.filepath): #not a directory
				os.system("rm "+self.filepath) #remove it and make it a directory
				os.mkdir(self.filepath)

		self.filepath += "/"+self.date #company_name/date
		if not os.path.exists(self.filepath):
			os.mkdir(self.filepath)
		else: #path exists, ensure it is a directory
			if not os.path.isdir(self.filepath): #not a directory
				os.system("rm "+self.filepath) #remove it and make it a directory
				os.mkdir(self.filepath)

		self.filepath += "/" #the path to make the file on each interval

	def put(self,graphstr):
		f = self.companynameforfile #file name
		ft = f + "_t" #temporary file name
		dbf = self.time+"_"+graphstr+".html" #file to go in database
		r = str(p.interval)
		os.system("cp "+f+" "+dbf) #copy file to put in database later

		#sed 's/<head>/<head>\n<meta http-equiv="refresh" content="20">/' $1 > $1_t
		sedcmd = "sed 's/<head>/<head>\\n<meta http-equiv=\"refresh\""\
		+" content=\""+r+"\">/' "+f+" > "+ft

		os.system(sedcmd) #replace the head with a head and meta refresh tag
		os.system("rm "+f) #remove file
		os.system("mv "+ft+" "+self.path+"/"+f)
		os.system("mv "+dbf+" "+self.filepath+dbf)

if __name__ == "__main__":
	p = parser()
	ret = p.parse_args()
	if ret == 0:
		exit(1)

	auth = tweepy.OAuthHandler("StBTJPvpNnlb7jxO7joCwt0GZ",
	"8M3ReVr2Knkmdci1zBGtfM4NUsLJH2NvQJbWorGRNg0o64rJfT")
	auth.set_access_token("3008646015-2ae2vykbLAT65ceJueytFDVkFaoOHjbmv8gELw6",
	"88sNWTJSx0VnSmEKeeJk1s2zJd1kB8VVB4NBSFkvpaHDO")
	api = tweepy.API(auth)

	sapi = tweepy.streaming.Stream(auth, CustomStreamListener(p))
	sapi.filter(track=p.track_array)
