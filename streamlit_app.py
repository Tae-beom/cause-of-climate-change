import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# =========================================
# 자전축 경사각 변화 시뮬레이션 함수
# =========================================
def draw_earth(axial_tilt_deg):
    fig, ax = plt.subplots(figsize=(6, 6))
    earth = plt.Circle((0, 0), 1, color='skyblue', zorder=1)
    ax.add_artist(earth)

    theta = np.deg2rad(axial_tilt_deg)
    x1 = np.sin(theta) * 1.3
    y1 = np.cos(theta) * 1.3
    ax.plot([-x1, x1], [-y1, y1], color='navy', linewidth=3, label='Axial Tilt')

    ex = np.cos(theta)
    ey = -np.sin(theta)
    ax.plot([-ex, ex], [-ey, ey], color='white', linewidth=2, linestyle='--', label='Equator')

    ax.arrow(1.4, 0.0, -0.6, 0, head_width=0.06, head_length=0.1,
             fc='orange', ec='orange', linewidth=2)
    ax.text(1.55, 0.0, "☀️ Sunlight", color='orange', fontsize=12, va='center')

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='lower right')
    return fig

# =========================================
# 계절별 에너지 계산
# =========================================
def declination(season_angle_deg, tilt_deg):
    return tilt_deg * np.sin(np.deg2rad(season_angle_deg))

def solar_energy(lat, tilt, season_angle_deg):
    delta = declination(season_angle_deg, tilt)
    solar_alt = 90 - abs(lat - delta)
    return round(np.maximum(np.sin(np.deg2rad(solar_alt)), 0) * 100, 1)

# =========================================
# 세차운동 시뮬레이션 함수
# =========================================
def draw_precession_cycle(years):
    fig, ax = plt.subplots(figsize=(7, 7))

    # ===== 타원형 궤도 =====
    a = 3
    b = 2.4
    e = np.sqrt(1 - (b**2 / a**2))
    c = a * e

    # 타원 궤도
    orbit_theta = np.linspace(0, 2*np.pi, 300)
    x_orbit = a * np.cos(orbit_theta)
    y_orbit = b * np.sin(orbit_theta)
    ax.plot(x_orbit, y_orbit, color='lightgray', linewidth=1.5)

    # ===== 태양 위치 (중심과 초점의 중간) =====
    sun_x, sun_y = (c / 2), 0
    ax.plot(sun_x, sun_y, 'o', color='orange', markersize=18, label='Sun')

    # ===== 근일점 / 원일점 =====
    perihelion_pos = (a, 0)
    aphelion_pos = (-a, 0)

    # 라벨 (태양 기준으로 근일점/원일점 위치 조정)
    offset_text = 0.6  # 알파벳 약 3자 정도 거리
    ax.text((c / 2) + offset_text, 0.0, "Perihelion", fontsize=10, fontweight='bold', ha='left')
    ax.text(-a - offset_text, 0.0, "Aphelion", fontsize=10, fontweight='bold', ha='right')

    # ===== 계절 반전 여부 (23000년 기준) =====
    reverse_season = (years == 23000)

    # ===== 지구 그리는 함수 =====
    def draw_earth_with_axis(pos, is_aphelion):
        earth = plt.Circle(pos, 0.25, color='skyblue', zorder=3)
        ax.add_artist(earth)

        tilt_rad = np.deg2rad(23.5)
        if reverse_season:
            axis_x = -np.sin(tilt_rad) * 0.6
        else:
            axis_x = np.sin(tilt_rad) * 0.6
        axis_y = np.cos(tilt_rad) * 0.6

        ax.plot([pos[0] - axis_x, pos[0] + axis_x],
                [pos[1] - axis_y, pos[1] + axis_y],
                color='navy', linewidth=2.5)

        # 계절 라벨 (궤도 밖, 지구 가까이)
        offset = 0.4
        if is_aphelion:
            season = "Summer" if not reverse_season else "Winter"
        else:
            season = "Winter" if not reverse_season else "Summer"

        ax.text(pos[0], pos[1] + 0.25 + offset, season,
                ha='center', fontsize=10, fontweight='bold')

    # 지구 배치
    draw_earth_with_axis(perihelion_pos, is_aphelion=False)
    draw_earth_with_axis(aphelion_pos, is_aphelion=True)

    # 화면 설정
    ax.set_aspect('equal')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    ax.legend(loc='upper left')
    return fig

# =========================================
# Sidebar Navigation
# =========================================
st.sidebar.title("📌 Menu")
main_menu = st.sidebar.radio("Select Category", ["Main", "External Factors", "Internal Factors"], key="main_menu_radio")

# =========================================
# Main Page
# =========================================
if main_menu == "Main":
    st.title("🌍 Earth Climate Change Factors")
    st.markdown("""
    Earth's climate changes are influenced by **external** and **internal** factors.  
    Use the menu on the left to explore different influences.
    """)

# =========================================
# External Factors
# =========================================
elif main_menu == "External Factors":
    ext_menu = st.sidebar.radio("Select External Factor", ["Precession", "Axial Tilt Change", "Orbital Eccentricity Change"], key="external_factor_radio")

    # ---- Precession ----
    if ext_menu == "Precession":
        st.title("Earth's Precession (세차운동)")
        st.markdown("""
        Earth's precession is the slow rotation of the direction of Earth's axis  
        over a cycle of about **26,000 years**.

        In this simulation:
        - The orbit is drawn **elliptical** so perihelion and aphelion are obvious.
        - The Sun is placed **between the center and the focus near perihelion**.
        - At **23,000 years**, the axial tilt direction flips (y-axis symmetry), reversing seasons relative to perihelion/aphelion.
        """)

        # 0, 23000, 46000에서만 선택 가능
        years = st.select_slider(
            "Precession Cycle Position (years)",
            options=[0, 23000, 46000],
            value=0
        )

        # 눈금 마크 (0, 23000, 46000 - 가로줄과 정렬)
        st.markdown(
            f"""
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: gray; margin-top:-10px;">
                <span>0</span>
                <span style="color:red; font-weight:bold;">23,000 ▼</span>
                <span>46,000</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        fig_prec = draw_precession_cycle(years)
        st.pyplot(fig_prec)

    # ---- Axial Tilt Change ----
    elif ext_menu == "Axial Tilt Change":
        st.title("Axial Tilt Change Simulation")
        angle = st.slider("Axial Tilt (°)", 21.5, 24.5, 23.5, 0.1)

        fig1 = draw_earth(angle)
        st.pyplot(fig1)

        st.subheader("Seasonal Solar Energy at 37°N (Noon)")
        seasons = {"Spring (Mar)": 0, "Summer (Jun)": 90, "Autumn (Sep)": 180, "Winter (Dec)": 270}
        latitude = 37
        energies = [solar_energy(latitude, angle, seasons[s]) for s in seasons]

        fig2, ax2 = plt.subplots(figsize=(5.5, 3))
        bars = ax2.bar(seasons.keys(), energies, color=['#FFD700', '#FF8C00', '#87CEEB', '#1E90FF'])

        for bar, val in zip(bars, energies):
            ax2.text(bar.get_x() + bar.get_width()/2, val / 2, f"{val}%",
                     ha='center', va='center', fontsize=9, color='white', fontweight='bold')

        ax2.set_ylabel("Relative Solar Energy (%)")
        ax2.set_ylim(0, 100)
        ax2.set_title("Noon Solar Energy by Season")
        st.pyplot(fig2)

    # ---- Orbital Eccentricity Change ----
    elif ext_menu == "Orbital Eccentricity Change":
        st.title("Orbital Eccentricity Change")
        st.write("Information and simulation about Earth's orbital eccentricity changes will be here.")

# =========================================
# Internal Factors
# =========================================
elif main_menu == "Internal Factors":
    int_menu = st.sidebar.radio("Select Internal Factor", ["Natural Causes", "Human-Induced Causes"], key="internal_factor_radio")

    if int_menu == "Natural Causes":
        st.title("Natural Internal Causes")
        st.write("Information about natural internal causes will be here.")

    elif int_menu == "Human-Induced Causes":
        st.title("Human-Induced Internal Causes")
        st.write("Information about human-induced internal causes will be here.")
