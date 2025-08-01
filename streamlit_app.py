import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------
# App Title
# -------------------------------
st.title("Earth's Axial Tilt & Seasonal Solar Energy")

st.markdown(
    "Use the slider to adjust Earth's axial tilt. "
    "The tilt affects the axis and equator orientation, but **Sunlight** stays fixed along the horizontal diameter."
)

# -------------------------------
# Slider for Axial Tilt
# -------------------------------
angle = st.slider("Axial Tilt (degrees)", min_value=21.5, max_value=24.5, value=23.5, step=0.1)

# -------------------------------
# Function to Draw Earth Diagram
# -------------------------------
def draw_earth(axial_tilt_deg):
    fig, ax = plt.subplots(figsize=(6, 6))

    # Draw Earth as a circle
    earth = plt.Circle((0, 0), 1, color='skyblue', zorder=1)
    ax.add_artist(earth)

    # Axial tilt line
    theta = np.deg2rad(axial_tilt_deg)
    x1 = np.sin(theta) * 1.3
    y1 = np.cos(theta) * 1.3
    ax.plot([-x1, x1], [-y1, y1], color='navy', linewidth=3, label='Axial Tilt')

    # Equator line (90° to axial tilt)
    ex = np.cos(theta)
    ey = -np.sin(theta)
    ax.plot([-ex, ex], [-ey, ey], color='white', linewidth=2, linestyle='--', label='Equator')

    # Sunlight arrow - FIXED position (horizontal diameter extension)
    ax.arrow(1.4, 0.0, -0.6, 0, head_width=0.06, head_length=0.1,
             fc='orange', ec='orange', linewidth=2)
    ax.text(1.55, 0.0, "☀️ Sunlight", color='orange', fontsize=12, va='center')

    # Plot settings
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-1.6, 1.6)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.legend(loc='lower right')

    return fig

# -------------------------------
# Show Earth Diagram
# -------------------------------
fig1 = draw_earth(angle)
st.pyplot(fig1)

# -------------------------------
# Seasonal Solar Energy Chart
# -------------------------------
st.subheader("Seasonal Solar Energy at 37°N (Noon)")

# Season definitions (Sun's ecliptic longitude)
seasons = {
    "Spring (Mar)": 0,
    "Summer (Jun)": 90,
    "Autumn (Sep)": 180,
    "Winter (Dec)": 270
}

# Declination calculation
def declination(season_angle_deg, tilt_deg):
    return tilt_deg * np.sin(np.deg2rad(season_angle_deg))

# Solar energy calculation (relative %)
def solar_energy(lat, tilt, season_angle_deg):
    delta = declination(season_angle_deg, tilt)
    solar_alt = 90 - abs(lat - delta)
    return round(np.maximum(np.sin(np.deg2rad(solar_alt)), 0) * 100, 1)

latitude = 37
energies = [solar_energy(latitude, angle, seasons[s]) for s in seasons]

# Small bar chart
fig2, ax2 = plt.subplots(figsize=(5.5, 3))
bars = ax2.bar(seasons.keys(), energies, color=['#FFD700', '#FF8C00', '#87CEEB', '#1E90FF'])

# Label bars
for bar, val in zip(bars, energies):
    ax2.text(
        bar.get_x() + bar.get_width()/2,
        val / 2,  # 막대 중간쯤에 위치
        f"{val}%",
        ha='center',
        va='center',
        fontsize=9,
        color='white',  # 막대 내부에 잘 보이도록
        fontweight='bold'
    )
ax2.set_ylabel("Relative Solar Energy (%)")
ax2.set_ylim(0, 100)
ax2.set_title("Noon Solar Energy by Season")
st.pyplot(fig2)
