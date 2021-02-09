const baseurl = 'http://localhost:5000/';

// If we were to use axios library instead? Up to us
/*
import axios from 'axios';
function get(path) {
  return axios.get(baseurl + path);
}

function post(path, data) {
  axios.post(baseurl + path, data)
  .catch(error => console.log(error));
}
*/

async function get(path) {
  const p = baseurl + path;
  const r = await fetch(p);
  const d = await r.json();
  return d;
}

async function post(path, data) {
  const r = fetch(baseurl + path, {
    headers: {
      'Content-Type': 'application/json',
    },
    method: 'POST',
    body: JSON.stringify(data),
  });
  return r;
}

export { get, post };
