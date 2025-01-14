import psycopg2

# PostgreSQL 연결 설정
DB_SETTINGS = {
    "dbname": "hwechang",
    "user": "hwechang",
    "password": "hwechang",
    "host": "10.0.1.160",
    "port": 5432
}

# 날씨 상태 데이터 (한글 설명 포함)
weather_descriptions = [
    {"id": 800, "main": "Clear", "description_en": "clear sky", "description_kr": "맑은 하늘"},
    {"id": 801, "main": "Clouds", "description_en": "few clouds", "description_kr": "구름 조금"},
    {"id": 802, "main": "Clouds", "description_en": "scattered clouds", "description_kr": "흩어진 구름"},
    {"id": 803, "main": "Clouds", "description_en": "broken clouds", "description_kr": "부서진 구름"},
    {"id": 804, "main": "Clouds", "description_en": "overcast clouds", "description_kr": "흐린 구름"},
    {"id": 500, "main": "Rain", "description_en": "light rain", "description_kr": "약한 비"},
    {"id": 501, "main": "Rain", "description_en": "moderate rain", "description_kr": "중간 정도의 비"},
    {"id": 502, "main": "Rain", "description_en": "heavy intensity rain", "description_kr": "강한 비"},
    {"id": 503, "main": "Rain", "description_en": "very heavy rain", "description_kr": "매우 강한 비"},
    {"id": 504, "main": "Rain", "description_en": "extreme rain", "description_kr": "극심한 비"},
    {"id": 511, "main": "Rain", "description_en": "freezing rain", "description_kr": "어는 비"},
    {"id": 520, "main": "Rain", "description_en": "shower rain", "description_kr": "소나기"},
    {"id": 600, "main": "Snow", "description_en": "light snow", "description_kr": "약한 눈"},
    {"id": 601, "main": "Snow", "description_en": "snow", "description_kr": "눈"},
    {"id": 602, "main": "Snow", "description_en": "heavy snow", "description_kr": "폭설"},
    {"id": 701, "main": "Atmosphere", "description_en": "mist", "description_kr": "옅은 안개"},
    {"id": 711, "main": "Atmosphere", "description_en": "smoke", "description_kr": "연기"},
    {"id": 721, "main": "Atmosphere", "description_en": "haze", "description_kr": "연무"},
    {"id": 731, "main": "Atmosphere", "description_en": "sand/ dust whirls", "description_kr": "모래/먼지 소용돌이"},
    {"id": 741, "main": "Atmosphere", "description_en": "fog", "description_kr": "안개"},
    {"id": 751, "main": "Atmosphere", "description_en": "sand", "description_kr": "모래"},
    {"id": 761, "main": "Atmosphere", "description_en": "dust", "description_kr": "먼지"},
    {"id": 762, "main": "Atmosphere", "description_en": "volcanic ash", "description_kr": "화산재"},
    {"id": 771, "main": "Atmosphere", "description_en": "squalls", "description_kr": "돌풍"},
    {"id": 781, "main": "Atmosphere", "description_en": "tornado", "description_kr": "토네이도"}
]

def create_table():
    """weather_descriptions 테이블 생성"""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS weather_descriptions (
        id INT PRIMARY KEY,
        main VARCHAR(50),
        description_en VARCHAR(100),
        description_kr VARCHAR(100)
    );
    """
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cur = conn.cursor()
        cur.execute(create_table_query)
        conn.commit()
        print("테이블 생성 완료.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"테이블 생성 중 오류 발생: {e}")

def insert_descriptions(data):
    """데이터를 weather_descriptions 테이블에 삽입"""
    insert_query = """
    INSERT INTO weather_descriptions (id, main, description_en, description_kr)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING;
    """
    try:
        conn = psycopg2.connect(**DB_SETTINGS)
        cur = conn.cursor()
        for item in data:
            cur.execute(insert_query, (item["id"], item["main"], item["description_en"], item["description_kr"]))
        conn.commit()
        print("데이터 삽입 완료.")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"데이터 삽입 중 오류 발생: {e}")

def main():
    """메인 함수"""
    create_table()
    insert_descriptions(weather_descriptions)

if __name__ == "__main__":
    main()
