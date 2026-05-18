# Tokenization policy (NOT regex): which code points count as
# word characters for English + Arabic + Hebrew. Written as
# integer (lo, hi) inclusive ranges — hand-typable on any
# keyboard, verifiable 1:1 against the Unicode charts. The regex
# mechanism lives entirely in URe (URe.extract_runs); f_nlp only
# declares the policy and delegates.
#   0x0030-0x0039 0-9      0x0041-0x005A A-Z   0x005F _   a-z
#   Arabic : signs, letters+tatweel+harakat, Arabic-Indic digits,
#            superscript alef / alef wasla, Quranic marks
#   Hebrew : cantillation+niqqud, rafe, shin/sin dots, upper/
#            lower marks, qamats qatan, letters, ligatures
# Arabic ، ؟, Hebrew maqaf (0x05BE), paseq (0x05C0), sof pasuq
# (0x05C3) and nun hafukha (0x05C6) are punctuation and are
# deliberately excluded so they delimit.
_TOKEN_RANGES = (
    # --- English / ASCII ---
    (0x0030, 0x0039),   # 0-9
    (0x0041, 0x005A),   # A-Z
    (0x005F, 0x005F),   # _
    (0x0061, 0x007A),   # a-z
    # --- Arabic ---
    (0x0610, 0x061A),   # signs / honorific marks
    (0x0621, 0x065F),   # letters + tatweel + harakat/tanwin
    (0x0660, 0x0669),   # Arabic-Indic digits
    (0x0670, 0x0671),   # superscript alef, alef wasla
    (0x06D6, 0x06ED),   # Quranic annotation signs
    # --- Hebrew ---
    (0x0591, 0x05BD),   # cantillation + niqqud
    (0x05BF, 0x05BF),   # rafe
    (0x05C1, 0x05C2),   # shin / sin dots
    (0x05C4, 0x05C5),   # upper / lower marks
    (0x05C7, 0x05C7),   # qamats qatan
    (0x05D0, 0x05EA),   # letters
    (0x05EF, 0x05F2),   # yod-triangle + ligatures
)


# Optional marks (a strict subset of the *mark* portion of
# _TOKEN_RANGES — letters/digits excluded): the diacritics that
# _Strip.marks() removes so vocalized/pointed and plain spellings
# compare equal. Arabic alef-wasla (0x0671) is a LETTER and is
# deliberately NOT here (removing it would corrupt the word).
_MARK_RANGES = (
    # --- Arabic optional marks ---
    (0x0610, 0x061A),   # signs / honorific marks
    (0x0640, 0x0640),   # tatweel (kashida — elongation only)
    (0x064B, 0x065F),   # harakat + tanwin + extended marks
    (0x0670, 0x0670),   # superscript alef
    (0x06D6, 0x06ED),   # Quranic annotation signs
    # --- Hebrew optional marks ---
    (0x0591, 0x05BD),   # cantillation + niqqud (incl. dagesh)
    (0x05BF, 0x05BF),   # rafe
    (0x05C1, 0x05C2),   # shin / sin dots
    (0x05C4, 0x05C5),   # upper / lower marks
    (0x05C7, 0x05C7),   # qamats qatan
)
