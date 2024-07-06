from proj.myq.gsheets.english.i_1_words import SheetWords


qs = SheetWords().to_questions()
for q in qs:
    print(q)
