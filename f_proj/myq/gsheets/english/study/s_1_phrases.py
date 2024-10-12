from f_proj.myq.gsheets.english.i_1_phrases import SheetPhrases


qs = SheetPhrases().to_questions()
for q in qs:
    print(q)
