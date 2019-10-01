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

# here's some text of a sample job posting that Emsi uses on it's open skills site
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
