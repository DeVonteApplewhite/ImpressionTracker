#!/bin/bash
sed 's/<head>/<head>\n<meta http-equiv="refresh" content="20">/' $1 > $1_t
rm $1
mv $1_t ~/www/$1
