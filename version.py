VERSION = (0, 9, 0)

def get_version():
    """
    Return version number (used by context processor)
    """
    return "%s.%s.%s" % (VERSION[0],VERSION[1],VERSION[2])

