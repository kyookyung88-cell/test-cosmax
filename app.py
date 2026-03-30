import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="시제품 개발 현황 대시보드", layout="wide")
st.title("🧪 시제품 개발 현황 대시보드")

uploaded_file = st.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx", "xls"])

if uploaded_file is not None:
    xls = pd.ExcelFile(uploaded_file, engine="openpyxl")
    df = pd.read_excel(xls, sheet_name="시제품정보")
    df["작성일"] = pd.to_datetime(df["작성일"])

    df_test = pd.read_excel(xls, sheet_name="안정성테스트결과")
    df_test["측정일"] = pd.to_datetime(df_test["측정일"])

    # ── 사이드바 필터 ──
    st.sidebar.header("필터")
    sel_type = st.sidebar.multiselect("제품유형", df["제품유형"].unique(), default=df["제품유형"].unique())
    sel_stage = st.sidebar.multiselect("개발단계", df["개발단계"].unique(), default=df["개발단계"].unique())
    sel_skin = st.sidebar.multiselect("목표피부타입", df["목표피부타입"].unique(), default=df["목표피부타입"].unique())

    st.sidebar.divider()
    st.sidebar.header("안정성테스트 필터")
    sel_condition = st.sidebar.multiselect("테스트조건", df_test["테스트조건"].unique(), default=df_test["테스트조건"].unique())
    sel_scent = st.sidebar.multiselect("향변화여부", df_test["향변화여부"].unique(), default=df_test["향변화여부"].unique())

    filtered = df[
        df["제품유형"].isin(sel_type)
        & df["개발단계"].isin(sel_stage)
        & df["목표피부타입"].isin(sel_skin)
    ]

    filtered_test = df_test[
        df_test["테스트조건"].isin(sel_condition)
        & df_test["향변화여부"].isin(sel_scent)
    ]

    # ══════════════════════════════════════════════
    # 탭 구성
    # ══════════════════════════════════════════════
    tab1, tab2 = st.tabs(["📋 시제품 현황", "🔬 안정성 테스트 분석"])

    # ── 탭 1: 시제품 현황 ──
    with tab1:
        # KPI 카드
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("총 시제품 수", f"{len(filtered)}건")
        c2.metric("제품유형 수", f"{filtered['제품유형'].nunique()}종")
        c3.metric("담당팀 수", f"{filtered['담당팀'].nunique()}팀")
        c4.metric("주요컨셉 수", f"{filtered['주요컨셉'].nunique()}개")

        st.divider()

        # 차트 Row 1
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("제품유형별 시제품 수")
            type_counts = filtered["제품유형"].value_counts().reset_index()
            type_counts.columns = ["제품유형", "건수"]
            fig1 = px.bar(type_counts, x="제품유형", y="건수", color="제품유형", text_auto=True)
            fig1.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            st.subheader("개발단계 분포")
            stage_counts = filtered["개발단계"].value_counts().reset_index()
            stage_counts.columns = ["개발단계", "건수"]
            fig2 = px.pie(stage_counts, names="개발단계", values="건수", hole=0.4)
            fig2.update_layout(height=350)
            st.plotly_chart(fig2, use_container_width=True)

        # 차트 Row 2
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("목표피부타입별 시제품 수")
            skin_counts = filtered["목표피부타입"].value_counts().reset_index()
            skin_counts.columns = ["목표피부타입", "건수"]
            fig3 = px.bar(skin_counts, x="목표피부타입", y="건수", color="목표피부타입", text_auto=True)
            fig3.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig3, use_container_width=True)
        with col4:
            st.subheader("제형별 시제품 수")
            form_counts = filtered["제형"].value_counts().reset_index()
            form_counts.columns = ["제형", "건수"]
            fig4 = px.pie(form_counts, names="제형", values="건수", hole=0.4)
            fig4.update_layout(height=350)
            st.plotly_chart(fig4, use_container_width=True)

        # 차트 Row 3
        col5, col6 = st.columns(2)
        with col5:
            st.subheader("주요컨셉 분포")
            concept_counts = filtered["주요컨셉"].value_counts().reset_index()
            concept_counts.columns = ["주요컨셉", "건수"]
            fig5 = px.bar(concept_counts, x="주요컨셉", y="건수", color="주요컨셉", text_auto=True)
            fig5.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig5, use_container_width=True)
        with col6:
            st.subheader("담당팀별 시제품 수")
            team_counts = filtered["담당팀"].value_counts().reset_index()
            team_counts.columns = ["담당팀", "건수"]
            fig6 = px.bar(team_counts, x="담당팀", y="건수", color="담당팀", text_auto=True)
            fig6.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig6, use_container_width=True)

        # 타임라인
        st.subheader("시제품 등록 타임라인")
        timeline = filtered.sort_values("작성일")
        fig7 = px.scatter(
            timeline, x="작성일", y="제품유형", color="개발단계",
            size_max=12, hover_data=["시제품코드", "제형", "주요컨셉", "담당팀"],
        )
        fig7.update_traces(marker=dict(size=14))
        fig7.update_layout(height=300)
        st.plotly_chart(fig7, use_container_width=True)

        # 원본 데이터
        st.subheader("원본 데이터")
        st.dataframe(filtered, use_container_width=True, hide_index=True)

    # ── 탭 2: 안정성 테스트 분석 ──
    with tab2:
        # KPI 카드
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("총 테스트 수", f"{len(filtered_test)}건")
        scent_y = len(filtered_test[filtered_test["향변화여부"] == "Y"])
        k2.metric("향 변화 발생", f"{scent_y}건")
        color_avg = filtered_test["색상변화등급"].mean()
        k3.metric("평균 색상변화등급", f"{color_avg:.1f}")
        pass_count = len(filtered_test[filtered_test["판정결과"] == "적합"])
        k4.metric("적합 판정", f"{pass_count}건")

        st.divider()

        # ── 핵심 차트: 향 변화 여부에 따른 색상변화등급 비교 ──
        st.subheader("향 변화 여부에 따른 색상변화등급 비교")
        col_a, col_b = st.columns(2)

        with col_a:
            # 박스플롯
            fig_box = px.box(
                filtered_test, x="향변화여부", y="색상변화등급",
                color="향변화여부",
                color_discrete_map={"Y": "#FF6B6B", "N": "#4ECDC4"},
                labels={"향변화여부": "향 변화 여부", "색상변화등급": "색상변화등급"},
                points="all",
            )
            fig_box.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_box, use_container_width=True)

        with col_b:
            # 평균 비교 막대 차트
            avg_by_scent = (
                filtered_test.groupby("향변화여부")["색상변화등급"]
                .mean()
                .reset_index()
            )
            avg_by_scent.columns = ["향변화여부", "평균 색상변화등급"]
            fig_avg = px.bar(
                avg_by_scent, x="향변화여부", y="평균 색상변화등급",
                color="향변화여부",
                color_discrete_map={"Y": "#FF6B6B", "N": "#4ECDC4"},
                text_auto=".2f",
            )
            fig_avg.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_avg, use_container_width=True)

        # ── 테스트조건별 향 변화 vs 색상변화등급 ──
        st.subheader("테스트조건별 향 변화 × 색상변화등급")
        fig_scatter = px.strip(
            filtered_test, x="테스트조건", y="색상변화등급",
            color="향변화여부",
            color_discrete_map={"Y": "#FF6B6B", "N": "#4ECDC4"},
            hover_data=["테스트ID", "시제품코드", "판정결과"],
        )
        fig_scatter.update_traces(marker=dict(size=10))
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True)

        # ── 히트맵: 테스트조건 × 향변화여부별 평균 색상변화등급 ──
        st.subheader("테스트조건 × 향변화여부 — 평균 색상변화등급 히트맵")
        heatmap_data = (
            filtered_test.groupby(["테스트조건", "향변화여부"])["색상변화등급"]
            .mean()
            .reset_index()
            .pivot(index="테스트조건", columns="향변화여부", values="색상변화등급")
        )
        fig_heat = px.imshow(
            heatmap_data,
            text_auto=".1f",
            color_continuous_scale="RdYlGn_r",
            labels=dict(x="향변화여부", y="테스트조건", color="평균 색상변화등급"),
            aspect="auto",
        )
        fig_heat.update_layout(height=350)
        st.plotly_chart(fig_heat, use_container_width=True)

        # ── 판정결과 분포 (향 변화 여부별) ──
        st.subheader("향 변화 여부별 판정결과 분포")
        judge_data = (
            filtered_test.groupby(["향변화여부", "판정결과"])
            .size()
            .reset_index(name="건수")
        )
        fig_judge = px.bar(
            judge_data, x="판정결과", y="건수",
            color="향변화여부",
            color_discrete_map={"Y": "#FF6B6B", "N": "#4ECDC4"},
            barmode="group", text_auto=True,
        )
        fig_judge.update_layout(height=400)
        st.plotly_chart(fig_judge, use_container_width=True)

        # 원본 데이터
        st.subheader("안정성 테스트 원본 데이터")
        st.dataframe(filtered_test, use_container_width=True, hide_index=True)

else:
    st.info("엑셀 파일(.xlsx)을 업로드하면 대시보드가 표시됩니다.")
