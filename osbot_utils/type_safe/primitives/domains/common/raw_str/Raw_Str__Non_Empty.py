from osbot_utils.type_safe.primitives.core.Raw_Str import Raw_Str

class Raw_Str__Non_Empty(Raw_Str):                                               # String that cannot be empty
    allow_empty = False

# todo: do the same to Safe_Str__Html
# class Raw_Str__Html(Raw_Str):                                                    # HTML content (not sanitized)
#     max_length  = 10 * 1024 * 1024                                               # 10 MB limit
#     allow_empty = True