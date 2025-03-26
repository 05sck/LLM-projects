<template>
  <div class="sidebar">
    <nav>
      <ul>
        <li>
          <router-link to="/" @click="logClick('Home')" class="menu-link">
            <span class="menu-circle">
              <span class="jelly-emoji logo-emoji">🫘</span>
            </span>
          </router-link>
        </li>
        <li>
          <router-link to="/schedule" @click="logClick('Schedule')" class="menu-link">
            <span class="menu-circle">
              <span class="jelly-emoji">📅</span>
            </span>
          </router-link>
        </li>
        <li>
          <router-link to="/medication" @click="logClick('Medication')" class="menu-link">
            <span class="menu-circle">
              <span class="jelly-emoji">💊</span>
            </span>
          </router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script setup>
const logClick = (page) => {
  console.log(`Clicked: ${page}`);
};
</script>

<style scoped>
.sidebar {
  width: 70px;
  height: 100vh;
  background: linear-gradient(135deg, #ffd9d3 0%, #ffebdf 100%);
  padding: 25px;
  position: fixed;
  left: 0;
  top: 0;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  font-family: 'Noto Sans KR', sans-serif;
}

nav ul {
  list-style: none;
  padding: 0;
}

nav ul li {
  margin-bottom: 20px;
  position: relative; /* ::after를 위한 relative 설정 */
}

nav ul li a.menu-link {
  text-decoration: none;
  font-size: 1.2rem;
  color: #4a4a4a;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 15px;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.menu-circle {
  width: 40px;
  height: 40px;
  background-color: #ffffff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
}

.jelly-emoji {
  font-size: 1.2rem;
  transition: all 0.3s ease;
  display: inline-block;
}

.logo-emoji {
  font-size: 1.8rem;
  background: linear-gradient(45deg, #ff6f61, #ffb88c);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 1px 1px 3px rgba(255, 111, 97, 0.2);
}

nav ul li a:hover .menu-circle {
  transform: scale(1.1) rotate(10deg);
  box-shadow: 0 0 15px rgba(255, 111, 97, 0.6), 0 4px 10px rgba(255, 111, 97, 0.2);
}

nav ul li a:hover .jelly-emoji {
  transform: rotate(15deg);
}

nav ul li a:hover .logo-emoji {
  transform: scale(1.05) rotate(15deg);
  text-shadow: 2px 2px 5px rgba(255, 111, 97, 0.3);
}

nav ul li a:hover {
  color: #ff6f61;
}

nav ul li a.router-link-exact-active {
  color: #ff6f61;
  font-weight: 500;
}

nav ul li a.router-link-exact-active .menu-circle {
  box-shadow: 0 3px 8px rgba(255, 111, 97, 0.15);
}

/* 선택된 상태에서 오른쪽으로 흰색 사각형 연결 효과 */
nav ul li a.router-link-exact-active::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 30px; /* menu-circle의 중심에서 시작 (menu-circle width 40px / 2 + padding 조정) */
  width: 100px; /* 초기 너비 0으로 설정 */
  height: 40px; /* menu-circle과 동일한 높이 */
  background-color: #ffffff;
  border-radius: 0; /* 사각형 유지 */
  transform: translateY(-50%);
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0);
  animation: expandSquare 0.3s ease forwards;
  z-index: 0;
}


</style>