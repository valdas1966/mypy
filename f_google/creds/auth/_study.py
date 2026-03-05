from f_google.creds.auth import Auth

creds = Auth.Factory.rami()
print(creds.project_id)  # noteret
