#!/bin/bash

# Line break function
lb() {
	for lines in $1
	do
		echo ""
	done
}

# Dev environment functions...
check_for_dir() {
	if [ -d "./venv" ]
	then
		echo the venv directory is present, make sure that its active before continuing
		lb 1 
		read -p "Press Enter to Continue. . ."
		lb 1 
	else
		echo no venv detected, creating one now 
		python3 -m venv ./venv 
		echo venv created, activate the script at /venv/bin/activate before running this script again
		exit
	fi
}

# Confirm Python is 3.5+
python_ver_check() {
	echo checking for the correct version of Python . . .
	if ! python3 --version 2>&1 | grep -E "^(Python 3\.)(([5-9])|([1-9])([0-9]))"
	then	
		echo Make sure the venv is using Python version 3.5+	
		exit
	fi
}

check_pip_packages() {
	echo making sure your python packages are up to date . . .

	pip install -r ./requirements.txt 
}

check_for_dir
python_ver_check
check_pip_packages

PACKAGES=(
    python3-tk			# tkinter
	poppler-utils		# pdf -> png
	texlive-latex-base	# latex things...
	texlive-latex-extra
	texlive-extra-utils
)