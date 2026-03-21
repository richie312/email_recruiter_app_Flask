## Prepare the indepth analysis and make wiki book and push it to the branch using the following steps mentioned in Initial steps, read the repo structure and overall architecture.

## Initial Steps
    1. Please create another branch feature/architecture_wiki_books.
    2. Please check out to the feature/architecture_wiki_books.
    3. Make another folder and name it wiki_books or appropriate name.

## Read the repo structure
    1. Read the architecture of main.py wrt src,config, data and templates folder.
    2. noTify is simple interface which has following functionalities
        * List of jobs applied  # find out the correct api.
        * interface to apply for a specific job, it takes the default resume and email template which is sent to the recruiters
    3. there are two other helper scraper remotejob_agent and scrape_emails_jobs.py which push the jobs from online and candidate's email to existing kafka producer which is running as a separate microservice in same docker network.
    4. there is pythonresumebuilder module which helps you to make automated resume with different layouts. There is a json file resume.json which has the candidate's data.

## Overall architecture
1. Kafka Microservice is running as a separate microservice
2. MySql database is running as a separate microservice.
3. Redis is also running as microservice, to render the data repeatedly to the same consume, this act as a middle interface between notify application and kafka consumer.
4. The job data is ingested to my sql via two routes. one applying through manual entry via form post. Another route is through automated radiobutton selection from jobliast dashboard.