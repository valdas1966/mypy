from f_google.services.drive import Drive

drive = Drive.Factory.valdas()

# Search for the file - let's first check common locations
# Try listing root folders to find where papers might be
folders = drive.folders()
print("Root folders:", folders)
