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

    ax.arrow(1.8, 0.0, -0.6, 0, head_width=0.06, head_length=0.1,
             fc='orange', ec='orange', linewidth=2)
    ax.text(1.65, 0.0, "☀️ Sunlight", color='orange', fontsize=12, va='center')

    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal')
    ax.axis('off')
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

    a = 3
    b = 2.4
    e = np.sqrt(1 - (b**2 / a**2))
    c = a * e

    orbit_theta = np.linspace(0, 2*np.pi, 300)
    x_orbit = a * np.cos(orbit_theta)
    y_orbit = b * np.sin(orbit_theta)
    ax.plot(x_orbit, y_orbit, color='lightgray', linewidth=1.5)

    sun_x, sun_y = (c / 2), 0
    ax.plot(sun_x, sun_y, 'o', color='orange', markersize=18)

    perihelion_pos = (a, 0)
    aphelion_pos = (-a, 0)

    offset_text = 0.4
    ax.text((c / 2) + offset_text, 0.0, "Perihelion", fontsize=10, fontweight='bold', ha='left')
    ax.text(-a - offset_text, 0.0, "Aphelion", fontsize=10, fontweight='bold', ha='right')

    reverse_season = (years == 13000)

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

        offset = 0.4
        if is_aphelion:
            season = "Summer" if not reverse_season else "Winter"
        else:
            season = "Winter" if not reverse_season else "Summer"

        ax.text(pos[0], pos[1] + 0.25 + offset, season,
                ha='center', fontsize=10, fontweight='bold')

    draw_earth_with_axis(perihelion_pos, is_aphelion=False)
    draw_earth_with_axis(aphelion_pos, is_aphelion=True)

    ax.set_aspect('equal')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    return fig

# =========================================
# 이심률 변화 시뮬레이션 함수 (시각 과장 적용)
# =========================================
def draw_orbit_with_eccentricity(ecc):
    fig, ax = plt.subplots(figsize=(7, 7))

    a = 3
    e_vis = min(ecc * 1.5, 0.99)  # 시각적 과장
    b = a * np.sqrt(1 - e_vis**2)
    c = a * ecc  # 실제 초점 거리

    theta = np.linspace(0, 2*np.pi, 300)
    x_orbit = a * np.cos(theta)
    y_orbit = b * np.sin(theta)
    ax.plot(x_orbit, y_orbit, color='lightgray', linewidth=1.5)

    ax.plot(c, 0, 'o', color='orange', markersize=18)

    ax.plot(a, 0, 'o', color='skyblue', markersize=10)
    ax.plot(-a, 0, 'o', color='skyblue', markersize=10)

    ax.text(a * 0.8, 0.0, "Perihelion", fontsize=10, fontweight='bold', ha='center')
    ax.text(-a * 0.8, 0.0, "Aphelion", fontsize=10, fontweight='bold', ha='center')

    ax.set_aspect('equal')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    return fig

def calculate_solar_energy_at_points(ecc):
    a = 1
    r_peri = a * (1 - ecc)
    r_aphe = a * (1 + ecc)
    energy_peri = 1 / (r_peri**2)
    energy_aphe = 1 / (r_aphe**2)
    energy_peri_norm = 100
    energy_aphe_norm = energy_aphe / energy_peri * 100
    return energy_peri_norm, energy_aphe_norm

# =========================================
# Mount Pinatubo Aerosol & Temperature Plot
# =========================================
def draw_pinatubo_aerosol_temp_chart():
    import matplotlib.pyplot as plt
    import numpy as np

    # 1) 데이터 정의 (실제 관측 기반 예시)
    years = np.array([1990, 1991, 1992, 1993, 1994])
    aerosol_mt = np.array([1, 17, 10, 5, 2])  # SO₂ 방출량 (메가톤)
    temp_anomaly = np.array([0.0, -0.1, -0.5, -0.3, -0.1])  # 기온 편차 (°C)

    # 2) 그래프 틀 생성
    fig, ax1 = plt.subplots(figsize=(8,5))

    # 3) 왼쪽 y축 - 에어로졸 방출량
    color = 'tab:blue'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('SO$_2$ Emission (Mt)', color=color)
    ax1.plot(years, aerosol_mt, color=color, marker='o', label='SO$_2$ Emission')
    ax1.tick_params(axis='y', labelcolor=color)

    # 4) 오른쪽 y축 - 기온 편차
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Temperature Anomaly (°C)', color=color)
    ax2.plot(years, temp_anomaly, color=color, marker='s', label='Temp Anomaly')
    ax2.tick_params(axis='y', labelcolor=color)

    # 5) 제목, 범례, 격자
    fig.suptitle('Mount Pinatubo: Aerosol Emission vs. Temperature Anomaly', fontsize=14)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
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
    st.markdown(
        """
        <div style='font-size: 20px;'>
        Earth's climate changes are influenced by <b>external</b> and <b>internal</b> factors.<br>
        Use the menu on the left to explore different influences.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================
# External Factors
# =========================================
elif main_menu == "External Factors":
    ext_menu = st.sidebar.radio("Select External Factor", ["Precession", "Axial Tilt Change", "Orbital Eccentricity Change"], key="external_factor_radio")

    # ---- Precession ----
    if ext_menu == "Precession":
        st.title("Earth's Precession (세차운동)")
        st.markdown(
            """
            <div style='font-size: 20px;'>
            Earth's precession is the slow rotation of the direction of Earth's axis  
            over a cycle of about <b>26,000 years</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

        years = st.select_slider("Precession Cycle Position (years)", options=[0, 13000, 26000], value=0)

        st.markdown(
            """
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: gray; margin-top:-10px;">
                <span>0</span>
                <span style="color:red; font-weight:bold;">13,000 ▲</span>
                <span>26,000</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        fig_prec = draw_precession_cycle(years)
        st.pyplot(fig_prec)

    # ---- Axial Tilt Change ----
    elif ext_menu == "Axial Tilt Change":
        st.title("Axial Tilt Change Simulation")
        st.markdown(
            """
            <div style='font-size: 20px;'>
            The axial tilt of the Earth changes over a cycle of about <b>41,000 years</b>,  
            ranging roughly from <b>21.5° to 24.5°</b>.  
            This affects the <b>intensity of the seasons</b>.
            </div>
            """,
            unsafe_allow_html=True
        )

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
            ax2.text(bar.get_x() + bar.get_width()/2, val / 2, f"{val}%", ha='center', va='center', fontsize=9, color='white', fontweight='bold')

        ax2.set_ylabel("Relative Solar Energy (%)")
        ax2.set_ylim(0, 100)
        ax2.set_title("Noon Solar Energy by Season")
        st.pyplot(fig2)

    # ---- Orbital Eccentricity Change ----
    elif ext_menu == "Orbital Eccentricity Change":
        st.title("Orbital Eccentricity Change Simulation")
        st.markdown(
            """
            <div style='font-size: 20px;'>
            The Earth's orbital eccentricity changes over time,  
            altering the distance between the Earth and Sun at perihelion and aphelion.
            </div>
            """,
            unsafe_allow_html=True
        )

        ecc = st.slider("Orbital Eccentricity", 0.0, 0.2, 0.0167, step=0.005)

        fig_orbit = draw_orbit_with_eccentricity(ecc)
        st.pyplot(fig_orbit)

        peri_energy, aphe_energy = calculate_solar_energy_at_points(ecc)

        st.subheader("Relative Solar Energy (%)")
        fig3, ax3 = plt.subplots(figsize=(5.5, 3))
        bars = ax3.bar(["Perihelion", "Aphelion"], [peri_energy, aphe_energy], color=['#FF8C00', '#1E90FF'])
        for bar, val in zip(bars, [peri_energy, aphe_energy]):
            ax3.text(bar.get_x() + bar.get_width()/2, val / 2, f"{val:.1f}%", ha='center', va='center', fontsize=9, color='white', fontweight='bold')

        ax3.set_ylim(0, 110)
        st.pyplot(fig3)

# =========================================
# Internal Factors
# =========================================

elif main_menu == "Internal Factors":
    int_menu = st.sidebar.radio("Select Internal Factor", ["Natural Causes", "Human-Induced Causes"], key="internal_factor_radio")

    if int_menu == "Natural Causes":
        st.title("🌋 Natural Internal Causes")

        st.markdown(
            """
            <div style='font-size: 20px;'>
            Natural internal factors include volcanic eruptions that can significantly affect the climate.<br><br>
            One major example is the <b>1991 Mount Pinatubo eruption</b>, which injected millions of tons of sulfur dioxide (SO₂)
            into the stratosphere, reflecting sunlight and cooling the Earth's surface for several years.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("📈 Aerosol Emissions and Temperature Change After Pinatubo")

        # 피나투보 에어로졸-기온 변화 그래프 표시
        fig_pinatubo = draw_pinatubo_aerosol_temp_chart()
        st.pyplot(fig_pinatubo)


    elif int_menu == "Human-Induced Causes":
        st.title("Human-Induced Internal Causes")
        st.write("Information about human-induced internal causes will be here.")
