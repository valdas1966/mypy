from f_proj.myq.gsheets.cs.i_0_cs import SheetCS, Question


s = SheetCS()
text, a = s._sheet.to_tuples(col_first=2, col_last=3,
                             row_first=44, row_last=44)[0]
for _ in range(10):
    print(Question(text=text, answer=a, exclude=s._exclude))
