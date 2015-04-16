#!/afs/nd.edu/user14/csesoft/new/bin/python
import os,sys

#arguments: html_file,refresh_rate

if len(sys.argv) != 3:
	print "usage: %s <html_file_name> <refresh_rate>"%(sys.argv[0])
	exit(1)

f = sys.argv[1] #file name
ft = sys.argv[1] + "_t" #temporary file name
r = sys.argv[2] #refresh rate

#sed 's/<head>/<head>\n<meta http-equiv="refresh" content="20">/' $1 > $1_t
sedcmd = "sed 's/<head>/<head>\\n<meta http-equiv=\"refresh\""\
+" content=\""+r+"\">/' "+f+" > "+ft

os.system(sedcmd) #replace the head with a head and meta refresh tag
os.system("rm "+f) #remove file
os.system("mv "+ft+" ~/www/"+f)
