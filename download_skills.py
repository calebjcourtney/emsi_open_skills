import pandas as pd

from emsi_connection import SkillsClassificationConnection


def main():
    # make sure that you input your credentials.
    # you can request credentials on the skills site here: https://skills.emsidata.com/access
    client_id = ""
    client_secret = ""

    # create the connection to the skills API
    skills_conn = SkillsClassificationConnection(client_id, client_secret)

    # get all the skills from the latest version
    all_skills_response = skills_conn.list_all_skills().json()

    # load into a pandas dataframe for easy exporting to excel
    df = pd.DataFrame(all_skills_response['skills'])

    # export to excel
    writer = pd.ExcelWriter('all_emsi_skills.xlsx')
    df.to_excel(writer, 'Data', index = False)
    writer.save()


if __name__ == '__main__':
    main()
