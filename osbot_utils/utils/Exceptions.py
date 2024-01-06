def syntax_error(error):
    if type(error) is SyntaxError:
        error_message = f"{error.msg} in {error.filename} at line {error.lineno} column {error.offset}\n\n"
        error_message += f"    {error.text}"
        error_message += f"    {' ' * (error.offset - 1)}^"
        return Exception(f'[SyntaxError] \n\nError parsing code: {error_message}')
    return Exception(f'{error}')
