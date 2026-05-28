import requests
import json

pergunta = input("Digite sua pergunta: ")

response = requests.post(
    "http://127.0.0.1:8000/api/chat/",
    json={
        "prompt": pergunta
    }
)

#print(response.status_code)
#print(response.text)
texto = response.text
dados = json.loads(texto)
resposta = ""

for item in dados:
    if item["event"] == "message":
        resposta += item["data"]["content"]

print(resposta)