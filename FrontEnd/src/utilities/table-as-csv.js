// const csvDataPrefix = 'data:text/csv;charset=utf-8,';
const csvDataPrefix = '';

function rowAsCsv(row, cellTag, separator, quoteChar) {
  return Array.from(row
    .querySelectorAll(cellTag))
    .map((c) => quoteChar + c.textContent + quoteChar)
    .join(separator);
}

function tableAsCsv(tbl) {
  if (!tbl) {
    return undefined;
  }

  console.log(tbl);

  const s = [];

  const h = tbl.querySelector('thead tr');

  if (h) {
    s.push(rowAsCsv(h, 'th', ',', '"'));
  }

  tbl.querySelectorAll('tbody tr')
    .forEach((r) => {
      s.push(rowAsCsv(r, 'td', ',', '"'));
    });

  return csvDataPrefix + s.join('\n');
}

function download(data, filename, contentType) {
  const blob = new Blob([data], { type: contentType });
  if (window.navigator.msSaveOrOpenBlob) {
    window.navigator.msSaveBlob(blob, filename);
  } else {
    const elem = window.document.createElement('a');
    elem.href = window.URL.createObjectURL(blob);
    elem.download = filename;
    document.body.appendChild(elem);
    elem.click();
    setTimeout(() => {
      window.URL.revokeObjectURL(elem.href);
      document.body.removeChild(elem);
    }, 1000);
  }
}

export {
  tableAsCsv,
  download,
};
