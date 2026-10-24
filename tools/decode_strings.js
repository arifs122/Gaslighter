#!/usr/bin/env node
/* Mini-FLOSS (JS) v2: dosyanin tamamini sandbox'ta yukleyip
 * obfuscator'un decoder fonksiyonunu cagirir.
 *
 * Kullanim: node decode_strings.js <bundle.js> <out.json> [decoderAdi]
 */
const fs = require('fs');
const vm = require('vm');

const file = process.argv[2];
const outPath = process.argv[3];
const decName = process.argv[4] || null;
const src = fs.readFileSync(file, 'utf8');

// Decoder adini bul: en cok cagrilan `_0xXXXX(` fonksiyonu
function guessDecoder(s) {
  const counts = {};
  const re = /\b(_0x[0-9a-f]{4,})\s*\(/g;
  let m;
  while ((m = re.exec(s))) counts[m[1]] = (counts[m[1]] || 0) + 1;
  // fonksiyon tanimi olanlari tercih et
  const defined = Object.keys(counts).filter(n =>
    new RegExp(`function\\s+${n}\\s*\\(`).test(s) || new RegExp(`(?:const|let|var)\\s+${n}\\s*=\\s*function`).test(s));
  const pool = defined.length ? defined : Object.keys(counts);
  pool.sort((a, b) => (counts[b] || 0) - (counts[a] || 0));
  return pool[0];
}

const decoder = decName || guessDecoder(src);
if (!decoder) { console.error('decoder bulunamadi'); process.exit(1); }

// Dosyayi calistirilabilir hale getir: modul yukleme cagrilarini no-op yap
const patched = src
  .replace(/require\s*\([^)]*\)/g, '({})')
  .replace(/process\.(stdout|stderr)\.write/g, '(()=>{})')
  .replace(/process\.exitCode/g, '0')
  .replace(/process\.argv/g, '["node","x"]');

const sandbox = {
  console: { log() {}, error() {}, warn() {} },
  decodeURIComponent, encodeURIComponent, String, parseInt, parseFloat,
  Math, Array, Object, JSON, Number, Boolean, RegExp, Error, Date,
  Buffer, module: { exports: {} }, exports: {}, require: () => ({}),
  process: { argv: ['node', 'x'], exitCode: 0, stdout: { write() {} }, stderr: { write() {} } },
};
sandbox.globalThis = sandbox;
vm.createContext(sandbox);

let decoded = [];
let err = null;
try {
  vm.runInContext(patched, sandbox, { timeout: 15000 });
} catch (e) {
  err = e.message;
}

const fn = sandbox[decoder] || (sandbox.module && sandbox.module.exports && sandbox.module.exports[decoder]);
if (typeof fn === 'function') {
  for (let i = 0; i < 2000; i++) {
    try {
      const v = fn(i);
      if (typeof v === 'string') decoded.push(v);
    } catch (e) { /* aralik disi */ }
  }
}

const printable = [...new Set(decoded.filter(s => s && /^[\x20-\x7e]+$/.test(s)))];
fs.writeFileSync(outPath, JSON.stringify({
  decoder, loaded: !err, error: err,
  total: decoded.length, printable: printable.length, strings: printable,
}, null, 2));

console.log(`decoder=${decoder} yuklendi=${!err} cozulen=${decoded.length} yazdirilabilir=${printable.length}`);
if (err) console.log('hata:', err.slice(0, 120));
console.log(printable.slice(0, 12).join('\n'));
