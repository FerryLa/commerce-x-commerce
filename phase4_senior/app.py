# =============================================================================
# Phase 4 — 시니어·주니어 지식 자산 네트워크 (Knowledge Graph 시각화)
# =============================================================================

import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

from phase4_senior.data import (
    NODES_DATA, EDGES_DATA, NODE_BY_ID,
    REGIONS, NODE_TYPES, NODE_COLORS, NODE_SIZES, get_badge,
)


def _build_graph(region_filter: str, type_filter: list[str]):
    """필터 조건에 따라 agraph Node/Edge 목록을 반환합니다."""
    # 표시할 노드 ID 결정
    visible_ids = set()
    for n in NODES_DATA:
        if "전체" not in type_filter and n["type"] not in type_filter:
            continue
        if region_filter != "전체":
            # Region 노드 자체는 필터 지역만 표시
            if n["type"] == "Region" and n.get("label") != region_filter:
                continue
            # Person 노드는 해당 지역만
            if n["type"] in ("Senior", "Junior") and n.get("region") != region_filter:
                continue
        visible_ids.add(n["id"])

    # 엣지가 연결하는 노드도 visible에 포함 (Skill/Problem은 연결된 경우만 표시)
    edge_visible = set()
    for e in EDGES_DATA:
        if e["source"] in visible_ids and e["target"] in visible_ids:
            edge_visible.add(e["source"])
            edge_visible.add(e["target"])
        elif e["source"] in visible_ids:
            t_node = NODE_BY_ID.get(e["target"], {})
            if t_node.get("type") in ("Skill", "Problem"):
                edge_visible.add(e["target"])
        elif e["target"] in visible_ids:
            s_node = NODE_BY_ID.get(e["source"], {})
            if s_node.get("type") in ("Skill", "Problem"):
                edge_visible.add(e["source"])

    final_ids = visible_ids | edge_visible

    nodes = []
    for n in NODES_DATA:
        if n["id"] not in final_ids:
            continue
        score = n.get("reputation_score", 0)
        badge = f" {get_badge(score)}" if score else ""
        nodes.append(
            Node(
                id=n["id"],
                label=n["label"] + badge if n["type"] == "Senior" else n["label"],
                size=NODE_SIZES.get(n["type"], 20),
                color=NODE_COLORS.get(n["type"], "#CCCCCC"),
                font={"size": 11, "color": "#333333"},
            )
        )

    edges = []
    for e in EDGES_DATA:
        if e["source"] in final_ids and e["target"] in final_ids:
            color = "#FF6B6B" if e["type"] == "MENTORED" else "#AAAAAA"
            edges.append(
                Edge(
                    source=e["source"],
                    target=e["target"],
                    label=e["label"],
                    color=color,
                    font={"size": 9, "color": "#666666"},
                )
            )

    return nodes, edges


def _reputation_panel(node_data: dict):
    """시니어 노드 선택 시 Reputation 점수 패널."""
    score = node_data.get("reputation_score", 0)
    badge = get_badge(score)
    contributions = node_data.get("contributions", [])

    st.markdown(f"### {node_data['name']} — 평판 점수")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("총 점수", f"{score}점", badge)
    with col2:
        st.progress(score / 100)

    if contributions:
        st.markdown("**기여 이벤트 내역**")
        for c in contributions:
            st.markdown(f"- {c['event']} → **+{c['score']}점**")


def _node_detail_panel(node_id: str):
    """선택된 노드의 상세 정보 패널."""
    n = NODE_BY_ID.get(node_id)
    if not n:
        return

    ntype = n["type"]
    color = NODE_COLORS.get(ntype, "#CCC")

    st.markdown(
        f"<div style='border-left:4px solid {color}; padding-left:12px;'>",
        unsafe_allow_html=True,
    )
    st.markdown(f"**유형**: `{ntype}`")

    if ntype == "Senior":
        st.markdown(f"**이름**: {n['name']} ({n['age']}세) | 지역: {n['region']}")
        st.markdown(f"**경력**: {', '.join(n['skills'])} {n['experience_years']}년")
        st.markdown(f"**소개**: {n['bio']}")
        st.divider()
        _reputation_panel(n)

    elif ntype == "Junior":
        st.markdown(f"**이름**: {n['name']} ({n['age']}세) | 지역: {n['region']}")
        st.markdown(f"**목표**: {n['goal']}")
        st.markdown(f"**현재 위기**: {n['crisis']}")
        st.markdown(f"**소개**: {n['bio']}")

    elif ntype == "Skill":
        st.markdown(f"**기술명**: {n['label']}")
        st.markdown(f"**수요 레벨**: {n.get('demand', '-')}")

    elif ntype == "Region":
        st.markdown(f"**지역**: {n['label']} ({n.get('province', '')})")

    elif ntype == "Problem":
        st.markdown(f"**문제**: {n['label']}")
        st.markdown(f"**심각도**: {n.get('severity', '-')}")

    st.markdown("</div>", unsafe_allow_html=True)


def render_network():
    st.title("🔗 시니어·주니어 지식 자산 네트워크")
    st.caption(
        "노인·청소년 일자리 정책 — 시니어의 무형자산을 데이터로 시각화합니다."
    )

    # ── 범례 ──────────────────────────────────────────────────────────────────
    with st.expander("노드 범례 보기", expanded=False):
        cols = st.columns(5)
        legend = [
            ("시니어", "#FF6B6B"),
            ("주니어", "#4ECDC4"),
            ("기술",   "#45B7D1"),
            ("지역",   "#96CEB4"),
            ("문제",   "#FFD93D"),
        ]
        for col, (name, color) in zip(cols, legend):
            col.markdown(
                f"<span style='background:{color};border-radius:50%;display:inline-block;"
                f"width:14px;height:14px;margin-right:4px;vertical-align:middle'></span> {name}",
                unsafe_allow_html=True,
            )

    # ── 사이드바 필터 ─────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("## 필터")
        region_filter = st.selectbox("지역", REGIONS)
        type_filter = st.multiselect(
            "노드 유형",
            NODE_TYPES[1:],  # "전체" 제외
            default=NODE_TYPES[1:],
        )
        if not type_filter:
            type_filter = NODE_TYPES[1:]

        st.divider()
        st.markdown("### 관계 유형 안내")
        rel_info = {
            "보유 기술": "시니어 → 기술 보유",
            "필요 기술": "주니어 → 기술 필요",
            "거주":     "인물 → 지역",
            "멘토링":   "시니어 → 주니어 (빨강)",
            "위기 상태": "주니어 → 문제",
            "해결 경험": "시니어 → 문제",
        }
        for k, v in rel_info.items():
            st.caption(f"**{k}**: {v}")

    # ── 그래프 렌더링 ─────────────────────────────────────────────────────────
    nodes, edges = _build_graph(region_filter, type_filter)

    config = Config(
        width=820,
        height=520,
        directed=True,
        physics=True,
        hierarchical=False,
        nodeHighlightBehavior=True,
        highlightColor="#F7A7A6",
        collapsible=False,
        node={"labelProperty": "label"},
        link={"labelProperty": "label", "renderLabel": True},
    )

    col_graph, col_detail = st.columns([3, 2])

    with col_graph:
        st.markdown("#### 지식 그래프")
        st.caption("노드를 클릭하면 상세 정보를 볼 수 있습니다.")
        selected = agraph(nodes=nodes, edges=edges, config=config)

    with col_detail:
        st.markdown("#### 노드 상세")
        if selected:
            _node_detail_panel(selected)
        else:
            st.info("그래프에서 노드를 클릭하세요.")
            _show_stats()


def _show_stats():
    """기본 상태: 전체 통계 요약."""
    seniors = [n for n in NODES_DATA if n["type"] == "Senior"]
    juniors = [n for n in NODES_DATA if n["type"] == "Junior"]
    mentored = [e for e in EDGES_DATA if e["type"] == "MENTORED"]
    avg_score = sum(s["reputation_score"] for s in seniors) / len(seniors)

    st.markdown("**네트워크 현황**")
    st.metric("등록 시니어", f"{len(seniors)}명")
    st.metric("등록 주니어", f"{len(juniors)}명")
    st.metric("멘토링 완료", f"{len(mentored)}건")
    st.metric("평균 평판 점수", f"{avg_score:.0f}점")
