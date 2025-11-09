import requests

url = "https://api.elevenlabs.io/v1/text-to-speech/nPczCjzI2devNBz1zQrb"  # example voice ID
headers = {
    "xi-api-key": "sk_3d8621f113a1e3c607517ff3788460a95010d31fd944bf4b",
    "Content-Type": "application/json"
}
data = {
    "text": "Hello from ElevenLabs test.",
    "model_id": "eleven_multilingual_v2"
}

response = requests.post(url, headers=headers, json=data)


with open("output.mp3", "wb") as f:
    f.write(response.content)