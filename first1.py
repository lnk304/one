import streamlit as st
import pandas as pd

# 제목
st.title("2025년 5월 기준 연령별 인구 현황 분석")

# 데이터 불러오기 (EUC-KR 인코딩)
file_path = "./202505_202505_연령별인구현황_월간.csv"
df = pd.read_csv(file_path, encoding="euc-kr")

# 연령별 컬럼 전처리
age_cols = [col for col in df.columns if col.startswith("2025년05월_계_")]
df_age = df.copy()

# 연령 숫자만 컬럼명으로 추출
renamed_cols = {col: col.replace("2025년05월_계_", "") for col in age_cols}
df_age.rename(columns=renamed_cols, inplace=True)

# 총인구수 기준 상위 5개 행정구역 선택
top5_df = df_age.sort_values(by="총인구수", ascending=False).head(5)

# 연령별 인구 데이터만 추출
age_data = top5_df[renamed_cols.values()]
age_data.index = top5_df["행정구역"]  # 행정구역명을 index로 설정
age_data = age_data.transpose()  # 연령을 세로축으로, 인구를 가로축으로

# 그래프 표시
st.subheader("연령별 인구 추세 (상위 5개 지역)")
st.line_chart(age_data)

# 원본 데이터 표시
st.subheader("원본 데이터 (상위 5개 행정구역 기준)")
st.dataframe(top5_df)
