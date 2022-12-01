import re
from setuptools import setup, find_packages
from typing import List

#Declaring variables for setup functions
PROJECT_NAME = "creditcarddefault"
VERSION = "0.0.1"
AUTHOR = "Subramanya Chelmanda"
DESCRIPTION = "This is a machine learning project to predict credit card defaults"
REQUIREMENT_FILE_NAME = "requirements.txt"


def get_requirements_list()->List[str]:
    """
    Decsription: This function is going to return a list of 
    requirements mentioned in the requirements.txt file.

    Return: This function will return a list of libraries 
    from the requirements.txt file.
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = [lib_name.replace("\n","") for lib_name in requirement_file.readlines()]
        print(requirement_list)
        if "-e ." in requirement_list:
            requirement_list.remove('-e .')
        return requirement_list

setup(
name = PROJECT_NAME,
version = VERSION,
author = AUTHOR,
description = DESCRIPTION,
packages = find_packages(),
install_requires = get_requirements_list()
)