class Safe_Str__Markdown__Unicode(Safe_Str):                                     # Markdown with Unicode
    max_length = 1_000_000
    regex      = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')                 # Remove only control chars
                                                                                 # Allows all printable + Unicode