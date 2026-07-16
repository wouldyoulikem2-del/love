import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# 1. 페이지 기본 설정
st.set_page_config(page_title="FAI Analyzer", page_icon="📊", layout="wide")
st.title("📊 FAI Analyzer : 금융 접근성 평가 시스템")
st.markdown("사용자가 직접 지역 데이터와 가중치를 조정하여 금융 접근성을 평가하는 의사결정 지원 시스템입니다.")

# 2. UI 레이아웃 (2단 분할)
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 지역 데이터 입력")
    val_pop = st.slider('접근가능 인구비율', 0.0, 2.0, 0.40)
    val_elder = st.slider('노인 접근가능비율', 0.0, 2.0, 0.40)
    val_biz = st.slider('사업체 접근율', 0.0, 3.0, 1.99)
    val_worker = st.slider('종사자 접근율', 0.0, 3.0, 1.50)

with col2:
    st.subheader("⚖️ 가중치 설정 (실시간 반영)")
    wt_pop = st.slider('주민 가중치(%)', 0, 100, 35)
    wt_elder = st.slider('노인 가중치(%)', 0, 100, 35)
    wt_biz = st.slider('사업체 가중치(%)', 0, 100, 15)
    wt_worker = st.slider('종사자 가중치(%)', 0, 100, 15)

# 3. FAI 계산
total_wt = wt_pop + wt_elder + wt_biz + wt_worker
if total_wt == 0: total_wt = 1
w1, w2, w3, w4 = wt_pop/total_wt, wt_elder/total_wt, wt_biz/total_wt, wt_worker/total_wt

fai = (val_pop * w1) + (val_elder * w2) + (val_biz * w3) + (val_worker * w4)

# 4. 결과 출력
st.divider()
st.subheader("📈 분석 결과")

stars = "★★★★★" if fai >= 0.8 else "★★★★☆" if fai >= 0.6 else "★★★☆☆" if fai >= 0.4 else "★★☆☆☆" if fai >= 0.2 else "★☆☆☆☆"
st.markdown(f"### 최종 FAI 점수 : **{fai:.3f}** {stars}")

# 5. 그래프 영역 (2단 분할)
graph_col1, graph_col2 = st.columns(2)

with graph_col1:
    # 막대 그래프 (서울/광주 비교)
    df_bar = pd.DataFrame({
        '지역': ['입력지역', '서울 중구', '광주 동구'],
        'FAI': [fai, 0.678, 0.804]
    })
    fig_bar = go.Figure(data=[go.Bar(x=df_bar['지역'], y=df_bar['FAI'], marker_color=['#3498db', '#95a5a6', '#2ecc71'])])
    fig_bar.update_layout(title="주요 지역 FAI 비교", yaxis_title="FAI 점수", height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with graph_col2:
    # 레이더 차트
    categories = ['접근가능인구', '노인접근', '사업체접근', '종사자접근']
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=[val_pop, val_elder, val_biz, val_worker],
        theta=categories,
        fill='toself',
        name='입력지역',
        line_color='#2980b9'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 3])),
        showlegend=False,
        title="세부 지표 레이더 차트",
        height=400
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# 6. 정책 제안 자동 생성
st.subheader("💡 맞춤형 정책 제안")
policies_found = False

if val_elder < 0.5:
    st.error("🔹 **노인 접근성 부족:** 이동 금융버스 정기 운영 및 경로당 연계 금융교육이 권장됩니다.")
    policies_found = True
if val_biz < 1.0:
    st.warning("🔹 **사업체 접근성 부족:** 기업 금융거점 확충 및 비대면 법인 서비스 인프라 지원이 필요합니다.")
    policies_found = True
if val_pop < 0.5:
    st.error("🔹 **주민 접근성 부족:** 생활권 내 우체국/편의점 연계 공동 금융거점 조성이 필요합니다.")
    policies_found = True
if val_worker < 1.0 and fai > 0.6:
    st.info("🔹 **종사자 접근성 부족:** 업무지구 내 직장인을 위한 점심/퇴근시간 연장 특화점포가 필요합니다.")
    policies_found = True

if not policies_found:
    st.success("🔹 현재 지표상 심각한 결점은 없으며, 현 금융 인프라 수준을 유지·보수하는 것을 권장합니다.")