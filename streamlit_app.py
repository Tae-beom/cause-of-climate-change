import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc
import numpy as np

# ▶ 한글 폰트 설정
rc('font', family='NanumGothic')

# 앱 제목
st.title("🌏 지구 자전축과 계절 변화 시뮬레이션")

# -------------------------------
# 1️⃣ 지구 자전축 시각화
# -------------------------------
st.subheader("1. 지구 자전축 시각화")

# 그래프 그리기
fig1, ax1 = plt.subplots(figsize=(6, 6))

# 지구 원 (반지름 = 1)
earth = plt.Circle((0, 0), 1, color='lightblue', zorder=1)
ax1.add_artist(earth)

# ▶ 자전축 경사각 설정
# 기본값은 아래에서 받음
default_angle = 23.5

# 자전축 선 (위아래로 연장, 총 길이 3)
radians = np.deg2rad(default_angle)
x = np.sin(radians) * 1.5
y = np.cos(radians) * 1.5
ax1.plot([-x, x], [-y, y], color='darkblue', linewidth=3, label='자전축')

# ▶ 적도선: 자전축과 항상 90도 되도록 회전된 직선
# 적도선은 자전축에 수직, 즉 (cos, -sin) 방향으로 회전
ex = np.cos(radians)
ey = -np.sin(radians)
ax1.plot([-ex, ex], [-ey, ey], color='white', linewidth=2, linestyle='--', label='적도')

# ▶ 태양광 화살표: 지구를 관통하지 않도록 짧게 그림
arrow_length = 0.8  # 관통 방지용 길이
ax1.arrow(1.6, 0.5, -arrow_length, 0, head_width=0.08, head_length=0.1,
          fc='orange', ec='orange', linewidth=2, zorder=2)
ax1.text(1.7, 0.5, "☀️ 태양광", fontsize=12, color='orange', va='bottom')

# 설정
ax1.set_aspect('equal')
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)
ax1.axis('off')
ax1.legend()

# ▶ 그림 먼저 출력
st.pyplot(fig1)

# ▶ 경사각 슬라이더를 아래쪽에 위치
angle = st.slider("지구 자전축 경사각 조절 (°)", min_value=21.5, max_value=24.5, value=23.5, step=0.1)

# ▶ 슬라이더 변경을 반영해서 다시 그림
fig1, ax1 = plt.subplots(figsize=(6, 6))

# 지구 원
earth = plt.Circle((0, 0), 1, color='lightblue', zorder=1)
ax1.add_artist(earth)

# 자전축 선
radians = np.deg2rad(angle)
x = np.sin(radians) * 1.5
y = np.cos(radians) * 1.5
ax1.plot([-x, x], [-y, y], color='darkblue', linewidth=3, label='자전축')

# 적도: 자전축에 직각 방향으로 회전
ex = np.cos(radians)
ey = -np.sin(radians)
ax1.plot([-ex, ex], [-ey, ey], color='white', linewidth=2, linestyle='--', label='적도')

# 태양광 (지구 외부에서 관통하지 않도록 길이 조절)
arrow_length = 0.8
ax1.arrow(1.6, 0.5, -arrow_length, 0, head_width=0.08, head_length=0.1,
          fc='orange', ec='orange', linewidth=2, zorder=2)
ax1.text(1.7, 0.5, "☀️ 태양광", fontsize=12, color='orange', va='bottom')

# 설정
ax1.set_aspect('equal')
ax1.set_xlim(-2, 2)
ax1.set_ylim(-2, 2)
ax1.axis('off')
ax1.legend()
st.pyplot(fig1)

