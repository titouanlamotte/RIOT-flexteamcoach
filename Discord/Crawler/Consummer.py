import requests
import time
from pprint import pprint

def getcall(url, headers):
    try:
        pprint(url)
        #pprint(headers)
        response = requests.get(url, headers, timeout=10)
        #pprint(response)
        response.raise_for_status()
        # only if 200 response
        r=response.json()
        if r == [] or r == None:
            print('[]')
            return False
            
        elif 'status' in r:
            print('! status message: ')
            print(r)
            time.sleep(500)
            return False

        else:
            return response

    except requests.exceptions.HTTPError as errh:
        print(errh)
        return False
    except requests.exceptions.ConnectionError as errc:
        print(errc)
        return False
    except requests.exceptions.Timeout as errt:
        print(errt)
        return False
    except requests.exceptions.RequestException as err:
        print(err)
        return False