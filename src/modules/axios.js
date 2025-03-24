import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

function get(url, config = {}) {
  const finalUrl = url.startsWith('http') ? url : BASE_URL + url;
  console.log(`GET 요청: ${finalUrl}`);  // 디버깅
  return axios.get(finalUrl, config);
}

function post(url, data) {
  const finalUrl = url.startsWith('http') ? url : BASE_URL + url;
  console.log(`POST 요청: ${finalUrl}`, data);  // 디버깅
  return axios.post(finalUrl, data);
}

export default {
  get,
  post,  // post 메서드 추가
};