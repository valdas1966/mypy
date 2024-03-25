from f_google.auth.auth import Auth


creds = Auth.get_creds(user='VALDAS')
print(type(creds))

"""
creds = Auth.get_creds(user='RAMI')
print(creds.project_id)
"""
