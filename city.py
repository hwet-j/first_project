import requests

API_KEY = "04f67711de66ce8add24a0588fde4d61"
CITIES = [
    "Seoul", "Busan", "Incheon", "Daegu", "Daejeon",
	"Gwangju", "Ulsan", "Jeonju", "Changwon", "Suwon",
    "Goyang", "Yongin", "Ansan", "Pohang", "Yeosu",
	"Gimhae", "Cheongju", "Jeju", "Seongnam", "Mokpo"
]

def get_city_id(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["id"]
    else:
        print(f"City {city_name} not found.")
        return None

city_ids = []

for city in CITIES:
    city_id = get_city_id(city)
    if city_id:
        city_ids.append(city_id)

print("City IDs:", city_ids)
