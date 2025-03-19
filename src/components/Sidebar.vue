<template>
  <div class="sidebar">
    <h2>✅ 유치원</h2>
    <nav>
      <ul>
        <li>
          <router-link to="/">🏠 홈</router-link>
        </li>
        <li>
          <router-link to="/schedule">📅 일정</router-link>
        </li>
        <li>
          <router-link to="/medication">💊 복약</router-link>
        </li>
      </ul>
    </nav>
  </div>
</template>

<style scoped>
.sidebar {
  width: 200px;
  height: 100vh;
  background-color: #f8f9fa;
  padding: 20px;
  position: fixed;
  left: 0;
  top: 0;
}

h2 {
  font-size: 1.5rem;
  margin-bottom: 20px;
}

nav ul {
  list-style: none;
  padding: 0;
}

nav ul li {
  margin-bottom: 15px;
}

nav ul li a {
  text-decoration: none;
  font-size: 1.2rem;
  color: #333;
}

nav ul li a:hover {
  color: #007bff;
}
</style>
