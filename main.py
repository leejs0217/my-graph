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
# ==========================================
# 그래프 3
# 날짜별 10위권 일관객 합계 영역 그래프
# ==========================================

st.divider()

st.header("그래프 3. 날짜별 10위권 일관객 합계")

st.write(
    "매일 박스오피스 10위권 영화의 일관객을 모두 더해 "
    "날짜별 전체 관객 규모를 확인합니다."
)

# 날짜별 일관객 합계 계산
daily_total = (
    df.groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 일관객 합계가 가장 큰 날 TOP 3
top3_days = (
    daily_total
    .sort_values("일관객", ascending=False)
    .head(3)
    .sort_values("날짜")
)

# 영역 그래프
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="날짜별 10위권 일관객 합계",
    labels={
        "날짜": "날짜",
        "일관객": "10위권 일관객 합계"
    },
    hover_data={
        "날짜": "|%Y-%m-%d",
        "일관객": ":,.0f"
    }
)

# 영역 그래프 위에 TOP 3 날짜 표시
fig3.add_scatter(
    x=top3_days["날짜"],
    y=top3_days["일관객"],
    mode="markers+text",
    name="일관객 합계 TOP 3",
    text=[
        f"{date.strftime('%Y-%m-%d')}<br>{audience:,.0f}명"
        for date, audience in zip(
            top3_days["날짜"],
            top3_days["일관객"]
        )
    ],
    textposition="top center",
    marker=dict(
        size=11,
        color="red",
        line=dict(
            width=1,
            color="white"
        )
    ),
    hovertemplate=(
        "날짜: %{x|%Y-%m-%d}<br>"
        "10위권 일관객 합계: %{y:,.0f}명"
        "<extra></extra>"
    )
)

fig3.update_layout(
    hovermode="x unified",
    xaxis_title="날짜",
    yaxis_title="10위권 일관객 합계 (명)",
    height=600
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# 설명 작성 자리
st.subheader("이 그래프로 알 수 있는 것")

st.info(
    "여기에 이 그래프를 통해 알 수 있는 내용을 한 문장으로 작성하세요."
)

# TOP 3 날짜 표
st.caption("일관객 합계가 가장 컸던 날 TOP 3")

top3_display = top3_days.copy()
top3_display["날짜"] = top3_display["날짜"].dt.strftime("%Y-%m-%d")
top3_display["일관객"] = top3_display["일관객"].map(
    lambda x: f"{x:,.0f}명"
)

st.dataframe(
    top3_display,
    hide_index=True,
    use_container_width=True
)


# ==================================================
# # ==========================================
# 그래프 4
# 영화별 일관객 합계 TOP 10
# ==========================================

st.divider()

st.header("그래프 4. 영화별 일관객 합계 TOP 10")

st.write(
    "이 기간 동안 일관객 합계가 가장 큰 10편의 영화를 "
    "가로 막대그래프로 비교합니다."
)

# 영화별 일관객 합계와 10위권에 든 날수 계산
movie_summary = (
    df.groupby("영화명")
    .agg(
        일관객합계=("일관객", "sum"),
        10위권에_든_날수=("날짜", "nunique")
    )
    .reset_index()
)

# 일관객 합계가 큰 순서로 정렬 후 TOP 10
top10_movies = (
    movie_summary
    .sort_values("일관객합계", ascending=False)
    .head(10)
    .copy()
)

# 가로 막대그래프는 아래에서 위로 그려지므로
# 관객이 많은 영화가 위에 오도록 역순 정렬
top10_movies = top10_movies.sort_values(
    "일관객합계",
    ascending=True
)

# 가로 막대그래프
fig4 = px.bar(
    top10_movies,
    x="일관객합계",
    y="영화명",
    orientation="h",
    title="영화별 일관객 합계 TOP 10",
    labels={
        "일관객합계": "기간 내 일관객 합계",
        "영화명": "영화"
    },
    hover_data={
        "일관객합계": ":,.0f",
        "10위권에_든_날수": ":,.0f"
    }
)

# 마우스를 올렸을 때 표시되는 정보
fig4.update_traces(
    hovertemplate=(
        "영화: %{y}<br>"
        "기간 내 일관객 합계: %{x:,.0f}명<br>"
        "10위권에 든 날수: %{customdata[0]}일"
        "<extra></extra>"
    ),
    customdata=top10_movies[
        ["10위권에_든_날수"]
    ].values
)

fig4.update_layout(
    xaxis_title="기간 내 일관객 합계 (명)",
    yaxis_title="영화",
    height=600,
    yaxis=dict(
        categoryorder="total ascending"
    )
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# 설명 작성 자리
st.subheader("이 그래프로 알 수 있는 것")

st.info(
    "여기에 이 그래프를 통해 알 수 있는 내용을 한 문장으로 작성하세요."
)

# TOP 10 표
st.caption("일관객 합계 TOP 10 영화")

top10_display = top10_movies.sort_values(
    "일관객합계",
    ascending=False
).copy()

top10_display["일관객합계"] = top10_display[
    "일관객합계"
].map(lambda x: f"{x:,.0f}명")

top10_display = top10_display.rename(
    columns={
        "영화명": "영화",
        "일관객합계": "기간 내 일관객 합계",
        "10위권에_든_날수": "10위권에 든 날수"
    }
)

st.dataframe(
    top10_display,
    hide_index=True,
    use_container_width=True
)
