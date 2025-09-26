import os
import getpass

def get_user():

    """
    Returns the name of the current operating system user.
    """
    user = os.getenv('USERNAME') or os.getenv('USER')
    if not user:
        # fallback for specific cases
        user = getpass.getuser()
    return user