from proj.myq.gsheets.english.i_1_definitions import SheetDefinitions


qs = SheetDefinitions().to_questions()
for q in qs:
    print(q)
