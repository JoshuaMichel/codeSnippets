# Create a dataset with updated information on all the projects in the Dataiku instance

import dataiku
import pandas as pd
import numpy as np
from dataiku import pandasutils as pdu

# Get all project's info on the Dataiku instance & return as a dictionary
def get_project_data(client):
    project_data = []
    
    # For every project in the DSS instance
    for project_key in client.list_project_keys():
        dss_project = client.get_project(project_key)
        metadata = dss_project.get_metadata()
        owner_sso = dss_project.get_permissions().get('owner')
        
        project_name = metadata.get('label', 'Unnamed Project')
        
        # In case a project exists in which the owner's account has been removed
        try:
            user_settings = client.get_user(owner_sso).get_settings().get_raw()
            user_group = user_settings.get('groups', 'Owner account removed')
            owner_name = user_settings.get('displayName', 'Owner account removed')
        except Exception:
            user_group = 'Owner account removed'
            owner_name = 'Owner account removed'
        
        description_long = metadata.get('description', '')
        description_short = metadata.get('shortDesc', '')
        
        project_data.append({
            'name': project_name,
            'owner group': user_group,
            'owner': owner_name,
            'value': '',
            'desc long': description_long,
            'desc short': description_short,
            'project key': project_key,
        })
    
    return project_data

def main():
    client = dataiku.api_client()
    
    project_data = get_project_data(client)
    project_data_df = pd.DataFrame(project_data)
    
    projects_report_dataset = dataiku.Dataset("projects_report_stg")
    projects_report_dataset.write_with_schema(project_data_df)

if __name__ == "__main__":
    main()
