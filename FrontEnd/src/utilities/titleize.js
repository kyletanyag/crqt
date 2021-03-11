export default function (s) {
  if (!s) {
    return s;
  }
  const result = s.replace(/([A-Z])([^A-Z])/g, ' $1$2');
  return result.charAt(0).toUpperCase() + result.slice(1);
}
