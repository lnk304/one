import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Streamlit 제목
st.title("🗺️ 2025년 5월 기준 연령별 인구 현황 지도 시각화")

# CSV 파일 로딩
df = pd.read_csv("202505_202505_연령별인구현황_월간.csv", encoding='euc-kr')

# 총인구수 처리
df['총인구수'] = df['2025년05월_계_총인구수'].str.replace(',', '').astype(int)

# 나이 컬럼 처리
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_') and ('세' in col or '100세 이상' in col)]
new_columns = []
for col in age_columns:
    if '100세 이상' in col:
        new_columns.append('100세 이상')
    else:
        new_columns.append(col.replace('2025년05월_계_', '').replace('세', '') + '세')

df_age = df[['행정구역', '총인구수'] + age_columns].copy()
df_age.columns = ['행정구역', '총인구수'] + new_columns

# 상위 5개 행정구역 추출
top5_df = df_age.sort_values(by='총인구수', ascending=False).head(5)

# 위도, 경도 매핑 예시 (상위 5개만 수동 지정)
location_dict = {
    '서울특별시': (37.5665, 126.9780),
    '부산광역시': (35.1796, 129.0756),
    '경기도': (37.4138, 127.5183),
    '인천광역시': (37.4563, 126.7052),
    '대구광역시': (35.8714, 128.6014),
    # 필요 시 다른 지역 추가
}

# 지도 생성 (기본 위치는 서울)
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 마커 추가
for _, row in top5_df.iterrows():
    region = row['행정구역']
    population = row['총인구수']
    
    if region in location_dict:
        lat, lon = location_dict[region]
        folium.CircleMarker(
            location=(lat, lon),
            radius=population / 1000000,  # 인구수에 따라 반지름 조정
            color='blue',
            fill=True,
            fill_opacity=0.4,
            popup=f"{region}<br>총인구수: {population:,}명",
        ).add_to(m)

# 지도 출력
st.subheader("🗺️ 상위 5개 행정구역 인구 분포 (원형 마커)")
folium_static(m)
