import streamlit as st
import pandas as pd
import plotly.express as px


# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "1년간 박스오피스 10위권에 든 영화 중 이 기간에 개봉한 216편의 데이터를 "
    "이용하여 영화의 분포와 관계를 살펴봅니다."
)


# -----------------------------
# 데이터 불러오기
# -----------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/"
    "kobis_movies.csv"
)

df = pd.read_csv(DATA_URL)


# -----------------------------
# 데이터 전처리
# -----------------------------

# 여러 장르가 있는 경우 첫 번째 장르만 사용
df["genre_first"] = (
    df["genre"]
    .fillna("미상")
    .astype(str)
    .str.split("|")
    .str[0]
    .str.strip()
)

df["genre_first"] = df["genre_first"].replace("", "미상")

# 총 관객 수 숫자로 변환
df["total_audi"] = pd.to_numeric(
    df["total_audi"],
    errors="coerce"
).fillna(0)


# =========================================================
# 1. 장르별 영화 편수
# =========================================================

st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre_first"]
    .value_counts()
    .reset_index()
)

genre_counts.columns = ["장르", "영화 편수"]


fig1 = px.pie(
    genre_counts,
    names="장르",
    values="영화 편수",
    hole=0.55,
    title="장르별 영화 편수"
)

fig1.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    ),
    textposition="inside",
    textinfo="percent"
)

fig1.update_layout(
    height=550,
    margin=dict(t=70, b=30, l=30, r=30)
)

st.plotly_chart(fig1, use_container_width=True)


# -----------------------------
# 그래프 1 설명 구역
# -----------------------------
st.markdown("---")

st.subheader("이 그래프로 알 수 있는 것")

st.info(
    "여기에 장르별 영화 편수와 비율을 보고 알 수 있는 특징을 한 문장으로 작성하세요."
)


# =========================================================
# 2. 장르별 영화 트리맵
# =========================================================

st.header("2. 장르별 영화와 총 관객")

st.write(
    "각 장르 안에 해당 장르의 영화가 배치되며, "
    "칸의 크기는 총 관객 수를 나타냅니다."
)


fig2 = px.treemap(
    df,
    path=["genre_first", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객 트리맵"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    height=700,
    margin=dict(t=70, b=30, l=30, r=30)
)

st.plotly_chart(fig2, use_container_width=True)


# -----------------------------
# 그래프 2 설명 구역
# -----------------------------
st.markdown("---")

st.subheader("이 그래프로 알 수 있는 것")

st.info(
    "여기에 장르별 영화의 총 관객 규모와 관객이 많은 영화를 보고 알 수 있는 특징을 한 문장으로 작성하세요."
)
