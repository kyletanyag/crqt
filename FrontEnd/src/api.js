const baseurl = 'https://localhost:5000';

async function get(path) {
  const p = baseurl + path;
  const r = await fetch(p);
  const d = await r.json();
  return d;
}

async function post(path, data) {
  const r = await fetch(baseurl + path, {
    headers: {
      'Content-Type': 'application/json',
    },
    method: 'POST',
    body: JSON.stringify(data),
  });
  const d = await r.json();
  return d;
}

export { get, post };
