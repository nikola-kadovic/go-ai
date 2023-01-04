# Returns true iff lists a contains all elements in list b, and list b contains all elements in list a.
def is_equal_unordered(a: list, b: list) -> bool:
    return len(a) == len(b) and set(a) == set(b)
