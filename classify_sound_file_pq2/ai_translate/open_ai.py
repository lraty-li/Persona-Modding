from openai import OpenAI
from queue import Queue
from openai_api_ket import API_KEY

# Set your OpenAI API key
MODEL = "gpt-3.5-turbo-0125"
# OpenAI.api_key = API_KEY

CONTEXT_THREAD_HOLD = 4  # 往前的回复
contextQueue = Queue(maxsize=CONTEXT_THREAD_HOLD)

systemMsg = {
    "role": "system",
    "content": "You will be provided with a sentence in japanese, and your task is to translate it into simplified Chinese.",
}


def translate(client, japanese_text, enableContext=False):
    userMsg = {
            "role": "user",
            "content": "{}".format(japanese_text),
        }
    requestMsg = []
    requestMsg.append(systemMsg)
    requestMsg.append(userMsg)
    if(enableContext):
        for contextMsg in contextQueue.queue:
            requestMsg.append(
                {
                    "role": "assistant",
                    "content": "{}".format(contextMsg),
                }
            )
    response = client.chat.completions.create(
        model=MODEL,
        messages=requestMsg,
        temperature=0.9,
        top_p=0.5,
    )

    # Extract translated text from the response
    translation = response.choices[0].message.content
    if(enableContext):
        if(contextQueue.full()):
            contextQueue.get()
        contextQueue.put(translate)
    return translation


if __name__ == "__main__":

    japanese_text = "オイオイ、しっかりしろよ。"

    client = OpenAI(
        api_key=API_KEY,
        base_url="https://api.chatanywhere.tech/v1",
    )
    translated_text = translate(client, japanese_text)

    print("Japanese text:", japanese_text)
    print("Translated text (Chinese):", translated_text)

# 可恶，deepl国内不能注册
