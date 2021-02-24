import axios from "axios";

export default axios.create({
  baseURL: "http://localhost:5000",
  headers: {
    "Content-type": "application/json",
  }
});

/*
OLD API CODE
const baseurl = 'http://localhost:5000/';

// If we were to use axios library instead? Up to us

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

*/