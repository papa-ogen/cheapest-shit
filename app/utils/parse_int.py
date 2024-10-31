def parse_int(s: str) -> int | None:
    num_str = ""
    for char in s:
        if char.isdigit():  # Check if the character is a digit
            num_str += char  # Add it to the result string
        else:
            break  # Stop at the first invalid character
    return int(num_str) if num_str else None  # Convert to int or return None if empty
