import requests
import json
from datetime import datetime

def get_json() :
    
    url = 'https://coopcycle.org/coopcycle.json?_=1704296951899'

    response = requests.get(url)

    if response.status_code == 200:
        
        json_data = response.json()
        
        format_date = "%d_%m_%y_%H_%M_%S"

        file_name = f"JsonData{datetime.now().strftime(format_date)}.json"

        with open(file_name, 'w') as file:
            json.dump(json_data, file)

    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

    return(file_name)