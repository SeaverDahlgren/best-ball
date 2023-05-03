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
        print(f'POST request failed with status code: {response.status_code}')

# def add_stroke(ball_id):
#     # Specify the URL endpoint to send the POST request to
#     url = 'https://sman101.pythonanywhere.com/bestballapp/add_stroke/'
#
#     # Create a dictionary of the data to send in the POST request
#     data = {
#         'ball_id': ball_id,
#     }
#
#     # Send the POST request
#     response = requests.post(url, data=data)
#
#     # Check the response status code
#     if response.status_code == 200:
#         # Request was successful
#         print('POST request successful')
#     else:
#         # Request failed
#         print(f'POST request failed with status code: {response.status_code}')

