# Description of the task:

The scope of this APT is to create a dashboard aimed at harvesting
information from various sources and amalgamating it into one
cohesive view. The student is expected to perform the following
tasks:

## Harvesting Phase
1.  Create a scraper which regularly downloads top pages from
Google based upon specific search terms (which are provided in the
settings)
2.  Create a scraper capable of harvesting information from other
websites, online newspapers and others (which are provided in the
settings).
3.  Create a scraper capable of monitoring tweets of influential people
on twitter, or particular groups on Facebook. All these
will be set in the settings.

## Analysis
1.  Create a web interface which gives statistics on important topics
(identify the most important topics over time, look for emerging
topics, etc.)
2.  Allows the user to create a monitoring alert which creates a tab on
the webpage summarizing that topic, and when a particular topic
gets prominence, an email is sent to the use which gives a summary
of the findings.

The following are the steps taken to install all dependancies needed for the Dashboard, please follow each step line by line and in order.
This will create a venv folder 'IAPT_env', packages will be installed via 'requirements.txt' into this virtual enviroment and finally within this virtual enviroment the website can be loaded.
At the end a short breakdown of the file contents is provided.

# System Flow
The full process achieved by this IAPT is showcased
as a chart of the full breakdown of each step taken from harvesting
data, to Data Processing and showcasing the final results:

![image](https://github.com/kparnis3/IAPT/assets/81303628/bbbf16f5-c4e2-4dd4-b603-1aa10b93601a)

## Data Harvesting

When harvesting Data, a user can specify specific information to
receive and the quantity of how much information they wish to
receive. The following is a breakdown of each of the four different
data collectors and how they go about retrieving data.

### Twiiter API:

The user enters the specific information they would like to receive
prefixed by hashtag examples: #technology, #IT #Devops etc. and
the exact number of tweets they would like to receive. The full text
of the top x most recent tweets in their entirety are then received
followed by the links to the original tweets. When acquiring tweets,
retweets are filtered out to avoid the possibility of receiving
duplicate tweets and the tweets written in English are exclusively
harvested.

### Facebook API

Information is received uniquely from Facebook groups; thus, the
user would need to specify the name of the group (Private groups
cannot be accessed). The API functions by crawling between
different pages within the group (First two pages might not yield a
result) so an option for a specific page amount is given.


### News Articles API:

Newspaper allows several features for extracting information
from websites, this can be used both for article extracting as well
as general website extracting, the user would need to pass in a
specific URL to an article, then the API proceeds to attempt to
download every article found within the page and extract each
articles data.

### Google API

The user can request any search term from the internet and
depending on the size requested, the exact amount of googles top
search results URLs are first received, this is then synchronized
with the news article API to parse and extract all the relevant text
found within the URLs themselves.


## Data Cleaning

Once the data is collected in a raw format, cleaning would need to
take place to remove unwanted information that might lower the
quality of analysis. The following is the process the data goes
through for cleaning:

- Any links found within text are filtered out.
- #, @, $, ! symbols are removed.
- White spaces are removed.
- All the data is set to lower case.
- Stop words are removed.
- Individual words are broken down to their stem.

## Sentimental Analyses

The VADER model provided by NLTK was used to go through the
individual documents collected and give a ranking of Positivity /
Neutrality / Negativity. These scored are assessed out of a total of
a 100% split among these categories (Each are kept at two decimal
places)

## Topic Modelling

When it came to topic modelling a specific number of topics were
chosen beforehand, these are Topics A-H. This has been tested to
give the best generalization of topics as the dataset groups grow
larger. Before the Latent Dirichlet Allocation model could be used,
the cleaned data had to be transformed into the Vector Space
Model: TF IDF and after fitting this with LDA. Information such
as links and SA score are retained, and a summary of the original
text is achieved with Newspaper3k to give users better readability.
Finally, after the model has been fit, a sorting pass was taken on the
topics to maintain an alphabetical order of documents.

## Name Entity Recognition

The NER was used to count the number of times specific entities
such as People, Places and Brands appear within all the documents
present within a particular Topic. For each topic a sorted count of
was then displayed to the user along with the topics themselves. A
choice was taken to display the top five most mentioned entities
within each document to keep a balance of informative while not
presenting too much (if the dataset is smaller).

## Visualization
The Flask framework was used after all the prior individual
components were finalized within a Jupiter Notebook as a backend
to house all the major workings of the solution, this would allow
the user to make requests on the frontend (html), process this
request and achieve a result and then finally return the result back
to the frontend where the results would be shown in a presentable
way. The following is a breakdown of all the individual aspects
within the final dashboard.

### First Access

Upon first accessing the site one tab is shown that allows the user
to enter specific information for each of the four retrieval methods
{Twitter, Facebook, Article, Google} a user can simply choose to
allocate more input boxes to add more websites, hashtags, groups
etc. and upon doing so the user is able to press ‘add data’ which
starts the harvesting phase. 

### Data Collection

When the data is harvested a new tab appears below the dashboard
which presents all the data retrieved by the harvesters, these are in
the form of data | source link. The user is given a couple of options
to proceed: they can delete the data and attempt to retrieve other
types of data, they can go back and choose to continue to harvest 
more data, and this is added to the current data kept and finally,
once they decide that the data is sufficient, they can start the
processing stage. This will then proceed to add two new tabs which
showcase the different results present. 

### NER Results

The tab labelled ‘Mentioned Brands/People in particular topics’
presents all the topics A-H alongside the results of the named entity
recognizer. As already stated, these are the results from iterating
over each document within a topic and taking the top five most
mentioned entities.

### LDA and VADER Results

The final tab ‘Processed Results’ presents all the topics A-H with
the formulated keywords of the topic with the documents of their
respective categorization. Each document is presented in the form
{Text Summarization | Sentiment Score | Reference}. Finally,
below the last topic the user can choose to enter an email address
and all the processed data within this tab will then be sent to that
respective email address by the system. This processed is achieved
with the use of Flask’s mail feature.

# Folder Structure
- Python version used 3.10.5

## Installing virtual enviroments for packages
1)  Open a new cmd promt
2)  cd to 'ARI2201-Artifact-and-Report-Submission-Kian-Parnis-0107601L' folder
3)  enter 'python3 -m venv IAPT_env' in terminal
4)  Activate virtual enviroment from console with 'IAPT_env\Scripts\activate.bat'

## Installing packages from venv env
- In 'C:\Users\User\Desktop\ARI2201-Artifact-and-Report-Submission-Kian-Parnis-0107601L' with venv activated run:
1)  'cmd < requirements.txt'
1.1)  Small note, running this might sometimes pose an os error i.e. a particular package doesnt install successfully, in that case open 'requirements.txt' and manually install particular package ex: google doesn't install therefore write 'pip install google==3.0.0' into cmd
from console:
2)  write command 'python'
3)  write command 'import nltk'
4)  write command 'nltk.download('punkt')'
5)  write command 'quit()'

## Booting up Website
from venv:
1)  cd to 'Flask Server' folder
2)  write command 'set FLASK_APP=Flask.py'
3)  write command 'python -m flask run'
4)  finally, copy address given by the cmd and paste into google. (might need to wait a few seconds to recieve link)


## Breakdown of Flask Server
1)  Backend (python script) can be found 'Flask Server\Flask.py'
2)  'Flask Server\templates' contains HTML file
3)  'lask Server\static\styles' contains CSS file
