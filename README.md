# No Longer Maintained
This library is no longer maintained and has been moved to a more comprehensive [python library here](https://github.com/calebjcourtney/EmsiApiPy)

# Emsi Open Skills
A python library for accessing Emsi's open skills library. Read here for more info on the open skills library: https://skills.emsidata.com/

Emsi has open-sourced their skills classification, but it comes with its own terms of use, which you can find here: https://skills.emsidata.com/emsi-open-skills-license-agreement.pdf

Please note that this is an unofficial repository and not maintained by Emsi. It is provided as-is.

# Usage
All of the scripts have been tested with python 3.7.3

Libraries were installed using [pip](https://pypi.org/project/pip/) and are available in the `requirements.txt` file. You can install them by running `pip install -r requirements.txt`

## Documentation
API connection class is available in the `emsi_connection.py` script. It provides automatic handling of generating an Oauth 2.0 token from Emsi's Auth server, as well as ensuring the access token is valid.

A script in `download_skills.py` has also been provided, which downloads the latest list of skills from Emsi's API.

Here's an example of how to use the Emsi connection library in this repo (also available in `skills_sample.py`):
```python
# import the connection class
from emsi_connection import SkillsClassificationConnection

# make sure that you input your credentials.
# you can request credentials on the skills site here: https://skills.emsidata.com/access
client_id = ""
client_secret = ""

skills_conn = SkillsClassificationConnection(client_id, client_secret)

# ensure we have an access token
print(skills_conn.token)

# is it a valid access token?
print(skills_conn.is_valid_token())

# get a list of the versions available in the API
print(skills_conn.list_versions().text)

# get a list of all of the skills in the latest version of the API
print(skills_conn.list_all_skills().text)

# search for skills related to python
search_response = skills_conn.search_skills(search_string = 'python')
print(search_response.text)

# get the Skill ID from the first item in the response
print(search_response.json()['skills'][0]['id'])

# get the information for just the python programming language, based on its ID
print(skills_conn.get_skill_by_id(search_response.json()['skills'][0]['id']).text)

# get a list of the different skill types available
print(skills_conn.list_skill_types().text)

# here's some text of a sample job posting that Emsi uses on their open skills site
job_posting_text = """
    Full Stack Web Developer
    Emsi is a trusted advisor on labor market information for customers across a wide array of markets. We build SaaS products that combine many different kinds of workforce data to accurately inform our clients' decisions about college course offerings, hiring, site selection, economic development, and much more. We need an experienced developer to join us in producing premier software tools for understanding labor market data.

    If you're ready to join a high-functioning team of full stack devs working closely with product managers, data engineers, and designers to create interfaces and visualizations that make nuanced data intelligible, we'd love to hear from you.
    Candidates must have...

        Experience with the front-end basics: HTML5, CSS3, and JS
        Experience using a version control system
        Familiarity with MV* frameworks, e.g. React, Ember, Angular, Vue
        Familiarity with server-side languages like PHP, Python, or Node

    Great candidates also have...

        Experience with a particular JS MV* framework (we happen to use React)
        Experience working with databases
        Experience with AWS
        Familiarity with microservice architecture
        Familiarity with modern CSS practices, e.g. LESS, SASS, CSS-in-JS

    People who succeed in this position are...

        Team oriented and ready to work closely with other developers
        Determined to produce clean, well-tested code
        Comfortable with working in rapid development cycles
        Skilled oral and written communicators
        Enthusiastic for learning and pushing the envelope

    Emsi is an equal opportunity employer.
"""
print(skills_conn.extract_skills(job_posting_text).text)

# in the skills tagging, include the source for why this text gets tagged
print(skills_conn.extract_skills_with_source(job_posting_text).text)
```
