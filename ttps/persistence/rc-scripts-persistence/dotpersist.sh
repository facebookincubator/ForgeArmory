#!/bin/bash
# Check if the number of arguments is equal to 1

if [ "$#" -ne 1 ]; then
 echo "One input arguments required:"
 echo "1: Type of RC SHELL configuration files through which persistence needs to be established."
 exit 1
fi

# modify the RC file based on type of given argument.
if [ ! -f ~/.$1 ]; then
 echo -e "\nNo ~/.$1 file found so creating an empty file\n"
 touch ~/.$1
else
 echo -e "\nValid ~/.$1 file found. Creating a backup copy of it and making a new one. \n"
 mv ~/.$1 ~/.$1.tmp
 touch ~/.$1
fi

# Add a persistence command to RC dotfiles
echo -e "#!/bin/bash\nuname -a > /tmp/system-info.txt" > ~/.$1

# Reload the SHELL configuration and display the output of command executed
source ~/.$1
cat /tmp/system-info.txt
