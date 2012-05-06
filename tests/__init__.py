def raise_error(error, message):
    """
    This method serves to appease the code analysis tools of IDE's that object
    (as they should) to statements after the raise keyword.
    """
    raise error(message)