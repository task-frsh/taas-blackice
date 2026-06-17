"""TAAS 결빙(블랙아이스) 교통사고 분석 — Streamlit.

data/blackice.csv (실데이터)를 읽어 지도+차트+표로 보여준다.
실데이터가 없으면 data/sample_blackice.csv 로 폴백한다.
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import pydeck as pdk
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
REAL_PATH = DATA_DIR / "blackice.csv"
SAMPLE_PATH = DATA_DIR / "sample_blackice.csv"


@st.cache_data
def load_data() -> tuple[pd.DataFrame, bool]:
    """실데이터 우선 로드. 없으면 샘플. (df, is_real) 반환."""
    if REAL_PATH.exists():
        df = pd.read_csv(REAL_PATH)
        is_real = True
    else:
        df = pd.read_csv(SAMPLE_PATH)
        is_real = False

    # 스키마 정규화: 시도 컬럼 보장
    if "시도" not in df.columns:
        if "시도시군구" in df.columns:
            df["시도"] = df["시도시군구"].astype(str).str.split().str[0]
        else:
            df["시도"] = "미상"
    return df, is_real


def render_map(df: pd.DataFrame) -> None:
    st.subheader("🗺️ 결빙사고 다발지역 지도")
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position="[경도, 위도]",
        get_radius="발생건수 * 1200 + 600",
        get_fill_color="[220, 50, 50, 160]",
        pickable=True,
    )
    view = pdk.ViewState(latitude=36.8, longitude=127.8, zoom=6.3)
    tooltip = {
        "html": "<b>{지점명}</b><br/>발생 {발생건수}건 · 사상자 {사상자수}명<br/>"
                "사망 {사망자수} · 중상 {중상자수} · 경상 {경상자수}",
        "style": {"backgroundColor": "#1a1a1a", "color": "white"},
    }
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, tooltip=tooltip))


def render_ranking(df: pd.DataFrame) -> None:
    st.subheader("📊 지역별 순위")
    col1, col2 = st.columns(2)
    with col1:
        by_sido = df.groupby("시도")["발생건수"].sum().sort_values(ascending=False).reset_index()
        fig = px.bar(by_sido, x="발생건수", y="시도", orientation="h", title="시도별 발생건수")
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        top10 = df.sort_values("사상자수", ascending=False).head(10)
        fig2 = px.bar(top10, x="사상자수", y="지점명", orientation="h", title="사상자 Top 10 지점")
        fig2.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig2, use_container_width=True)


def render_table(df: pd.DataFrame) -> None:
    st.subheader("📋 원본 데이터")
    keyword = st.text_input("지점/지역 검색", placeholder="예: 고속도로, 경기")
    cols = [c for c in ["연도", "지점명", "시도", "발생건수", "사상자수",
                        "사망자수", "중상자수", "경상자수", "위도", "경도"] if c in df.columns]
    view = df[cols]
    if keyword:
        mask = df.apply(lambda r: keyword in str(r.get("지점명", "")) or keyword in str(r.get("시도", "")), axis=1)
        view = df.loc[mask, cols]
    st.dataframe(view, use_container_width=True, hide_index=True)


def main() -> None:
    st.set_page_config(page_title="결빙사고 분석 | TAAS", page_icon="🧊", layout="wide")
    st.title("🧊 결빙(블랙아이스) 교통사고 다발지역 분석")

    df, is_real = load_data()

    # 연도 필터 (실데이터에 연도 있을 때)
    if "연도" in df.columns:
        years = sorted(df["연도"].astype(str).unique(), reverse=True)
        picked = st.multiselect("연도 선택", years, default=years)
        if picked:
            df = df[df["연도"].astype(str).isin(picked)]
        st.caption(f"데이터 기준연도: {', '.join(years)} · 출처: 도로교통공단 TAAS")
    if not is_real:
        st.warning("⚠️ 샘플 데이터입니다. data/blackice.csv 수집 후 자동으로 실데이터로 전환됩니다.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("다발지역 수", f"{len(df):,}곳")
    c2.metric("총 발생건수", f"{df['발생건수'].sum():,}건")
    c3.metric("총 사상자", f"{df['사상자수'].sum():,}명")
    c4.metric("총 사망자", f"{df['사망자수'].sum():,}명")

    st.divider()
    render_map(df)
    st.divider()
    render_ranking(df)
    st.divider()
    render_table(df)

    st.divider()
    st.caption("출처: 도로교통공단 TAAS / 공공데이터포털(data.go.kr) · 공공데이터 이용약관에 따른 출처표시. "
               "본 사이트는 참고용이며 통계 해석의 책임은 이용자에게 있습니다.")


if __name__ == "__main__":
    main()
