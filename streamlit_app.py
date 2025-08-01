import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# 자전축 경사각 변화 시뮬레이션 함수
# -------------------------------
def draw_earth(axial_tilt_deg):
    fig, ax = plt.subplots(figsize=(6, 6))

    # 지구 원
    earth = plt.Circle((0, 0), 1, color='skyblue', zorder=1)
    ax.add_artist(earth)

    # 자전축
    theta = np.deg2rad(axial_tilt_deg)
    x1 = np.sin(theta) * 1.3
    y1 = np.cos(theta) * 1.3
    ax.plot([-x1, x1], [-y1, y1], color='navy', linewidth=3, label='Axial Tilt')

    # 적도
    ex = np.cos(theta)
    ey = -np.sin(theta)
    ax.plot([-ex, ex], [-ey, ey], color='white', linewidth=2, linestyle='--', label='Equator')

    # Sunlight arrow (항상 고정, y=0)
    ax.arrow(1.4, 0.0, -0.6, 0, head_width=0.06, head_length=0.1,
             fc='orange', ec='orange', linewidth=2)
    ax.text(1.55, 0.0, "☀️ Sunlight", color='orange', fontsize=12, va='center')

    # 설정
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='lower right')

    return fig

def declination(season_angle_deg, tilt_deg):
    return tilt_deg * np.sin(np.deg2rad(season_angle_deg))

def solar_energy(lat, tilt, season_angle_deg):
    delta = declination(season_angle_deg, tilt)
    solar_alt = 90 - abs(lat - delta)
    return round(np.maximum(np.sin(np.deg2rad(solar_alt)), 0) * 100, 1)

# -------------------------------
# 사이드바 메뉴 구성
# -------------------------------
st.sidebar.title("📌 Menu")
main_menu = st.sidebar.radio("Select Category", ["Main", "External Factors", "Internal Factors"])

# -------------------------------
# 메인 화면
# -------------------------------
if main_menu == "Main":
    st.title("🌍 Earth Climate Change Factors")
    st.markdown("""
    Earth’s climate changes are influenced by **external** and **internal** factors.
    Use the menu on the left to explore different influences.
    """)

# -------------------------------
# 외적 요인
# -------------------------------
elif main_menu == "External Factors":
    ext_menu = st.sidebar.radio("Select External Factor", ["Precession", "Axial Tilt Change", "Orbital Eccentricity Change"])

    if ext_menu == "Precession":
        st.title("Precession")
        st.write("Information and simulation about Earth's precession will be here.")

    elif ext_menu == "Axial Tilt Change":
        st.title("Axial Tilt Change Simulation")

        # Tilt slider
        angle = st.slider("Axial Tilt (°)", 21.5, 24.5, 23.5, 0.1)

        # Draw Earth diagram
        fig1 = draw_earth(angle)
        st.pyplot(fig1)

        # Seasonal Solar Energy Graph
        st.subheader("Seasonal Solar Energy at 37°N (Noon)")
        seasons = {
            "Spring (Mar)": 0,
            "Summer (Jun)": 90,
            "Autumn (Sep)": 180,
            "Winter (Dec)": 270
        }
        latitude = 37
        energies = [solar_energy(latitude, angle, seasons[s]) for s in seasons]

        fig2, ax2 = plt.subplots(figsize=(5.5, 3))
        bars = ax2.bar(seasons.keys(), energies, color=['#FFD700', '#FF8C00', '#87CEEB', '#1E90FF'])

        # 값 막대 안쪽에 표시
        for bar, val in zip(bars, energies):
            ax2.text(bar.get_x() + bar.get_width()/2, val / 2, f"{val}%",
                     ha='center', va='center', fontsize=9, color='white', fontweight='bold')

        ax2.set_ylabel("Relative Solar Energy (%)")
        ax2.set_ylim(0, 100)
        ax2.set_title("Noon Solar Energy by Season")
        st.pyplot(fig2)

    elif ext_menu == "Orbital Eccentricity Change":
        st.title("Orbital Eccentricity Change")
        st.write("Information and simulation about Earth's orbital eccentricity changes will be here.")

# -------------------------------
# 내적 요인
# -------------------------------
elif main_menu == "Internal Factors":
    int_menu = st.sidebar.radio("Select Internal Factor", ["Natural Causes", "Human-Induced Causes"])

    if int_menu == "Natural Causes":
        st.title("Natural Internal Causes")
        st.write("Information about natural internal causes will be here.")

    elif int_menu == "Human-Induced Causes":
        st.title("Human-Induced Internal Causes")
        st.write("Information about human-induced internal causes will be here.")
