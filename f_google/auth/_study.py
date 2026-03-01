from f_google.auth import Auth, ServiceAccount

account=ServiceAccount.RAMI
creds = Auth.get_creds(account=account)
print(creds.project_id)  # noteret
