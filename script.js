const R = 8.314;

function toKelvin(value, unit){
  if(unit === 'Celsius') return Number(value) + 273.15;
  return Number(value);
}

function showResult(id, text, color){
  const el = document.getElementById(id);
  el.textContent = text;
  if(color) el.style.background = color; else el.style.background = '';
}

function safeNumber(v){
  if(v === null || v === undefined || v === '') return NaN;
  return Number(v);
}

document.addEventListener('DOMContentLoaded', ()=>{
  // Tab switching
  document.querySelectorAll('.tab-btn').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      document.querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
      document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
      btn.classList.add('active');
      const target = btn.dataset.target;
      document.getElementById(target).classList.add('active');
    });
  });

  // Phase change
  document.getElementById('ph_calc').addEventListener('click', ()=>{
    const dh = safeNumber(document.getElementById('ph_dh').value);
    const t = safeNumber(document.getElementById('ph_t').value);
    const unit = document.getElementById('ph_unit').value;
    if(isNaN(dh) || isNaN(t)){
      alert('Please enter valid numbers for ΔH and Temperature.');
      return;
    }
    const t_k = toKelvin(t, unit);
    if(t_k <= 0){ alert('Temperature must be > 0 K'); return; }
    const dh_j = dh * 1000;
    const ds = dh_j / t_k;
    const text = `Temperature: ${t_k.toFixed(2)} K\nΔH: ${dh_j.toFixed(2)} J/mol\n\nΔS = ${ds.toFixed(4)} J/(mol·K)`;
    showResult('ph_result', text);
  });
  document.getElementById('ph_clear').addEventListener('click', ()=>{
    document.getElementById('ph_dh').value = '';
    document.getElementById('ph_t').value = '';
    showResult('ph_result', 'No result yet.');
  });

  // Heating
  document.getElementById('heat_calc').addEventListener('click', ()=>{
    const n = safeNumber(document.getElementById('heat_n').value);
    const c = safeNumber(document.getElementById('heat_c').value);
    const t1 = safeNumber(document.getElementById('heat_t1').value);
    const t2 = safeNumber(document.getElementById('heat_t2').value);
    const unit = document.getElementById('heat_unit').value;
    if([n,c,t1,t2].some(v=>isNaN(v))){ alert('Please enter valid numbers.'); return; }
    const t1k = toKelvin(t1, unit);
    const t2k = toKelvin(t2, unit);
    if(t1k <=0 || t2k <=0){ alert('Temps must be > 0 K'); return; }
    const ds = n * c * Math.log(t2k / t1k);
    const text = `Initial T: ${t1k.toFixed(2)} K\nFinal T: ${t2k.toFixed(2)} K\n\nΔS = ${ds.toFixed(4)} J/K`;
    showResult('heat_result', text);
  });
  document.getElementById('heat_clear').addEventListener('click', ()=>{
    ['heat_n','heat_c','heat_t1','heat_t2'].forEach(id=>document.getElementById(id).value='');
    showResult('heat_result','No result yet.');
  });

  // Expansion
  document.getElementById('exp_calc').addEventListener('click', ()=>{
    const n = safeNumber(document.getElementById('exp_n').value);
    const v1 = safeNumber(document.getElementById('exp_v1').value);
    const v2 = safeNumber(document.getElementById('exp_v2').value);
    if([n,v1,v2].some(v=>isNaN(v)) || v1 <=0 || v2 <=0){ alert('Inputs must be positive numbers'); return; }
    const ds = n * R * Math.log(v2 / v1);
    const text = `Volume Ratio: ${(v2/v1).toFixed(2)}\nR used: ${R} J/(mol·K)\n\nΔS = ${ds.toFixed(4)} J/K`;
    showResult('exp_result', text);
  });
  document.getElementById('exp_clear').addEventListener('click', ()=>{
    ['exp_n','exp_v1','exp_v2'].forEach(id=>document.getElementById(id).value='');
    showResult('exp_result','No result yet.');
  });

  // Spontaneity
  document.getElementById('spon_calc').addEventListener('click', ()=>{
    const dh_kj = safeNumber(document.getElementById('spon_dh').value);
    const ds = safeNumber(document.getElementById('spon_ds').value);
    const t = safeNumber(document.getElementById('spon_t').value);
    const unit = document.getElementById('spon_unit').value;
    if([dh_kj,ds,t].some(v=>isNaN(v))){ alert('Invalid Input'); return; }
    const t_k = toKelvin(t, unit);
    if(t_k <= 0){ alert('T must be > 0 K'); return; }
    const dh_j = dh_kj * 1000;
    const dg = dh_j - (t_k * ds);
    let status = 'EQUILIBRIUM';
    let color = '';
    if(dg < 0){ status = 'SPONTANEOUS'; color = 'lightgreen'; }
    else if(dg > 0){ status = 'NON-SPONTANEOUS'; color = '#ffcccc'; }
    const text = `ΔH: ${dh_j.toFixed(2)} J\nT: ${t_k.toFixed(2)} K\nΔG = ${dg.toFixed(2)} J\n\nResult: ${status}`;
    showResult('spon_result', text, color);
  });
  document.getElementById('spon_clear').addEventListener('click', ()=>{
    ['spon_dh','spon_ds','spon_t'].forEach(id=>document.getElementById(id).value='');
    showResult('spon_result','No result yet.');
  });
});

