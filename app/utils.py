import babel
import dateutil.parser

""" Format date into more readable format"""

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    
    return babel.dates.format_datetime(date, format, locale='en')

