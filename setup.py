from setuptools import setup,find_packages
from typing import List


PROJECT_NAME="Creditcard_default_prediction"
DESCRIPTION="We will be finding whether a customer is creditcard defaulter or not"
AUTHOR="Ramesh Kumar"
VERSION="0.0.1"
REQUIREMENT_FILE_NAME="requirements.txt"
ALL_PACKAGES="-e ."
def get_requirements_list()->List[str]:
    """
    This function returns the list of modules required to run this project
    """
    with open(REQUIREMENT_FILE_NAME,'r') as requirements_list:
        requirements_list = requirements_list.readlines()
        requirements_list = [requirement.replace("\n","") for requirement in requirements_list]
        if ALL_PACKAGES in requirements_list:
            requirements_list.remove(ALL_PACKAGES)
        return requirements_list

        
        
setup(
name=PROJECT_NAME,
description=DESCRIPTION,
author=AUTHOR,
version=VERSION,
packages=find_packages(),
install_requires=get_requirements_list()
)