import requests
import json

API_KEY = "ark-b6a4c4f0-e33a-4e76-bfdf-c08b4f77e6e9-c85a3"

url = "https://ark.cn-beijing.volces.com/api/v3/responses"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": "doubao-seed-2-0-pro-260215",
    "input": [
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "变压器是什么"}
            ]
        }
    ]
}

# ⭐ 关键：手动编码
body = json.dumps(data, ensure_ascii=False).encode("utf-8")

response = requests.post(url, headers=headers, data=body)

print(response.status_code)
print(response.text)