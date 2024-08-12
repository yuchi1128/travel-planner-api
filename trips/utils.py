import requests
import openai

# 緯度・経度を取得する関数
def get_lat_long(place_name, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': place_name,
        'key': api_key
    }
    response = requests.get(base_url, params=params)
    results = response.json().get('results')

    if results:
        location = results[0]['geometry']['location']
        return location['lat'], location['lng']
    return None, None

# 天気予報を取得する関数
def get_weather_forecast(lat, lon, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'lat': lat,
        'lon': lon,
        'units': 'metric',
        'appid': api_key
    }
    response = requests.get(base_url, params=params)
    return response.json()

# AIによる旅行プランを生成する関数
# def generate_travel_plan(destination, weather, days, openai_key):
#     openai.api_key = openai_key

#     prompt = f"Generate a {days}-day travel plan for {destination} considering the following weather forecast: {weather}. Make it detailed and engaging."
    
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=150
#     )
    
#     return response.choices[0].text.strip()
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def generate_travel_plan(destination, weather, days):
    """
    GPT-2を使用して旅行プランを生成します。

    Parameters:
    - destination: 旅行先の名前
    - weather: 天気予報の概要
    - days: 旅行日数

    Returns:
    - 生成された旅行プランのテキスト
    """

    # GPT-2のモデルとトークナイザーをロード
    model_name = 'gpt2'
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # プロンプトを作成
    prompt = f"Create a {days}-day travel plan for {destination} considering the following weather forecast: {weather}. The plan should include detailed daily activities."

    # トークン化
    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)

    # テキスト生成
    outputs = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2, early_stopping=True)

    # 生成されたテキストをデコード
    plan = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return plan