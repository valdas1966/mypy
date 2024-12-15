from f_google.utils.u_service import UService


user = 'VALDAS'

drive = UService.drive(user=user)
print(drive)

sheets = UService.sheets(user=user)
print(sheets)
