#!/bin/sh

echo "Enter sensor directory.."
read Sensor
echo "Name the Edge.."
read Edge
echo "Running each sensor in , $Sensor"
echo "using , $Edge as Edge Node"

dirlist=$(find $Sensor -mindepth 1 -maxdepth 1 -type d)
#open -a Terminal "$Sensor/$Edge" 

for dir in $dirlist
do
	# try this for ubuntu instead of the osascrpit lines, this is something I had found but don't know if it works
	#gnome-terminal --window-with-profile=NAMEOFTHEPROFILE -e "cd '$dir'; python3 Node.py"
	osascript <<END 
		tell application "Terminal"
    	do script "cd \"`pwd`/$dir\"; python3 Node.py " 
    	#do script "python3 Node.py"
	end tell
END
  
done

#open -a Terminal "$Sensor/$Edge" 
cd "$Sensor"
cd "$Edge"
python3 Edge.py




