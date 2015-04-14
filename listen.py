#/afs/nd.edu/user14/csesoft/new/bin/python
from tweepy import StreamListener
import json, time, sys, os
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
from mood import mood

class parser():
	def __init__(self):
		self.track_array = []
		self.run_mode = None

		self.interval = None
	def help():
		print "usage listen.py options and arguments"
		print "Options (short/long if available) [arguments] and explanations"
		print "-f --filename [name of file containing track words]"
		print "-i --interval [value in seconds] interval between data dumps"
		print "-h --help displays helpful information on options available"
		print "-p --print prints out tweets to STDOUT"
		print "\t(if this option is passed, -w or --web cannot used)"
		print "-t --track [word1 word2 ... wordN] list of words to track"
		print "-w --web processes tweets and sends results to html files"

	def parse_args(self):
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
			elif item == '-p' or item == '--print':
				if self.run_mode == 'w': #asked for both w and p
					print "Cannot operate in both web and print mode"
					return 0
				self.run_mode = 'p' #set for print mode
				print "set to print"
			elif item == '-t' or item == '--track':
				mode = '-t'
			elif item == '-w' or item == '--web':
				if self.run_mode == 'p': #asked for both w and p
					print "Cannot operate in both web and print mode"
					return 0
				self.run_mode = 'w' #set for web mode
				print "set to web"
			else: #process based on modes
				if mode == '-f':
					f = open(item)
					for line in f:
						self.track_array.append(line.rstrip()) #add word to tracker
					atleastoneword = 1
				elif mode == '-i':
					self.interval = int(item) #set interval
					print "set interval"
				elif mode == '-t':
					self.track_array.append(item.rstrip())
					atleastoneword = 1
				else:
					print "Unexpected input"
					self.help()
					return 0

		if atleastoneword == 1:
			return 1
		else: #no words were passed
			print "No words were passed in to listen for"
			return 0

class CustomStreamListener(tweepy.StreamListener): #listens for incomming tweets
	def __init__(self,mode=None,interval=None):
		super(CustomStreamListener, self).__init__()
		self.count = 0 #count tweet

		self.mode = None
		if mode != None:
			self.mode = mode

		self.impression = None
		if interval != None:
			self.impression = mood(interval)
		else:
			self.impression = mood(20)

		self.impression.load('positive-words.txt','negative-words.txt')

	def on_data(self, data):
		outString = data.encode('utf-8')

		if self.mode == 'w': #want to process data internally
			result = self.impression.add(outString)

			if result == 1: #show dumped data
				self.impression.linegraph('Apple',"appleline",1)
				os.system("./putinwww.sh appleline.html")
				print "OUT"

		else: #want to print data (None or p fall under this case)
			print outString.rstrip()
		
		return True

	def on_error(self, status_code):
		print >> sys.stderr, 'Encountered error with status code:', status_code
		return True # Don't kill the stream
	def on_timeout(self):
		print >> sys.stderr, 'Timeout...'
		return True # Don't kill the stream

if __name__ == "__main__":
	p = parser()
	ret = p.parse_args()
	if ret == 0:
		exit(1)

	print p.run_mode
	print p.interval
	auth = tweepy.OAuthHandler("StBTJPvpNnlb7jxO7joCwt0GZ",
	"8M3ReVr2Knkmdci1zBGtfM4NUsLJH2NvQJbWorGRNg0o64rJfT")
	auth.set_access_token("3008646015-2ae2vykbLAT65ceJueytFDVkFaoOHjbmv8gELw6",
	"88sNWTJSx0VnSmEKeeJk1s2zJd1kB8VVB4NBSFkvpaHDO")
	api = tweepy.API(auth)
	sapi = tweepy.streaming.Stream(auth, CustomStreamListener(p.run_mode,p.interval))

	sapi.filter(track=p.track_array)
	#sapi.filter(track=['Walmart', 'Sam''s Club', 'Sams Club', 'rollback', 'roll-back'])