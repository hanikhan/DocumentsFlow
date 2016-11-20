# DocumentsFlow
Web app for managing the documents flows.

Year 2016/2017 UBB Computer Science Collective Project.

**Created in python 3 using Django Framework.**

Please refere to the **Wiki** page for more information.

# Contributors (ordered alphabetically):
  - Alex Damian: axl95
  - Eugen I. Meltis: meltiseugen
  - Florina A. Padurean: florinapadurean
  - Patricia Mazere: patriciamazere
  - Sorin Merca
  - Vlad M. Luca: vladluca
  
# Installation Steps:
  - clone project and change directory to it.
    - git clone https://github.com/meltiseugen/DocumentsFlow.git . && cd DocumentsFlow
  - install project dependecies
    - pip install -r requrements.txt
  - execute the migrations
    - python manager.py migrate
  - create the admin user (first check if you can log in with the admin credentials, if yes then skip this step)
    - python manager.py create superuser
  - start the service
    - python manager.py runserver (go to: \<the link displayed>/admin)
  

