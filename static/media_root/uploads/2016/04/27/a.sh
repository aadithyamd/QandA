page="$(curl http://notepad.cc/qdsvsd)" #-f43-
dwlink="$(echo "$page" | grep "download http://" | cut -d " " -f2-)"
ddlink="$(echo "$page" | grep "downloaddir http://" | cut -d " " -f2-)"
echo $dwlink
echo $ddlink
if [ -n "$ddlink" ]
then echo "ddlink not empty"
#export https_proxy=http://mec:mec@192.168.0.4:3128
#export http_proxy=http://mec:mec@192.168.0.4:3128
#export ftp_proxy=http://mec:mec@192.168.0.4:3128
wget --header="Accept: text/html" --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0" -c -mirror -r -nH --cut-dirs=2 --no-parent -A "*720p.x265*" $ddlink
#axel -n 10 http://dl.fardadownload.ir/Serial/Banshee/S02
fi
if [ -n "$dwlink" ]
then echo "dwlink not empty"
fi
