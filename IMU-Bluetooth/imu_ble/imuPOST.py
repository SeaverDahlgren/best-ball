import requests

def add_stroke(ball_id):
    # Specify the URL endpoint to send the POST request to
    url = 'https://sman101.pythonanywhere.com/bestballapp/add_stroke/'

    # Create a dictionary of the data to send in the POST request
    data = {
        'ball_id': ball_id,
    }

    # Send the POST request
    response = requests.post(url, data=data)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        print('POST request successful')
    else:
        # Request failed
        try:
            url = 'http://localhost:8765/bestballapp/add_stroke/'
            requests.post(url, data=data)
        except:
            print(f'POST request failed with status code: {response.status_code}')

def set_spin(ball_id, spin):
    # Specify the URL endpoint to send the POST request to
    url = 'https://sman101.pythonanywhere.com/bestballapp/set_spin/'

    # Create a dictionary of the data to send in the POST request
    data = {
        'ball_id': ball_id,
        'spin_rate': spin
    }

    # Send the POST request
    response = requests.post(url, data=data)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        print('POST request successful')
    else:
        # Request failed
        try:
            url = 'http://localhost:8765/bestballapp/set_spin/'
            requests.post(url, data=data)
        except:
            print(f'POST request failed with status code: {response.status_code}')

