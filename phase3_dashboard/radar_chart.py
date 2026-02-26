# =============================================================================
# Phase 3 — Plotly 6각형 레이더 차트
# =============================================================================

import plotly.graph_objects as go


def build_radar_chart(category_scores: dict, title: str = "") -> go.Figure:
    """
    6각형 레이더 차트를 생성한다.

    Args:
        category_scores: {category_name: score (0-100)}
        title: 차트 제목 (선택)

    Returns:
        Plotly Figure
    """
    categories = list(category_scores.keys())
    values = [round(v) for v in category_scores.values()]

    # 폴리곤을 닫기 위해 첫 번째 항목 반복
    cats_closed = categories + [categories[0]]
    vals_closed = values + [values[0]]

    fig = go.Figure()

    # 기준선 — 50점 / 75점 참고용 (배경 채우기)
    fig.add_trace(
        go.Scatterpolar(
            r=[75] * (len(categories) + 1),
            theta=cats_closed,
            fill="toself",
            fillcolor="rgba(232, 232, 232, 0.25)",
            line=dict(color="rgba(200,200,200,0.4)", width=1, dash="dot"),
            hoverinfo="skip",
            showlegend=False,
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=[50] * (len(categories) + 1),
            theta=cats_closed,
            fill="toself",
            fillcolor="rgba(255, 255, 255, 0)",
            line=dict(color="rgba(200,200,200,0.3)", width=1, dash="dot"),
            hoverinfo="skip",
            showlegend=False,
        )
    )

    # 실제 점수 다각형
    fig.add_trace(
        go.Scatterpolar(
            r=vals_closed,
            theta=cats_closed,
            fill="toself",
            fillcolor="rgba(250, 93, 41, 0.15)",
            line=dict(color="#FA5D29", width=2.5),
            marker=dict(size=7, color="#FA5D29", symbol="circle"),
            name="역량 점수",
            hovertemplate="%{theta}<br><b>%{r}점</b><extra></extra>",
            showlegend=False,
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[25, 50, 75, 100],
                ticktext=["25", "50", "75", "100"],
                tickfont=dict(size=9, color="#AAAAAA"),
                gridcolor="#EEEEEE",
                linecolor="#EEEEEE",
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color="#333333", family="sans-serif"),
                linecolor="#DDDDDD",
                gridcolor="#EEEEEE",
            ),
            bgcolor="#FFFFFF",
        ),
        showlegend=False,
        title=dict(
            text=title,
            x=0.5,
            font=dict(size=14, color="#111111", family="sans-serif"),
        )
        if title
        else None,
        margin=dict(l=70, r=70, t=60 if title else 40, b=50),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        height=440,
    )

    return fig


def build_comparison_chart(before: dict, after: dict) -> go.Figure:
    """
    목표 전·후 비교 레이더 차트 (현재 vs 목표).

    Args:
        before: 현재 점수 {category_name: score}
        after:  목표 점수 {category_name: score}
    """
    categories = list(before.keys())
    cats_closed = categories + [categories[0]]

    before_vals = [round(before[c]) for c in categories] + [round(before[categories[0]])]
    after_vals = [round(after.get(c, 0)) for c in categories] + [round(after.get(categories[0], 0))]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=before_vals,
            theta=cats_closed,
            fill="toself",
            fillcolor="rgba(250, 93, 41, 0.12)",
            line=dict(color="#FA5D29", width=2),
            name="현재",
            hovertemplate="%{theta}<br>현재: %{r}점<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatterpolar(
            r=after_vals,
            theta=cats_closed,
            fill="toself",
            fillcolor="rgba(43, 192, 184, 0.12)",
            line=dict(color="#2BC0B8", width=2, dash="dash"),
            name="목표",
            hovertemplate="%{theta}<br>목표: %{r}점<extra></extra>",
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickvals=[25, 50, 75, 100],
                tickfont=dict(size=9, color="#AAAAAA"),
                gridcolor="#EEEEEE",
                linecolor="#EEEEEE",
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color="#333333"),
                gridcolor="#EEEEEE",
            ),
            bgcolor="#FFFFFF",
        ),
        showlegend=True,
        legend=dict(x=0.85, y=1.1, font=dict(size=12)),
        margin=dict(l=70, r=70, t=40, b=50),
        paper_bgcolor="#FFFFFF",
        height=440,
    )

    return fig
