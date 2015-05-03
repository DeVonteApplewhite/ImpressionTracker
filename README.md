# ImpressionTracker
This is a class project for CSE 40437

To run the Impression tracker, you will need python2.7.9
Example run: python2.7.9 listen.py [command line options]

usage listen.py options and arguments
Options -short (--long) [arguments] explanation
-c --company [name of company] company to track
-f --filename [name of file containing track words]
-g --graph [line/pie/all] which graph to create **OBSOLETE**
-i --interval [value in seconds] interval between data dumps
-h --help displays helpful information on options available
-t --track [word1 word2 ... wordN] list of words to track
-w --write writes tweets to a file named <company name>.txt

You must pass a company name and at least one word to track
in order for the listener to work. Upon each interval,
an html file will be generated and sent to your www space
for you to view in real-time. Another 'snapshot' version
of the file will be saved in your www space under a folder
named 'it' which will be organized by company, day, and
each file will be with the time you ran the listener.
