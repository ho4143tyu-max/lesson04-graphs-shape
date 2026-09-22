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

# 숫자형 데이터로 변환
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

st.markdown("---")

st.subheader("이 그래프로 알 수 있는 것")

st.info(
    "여기에 장르별 영화의 총 관객 규모와 관객이 많은 영화를 보고 알 수 있는 특징을 한 문장으로 작성하세요."
)


# =========================================================
# 3. 총 관객 수 히스토그램
# =========================================================

st.header("3. 영화별 총 관객 수 분포")

fig3 = px.histogram(
    df,
    x="total_audi",
    nbins=20,
    title="영화별 총 관객 수 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    height=550,
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수",
    margin=dict(t=70, b=60, l=60, r=30)
)

st.plotly_chart(fig3, use_container_width=True)


# -----------------------------
# 히스토그램 분석 결과
# -----------------------------

# 관객이 가장 많은 영화 찾기
max_audience_index = df["total_audi"].idxmax()
max_movie = df.loc[max_audience_index, "movieNm"]
max_audience = df.loc[max_audience_index, "total_audi"]

# 가장 많은 영화가 속한 구간 계산
min_audience = df["total_audi"].min()
max_audience_value = df["total_audi"].max()

# 히스토그램과 동일한 20개 구간을 계산
bins = pd.cut(
    df["total_audi"],
    bins=20,
    include_lowest=True
)

bin_counts = bins.value_counts().sort_index()

most_common_bin = bin_counts.idxmax()

# 구간의 시작/끝 값
range_start = int(most_common_bin.left)
range_end = int(most_common_bin.right)


st.markdown("---")

st.subheader("이 그래프로 알 수 있는 것")

st.info(
    f"대부분의 영화는 총 관객 약 {range_start:,}명~{range_end:,}명 구간에 몰려 있으며, "
    f"가장 관객이 많은 영화는 「{max_movie}」로 총 {max_audience:,.0f}명의 관객을 기록했습니다."
)

# =========================================================
# 4. 개봉일 스크린 수와 총 관객의 관계
# =========================================================

st.header("4. 개봉일 스크린 수와 총 관객의 관계")

# 숫자형으로 변환
df["first_scrn"] = pd.to_numeric(
    df["first_scrn"],
    errors="coerce"
)

# 필요한 데이터가 있는 영화만 사용
scatter_df = df.dropna(
    subset=["first_scrn", "total_audi", "movieNm", "genre_first"]
)

fig4 = px.scatter(
    scatter_df,
    x="first_scrn",
    y="total_audi",
    color="genre_first",
    hover_name="movieNm",
    title="개봉일 스크린 수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린 수",
        "total_audi": "총 관객 수",
        "genre_first": "장르"
    }
)

fig4.update_traces(
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,.0f}개<br>"
        "총 관객: %{y:,.0f}명"
        "<extra></extra>"
    ),
    marker=dict(
        size=9,
        opacity=0.75
    )
)

fig4.update_layout(
    height=650,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="총 관객 수",
    margin=dict(t=70, b=60, l=60, r=30)
)

st.plotly_chart(fig4, use_container_width=True)


# -----------------------------
# 그래프 4 설명 구역
# -----------------------------

st.markdown("---")

st.subheader("이 그래프로 알 수 있는 것")

st.info(
    "개봉일 스크린 수와 총 관객 수가 어떤 관계를 보이는지 영화들의 분포를 통해 확인할 수 있습니다."
)
