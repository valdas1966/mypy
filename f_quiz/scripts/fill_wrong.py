from f_google.services.sheets.spread import Spread


# Antonyms / contextually wrong alternatives
_OPPOSITES: dict[str, str] = {
    'Logic': 'Intuition',
    'has': 'lacks',
    'independent': 'dependent',
    'origins': 'endings',
    'in': 'outside',
    'Greece': 'Egypt',
    'India': 'Japan',
    'and': 'or',
    'China': 'Brazil',
    'Propositional': 'Predicate',
    'is': 'was',
    'formal': 'informal',
    'system': 'chaos',
    'for': 'against',
    'reasoning': 'guessing',
    'with': 'without',
    'propositions': 'assumptions',
    'A': 'No',
    'proposition': 'assumption',
    'the': 'a',
    'truth-apt': 'truth-inapt',
    'meaning': 'nonsense',
    'of': 'about',
    'a': 'no',
    'declarative': 'interrogative',
    'sentence': 'word',
    'Every': 'No',
    'expresses': 'conceals',
    'same': 'different',
    'can': 'cannot',
    'be': 'never',
    'expressed': 'concealed',
    'by': 'without',
    'multiple': 'single',
    'sentences': 'words',
    'Snow': 'Rain',
    'white': 'black',
    'classic': 'modern',
    'example': 'exception',
}


def run() -> None:
    """
    ========================================================================
     Fill empty 'Wrong' cells in the Options sheet with opposites.
    ========================================================================
    """
    spread = Spread.Factory.questions()
    sheet = spread['Options']
    last_row = sheet.last_row()
    filled = 0
    skipped: list[tuple[int, str]] = []
    for i in range(1, last_row):
        row = sheet[i]
        core = str(row[2]).strip()
        wrong = str(row[3]).strip()
        if core and not wrong:
            opposite = _OPPOSITES.get(core)
            if opposite:
                row[3].value = opposite
                filled += 1
                print(f'  Row {i}: "{core}" -> "{opposite}"')
            else:
                skipped.append((i, core))
    print(f'\nFilled: {filled}')
    if skipped:
        print(f'Skipped (no opposite found): {len(skipped)}')
        for idx, word in skipped:
            print(f'  Row {idx}: "{word}"')


if __name__ == '__main__':
    run()
