import os
import sys

from dotenv import load_dotenv

def load_env_file():
    # Determine the path to the .env file
    if hasattr(sys, '_MEIPASS'):
        # If running in packaged mode
        env_path = os.path.join(sys._MEIPASS, '.env')
    else:
        # If running in development mode
        env_path = os.path.join(os.path.dirname(__file__), '../../.env')

    # Load the .env file
    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path)
        return True

    sys.exit("Couldn't find .env file")
