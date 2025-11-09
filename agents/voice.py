import requests

headers = {
    "xi-api-key": "sk_3d8621f113a1e3c607517ff3788460a95010d31fd944bf4b"
}

response = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
voices = response.json()

for v in voices["voices"]:
    print(v["name"], ":", v["voice_id"])