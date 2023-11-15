import asyncio
import json

try:
    import websockets
except ImportError:
    print("Websockets package not found. Make sure it's installed.")

uri = "ws://localhost:7862"


async def generate_nostream(exllamav2_params):
    stop_string = exllamav2_params["stop"][0]
    prompt = exllamav2_params["prompt"][1]
    request = {
        "request_id": 123,
        "action": "infer",
        "stream": False,
        "text": prompt,
        "max_new_tokens": exllamav2_params["n_predict"],
        "top_p": exllamav2_params["top_p"],
        "top_k": exllamav2_params["top_k"],
        "typical": exllamav2_params["typical_p"],
        "temperature": exllamav2_params["temperature"],
        "rep_pen": exllamav2_params["repeat_penalty"],
        "stop_conditions": str(stop_string),
        "token_healing": False,
    }
    final_request = json.dumps(request)
    uri = "ws://localhost:7862"
    async with websockets.connect(uri) as websocket:
        await websocket.send(final_request)
        response = await websocket.recv()
        json_response = json.loads(response)
    return json_response


def launch(exllamav2_params):
    json_response = asyncio.run(generate_nostream(exllamav2_params))
    return json_response


async def generate_streaming(exllamav2_params):
    stop_string = exllamav2_params["stop"][0]
    prompt = exllamav2_params["prompt"]
    # Note: the selected defaults change from time to time.
    request = {
        "request_id": 123,
        "action": "infer",
        "stream": True,
        "text": prompt,
        "max_new_tokens": exllamav2_params["n_predict"],
        "top_p": exllamav2_params["top_p"],
        "top_k": exllamav2_params["top_k"],
        "typical": exllamav2_params["typical_p"],
        "temperature": exllamav2_params["temperature"],
        "rep_pen": exllamav2_params["repeat_penalty"],
        "stop_conditions": str(stop_string),
        "token_healing": False,
    }

    async with websockets.connect(uri, ping_interval=None) as websocket:
        await websocket.send(json.dumps(request))

        while True:
            incoming_data = await websocket.recv()
            incoming_data = json.loads(incoming_data)

            match incoming_data["response_type"]:
                case "full":
                    return
            yield incoming_data["chunk"]
