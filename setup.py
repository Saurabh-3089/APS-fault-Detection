#This file is created so that we can use our code afterwards like a "library"
#If in any folder __init__.py is found then it is considered as package eg. in setup folder

from setuptools import find_packages,setup
from typing import List

REQUIREMENT_FILE_NAME="requirements.txt"
HYPHEN_E_DOT="-e .p"
def get_requirements()->List[str]:
    with open(REQUIREMENT_FILE_NAME) as requirement_files:
        requirement_list = requirement_files.readlines()
        requirement_list = [requirement_name.replace("\n","") for requirement_name in requirement_list]

    if HYPHEN_E_DOT in requirement_list:
        requirement_list.remove(HYPHEN_E_DOT)
    return requirement_list



setup(
    name="sensor",
    version="0.0.1",
    author="saurabh_chauhan",
    author_email="saurabhchauhan1089@gmail.com",
    packages = find_packages(),
    install_requirements=get_requirements(),

)


 
 