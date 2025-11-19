import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="MealSync", layout="wide")

html = r"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>MealSync - Embedded UI</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root{
      --bg:#0b1116;
      --card:#0d1620;
      --muted:#9fb6c9;
      --accent:#60a5fa;
      --accent2:#7c3aed;
      --frame: rgba(148,163,184,0.45);
      --green:#4ade80;
      --red:#fb7185;
      --text:#e6eef8;
      --card-padding:12px;
      font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }
    html,body { height:100%; margin:0; padding:0; background: linear-gradient(180deg,#020617 0%, #070b10 100%); color:var(--text); }
    .container { max-width:1200px; margin:18px auto; padding:18px; }
    h1 { text-align:center; color:var(--accent); font-size:36px; margin:0 0 6px 0; }
    p.subtitle { text-align:center; color: #9aaec0; margin:0 0 18px 0; }

    .week-row { display:flex; justify-content:center; gap:16px; margin:18px 0 18px 0; flex-wrap:wrap; }
    .week-btn { padding:8px 14px; border-radius:18px; border:1px solid rgba(255,255,255,0.04); background: rgba(255,255,255,0.02); color:var(--text); cursor:pointer; }
    .week-btn.active { background: linear-gradient(135deg,var(--accent),var(--accent2)); color:white; border-color:transparent; }

    /* 2x4 grid */
    .grid { display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-top:8px; }
    @media (max-width: 900px){ .grid { grid-template-columns:repeat(2,1fr);} }

    /* card frames */
    .card {
      background: var(--card);
      border-radius:10px;
      border: 1px solid var(--frame);
      padding: var(--card-padding);
      box-sizing:border-box;
      min-height: 120px;
    }

    .day-header {
      display:flex;
      justify-content:space-between;
      align-items:center;
      margin-bottom:8px;
    }
    .day-title { font-weight:700; color:var(--text); font-size:16px; }
    .day-title.sunday { color:#ffd6d8; }

    .toggle-btn { padding:6px 10px; border-radius:18px; border:1px solid rgba(255,255,255,0.04); background: rgba(255,255,255,0.02); cursor:pointer; font-size:13px; }

    .section-label { font-size:12px; color:var(--muted); margin:8px 0 6px 0; text-transform:uppercase; letter-spacing:0.06em; }

    select, input[type="text"] {
      width:100%;
      padding:10px 12px;
      border-radius:8px;
      background: rgba(0,0,0,0.35);
      border:1px solid rgba(255,255,255,0.03);
      color:var(--text);
      box-sizing:border-box;
      font-size:14px;
    }

    .budget-row { display:flex; gap:8px; align-items:center; margin-bottom:8px; }
    .budget-row .btn { padding:6px 10px; border-radius:10px; border:1px solid rgba(255,255,255,0.04); background: rgba(255,255,255,0.02); cursor:pointer; min-width:72px; white-space:nowrap; }
    .budget-row .label { font-size:13px; color:var(--muted); margin-bottom:4px; }

    .summary { margin-top:16px; border-radius:8px; padding:12px; background: rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.03); }
    .summary-row { display:flex; justify-content:space-between; margin-bottom:8px; }
    .summary-row .val { font-weight:700; color:#bfe6ff; }

    /* small helpers */
    .muted { color:var(--muted); font-size:13px; }
    .diff-pos { color:var(--green); font-weight:600; }
    .diff-neg { color:var(--red); font-weight:600; }

    /* make inputs not show spinner on number type when used */
    input::-webkit-outer-spin-button, input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
  </style>
</head>
<body>
<div class="container">
  <h1>MealSync</h1>
  <p class="subtitle">Your weekly meal planning, simplified.</p>

  <div class="week-row" id="weekRow"></div>

  <div style="height:10px;"></div>

  <div class="grid" id="grid"></div>

  <div style="height:12px;"></div>

  <div class="summary" id="summary">
    <div style="font-weight:700; margin-bottom:8px;">Cost Summary</div>
    <div class="summary-row"><div>Current Week Total:</div><div class="val" id="curWeekVal">Rs. 0.00</div></div>
    <div class="summary-row"><div>Sunday Total:</div><div class="val" id="sunTotalVal">Rs. 0.00</div></div>
    <hr style="border-color:rgba(255,255,255,0.04)"/>
    <div class="summary-row"><div>Weekdays Total:</div><div class="val" id="wdTotalVal">Rs. 0.00</div></div>
    <div class="summary-row"><div>Grand Total:</div><div class="val" id="grandVal">Rs. 0.00</div></div>
  </div>

</div>

<script>
/* ---------- Data ---------- */
const breakfastOptions = [
  {id:'medu', name:'Medu vada', price:20},
  {id:'pongal', name:'Pongal', price:25},
  {id:'sambar', name:'Sambar vada', price:32},
  {id:'curd', name:'Curd vada', price:32},
  {id:'pav', name:'Pav bhaji', price:38},
  {id:'alu', name:'Alu paratha', price:38},
  {id:'mac', name:'Macaroni', price:38},
  {id:'daal', name:'Daal poori', price:38}
];
const lunchOptions = [
  {id:'l1', name:'Mess Lunch', price:60},
  {id:'l2', name:'Special Lunch', price:80}
];
const dinnerOptions = [
  {id:'d1', name:'Mess Dinner', price:60},
  {id:'d2', name:'Special Dinner', price:80}
];

const DEFAULTS = [
  {week:1, day:2, meal_name:'Pav bhaji'},
  {week:3, day:3, meal_name:'Pav bhaji'},
  {week:1, day:4, meal_name:'Maggi'},
  {week:1, day:6, meal_name:'Alu paratha'},
  {week:4, day:4, meal_name:'Alu paratha'},
  {week:2, day:4, meal_name:'Macaroni'},
  {week:2, day:5, meal_name:'Macaroni'},
  {week:4, day:6, meal_name:'Daal poori'}
];

const DEFAULT_BUDGETS = {
  weekly:840, sunday:2140, weekdays:3360, grandTotal:5500
};

const WEEK_DAYS = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];

/* ---------- State ---------- 
 We'll store everything in localStorage under "mealsync_state"
 Structure:
 {
   selectedWeek: 1..4,
   weeks: { "1": { "w0-d0": {main:'medu', dinner:'d1', ...}, ... }, "2": {...} ... },
   dayChoice: { "1-w0": "breakfast" or "lunch", ... },
   budgets: { weekly: "840.00", sunday: "2140.00", ... }  // strings
 }
*/
function loadState(){
  const raw = localStorage.getItem('mealsync_state');
  if(raw) try { return JSON.parse(raw); } catch(e){}
  // new state
  const s = { selectedWeek:1, weeks:{}, dayChoice:{}, budgets:{} };
  for(let w=1;w<=4;w++) s.weeks[w] = {};
  // init budgets as strings
  for(const k in DEFAULT_BUDGETS) s.budgets[k] = DEFAULT_BUDGETS[k].toFixed(2);
  localStorage.setItem('mealsync_state', JSON.stringify(s));
  return s;
}
function saveState(){ localStorage.setItem('mealsync_state', JSON.stringify(state)); }

/* ---------- Helper utilities ---------- */
function priceForSelection(mealType, sel, week, day){
  if(sel==='skip') return 0;
  if(sel==='custom'){
    const key = `price-${week}-${day}-${mealType}`;
    const v = state.weeks[week][key];
    return parseFloat(v || 0) || 0;
  }
  const list = mealType==='breakfast' ? breakfastOptions : (mealType==='lunch' ? lunchOptions : dinnerOptions);
  const found = list.find(x=>x.id===sel);
  return found ? found.price : 0;
}
function getDefaultFor(week, day){
  const dd = DEFAULTS.find(d=>d.week===week && d.day===day+1);
  if(!dd) return null;
  const name = dd.meal_name.toLowerCase();
  return breakfastOptions.find(b=>b.name.toLowerCase()===name) || null;
}

/* ---------- Rendering ---------- */
const state = loadState();

function makeWeekButtons(){
  const wr = document.getElementById('weekRow');
  wr.innerHTML = '';
  for(let i=1;i<=4;i++){
    const b = document.createElement('button');
    b.className = 'week-btn' + (state.selectedWeek===i ? ' active' : '');
    b.innerText = 'Week '+i;
    b.onclick = ()=>{ state.selectedWeek = i; saveState(); makeGrid(); makeWeekButtons(); updateSummary(); }
    wr.appendChild(b);
  }
}

function makeGrid(){
  const grid = document.getElementById('grid');
  grid.innerHTML = '';
  const week = state.selectedWeek;

  // create 8 cells (7 days + 1 budgets)
  for(let cell=0; cell<8; cell++){
    const card = document.createElement('div');
    card.className = 'card';
    if(cell<7){
      const day = cell;
      // header row
      const hdr = document.createElement('div'); hdr.className='day-header';
      const title = document.createElement('div'); title.className='day-title';
      title.innerText = WEEK_DAYS[day];
      if(day===6) title.className += ' sunday';
      hdr.appendChild(title);

      // toggle button (only Mon-Sat)
      if(day!==6){
        const key = `${week}-w${day}`;
        if(!state.dayChoice[key]) state.dayChoice[key]='breakfast';
        const tbtn = document.createElement('button');
        tbtn.className='toggle-btn';
        tbtn.innerText = (state.dayChoice[key]==='breakfast' ? '☕ Breakfast — click to switch' : '🍛 Lunch — click to switch');
        tbtn.onclick = ()=>{
          state.dayChoice[key] = (state.dayChoice[key]==='breakfast' ? 'lunch' : 'breakfast');
          saveState();
          makeGrid();
          updateSummary();
        };
        hdr.appendChild(tbtn);
      }
      card.appendChild(hdr);

      // now inside the same card: sections for main meal and dinner
      const mainType = (day===6) ? 'lunch' : state.dayChoice[`${week}-w${day}`] || 'breakfast';

      // MAIN meal
      const mainLabel = document.createElement('div'); mainLabel.className='section-label'; mainLabel.innerText = mainType.toUpperCase();
      card.appendChild(mainLabel);

      const mainSelect = document.createElement('select');
      const mainSelKey = `sel-${week}-${day}-${mainType}`;
      // ensure entry exists
      if(!state.weeks[week][mainSelKey]) {
        // set default (for breakfast maybe default meal)
        let def = 'skip';
        if(mainType==='breakfast'){
          const d = getDefaultFor(week, day);
          if(d) def = d.id;
        }
        state.weeks[week][mainSelKey] = def;
        saveState();
      }
      // options
      const opts = (mainType==='breakfast') ? breakfastOptions : (mainType==='lunch' ? lunchOptions : dinnerOptions);
      mainSelect.innerHTML = '';
      const addOption = (value, label) => {
        const o = document.createElement('option'); o.value=value; o.innerText=label; if(state.weeks[week][mainSelKey]===value) o.selected = true; mainSelect.appendChild(o);
      };
      addOption('skip','Skip this meal');
      opts.forEach(m => addOption(m.id, `${m.name} (Rs. ${m.price.toFixed(2)})`));
      addOption('custom','Custom price (type Rs.)');
      mainSelect.onchange = (e)=>{
        state.weeks[week][mainSelKey] = e.target.value;
        // if custom, create price key with default 0
        if(e.target.value==='custom'){
          const pk = `price-${week}-${day}-${mainType}`;
          if(!(pk in state.weeks[week])) state.weeks[week][pk] = '0';
        }
        saveState();
        makeGrid();
        updateSummary();
      };
      card.appendChild(mainSelect);

      // custom price input if needed
      if(state.weeks[week][mainSelKey] === 'custom') {
        const pk = `price-${week}-${day}-${mainType}`;
        if(!(pk in state.weeks[week])) state.weeks[week][pk] = '0';
        const input = document.createElement('input');
        input.type='text'; input.value = state.weeks[week][pk];
        input.oninput = (e)=>{
          state.weeks[week][pk] = e.target.value;
          saveState();
          updateSummary();
        };
        card.appendChild(input);
      }

      // DINNER
      const dinnerLabel = document.createElement('div'); dinnerLabel.className='section-label'; dinnerLabel.innerText = 'dinner'.toUpperCase();
      card.appendChild(dinnerLabel);
      const dinnerKey = `sel-${week}-${day}-dinner`;
      if(!state.weeks[week][dinnerKey]) state.weeks[week][dinnerKey] = 'skip';
      const dinnerSelect = document.createElement('select');
      dinnerSelect.innerHTML = '';
      const addD = (v,l)=>{ const o=document.createElement('option'); o.value=v; o.innerText=l; if(state.weeks[week][dinnerKey]===v) o.selected=true; dinnerSelect.appendChild(o); };
      addD('skip','Skip this meal');
      dinnerOptions.forEach(m => addD(m.id, `${m.name} (Rs. ${m.price.toFixed(2)})`));
      addD('custom','Custom price (type Rs.)');
      dinnerSelect.onchange = (e)=>{
        state.weeks[week][dinnerKey] = e.target.value;
        if(e.target.value==='custom'){
          const pk=`price-${week}-${day}-dinner`;
          if(!(pk in state.weeks[week])) state.weeks[week][pk] = '0';
        }
        saveState();
        makeGrid();
        updateSummary();
      };
      card.appendChild(dinnerSelect);

      if(state.weeks[week][dinnerKey] === 'custom'){
        const pk=`price-${week}-${day}-dinner`;
        if(!(pk in state.weeks[week])) state.weeks[week][pk]='0';
        const input = document.createElement('input'); input.type='text'; input.value= state.weeks[week][pk];
        input.oninput=(e)=>{ state.weeks[week][pk]=e.target.value; saveState(); updateSummary(); };
        card.appendChild(input);
      }

    } else {
      // budgets card (cell 7)
      const hdr = document.createElement('div'); hdr.className='day-header';
      const title = document.createElement('div'); title.className='day-title'; title.innerText='Budgets';
      hdr.appendChild(title);
      card.appendChild(hdr);

      // Budget rows: Default button left, input right
      const keys = [
        {k:'weekly', label:'Week Total'},
        {k:'sunday', label:'Sunday Total (all 4 weeks)'},
        {k:'weekdays', label:'Weekdays Total (all 4 weeks)'},
        {k:'grandTotal', label:'Grand Total'}
      ];
      keys.forEach(item=>{
        // row container
        const row = document.createElement('div'); row.className='budget-row';
        // button
        const btn = document.createElement('button'); btn.className='btn'; btn.innerText='Default';
        btn.onclick = ()=>{
          state.budgets[item.k] = DEFAULT_BUDGETS[item.k].toFixed(2);
          saveState();
          makeGrid();
          updateSummary();
        };
        row.appendChild(btn);
        // right column with label+input
        const right = document.createElement('div'); right.style.flex='1';
        const lab = document.createElement('div'); lab.className='label'; lab.innerText = item.label;
        lab.style.marginBottom='6px';
        right.appendChild(lab);
        const key = `budget-${item.k}`;
        if(!(key in state.budgets)) state.budgets[item.k] = DEFAULT_BUDGETS[item.k].toFixed(2);
        const inp = document.createElement('input'); inp.type='text'; inp.value=state.budgets[item.k];
        inp.oninput = (e)=>{ state.budgets[item.k] = e.target.value; saveState(); updateSummary(); };
        right.appendChild(inp);
        row.appendChild(right);
        card.appendChild(row);
      });
    }

    grid.appendChild(card);
  }

  saveState();
}

/* ---------- Summary/calculation ---------- */
function updateSummary(){
  // Current week total: sum mon-sat main + dinner for selectedWeek
  const week = state.selectedWeek;
  let curWeek = 0;
  for(let d=0; d<6; d++){
    // main type
    const mainType = (d===6) ? 'lunch' : (state.dayChoice[`${week}-w${d}`] || 'breakfast');
    const selKey = `sel-${week}-${d}-${mainType}`;
    const sel = state.weeks[week][selKey] || 'skip';
    curWeek += priceForSelection(mainType, sel, week, d);
    // dinner
    const dk = `sel-${week}-${d}-dinner`;
    const dsel = state.weeks[week][dk] || 'skip';
    curWeek += priceForSelection('dinner', dsel, week, d);
  }
  document.getElementById('curWeekVal').innerText = 'Rs. '+curWeek.toFixed(2);

  // Sunday total: sum Sunday for all weeks (lunch+dinner each)
  let sunTotal=0;
  for(let w=1; w<=4; w++){
    const s1 = state.weeks[w][`sel-${w}-6-lunch`] || 'skip';
    const s2 = state.weeks[w][`sel-${w}-6-dinner`] || 'skip';
    sunTotal += priceForSelection('lunch', s1, w, 6);
    sunTotal += priceForSelection('dinner', s2, w, 6);
  }
  document.getElementById('sunTotalVal').innerText = 'Rs. '+sunTotal.toFixed(2);

  // Weekdays total (Mon-Sat) across 4 weeks
  let weekdaysTotal=0;
  for(let w=1; w<=4; w++){
    for(let d=0; d<6; d++){
      const mt = (d===6) ? 'lunch' : (state.dayChoice[`${w}-w${d}`] || 'breakfast');
      const s = state.weeks[w][`sel-${w}-${d}-${mt}`] || 'skip';
      weekdaysTotal += priceForSelection(mt, s, w, d);
      const ds = state.weeks[w][`sel-${w}-${d}-dinner`] || 'skip';
      weekdaysTotal += priceForSelection('dinner', ds, w, d);
    }
  }
  document.getElementById('wdTotalVal').innerText = 'Rs. '+weekdaysTotal.toFixed(2);

  const grand = weekdaysTotal + sunTotal;
  document.getElementById('grandVal').innerText = 'Rs. '+grand.toFixed(2);

  // also optionally show difference next to values comparing budgets
  // (not shown inline here, but we kept budgets storage for comparisons)
}

/* ---------- Init ---------- */
function ensureStructure(){
  // make sure each week object has keys for all selects defaulted to skip so calculations straightforward
  for(let w=1; w<=4; w++){
    const wk = state.weeks[w] || {};
    for(let d=0; d<7; d++){
      const keys = [
        `sel-${w}-${d}-breakfast`,
        `sel-${w}-${d}-lunch`,
        `sel-${w}-${d}-dinner`,
        `price-${w}-${d}-breakfast`,
        `price-${w}-${d}-lunch`,
        `price-${w}-${d}-dinner`
      ];
      keys.forEach(k=>{ if(!(k in wk)) wk[k] = (k.startsWith('price') ? '0' : 'skip'); });
    }
    state.weeks[w] = wk;
  }
  saveState();
}

ensureStructure();
makeWeekButtons();
makeGrid();
updateSummary();

/* helpful: expose state to window for debugging (remove in prod) */
window.mealsyncState = state;
</script>
</body>
</html>
"""

components.html(html, height=900, scrolling=True)
