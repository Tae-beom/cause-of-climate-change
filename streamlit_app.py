import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

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
    ax.plot([-x1, x1], [-y1, y1], color='navy', linewidth=3)

    ex = np.cos(theta)
    ey = -np.sin(theta)
    ax.plot([-ex, ex], [-ey, ey], color='white', linewidth=2, linestyle='--')

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
    ax.plot(a * np.cos(orbit_theta), b * np.sin(orbit_theta), color='lightgray', linewidth=1.5)

    sun_x, sun_y = (c / 2), 0
    ax.plot(sun_x, sun_y, 'o', color='orange', markersize=18)

    perihelion_pos = (a, 0)
    aphelion_pos = (-a, 0)

    ax.text((c / 2) + 0.4, 0.0, "Perihelion", fontsize=10, fontweight='bold', ha='left')
    ax.text(-a - 0.4, 0.0, "Aphelion", fontsize=10, fontweight='bold', ha='right')

    reverse_season = (years == 13000)

    def draw_earth_with_axis(pos, is_aphelion):
        earth = plt.Circle(pos, 0.25, color='skyblue', zorder=3)
        ax.add_artist(earth)

        tilt_rad = np.deg2rad(23.5)
        axis_x = (-np.sin(tilt_rad) if reverse_season else np.sin(tilt_rad)) * 0.6
        axis_y = np.cos(tilt_rad) * 0.6

        ax.plot([pos[0] - axis_x, pos[0] + axis_x],
                [pos[1] - axis_y, pos[1] + axis_y],
                color='navy', linewidth=2.5)

        season = "Summer" if is_aphelion != reverse_season else "Winter"
        ax.text(pos[0], pos[1] + 0.65, season, ha='center', fontsize=10, fontweight='bold')

    draw_earth_with_axis(perihelion_pos, False)
    draw_earth_with_axis(aphelion_pos, True)

    ax.set_aspect('equal')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    return fig

# =========================================
# 이심률 변화 시뮬레이션 함수
# =========================================
def draw_orbit_with_eccentricity(ecc):
    fig, ax = plt.subplots(figsize=(7, 7))
    a = 3
    e_vis = min(ecc * 1.5, 0.99)
    b = a * np.sqrt(1 - e_vis**2)
    c = a * ecc

    theta = np.linspace(0, 2*np.pi, 300)
    ax.plot(a * np.cos(theta), b * np.sin(theta), color='lightgray', linewidth=1.5)

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

# =========================================
# 피나투보 화산 그래프
# =========================================
def draw_pinatubo_aerosol_temp_chart():
    years = np.array([1990, 1991, 1992, 1993, 1994])
    aerosol_mt = np.array([1, 17, 10, 5, 2])
    temp_anomaly = np.array([0.0, -0.1, -0.5, -0.3, -0.1])

    fig, ax1 = plt.subplots(figsize=(8,5))
    ax1.set_xlabel('Year')
    ax1.set_ylabel('SO$_2$ Emission (Mt)', color='tab:blue')
    ax1.plot(years, aerosol_mt, color='tab:blue', marker='o', label='SO$_2$ Emission')
    ax1.tick_params(axis='y', labelcolor='tab:blue')

    ax2 = ax1.twinx()
    ax2.set_ylabel('Temperature Anomaly (°C)', color='tab:red')
    ax2.plot(years, temp_anomaly, color='tab:red', marker='s', label='Temp Anomaly')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    fig.suptitle('Mount Pinatubo: Aerosol Emission vs. Temperature Anomaly', fontsize=14)
    ax1.legend(loc='upper right')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    return fig

# =========================================
# 기온 추세 분석 (연/월/일 자동 인식)
# =========================================
def draw_temp_trend_chart(df):
    date_col = df.columns[0]
    temp_col = df.columns[1]
    try:
        df[date_col] = pd.to_datetime(df[date_col])
        x_vals = df[date_col].map(lambda x: x.year + (x.month-1)/12 + (x.day-1)/365)
    except:
        x_vals = pd.to_numeric(df[date_col], errors='coerce')

    y_vals = pd.to_numeric(df[temp_col], errors='coerce')

    model = LinearRegression()
    model.fit(x_vals.values.reshape(-1, 1), y_vals.values)
    trend_line = model.predict(x_vals.values.reshape(-1, 1))
    slope_per_decade = model.coef_[0] * 10

    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(x_vals, y_vals, marker='o', label='Observed Temperature', color='skyblue')
    ax.plot(x_vals, trend_line, label='Trend Line', color='red', linewidth=2)
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.set_title("Temperature Trend Analysis")
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()

    return fig, slope_per_decade

# =========================================
# Sidebar Navigation
# =========================================
st.sidebar.title("📌 Menu")
main_menu = st.sidebar.radio("Select Category", ["Main", "External Factors", "Internal Factors"], key="main_menu_radio")

# =========================================
# Main
# =========================================
if main_menu == "Main":
    st.title("🌍 Earth Climate Change Factors")
    st.markdown(
        """
        <div style='font-size: 20px;'>
        Earth's climate changes are influenced by <b>external</b> and <b>internal</b> factors.<br><br>
        - <b>External Factors</b>: Changes in Earth's orbit, axial tilt, and precession.<br>
        - <b>Internal Factors</b>: Natural events (e.g., volcanic eruptions) and human-induced activities.<br><br>
        Use the menu on the left to explore different factors and see related simulations and data.
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================================
# External Factors
# =========================================
elif main_menu == "External Factors":
    ext_menu = st.sidebar.radio("Select External Factor", ["Precession", "Axial Tilt Change", "Orbital Eccentricity Change"])
    if ext_menu == "Precession":
        st.title("Earth's Precession (세차운동)")
        years = st.select_slider("Precession Cycle Position (years)", options=[0, 13000, 26000], value=0)
        st.pyplot(draw_precession_cycle(years))
    elif ext_menu == "Axial Tilt Change":
        st.title("Axial Tilt Change Simulation")
        angle = st.slider("Axial Tilt (°)", 21.5, 24.5, 23.5, 0.1)
        st.pyplot(draw_earth(angle))
    elif ext_menu == "Orbital Eccentricity Change":
        st.title("Orbital Eccentricity Change Simulation")
        ecc = st.slider("Orbital Eccentricity", 0.0, 0.2, 0.0167, step=0.005)
        st.pyplot(draw_orbit_with_eccentricity(ecc))

# =========================================
# Internal Factors
# =========================================
elif main_menu == "Internal Factors":
    int_menu = st.sidebar.radio("Select Internal Factor", ["Natural Causes", "Human-Induced Causes"])
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
        st.pyplot(draw_pinatubo_aerosol_temp_chart())

    elif int_menu == "Human-Induced Causes":
        st.title("📈 Human-Induced Climate Change Analysis")
        st.markdown(
            """
            <div style='font-size: 20px;'>
            Upload a CSV file containing <b>time</b> (year/month/day) and <b>temperature</b> data  
            to visualize the trend and calculate the average temperature rise over 10 years.
            </div>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            fig, slope_decade = draw_temp_trend_chart(df)
            st.pyplot(fig)
            st.subheader(f"📊 10-year Average Temperature Rise: {slope_decade:.3f} °C")
