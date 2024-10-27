import ast


def is_empty(s: str) -> bool:
    """
    ============================================================================
     Return True if the given str is Empty.
    ============================================================================
    """
    return s == str() or s is None


def to_dict(s: str) -> dict:
    """
    ============================================================================
     Desc: Convert Dict's Str-Representation into Dict.
    ============================================================================
    """
    return ast.literal_eval(s)


def endswith(text, extensions=set()):
    """
    =======================================================================
     Description: Return True if Text ends with one of the given Extension.
    =======================================================================
     Arguments:
    -----------------------------------------------------------------------
        1. text : str (Text to Check).
        2. extensions : set of str (Set of Extensions to Check).
    =======================================================================
     Return: bool (True if the Text ends with one of the given Extensions).
    =======================================================================
    """
    if not extensions:
        return True
    for e in extensions:
        if text.endswith(e):
            return True
    return False


def get_nums(text, len_min=1):
    """
    ===========================================================================
     Description: Return List of Numbers that extracted from the str.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. text : str 
    ===========================================================================
     Return: list of int
    ===========================================================================
    """
    nums = list()
    cur = str()
    for ch in text:
        if str.isdecimal(ch):
            if cur:
                cur += ch
            else:
                cur = ch
        else:
            if cur:                
                if len(cur)>=len_min:
                    nums.append(int(cur))    
                cur = str()
    if cur:
        if len(cur)>=len_min:
            nums.append(int(cur))
    return nums


def to_regex(value, digit='d', alpha='w', white='_', black='x'):
    li = list()
    for ch in str(value):
        if ch.isspace():
            li.append(white)
        elif ch.isalnum():
            if ch.isdigit():
                    li.append(digit)
            elif ch.isalpha():
                li.append(alpha)
        else:
            li.append(black)
    return ''.join(li)


def push_at(s, what, i):
    """
    ============================================================================
     Description: Push str into another str.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. s : str (Main String).
        2. what : str (String to Push).
        3. i : int (Index where to Push).
    ============================================================================
     Return: str (String after list Push process).
    ============================================================================
    """
    assert type(s) == str
    assert type(what) == str
    assert type(i) == int
    assert 0 <= i <= len(s)
    return f'{s[:i]}{what}{s[i:]}'


def wrap(s: str, ch: str) -> str:
    """
    ============================================================================
     Description: Wrap str "s" with "ch" from both sides.
    ============================================================================
    """
    return f'{ch}{s}{ch}'


def real_strip(s: str) -> str:
    """
    ============================================================================
     Description: Removes WhiteSpace and Multiple-Spaces.
    ============================================================================
    """
    return ' '.join(s.split())


def add_prefix(text: str, prefix: str = None) -> str:
    """
    ============================================================================
     Return the Text with Prefix at the Start.
    ============================================================================
    """
    return (prefix or str()) + text
