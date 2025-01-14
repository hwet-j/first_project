import requests
import psycopg2
from datetime import datetime

# OpenWeather API 설정
API_KEY = "04f67711de66ce8add24a0588fde4d61"  # OpenWeather에서 발급받은 API 키
BASE_URL = "https://api.openweathermap.org/data/2.5/group"

# PostgreSQL 연결 설정
DB_SETTINGS = {
    "dbname": "hwechang",
    "user": "hwechang",
    "password": "hwechang",
    "host": "10.0.1.160",
    "port": 5432
}

def create_table():
    """PostgreSQL에 weather_data 테이블을 생성합니다."""
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cur = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            city VARCHAR(50),
            temperature FLOAT,
            humidity INT,
            description VARCHAR(100),
            timestamp TIMESTAMP
        );
        """
        cur.execute(create_table_query)
        conn.commit()
        print("테이블이 성공적으로 생성되었습니다.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"테이블 생성 중 오류 발생: {e}")

def fetch_weather_data_for_cities(city_ids):
    """여러 도시의 날씨 데이터를 가져옵니다."""
    ids = ",".join(map(str, city_ids))
    url = f"{BASE_URL}?id={ids}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_data = []
        returned_ids = {city["id"] for city in data["list"]}

        for city in data["list"]:
            weather_data.append({
                "city": city["name"],
                "temperature": city["main"]["temp"],
                "humidity": city["main"]["humidity"],
                "description": city["weather"][0]["description"],
                "timestamp": datetime.now()
            })

        # 요청한 ID와 반환된 ID 비교
        requested_ids = set(city_ids)
        missing_ids = requested_ids - returned_ids
        if missing_ids:
            print(f"응답에 포함되지 않은 도시 ID: {missing_ids}")
        return weather_data
    else:
        print(f"API 요청 실패: {response.status_code}")
        return []

def save_weather_data_to_db(weather_list):
    """PostgreSQL에 다수의 날씨 데이터를 저장합니다."""
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cur = conn.cursor()
        insert_query = """
        INSERT INTO weather_data (city, temperature, humidity, description, timestamp)
        VALUES (%s, %s, %s, %s, %s)
        """
        for weather in weather_list:
            cur.execute(insert_query, (weather["city"], weather["temperature"], weather["humidity"], weather["description"], weather["timestamp"]))
        conn.commit()
        print(f"{len(weather_list)}개의 날씨 데이터가 저장되었습니다.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"데이터 저장 중 오류 발생: {e}")

def main():
    """메인 함수"""
    create_table()

    # 한국 주요 도시 20개의 ID
    korea_city_ids = [1835848, 1838524, 1843561, 1835327, 1835224,
                    1841811, 1833747, 1845457, 1846326, 1835553,
                    1842485, 1832427, 1846918, 1839071, 1832157,
                    1842943, 1845604, 1846266, 1897000, 1841066]

    weather_data = fetch_weather_data_for_cities(korea_city_ids)
    if weather_data:
        save_weather_data_to_db(weather_data)
    else:
        print("날씨 데이터를 가져오지 못했습니다.")

if __name__ == "__main__":
    main()
