import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

function get(url) {
  const finalUrl = url.startsWith('http') ? url : BASE_URL + url;
  return axios.get(finalUrl);
}

function post(url, data) {
  const finalUrl = url.startsWith('http') ? url : BASE_URL + url;
  return axios.post(finalUrl, data);
}

export default {
  get,
  post,  // post 메서드 추가
};