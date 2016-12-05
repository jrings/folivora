"""Read and write to thermostat API
"""

import requests


def get_state(url):
    """Get thermostat state
    """

    r = requests.get(url)
    return r.json()
