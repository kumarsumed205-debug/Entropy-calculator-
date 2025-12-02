function computeEntropy(text){
  if(!text) return {entropy:0,length:0,dist:[]};
  const freq = new Map();
  for(const ch of text){
    freq.set(ch, (freq.get(ch)||0)+1);
  }
  const len = text.length;
  let entropy = 0;
  const dist = [];
  for(const [sym,count] of freq){
    const p = count/len;
    entropy -= p * Math.log2(p);
    dist.push({sym, count, p});
  }
  dist.sort((a,b)=>b.count-a.count);
  return {entropy, length: len, dist};
}

function renderResults(obj){
  document.getElementById('entropy').textContent = obj.length ? obj.entropy.toFixed(4) : '—';
  document.getElementById('length').textContent = obj.length;
  const container = document.getElementById('distribution');
  container.innerHTML = '';
  if(obj.dist.length===0){ container.textContent = 'No characters.'; return; }
  const max = obj.dist[0].count;
  for(const d of obj.dist){
    const row = document.createElement('div');
    row.className = 'dist-item';

    const label = document.createElement('div');
    label.className = 'label';
    const display = d.sym===' ' ? '␣' : d.sym;
    label.textContent = `${display}`;

    const barWrap = document.createElement('div');
    barWrap.style.width = '100%';

    const bar = document.createElement('div');
    bar.className = 'bar';
    const pct = (d.count / max) * 100;
    bar.style.width = pct + '%';

    const meta = document.createElement('div');
    meta.style.minWidth = '90px';
    meta.style.marginLeft = '10px';
    meta.textContent = `${d.count} (${(d.p*100).toFixed(2)}%)`;

    barWrap.appendChild(bar);
    row.appendChild(label);
    row.appendChild(barWrap);
    row.appendChild(meta);
    container.appendChild(row);
  }
}

document.addEventListener('DOMContentLoaded', ()=>{
  const input = document.getElementById('inputText');
  const calc = document.getElementById('calcBtn');
  const clear = document.getElementById('clearBtn');

  function doCalc(){
    const txt = input.value;
    const r = computeEntropy(txt);
    renderResults(r);
  }

  calc.addEventListener('click', doCalc);
  input.addEventListener('keydown', (e)=>{ if(e.key==='Enter' && (e.ctrlKey||e.metaKey)) doCalc(); });
  clear.addEventListener('click', ()=>{ input.value=''; renderResults({entropy:0,length:0,dist:[]}); input.focus(); });
});
