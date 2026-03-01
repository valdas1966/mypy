from old_old_f_google.utils.u_authentication import UAuthentication


creds = UAuthentication.get(user='VALDAS')
print(type(creds))

"""
creds = UAuthentication.get_creds(user='RAMI')
print(creds.project_id)
"""
