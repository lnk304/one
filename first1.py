import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# CSV 파일 읽기 (EUC-KR 인코딩)
file_path = "202505_202505_연령별인구현황_월간 (1).csv"
df = pd.read_csv(file_path, encoding='euc-kr')

# 데이터 전처리
df = df.rename(columns=lambda x: x.strip())

# 연령별 컬럼만 추출 (2025년05월_계_로 시작하는 열)
age_columns = [col for col in df.columns if col.startswith('2025년05월_계_')]
# 연령 숫자만 남기기 (예: '2025년05월_계_0세' → '0')
age_mapping = {col: col.replace('2025년05월_계_', '').replace('세', '') for col in age_columns}
df = df.rename(columns=age_mapping)

# 총인구수 및 행정구역 관련 열
df = df.rename(columns={'2025년05월_계_총인구수': '총인구수'})

# 총인구수 기준 상위 5개 지역 추출
top5_df = df.nlargest(5, '총인구수')

# 연령별 인구 데이터만 추출
ages = list(age_mapping.values())
age_df = top5_df[['행정구역'] + ages].set_index('행정구역').T

# UI 설명
st.subheader("연령별 인구 추이 (상위 5개 행정구역)")
st.line_chart(age_df)

# 데이터 보기
st.subheader("원본 데이터")
st.dataframe(df)
