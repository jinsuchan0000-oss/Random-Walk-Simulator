import streamlit as st
import random
import math
import matplotlib.pyplot as plt
import time

# 1. 웹사이트 기본 설정
st.set_page_config(page_title="N차원 랜덤 워크 시뮬레이터", layout="wide")

# 2. 배경, 글자 크기, 워터마크 CSS 적용 (모든 입력창 라벨 가시성 완벽 해결)
st.markdown("""
    <style>
    /* 수학적이고 은은한 모눈종이(Graph paper) 배경 */
    .stApp { 
        background-color: #121212; 
        background-image: 
            linear-gradient(rgba(255,255,255,0.05) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.05) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #F0F0F0;
    }
    
    /* 전체 글자 기본 크기 */
    html, body, [class*="css"] {
        font-size: 1.15rem;
        font-weight: 400;
    }

    /* 부제목 가시성 개선 */
    .subtitle-text {
        font-size: 1.35rem;
        font-weight: 600;
        color: #FFFFFF;
        margin-bottom: 20px;
    }

    /* [수정] 차원 선택 등 일반 위젯 라벨 */
    div[data-testid="stWidgetLabel"] p {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
    }

    /* [추가] 이동 횟수, 반복 횟수 숫자 입력창 라벨 명확하게 타겟팅 */
    div[data-testid="stNumberInput"] label p {
        font-size: 1.5rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
    }
    
    /* 라디오 버튼 내부 텍스트(1차원, 2차원 등) */
    .stRadio label p {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #FFFFFF !important;
    }

    /* MADE BY JERRY 워터마크 (크기 2배) */
    .watermark {
        position: fixed;
        bottom: 15px;
        right: 20px;
        font-size: 28px;
        font-weight: bold;
        color: rgba(255, 255, 255, 0.4);
        z-index: 9999;
        pointer-events: none;
    }
    </style>
    <div class="watermark">MADE BY JERRY</div>
""", unsafe_allow_html=True)

st.title("🎲 N차원 랜덤 워크 시뮬레이터")
st.markdown('<p class="subtitle-text">입자들의 무작위 확산 과정을 시각화하고, <b>실험값과 이론값을 통계적으로 비교</b>합니다.</p>', unsafe_allow_html=True)
st.divider()

# 3. 입력 단계
col_dim, col_n, col_rep = st.columns(3)
with col_dim:
    차원 = st.radio("차원 선택", ["1차원", "2차원", "3차원"], horizontal=True)
with col_n:
    횟수 = st.number_input("이동 횟수 (N)", min_value=1, max_value=1000000, value=100)
with col_rep:
    반복 = st.number_input("시뮬레이션 반복 횟수", min_value=1, max_value=1000000, value=100)

시각화 = False
if 차원 in ["2차원", "3차원"]:
    vis_col1, vis_col2 = st.columns([1, 4])
    with vis_col1:
        시각화 = st.checkbox("시각화 활성화", value=True)
    with vis_col2:
        st.warning("⚠️ 주의: 시각화 시 처리하는 데 더 많은 시간이 소요됩니다.")

if 횟수 * 반복 >= 1000000000:
    st.error("🚨 주의: 이동 횟수와 반복 횟수의 곱이 매우 커 오랜 시간이 소요되거나 원활한 작동이 되지 않을 수 있습니다.")

st.divider()

# 4. 실행 버튼 및 로직
if st.button("🚀 시뮬레이션 실행", type="primary"):
    
    progress_text = "시뮬레이션 연산 중입니다... 잠시만 기다려주세요."
    my_bar = st.progress(0, text=progress_text)
    
    # ---------------------------------------------------------
    # [1차원 코딩]
    # ---------------------------------------------------------
    if 차원 == "1차원":
        최종위치 = []
        for i in range(반복):
            위치 = 0
            for _ in range(횟수):
                이동 = random.choice([-1, 1])
                위치 += 이동
            최종위치.append(위치)
            
            if i % max(1, 반복 // 100) == 0:
                my_bar.progress(i / 반복, text=progress_text)
                
        my_bar.progress(1.0, text="연산 완료!")
        
        실험적_평균 = sum(최종위치) / 반복
        실험적_분산 = sum((변량 - 실험적_평균) ** 2 for 변량 in 최종위치) / 반복
        실험적_표준편차 = math.sqrt(실험적_분산)
        이론적_분산 = 횟수
        이론적_표준편차 = math.sqrt(횟수)
        
        오차율 = abs(실험적_표준편차 - 이론적_표준편차) / 이론적_표준편차 * 100 if 이론적_표준편차 != 0 else 0
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.markdown("### 🧪 실험적 데이터")
            st.markdown(f"**실험적 평균:** {실험적_평균:.2f}")
            st.markdown(f"**실험적 평균제곱변위 [MSD] (분산):** {실험적_분산:.2f}")
            st.markdown(f"**실험적 확산정도 [RMSD] (표준편차):** {실험적_표준편차:.2f}")
            
        with res_col2:
            st.markdown("### 📐 이론적 데이터")
            st.markdown("**이론적 평균:** 0.00")
            st.markdown(f"**이론적 평균제곱변위 [MSD]:** {이론적_분산:.2f} $(N)$")
            st.markdown(f"**이론적 확산정도 [RMSD]:** {이론적_표준편차:.2f} $(\sqrt{{N}})$")
            
        st.divider()
        st.markdown(f"<h3 style='text-align: center; color: #FF4B4B;'>🎯 오차율 (RMSD 기준): {오차율:.2f} %</h3>", unsafe_allow_html=True)


    # ---------------------------------------------------------
    # [2차원 코딩]
    # ---------------------------------------------------------
    elif 차원 == "2차원":
        최종_x좌표_위치 = []
        최종_y좌표_위치 = []
        
        if 시각화:
            fig = plt.figure(figsize=(10, 8))
            fig.patch.set_alpha(0.0)
            ax = fig.add_subplot(111)
            ax.set_facecolor('#1E1E1E')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_edgecolor('white')

        for i in range(반복):
            x좌표, y좌표 = 0, 0
            if 시각화:
                x좌표_목록, y좌표_목록 = [0], [0]
                
            for _ in range(횟수):
                x좌표_이동 = random.choice([-1, 1, 0, 0])
                x좌표 += x좌표_이동
                if x좌표_이동 == 0:
                    y좌표_이동 = random.choice([-1, 1])
                    y좌표 += y좌표_이동
                
                if 시각화:
                    x좌표_목록.append(x좌표)
                    y좌표_목록.append(y좌표)
                    
            최종_x좌표_위치.append(x좌표)
            최종_y좌표_위치.append(y좌표)
            
            if 시각화:
                궤적 = ax.plot(x좌표_목록, y좌표_목록, alpha=0.3)
                선_색상 = 궤적[0].get_color()
                ax.plot(x좌표, y좌표, marker='o', markersize=6, color=선_색상)
                
            if i % max(1, 반복 // 100) == 0:
                my_bar.progress(i / 반복, text=progress_text)
                
        my_bar.progress(1.0, text="연산 완료!")

        실험적_평균_x위치 = sum(최종_x좌표_위치) / 반복
        실험적_평균_y위치 = sum(최종_y좌표_위치) / 반복
        실험적_평균_위치의_거리 = math.sqrt(실험적_평균_x위치**2 + 실험적_평균_y위치**2)
        실험적_평균_거리 = sum(math.sqrt(x**2 + y**2) for x, y in zip(최종_x좌표_위치, 최종_y좌표_위치)) / 반복
        실험적_x위치의_분산 = sum((x - 실험적_평균_x위치)**2 for x in 최종_x좌표_위치) / 반복
        실험적_y위치의_분산 = sum((y - 실험적_평균_y위치)**2 for y in 최종_y좌표_위치) / 반복
        실험적_평균제곱변위 = 실험적_x위치의_분산 + 실험적_y위치의_분산
        실험적_제곱근_평균제곱변위 = math.sqrt(실험적_평균제곱변위)
        
        이론적_평균제곱변위 = 횟수
        이론적_제곱근_평균제곱변위 = math.sqrt(횟수)
        
        오차율 = abs(실험적_제곱근_평균제곱변위 - 이론적_제곱근_평균제곱변위) / 이론적_제곱근_평균제곱변위 * 100 if 이론적_제곱근_평균제곱변위 != 0 else 0

        if 시각화:
            ax.plot(0, 0, marker='X', color='white', markersize=12, label='Start (0,0)')
            ax.set_title(f'2D Random Walk (N={횟수}, {반복}times)', color='white')
            ax.set_xlabel('X Coordinate', color='white')
            ax.set_ylabel('Y Coordinate', color='white')
            ax.legend(facecolor='#1E1E1E', labelcolor='white')
            ax.grid(True, color='gray', alpha=0.3)
            
            vis_res1, vis_res2 = st.columns([1.2, 1])
            with vis_res1:
                st.pyplot(fig)
            with vis_res2:
                st.markdown("### 🧪 실험적 데이터")
                st.markdown(f"**평균 위치 (x,y):** ({실험적_평균_x위치:.2f}, {실험적_평균_y위치:.2f})")
                st.markdown(f"**평균 위치의 거리:** {실험적_평균_위치의_거리:.2f}")
                st.markdown(f"**평균 거리:** {실험적_평균_거리:.2f}")
                st.markdown(f"**평균제곱변위 [MSD]:** {실험적_평균제곱변위:.2f}")
                st.markdown(f"**확산 정도 [RMSD]:** {실험적_제곱근_평균제곱변위:.2f}")
                
                st.markdown("### 📐 이론적 데이터")
                st.markdown("**평균 위치 (x,y):** (0.00, 0.00)")
                st.markdown("**평균 위치의 거리:** 0.00")
                이론_거리 = math.sqrt((math.pi * 횟수) / 4)
                st.markdown(f"**평균 거리:** {이론_거리:.2f} $(\sqrt{{\\frac{{\pi \\times N}}{4}}})$")
                st.markdown(f"**평균제곱변위 [MSD]:** {이론적_평균제곱변위:.2f} $(N)$")
                st.markdown(f"**확산 정도 [RMSD]:** {이론적_제곱근_평균제곱변위:.2f} $(\sqrt{{N}})$")
                
                st.divider()
                st.markdown(f"<h3 style='text-align: center; color: #FF4B4B;'>🎯 오차율 (RMSD 기준): {오차율:.2f} %</h3>", unsafe_allow_html=True)
                
        else:
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown("### 🧪 실험적 데이터")
                st.markdown(f"**평균 위치 (x,y):** ({실험적_평균_x위치:.2f}, {실험적_평균_y위치:.2f})")
                st.markdown(f"**평균 위치의 거리:** {실험적_평균_위치의_거리:.2f}")
                st.markdown(f"**평균 거리:** {실험적_평균_거리:.2f}")
                st.markdown(f"**평균제곱변위 [MSD]:** {실험적_평균제곱변위:.2f}")
                st.markdown(f"**확산 정도 [RMSD]:** {실험적_제곱근_평균제곱변위:.2f}")
            with res_col2:
                st.markdown("### 📐 이론적 데이터")
                st.markdown("**평균 위치 (x,y):** (0.00, 0.00)")
                st.markdown("**평균 위치의 거리:** 0.00")
                이론_거리 = math.sqrt((math.pi * 횟수) / 4)
                st.markdown(f"**평균 거리:** {이론_거리:.2f} $(\sqrt{{\\frac{{\pi \\times N}}{4}}})$")
                st.markdown(f"**평균제곱변위 [MSD]:** {이론적_평균제곱변위:.2f} $(N)$")
                st.markdown(f"**확산 정도 [RMSD]:** {이론적_제곱근_평균제곱변위:.2f} $(\sqrt{{N}})$")
            st.divider()
            st.markdown(f"<h3 style='text-align: center; color: #FF4B4B;'>🎯 오차율 (RMSD 기준): {오차율:.2f} %</h3>", unsafe_allow_html=True)


    # ---------------------------------------------------------
    # [3차원 코딩]
    # ---------------------------------------------------------
    elif 차원 == "3차원":
        최종_x좌표_위치 = []
        최종_y좌표_위치 = []
        최종_z좌표_위치 = []
        
        if 시각화:
            fig = plt.figure(figsize=(10, 10))
            fig.patch.set_alpha(0.0)
            ax = fig.add_subplot(projection='3d')
            ax.set_facecolor('#1E1E1E')
            ax.xaxis.set_tick_params(colors='white')
            ax.yaxis.set_tick_params(colors='white')
            ax.zaxis.set_tick_params(colors='white')

        for i in range(반복):
            x좌표, y좌표, z좌표 = 0, 0, 0
            if 시각화:
                x좌표_목록, y좌표_목록, z좌표_목록 = [0], [0], [0]
                
            for _ in range(횟수):
                x좌표_이동 = random.choice([-1, 1, 0, 0, 0, 0])
                x좌표 += x좌표_이동
                if x좌표_이동 == 0:
                    y좌표_이동 = random.choice([-1, 1, 0, 0])
                    y좌표 += y좌표_이동
                    if y좌표_이동 == 0:
                        z좌표_이동 = random.choice([-1, 1])
                        z좌표 += z좌표_이동
                
                if 시각화:
                    x좌표_목록.append(x좌표)
                    y좌표_목록.append(y좌표)
                    z좌표_목록.append(z좌표)
                    
            최종_x좌표_위치.append(x좌표)
            최종_y좌표_위치.append(y좌표)
            최종_z좌표_위치.append(z좌표)
            
            if 시각화:
                궤적 = ax.plot(x좌표_목록, y좌표_목록, z좌표_목록, alpha=0.3)
                선_색상 = 궤적[0].get_color()
                ax.scatter(x좌표, y좌표, z좌표, color=선_색상, marker='o', s=15)
                
            if i % max(1, 반복 // 100) == 0:
                my_bar.progress(i / 반복, text=progress_text)
                
        my_bar.progress(1.0, text="연산 완료!")

        실험적_평균_x위치 = sum(최종_x좌표_위치) / 반복
        실험적_평균_y위치 = sum(최종_y좌표_위치) / 반복
        실험적_평균_z위치 = sum(최종_z좌표_위치) / 반복
        실험적_평균_위치의_거리 = math.sqrt(실험적_평균_x위치**2 + 실험적_평균_y위치**2 + 실험적_평균_z위치**2)
        실험적_평균_거리 = sum(math.sqrt(x**2 + y**2 + z**2) for x, y, z in zip(최종_x좌표_위치, 최종_y좌표_위치, 최종_z좌표_위치)) / 반복
        실험적_x위치의_분산 = sum((x - 실험적_평균_x위치)**2 for x in 최종_x좌표_위치) / 반복
        실험적_y위치의_분산 = sum((y - 실험적_평균_y위치)**2 for y in 최종_y좌표_위치) / 반복
        실험적_z위치의_분산 = sum((z - 실험적_평균_z위치)**2 for z in 최종_z좌표_위치) / 반복
        실험적_평균제곱변위 = 실험적_x위치의_분산 + 실험적_y위치의_분산 + 실험적_z위치의_분산
        실험적_제곱근_평균제곱변위 = math.sqrt(실험적_평균제곱변위)
        
        이론적_평균제곱변위 = 횟수
        이론적_제곱근_평균제곱변위 = math.sqrt(횟수)
        
        오차율 = abs(실험적_제곱근_평균제곱변위 - 이론적_제곱근_평균제곱변위) / 이론적_제곱근_평균제곱변위 * 100 if 이론적_제곱근_평균제곱변위 != 0 else 0

        if 시각화:
            ax.scatter(0, 0, 0, marker='X', color='white', s=100, label='Start (0,0,0)')
            ax.set_title(f'3D Random Walk (N={횟수}, {반복}times)', color='white')
            ax.set_xlabel('X Coordinate', color='white')
            ax.set_ylabel('Y Coordinate', color='white')
            ax.set_zlabel('Z Coordinate', color='white')
            
            ax.xaxis.pane.fill = False
            ax.yaxis.pane.fill = False
            ax.zaxis.pane.fill = False
            ax.legend(facecolor='#1E1E1E', labelcolor='white')
            
            vis_res1, vis_res2 = st.columns([1.5, 1])
            with vis_res1:
                st.pyplot(fig)
            with vis_res2:
                st.markdown("### 🧪 실험적 데이터")
                st.markdown(f"**평균 위치:** ({실험적_평균_x위치:.2f}, {실험적_평균_y위치:.2f}, {실험적_평균_z위치:.2f})")
                st.markdown(f"**평균 위치의 거리:** {실험적_평균_위치의_거리:.2f}")
                st.markdown(f"**평균 거리:** {실험적_평균_거리:.2f}")
                st.markdown(f"**평균제곱변위 [MSD]:** {실험적_평균제곱변위:.2f}")
                st.markdown(f"**확산 정도 [RMSD]:** {실험적_제곱근_평균제곱변위:.2f}")
                
                st.markdown("### 📐 이론적 데이터")
                st.markdown("**평균 위치:** (0.00, 0.00, 0.00)")
                st.markdown("**평균 위치의 거리:** 0.00")
                이론_거리 = 2 * math.sqrt(2 * 횟수 / (3 * math.pi))
                st.markdown(f"**평균 거리:** {이론_거리:.2f} $(2\sqrt{{\\frac{{2N}}{{3\pi}}}})$")
                st.markdown(f"**평균제곱변위 [MSD]:** {이론적_평균제곱변위:.2f} $(N)$")
                st.markdown(f"**확산 정도 [RMSD]:** {이론적_제곱근_평균제곱변위:.2f} $(\sqrt{{N}})$")
                
                st.divider()
                st.markdown(f"<h3 style='text-align: center; color: #FF4B4B;'>🎯 오차율 (RMSD 기준): {오차율:.2f} %</h3>", unsafe_allow_html=True)
                
        else:
            res_col1, res_col2 = st.columns(2)
            with res_col1:
                st.markdown("### 🧪 실험적 데이터")
                st.markdown(f"**평균 위치:** ({실험적_평균_x위치:.2f}, {실험적_평균_y위치:.2f}, {실험적_평균_z위치:.2f})")
                st.markdown(f"**평균 위치의 거리:** {실험적_평균_위치의_거리:.2f}")
                st.markdown(f"**평균 거리:** {실험적_평균_거리:.2f}")
                st.markdown(f"**평균제곱변위 [MSD]:** {실험적_평균제곱변위:.2f}")
                st.markdown(f"**확산 정도 [RMSD]:** {실험적_제곱근_평균제곱변위:.2f}")
            with res_col2:
                st.markdown("### 📐 이론적 데이터")
                st.markdown("**평균 위치:** (0.00, 0.00, 0.00)")
                st.markdown("**평균 위치의 거리:** 0.00")
                이론_거리 = 2 * math.sqrt(2 * 횟수 / (3 * math.pi))
                st.markdown(f"**평균 거리:** {이론_거리:.2f} $(2\sqrt{{\\frac{{2N}}{{3\pi}}}})$")
                st.markdown(f"**평균제곱변위 [MSD]:** {이론적_평균제곱변위:.2f} $(N)$")
                st.markdown(f"**확산 정도 [RMSD]:** {이론적_제곱근_평균제곱변위:.2f} $(\sqrt{{N}})$")
            st.divider()
            st.markdown(f"<h3 style='text-align: center; color: #FF4B4B;'>🎯 오차율 (RMSD 기준): {오차율:.2f} %</h3>", unsafe_allow_html=True)
