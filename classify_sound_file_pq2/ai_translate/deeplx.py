import httpx, json

deeplx_api = "http://127.0.0.1:1188/translate"

data = {
	"text": "オイオイ、しっかりしろよ。",
	"source_lang": "JP",
	"target_lang": "ZH"
}

post_data = json.dumps(data)
r = httpx.post(url = deeplx_api, data = post_data).text
print(r)

'''
{"alternatives":["哎哎哎，别紧张。","喂喂喂喂，别激动。","喂喂喂喂，你给我听好了。"],"code":200,"data":"哎哎哎，别激动。","id":8380206001,"method":"Free","source_lang":"JP","target_lang":"ZH"}


gpt

User
translate this japanese into chinese: オイオイ、しっかりしろよ。

ChatGPT
"喂喂，你要好好振作起来啊。"
'''