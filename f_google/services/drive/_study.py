from f_google.services import Drive


drive = Drive.Factory.valdas()

for folder in drive.folders():
    print(folder)