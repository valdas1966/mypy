import math




def sublist_by_index(li, indices):
    """
    ===========================================================================
     Description: Return Sublist based on requested indices.
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. li : list (Source List).
        2. indices : list of int (List of Requested Indices).
    ===========================================================================
     Return: list (Sublist of Source List based on requested indices).
    ===========================================================================
    """
    sub = list()
    for index in indices:
        sub.append(li[index])
    return sub


def to_slices_breadth(li: list, num_slices: int) -> 'list of list':
    """
        ============================================================================
         Description: Slice List into Sub-Lists by given Size of Sub-List.
        ============================================================================
         Arguments:
        ----------------------------------------------------------------------------
            1. li : list
            2. num_slices : int
        ============================================================================
         Return: list (List of Sub-Lists).
        ============================================================================
         Example: [1, 2, 3, 4] -> [ [1, 3], [2, 4] ]
        ============================================================================
    """
    len_slices = math.ceil(len(li) / num_slices)
    slices = [[] for _ in range(num_slices)]
    for i in range(len_slices):
        for j in range(num_slices):
            index = num_slices*i+j
            if index < len(li):
                slices[j].append(li[index])
    return slices


def to_slices(li: list, size: int, mode: str = 'DEPTH') -> 'list of list':
    """
    ============================================================================
     Description: Slice List into Sub-Lists by given Size of Sub-List.
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. li : list
        2. size : int (Sub-List Size).
        3. mode : str (BREADTH | DEPTH).
    ============================================================================
     Return: list (List of Sub-Lists).
    ============================================================================
     Example: [BREADTH] [1, 2, 3, 4] -> [ [1, 3], [2, 4] ]
              [DEPTH]   [1, 2, 3, 4] -> [ [1, 2], [3, 4] ]
    ============================================================================
    """
    def breadth() -> None:
        slices = [[]]*len_slices
        for i in range(len(li)//len_slices):
            for j in range(len_slices):
                slices[j].append(li[len_slices*i+j])
        return slices

    def depth() -> None:
        slices = list()
        for i in range(len_slices):
            index_from = i * size
            index_to = (i + 1) * size
            slices.append(li[index_from: index_to])
        return slices

    len_slices = math.ceil(len(li)/size)
    if mode == 'BREADTH':
        return breadth()
    elif mode == 'DEPTH':
        return depth()


def bigram(li):
    """
    ===========================================================================
     Description: Convert List into List of Tuples (BiGram method).
    ---------------------------------------------------------------------------
        1. list('abc') => [ tuple('ab'), tuple('bc') ]
    ===========================================================================
     Arguments:
    ---------------------------------------------------------------------------
        1. li : list.
    ===========================================================================
     Return: list of tuple (List of Tuples in BiGram method).
    ===========================================================================
    """
    tuples = list()
    if len(li)<2:
        return tuples
    for i in range(len(li)-1):
        tuples.append((li[i],li[i+1]))
    return tuples


def to_str(li, delimiter=','):
    """
    ============================================================================
     Description: Return str-representation of list values (by delimiter).
    ============================================================================
     Arguments:
    ----------------------------------------------------------------------------
        1. li : list (To Represent).
        2. delimiter : str (Delimiter).
    ============================================================================
     Return: str 'value_1,'value-2'.
    ============================================================================
    """
    return delimiter.join([str(x) for x in li])
