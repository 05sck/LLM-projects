import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000';

function get(url) {
  const finalUrl = url.startsWith('http') ? url : BASE_URL + url;
  return axios.get(finalUrl);
}

export default {
  get,
};