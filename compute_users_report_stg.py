# Create a dataset with updated information on all the users in the Dataiku instance

import dataiku
import pandas as pd
from dataiku import pandasutils as pdu

client = dataiku.api_client()

# Get all user's info on the Dataiku instance & return as a dictionary
def get_user_info(user):
    myuser = client.get_user(user['login'])
    display_name = user['displayName']
    groups = user['groups']
    last_login = myuser.get_activity().last_successful_login
    login_name = user['login']
    email = user.get('email', 'N/A')
    
    return {
        'name': display_name,
        'groups': groups,
        'lastLogin': last_login,
        'ssoId': login_name,
        'email': email,
    }

def main():
    dss_users = client.list_users()
    user_data = [get_user_info(user) for user in dss_users]
    
    # Compute a Pandas dataframe to write into get_projects_report
    get_projects_report_df = pd.DataFrame(user_data)
    
    # Write recipe outputs
    get_projects_report = dataiku.Dataset("users_report_stg")
    get_projects_report.write_with_schema(get_projects_report_df)

if __name__ == "__main__":
    main()


