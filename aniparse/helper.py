def is_number(string) -> bool:
    """
    Check if the given `Token` object represents a number.

    Args:
        string: The string to check.

    Returns:
        bool: True if the `Token` object represents a number, False otherwise.
    """
    try:
        float(string)
        return True
    except (ValueError, TypeError):
        return False
