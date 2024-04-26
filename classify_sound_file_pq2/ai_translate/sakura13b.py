from openai import OpenAI

from openai_api_ket import API_KEY

# Set your OpenAI API key
MODEL = "gpt-3.5-turbo-0125"
# OpenAI.api_key = API_KEY

extra_query = {
    'do_sample': False,
    'num_beams': 1,
    'repetition_penalty': 1.0,
}

def translate(client, japanese_text):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个翻译引擎。根据原文逐行翻译，将每行原文翻译为简体中文。保留每行文本的原始格式，并根据所需格式输出翻译后的文本。在翻译文本时，请严格注意以下几个方面：首先，一些完整的文本可能会被分成不同的行。请严格按照每行的原始文本进行翻译，不要偏离原文。其次，无论句子的长度如何，每行都是一个独立的句子，确保不要将多行合并成一个翻译。第三，在每行文本中，转义字符（例如\, \r, 和\n）或非日语内容（例如数字、英文字母、特殊符号等）不需要翻译或更改，应保持原样",
            },
            {"role": "user", "content": f"{japanese_text}"},
        ],
        temperature=0.2,
        top_p=0.3,
        max_tokens=512,
        frequency_penalty=0.2,
        seed=-1,
        extra_query=extra_query,
        stream=False,
    )

    # Extract translated text from the response
    translation = response.choices[0].message.content

    return translation


if __name__ == "__main__":

    japanese_text = "オイオイ、しっかりしろよ。"

    client = OpenAI(
        api_key=API_KEY,
        base_url="http://localhost:5000/v1",
    )
    translated_text = translate(client, japanese_text)

    print("Japanese text:", japanese_text)
    print("Translated text (Chinese):", translated_text)

# 可恶，deepl国内不能注册
