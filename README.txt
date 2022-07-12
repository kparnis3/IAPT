The following are the steps taken to install all dependancies needed for the Dashboard, please follow each step line by line and in order.
This will create a venv folder 'IAPT_env', packages will be installed via 'requirements.txt' into this virtual enviroment and finally within this virtual enviroment the website can be loaded.
At the end a short breakdown of the file contents is provided.

------ Python version used ------
3.10.5

------ Installing virtual enviroments for packages ------
1) Open a new cmd promt
2) cd to 'ARI2201-Artifact-and-Report-Submission-Kian-Parnis-0107601L' folder
3) enter 'python3 -m venv IAPT_env' in terminal
4) Activate virtual enviroment from console with 'IAPT_env\Scripts\activate.bat'

------ Installing packages from venv env ------
In 'C:\Users\User\Desktop\ARI2201-Artifact-and-Report-Submission-Kian-Parnis-0107601L' with venv activated run:
1) 'cmd < requirements.txt'
1.1) Small note, running this might sometimes pose an os error i.e. a particular package doesnt install successfully, in that case open 'requirements.txt' and manually install particular package ex: google doesn't install therefore write 'pip install google==3.0.0' into cmd
from console:
2) write command 'python'
3) write command 'import nltk'
4) write command 'nltk.download('punkt')'
5) write command 'quit()'

------ Booting up Website ------
from venv:
1) cd to 'Flask Server' folder
2) write command 'set FLASK_APP=Flask.py'
3) write command 'python -m flask run'
4) finally, copy address given by the cmd and paste into google. (might need to wait a few seconds to recieve link)


------ Breakdown of Flask Server ------
1) Backend (python script) can be found 'Flask Server\Flask.py'
2) 'Flask Server\templates' contains HTML file
3) 'lask Server\static\styles' contains CSS file