from myq.gsheets.english.i_1_words import SheetWords


sheet = SheetWords()
qs = SheetWords().to_questions()
for q in qs:
    print(q)
