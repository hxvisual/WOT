import requests
import webbrowser
from config import VERSION, GITHUB_REPO


def check_version():
    try:
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
        response = requests.get(url)
        
        if response.status_code == 200:
            latest_release = response.json()
            latest_version = latest_release['tag_name'].lstrip('v')
            
            if latest_version != VERSION:
                webbrowser.open(latest_release['html_url'])
                return True
    except Exception:
        return False