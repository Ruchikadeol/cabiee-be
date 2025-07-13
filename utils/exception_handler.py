import re

def exception_handler(error):

    pattern = r"ErrorDetail\(string='(.*?)', code='.*?'\)"

    match = re.search(pattern, error)
    if match:
        message = match.group(1)
        print(message)
        return message