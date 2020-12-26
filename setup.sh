#!/bin/bash

# Confirm Python is 3.5+
python_ver_check() {
	echo checking for the correct version of Python . . .
	if ! python3 --version 2>&1 | grep -E "^(Python 3\.)(([5-9])|([1-9])([0-9]))"
	then	
		echo Make sure you are using Python version 3.5+	
		exit
	fi
}

python_ver_check

PACKAGES=(
    python3-tk			# tkinter
	poppler-utils		# pdf -> png
	texlive-latex-base	# latex things...
	texlive-latex-extra
	texlive-extra-utils
)

for item in ${PACKAGES[*]}
do
	apt install $item -y
done