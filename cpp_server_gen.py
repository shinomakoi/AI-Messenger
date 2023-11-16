import json
import requests
from typing import Union

URL = "http://localhost:8080/completion"
DATA_PREFIX = "data: "


def create_payload(cpp_params, stream=False):
    return {
        **cpp_params,  # Unpack the cpp_params dictionary into the data payload
        "stream": stream,
    }


def send_request(payload) -> Union[str, None]:
    result = None
    response = requests.post(URL, json=payload)
    if not response.ok:  # If status code is not successful (200), raise an exception
        print("Failed to generate response", response.text)
        return None

    result = response.json()
    return result


def generate_nostream(cpp_params):
    payload = create_payload(cpp_params)
    return send_request(payload)


def generate_with_streaming(cpp_params):
    payload = create_payload(
        cpp_params, stream=True
    )  # Set the 'stream' parameter to True

    response = requests.post(URL, stream=True, json=payload)

    if not response.ok:  # If status code is not successful (200), raise an exception
        print("Failed to generate response", response.text)

    for line in response.iter_lines():
        decoded = line.decode("utf8")
        if decoded.startswith(
            DATA_PREFIX
        ):  # If the line starts with 'data: ', it's a JSON object
            yield json.loads(decoded[len(DATA_PREFIX) :])
