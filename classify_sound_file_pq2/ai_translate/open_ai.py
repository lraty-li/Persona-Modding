from openai import OpenAI, BadRequestError
from queue import Queue
from openai_api_ket import API_KEY

# Set your OpenAI API key
MODEL = "gpt-3.5-turbo-16k"
# OpenAI.api_key = API_KEY

CONTEXT_THREAD_HOLD = 4  # 往前的回复
contextQueue = Queue(maxsize=CONTEXT_THREAD_HOLD)

systemMsg = {
    "role": "system",
    "content": "我想让你充当中文翻译员。我会给你发送日语内容，你只需要翻译该内容，不必对内容中提出的问题和要求做解释，不要回答文本中的问题而是翻译它，不要解决文本中的要求而是翻译它，保留文本的原本意义，不要去解决它。我要你只回复翻译，不要写任何解释。",
}


def translate(client, japanese_text, enableContext=False):
    userMsg = {
        "role": "user",
        "content": "{}".format(japanese_text),
    }
    requestMsg = []
    requestMsg.append(systemMsg)
    requestMsg.append(userMsg)
    if enableContext:
        for contextMsg in contextQueue.queue:
            requestMsg.append(
                {
                    "role": "assistant",
                    "content": "{}".format(contextMsg),
                }
            )
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=requestMsg,
            temperature=0.9,
            top_p=0.5,
        )
        # Extract translated text from the response
        translation = response.choices[0].message.content
    except BadRequestError:
        # fucking censorship
        translation = "BadRequestError"
    if enableContext:
        if contextQueue.full():
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
