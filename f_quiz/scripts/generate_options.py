from f_google.services.sheets.spread import Spread


def _split_token(token: str) -> tuple[str, str, str]:
    """
    ========================================================================
     Split a token into (prefix, core, suffix).
     Prefix/suffix are non-alphanumeric characters (quotes, parens, etc).
     Example: "'valid'" -> ("'", "valid", "'")
              "(logic)" -> ("(", "logic", ")")
              "arguments," -> ("", "arguments", ",")
    ========================================================================
    """
    start = 0
    while start < len(token) and not token[start].isalnum():
        start += 1
    end = len(token)
    while end > start and not token[end - 1].isalnum():
        end -= 1
    return token[:start], token[start:end], token[end:]


def run() -> None:
    """
    ========================================================================
     Process new sentences in the Options sheet.
     For each unique Full sentence, ensures all words are expanded
     into masked Question rows. Uses batch API calls.
    ========================================================================
    """
    spread = Spread.Factory.questions()
    sheet = spread['Options']
    last_row = sheet.last_row()
    # Count existing expanded rows per Full sentence
    existing: dict[str, int] = {}
    for i in range(1, last_row):
        full = str(sheet[i][0]).strip()
        question = str(sheet[i][1]).strip()
        if full and question:
            existing[full] = existing.get(full, 0) + 1
    # Find sentences that need expansion
    to_expand: list[tuple[int, str]] = []
    seen: set[str] = set()
    for i in range(1, last_row):
        full = str(sheet[i][0]).strip()
        if not full or full in seen:
            continue
        seen.add(full)
        n_words = len(full.split())
        n_rows = existing.get(full, 0)
        if n_rows < n_words:
            to_expand.append((i, full))
    if not to_expand:
        print('No new sentences to expand.')
        return
    print(f'Found {len(to_expand)} sentence(s) to expand.')
    # Process in reverse so row indices stay valid
    for first_idx, full in reversed(to_expand):
        words = full.split()
        n_words = len(words)
        n_existing = existing.get(full, 0)
        print(f'  "{full}" -> {n_words} words'
              f' ({n_existing} existing)')
        # Find contiguous block of existing rows
        block_end = first_idx
        for i in range(first_idx, len(sheet._rows)):
            if str(sheet._rows[i][0]).strip() == full:
                block_end = i
            else:
                break
        # Delete existing block (1 API call)
        start_1 = first_idx + 1
        end_1 = block_end + 1
        sheet._ws.delete_rows(start_1, end_1)
        for i in range(block_end, first_idx - 1, -1):
            sheet._rows.pop(i)
        # Build all rows
        cols = len(sheet._rows[0]) if sheet._rows else 4
        rows_data = []
        for w_idx, token in enumerate(words):
            prefix, core, suffix = _split_token(token)
            masked = ' '.join(
                f'{prefix}*****{suffix}' if j == w_idx
                else words[j]
                for j in range(n_words)
            )
            row = [''] * cols
            row[0] = full
            row[1] = masked
            row[2] = core
            rows_data.append(row)
        # Insert all rows at once (1 API call)
        sheet._ws.insert_rows(rows_data, row=first_idx + 1)
        for i, row in enumerate(rows_data):
            sheet._rows.insert(first_idx + i, row)
    print('Done.')


if __name__ == '__main__':
    run()
