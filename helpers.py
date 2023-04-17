def md_escape_chars(md_string):
    md_escaped_string = md_string.replace('-', '\-')
    md_escaped_string  = md_escaped_string.replace('_', '\_')
    return md_escaped_string
