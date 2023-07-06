import openai
from co_mmunity.settings import get_secret


openai.api_key = get_secret("API_KEY")

def text_to_image(user_keyword):
    """키워드로 이미지 만들어주는 함수

    Args:
        user_keyword (str): 이미지 키워드

    Returns:
        result['data'][0]['url']: DALL-E를 통해 만들어진 이미지의 url을 반환
    """
    gpt_prompt = []
    gpt_prompt.append({
        "role":"system",
        "content":"Translating Korean into English in detail."
    })
    gpt_prompt.append({
        "role":"system",
        "content":"Imagine the detail appearance of the input. Response shortly. Translating Korean into English in detail."
    })
    gpt_prompt.append({
        "role":"user",
        "content":user_keyword
    })
    
    prompt = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=gpt_prompt)
    prompt = prompt["choices"][0]["message"]["content"]
    
    result = openai.Image.create(prompt=prompt, size="512x512")
    return result['data'][0]['url']