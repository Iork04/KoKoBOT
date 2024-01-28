from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    gpt_identity = "You are KoKo, a chat robot trained by EUy_o."
    path_chatgpt = "./data/chatgpt/"
    max_massage_len = 10,
    url = "https://x.dogenet.win/api/v1/ai/chatgpt/chat"
    headers = {
        'Accept':
        'application/json, text/plain, */*',
        'Accept-Encoding':
        'gzip, deflate, br',
        'Accept-Language':
        'zh-CN,zh;q=0.9',
        'Authorization':
        'Bearer eyJhbGciOiJFUzUxMiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjIyNTYxIiwiZW1haWwiOiJ4cnlhemkxMTA0QG91dGxvb2suY29tIiwicHVycG9zZSI6IndlYiIsImlhdCI6MTcwNTI5NTA5NywiZXhwIjoxNzA2NTA0Njk3fQ.ALm-MWvpU_qXcxH1fk2M4Ab2IuEqvoIUfTiGndTKpzJvFgnjPurZ9djQZhzlBlLsmBULfpJ5Z7_HEbbRvqEgAGQoAJzl1VIw9QYVAjIGsmJU5Vp9tVFjaU9kI5G7jNRy7vh85IAniiH5gUgIdExLolPO0vR59gp4i16Rqzgc1Is_OVac',  # 改左边
        'Cache-Control':
        'no-cache',
        'Cookie':
        '_ga=GA1.1.576617952.1697654108; _ga_5C4RB337FM=GS1.1.1697654108.1.1.1697655679.0.0.0',
        'Origin':
        'https://x.dogenet.win',
        'Pragma':
        'no-cache',
        'Referer':
        'https://x.dogenet.win/pay',
        'Sec-Ch-Ua':
        '"Chromium";v="118", "Microsoft Edge";v="118", "Not=A?Brand";v="99"',
        'Sec-Ch-Ua-Mobile':
        '?0',
        'Sec-Ch-Ua-Platform':
        '"Windows"',
        'Sec-Fetch-Dest':
        'empty',
        'Sec-Fetch-Mode':
        'cors',
        'Sec-Fetch-Site':
        'same-origin',
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.2088.46'
    }
