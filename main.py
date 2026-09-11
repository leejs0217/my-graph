import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide",
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("1년치 일별 박스오피스 데이터를 이용해 영화의 흥행 흐름을 살펴봅니다.")


# --------------------------------------------------
# 데이터 불러오기
# --------------------------------------------------
DATA_URL = (
    "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜 열을 진짜 날짜형으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d",
    )

    # 숫자형 열을 숫자로 변환
    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    return df


df = load_data()


# ==================================================
# 그래프 1. 영화별 일관객 변화
# ==================================================
st.divider()
st.header("그래프 1. 영화별 일관객 변화")

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "영화를 선택하세요.",
    movie_list,
)

movie_df = (
    df[df["영화명"] == selected_movie]
    .sort_values("날짜")
    .copy()
)

fig1 = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"{selected_movie} - 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
    },
)

fig1.update_traces(
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig1.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
)

st.plotly_chart(
    fig1,
    width="stretch",
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 그래프에서 알 수 있는 내용을 작성하세요.")


# ==================================================
# 그래프 2. 일관객 합계가 가장 큰 영화 5편
# ==================================================
st.divider()
st.header("그래프 2. 일관객 합계가 가장 큰 영화 5편")

# 영화별 전체 기간 일관객 합계 계산
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)
)

# 영화명만 추출
top5_movie_names = top5_movies["영화명"].tolist()

# 상위 5편의 날짜별 일관객 데이터만 추출
top5_df = (
    df[df["영화명"].isin(top5_movie_names)]
    .sort_values(["영화명", "날짜"])
    .copy()
)

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계가 가장 큰 영화 5편의 날짜별 일관객",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화",
    },
)

fig2.update_traces(
    hovertemplate=(
        "영화: %{fullData.name}"
        "<br>날짜: %{x|%Y-%m-%d}"
        "<br>일관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    legend_title="영화",
)

st.plotly_chart(
    fig2,
    width="stretch",
)

st.markdown("**이 그래프로 알 수 있는 것**")
st.info("여기에 그래프에서 알 수 있는 내용을 작성하세요.")


# ==================================================
# 그래프 3. 앞으로 추가할 영역
# ==================================================
st.divider()
st.header("그래프 3")

st.info("앞으로 추가할 그래프 영역입니다.")


# ==================================================
# 그래프 4. 앞으로 추가할 영역
# ==================================================
st.divider()
st.header("그래프 4")

st.info("앞으로 추가할 그래프 영역입니다.")
