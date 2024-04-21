from openai import OpenAI

from openai_api_ket import API_KEY

# Set your OpenAI API key
MODEL = "gpt-3.5-turbo-0125"
# OpenAI.api_key = API_KEY


def translate(client, japanese_text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            # {
            #     "role": "system",
            #     "content": "You will be provided with a sentence in English, and your task is to translate it into French.",
            # },
            {
                "role": "user",
                "content": "translate japanese into just Chinese {}".format(japanese_text),
            },
        ],
        temperature=0.7,
        top_p=0.5,
    )

    # Extract translated text from the response
    translation = response.choices[0].message.content

    return translation

if __name__ == '__main__':

    japanese_text = "オイオイ、しっかりしろよ。"

    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.chatanywhere.tech/v1",
    )
    translated_text = translate(client, japanese_text)

    print("Japanese text:", japanese_text)
    print("Translated text (Chinese):", translated_text)

# 可恶，deepl国内不能注册
