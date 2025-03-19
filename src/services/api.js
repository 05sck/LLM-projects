import axios from "axios";

const API_URL = "https://api.jarvis.cx/api/v1";

// 🔑 토큰 가져오기 (localStorage 또는 Vuex 사용 가능)
const token = localStorage.getItem("authToken");

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
    "Authorization": token ? `Bearer ${token}` : "",
  },
});

// 🔥 401 오류 발생 시 로그인 페이지로 리디렉트
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      console.error("🚨 인증 실패! 로그인 페이지로 이동합니다.");
      window.location.href = "/login"; // 로그인 페이지로 이동
    }
    return Promise.reject(error);
  }
);

export default api;
