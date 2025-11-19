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
      --accent:#2563EB;   /* solid blue */
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
    .week-btn {
      padding:8px 14px;
      border-radius:18px;
      border:1px solid rgba(255,255,255,0.12);
      background: rgba(15,23,42,0.8);
      color:var(--text);
      cursor:pointer;
    }
    .week-btn.active {
      background: var(--accent);      /* solid colour */
      color:white;
      border-color:#1D4ED8;
    }

    /* 2x4 grid */
    .grid {
      display:grid;
      grid-template-columns:repeat(4,1fr);
      gap:14px;
      margin-top:8px;
    }
    @media (max-width: 900px){
      .grid { grid-template-columns:repeat(2,1fr); }
    }

    /* card frames – FIXED HEIGHT so all cards equal */
    .card {
      background: var(--card);
      border-radius:10px;
      border: 1px solid var(--frame);
      padding: var(--card-padding);
      box-sizing:border-box;
      height: 280px;           /* <- all cards same height */
    }

    .day-header {
      display:flex;
      justify-content:space-between;
      align-items:center;
      margin-bottom:8px;
    }
    .day-title { font-weight:700; color:#3B82F6; font-size:16px; }
    .day-title.sunday { color:#F87171; }
    .day-title.budgets { color:var(--text); }

    /* SMALL icon-only toggle button */
    .toggle-btn {
      width:28px;
      height:28px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,0.18);
      background: rgba(255,255,255,0.06);
      cursor:pointer;
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:16px;
      color:var(--muted);
      padding:0;
    }

    /* Selects with icons inside */
    .select-wrapper {
      position:relative;
      margin:8px 0 4px 0;
    }
    .select-wrapper select {
      width:100%;
      padding:10px 12px 10px 44px; /* extra left padding for icon */
      border-radius:8px;
      background: rgba(15,23,42,0.9);
      border:1px solid rgba(148,163,184,0.6);
      color:var(--text);
      box-sizing:border-box;
      font-size:14px;
      appearance:none;
      -webkit-appearance:none;
      -moz-appearance:none;
    }

    /* Dropdown list colours */
    select option {
      background-color:#020617;   /* dark dropdown panel */
      color:#e6eef8;              /* light text */
    }

    .select-icon {
      position:absolute;
      left:12px;
      top:50%;
      transform:translateY(-50%);
      pointer-events:none;
      display:flex;
      align-items:center;
      justify-content:center;
    }
    .select-icon svg {
      width:22px;
      height:22px;
      display:block;
    }
    .select-icon-breakfast svg { color:#93C5FD; }
    .select-icon-lunch svg     { color:#FDE047; }
    .select-icon-dinner svg    { color:#C9A8EE; }

    /* Budgets rows: label on its own line, then input + button on one row */
    .budget-label { font-size:13px; color:var(--muted); margin:6px 0 4px 0; }

    .budget-row {
      display:flex;
      gap:8px;
      align-items:center;
      margin-bottom:8px;
    }
    .budget-row input[type="text"] {
      flex:1;
      padding:10px 12px;
      border-radius:8px;
      background: rgba(15,23,42,0.9);
      border:1px solid rgba(148,163,184,0.6);
      color:var(--text);
      box-sizing:border-box;
      font-size:14px;
    }

    .budget-default-btn {
      padding:6px 10px;
      border-radius:10px;
      min-width:80px;
      white-space:nowrap;
      cursor:pointer;
      border:1px solid #1D4ED8;
      background: #2563EB;     /* solid colour, no gradient */
      color:#e5f2ff;
      font-size:12px;
      font-weight:600;
    }

    .summary { margin-top:16px; border-radius:8px; padding:12px; background: rgba(0,0,0,0.25); border:1px solid rgba(255,255,255,0.03); }
    .summary-row { display:flex; justify-content:space-between; margin-bottom:8px; }
    .summary-row .val { font-weight:700; color:#bfe6ff; }

    .muted { color:var(--muted); font-size:13px; }
    .diff-pos { color:var(--green); font-weight:600; }
    .diff-neg { color:var(--red); font-weight:600; }

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
    <div class="summary-row"><div>Current Week Total:</div><div class="val" id="curWeekVal">₹ 0.00</div></div>
    <div class="summary-row"><div>Sunday Total:</div><div class="val" id="sunTotalVal">₹ 0.00</div></div>
    <hr style="border-color:rgba(255,255,255,0.04)"/>
    <div class="summary-row"><div>Weekdays Total:</div><div class="val" id="wdTotalVal">₹ 0.00</div></div>
    <div class="summary-row"><div>Grand Total:</div><div class="val" id="grandVal">₹ 0.00</div></div>
  </div>

</div>

<script>
/* ---------- Breakfast data with special defaults ---------- */
const BF_MEDU   = {id:'medu',  name:'Medu vada',    price:20};
const BF_PONGAL = {id:'pongal',name:'Pongal',       price:25};
const BF_SAMBAR = {id:'sambar',name:'Sambar vada',  price:32};
const BF_CURD   = {id:'curd',  name:'Curd vada',    price:32};

const BF_PAV    = {id:'pav',   name:'Pav bhaji',    price:38};
const BF_MAGGI  = {id:'maggi', name:'Maggi',        price:38};
const BF_ALU    = {id:'alu',   name:'Alu paratha',  price:38};
const BF_MAC    = {id:'mac',   name:'Macaroni',     price:38};
const BF_DAAL   = {id:'daal',  name:'Daal poori',   price:38};

const breakfastBase = [BF_MEDU, BF_PONGAL, BF_SAMBAR, BF_CURD];

const specialBreakfastMap = {
  '1-1': BF_PAV,
  '3-2': BF_PAV,
  '1-3': BF_MAGGI,
  '1-5': BF_ALU,
  '4-3': BF_ALU,
  '2-3': BF_MAC,
  '2-4': BF_MAC,
  '4-5': BF_DAAL
};

const breakfastAll = [
  BF_MEDU, BF_PONGAL, BF_SAMBAR, BF_CURD,
  BF_PAV, BF_MAGGI, BF_ALU, BF_MAC, BF_DAAL
];

function getBreakfastConfig(week, dayIndex){
  const key = `${week}-${dayIndex}`;
  const special = specialBreakfastMap[key];
  if(special){
    return { defaultId: special.id, options: [special, ...breakfastBase] };
  }
  return { defaultId: null, options: breakfastBase };
}

/* ---------- Lunch & dinner options ---------- */
const lunchOptions = [
  {id:'l-biryani',  name:'Biryani',      price:85},
  {id:'l-sambar',   name:'Sambar rice',  price:57}
];

const dinnerOptions = [
  {id:'d-dosa',     name:'Dosa',     price:48},
  {id:'d-fish',     name:'Fish',     price:90},
  {id:'d-veg',      name:'Veg',      price:95},
  {id:'d-chicken',  name:'Chicken',  price:110},
  {id:'d-mushroom', name:'Mushroom', price:80},
  {id:'d-biryani',  name:'Biryani',  price:131}
];

const DEFAULT_BUDGETS = {
  weekly:840, sunday:2140, weekdays:3360, grandTotal:5500
};

const WEEK_DAYS = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];

/* ---------- State ---------- */
function loadState(){
  const raw = localStorage.getItem('mealsync_state');
  if(raw) {
    try {
      const parsed = JSON.parse(raw);
      if(!parsed.modified) parsed.modified = {};
      if(!parsed.budgets) parsed.budgets = {};
      if(!parsed.weeks) parsed.weeks = {};
      for(let w=1; w<=4; w++){
        if(!parsed.weeks[w]) parsed.weeks[w] = {};
      }
      return parsed;
    } catch(e){}
  }
  const s = { selectedWeek:1, weeks:{}, dayChoice:{}, budgets:{}, modified:{} };
  for(let w=1;w<=4;w++) s.weeks[w] = {};
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
  let list;
  if(mealType==='breakfast') list = breakfastAll;
  else if(mealType==='lunch') list = lunchOptions;
  else list = dinnerOptions;
  const found = list.find(x=>x.id===sel);
  return found ? found.price : 0;
}

/* ---------- Icon helper ---------- */
function createMealIcon(kind){
  const span = document.createElement('span');
  span.className = 'select-icon select-icon-' + kind;
  let svg = '';
  if(kind === 'breakfast'){
    svg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 10h13a3 3 0 0 0 0-6H4v6z"/><path d="M17 4v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V4"/><line x1="6" y1="18" x2="16" y2="18"/><line x1="8" y1="22" x2="14" y2="22"/></svg>';
  } else if(kind === 'lunch'){
    svg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="6.34" y2="6.34"/><line x1="17.66" y1="17.66" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="6.34" y2="17.66"/><line x1="17.66" y1="6.34" x2="19.07" y2="4.93"/></svg>';
  } else {
    svg = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  }
  span.innerHTML = svg;
  span.title = kind.charAt(0).toUpperCase() + kind.slice(1);
  return span;
}

/* ---------- Diff helper ---------- */
function diffHtml(cost, budgetVal){
  const b = parseFloat(budgetVal);
  if(isNaN(b)) return '';
  const diff = b - cost;
  if(Math.abs(diff) < 0.005) return '';
  const abs = Math.abs(diff).toFixed(2);
  const text = diff > 0 ? `+ ${abs}` : `- ${abs}`;
  const cls = diff > 0 ? 'diff-pos' : 'diff-neg';
  return ` <span class="${cls}">(${text})</span>`;
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

  for(let cell=0; cell<8; cell++){
    const card = document.createElement('div');
    card.className = 'card';
    if(cell<7){
      const day = cell;
      const hdr = document.createElement('div'); hdr.className='day-header';
      const title = document.createElement('div'); title.className='day-title';
      title.innerText = WEEK_DAYS[day];
      if(day===6) title.className += ' sunday';
      hdr.appendChild(title);

      if(day!==6){
        const key = `${week}-w${day}`;
        if(!state.dayChoice[key]) state.dayChoice[key]='breakfast';
        const tbtn = document.createElement('button');
        tbtn.className='toggle-btn';
        tbtn.innerText='⇄';
        tbtn.title='Toggle breakfast / lunch';
        tbtn.onclick = ()=>{
          state.dayChoice[key] = (state.dayChoice[key]==='breakfast' ? 'lunch' : 'breakfast');
          saveState();
          makeGrid();
          updateSummary();
        };
        hdr.appendChild(tbtn);
      }
      card.appendChild(hdr);

      const mainType = (day===6) ? 'lunch' : state.dayChoice[`${week}-w${day}`] || 'breakfast';

      /* MAIN SELECT */
      const mainWrapper = document.createElement('div');
      mainWrapper.className = 'select-wrapper';
      mainWrapper.appendChild(createMealIcon(mainType));
      const mainSelect = document.createElement('select');
      const mainSelKey = `sel-${week}-${day}-${mainType}`;

      let opts;
      let defaultVal = 'skip';
      if(mainType==='breakfast'){
        const cfg = getBreakfastConfig(week, day);
        opts = cfg.options;
        if(cfg.defaultId) defaultVal = cfg.defaultId;
      } else if(mainType==='lunch'){
        if(day === 6){ opts = []; } else { opts = lunchOptions; }
      } else {
        if(day === 6){ opts = []; } else { opts = dinnerOptions; }
      }

      if(!(mainSelKey in state.weeks[week])) {
        state.weeks[week][mainSelKey] = defaultVal;
      } else if(mainType==='breakfast') {
        if(defaultVal && state.weeks[week][mainSelKey] === 'skip' && !state.modified[mainSelKey]) {
          state.weeks[week][mainSelKey] = defaultVal;
        }
      }

      mainSelect.innerHTML = '';
      const addOption = (value, label) => {
        const o = document.createElement('option');
        o.value=value; o.innerText=label;
        if(state.weeks[week][mainSelKey]===value) o.selected = true;
        mainSelect.appendChild(o);
      };
      addOption('skip','Skip this meal');
      opts.forEach(m => addOption(m.id, `${m.name} (₹ ${m.price.toFixed(2)})`));
      addOption('custom','Custom price (type ₹)');
      mainSelect.onchange = (e)=>{
        state.weeks[week][mainSelKey] = e.target.value;
        state.modified[mainSelKey] = true;
        if(e.target.value==='custom'){
          const pk = `price-${week}-${day}-${mainType}`;
          if(!(pk in state.weeks[week])) state.weeks[week][pk] = '0';
        }
        saveState();
        makeGrid();
        updateSummary();
      };
      mainWrapper.appendChild(mainSelect);
      card.appendChild(mainWrapper);

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

      /* DINNER SELECT */
      const dinnerWrapper = document.createElement('div');
      dinnerWrapper.className = 'select-wrapper';
      dinnerWrapper.appendChild(createMealIcon('dinner'));

      const dinnerKey = `sel-${week}-${day}-dinner`;
      if(!(dinnerKey in state.weeks[week])) state.weeks[week][dinnerKey] = 'skip';

      const dinnerSelect = document.createElement('select');
      dinnerSelect.innerHTML = '';

      const addD = (v,l)=>{
        const o=document.createElement('option');
        o.value=v; o.innerText=l;
        if(state.weeks[week][dinnerKey]===v) o.selected=true;
        dinnerSelect.appendChild(o);
      };

      addD('skip','Skip this meal');
      if(day !== 6){
        dinnerOptions.forEach(m => addD(m.id, `${m.name} (₹ ${m.price.toFixed(2)})`));
      }
      addD('custom','Custom price (type ₹)');
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
      dinnerWrapper.appendChild(dinnerSelect);
      card.appendChild(dinnerWrapper);

      if(state.weeks[week][dinnerKey] === 'custom'){
        const pk=`price-${week}-${day}-dinner`;
        if(!(pk in state.weeks[week])) state.weeks[week][pk]='0';
        const input = document.createElement('input');
        input.type='text';
        input.value= state.weeks[week][pk];
        input.oninput=(e)=>{
          state.weeks[week][pk]=e.target.value;
          saveState();
          updateSummary();
        };
        card.appendChild(input);
      }

      /* ---- DAY TOTAL ROW ---- */
      let dayTotal = 0;
      const mainSel = state.weeks[week][mainSelKey] || 'skip';
      dayTotal += priceForSelection(mainType, mainSel, week, day);
      const dSel = state.weeks[week][dinnerKey] || 'skip';
      dayTotal += priceForSelection('dinner', dSel, week, day);

      const dayLimit = (day === 6) ? 535 : 140; // Sun vs Mon–Sat

      const totalRow = document.createElement('div');
      totalRow.style.display = 'flex';
      totalRow.style.justifyContent = 'space-between';
      totalRow.style.marginTop = '6px';
      totalRow.style.fontSize = '13px';

      const totalLabel = document.createElement('div');
      totalLabel.textContent = 'Day total:';

      const totalVal = document.createElement('div');
      totalVal.innerHTML = '₹ ' + dayTotal.toFixed(2) + diffHtml(dayTotal, dayLimit);

      totalRow.appendChild(totalLabel);
      totalRow.appendChild(totalVal);
      card.appendChild(totalRow);

    } else {
      /* Budgets card */
      const hdr = document.createElement('div'); hdr.className='day-header';
      const title = document.createElement('div'); title.className='day-title budgets'; title.innerText='Budgets';
      hdr.appendChild(title);
      card.appendChild(hdr);

      const keys = [
        {k:'weekly', label:'Week Total'},
        {k:'sunday', label:'Sunday Total (all 4 weeks)'},
        {k:'weekdays', label:'Weekdays Total (all 4 weeks)'},
        {k:'grandTotal', label:'Grand Total'}
      ];
      keys.forEach(item=>{
        const lab = document.createElement('div');
        lab.className='budget-label';
        lab.innerText = item.label;
        card.appendChild(lab);

        const row = document.createElement('div');
        row.className='budget-row';

        if(!(item.k in state.budgets)) state.budgets[item.k] = DEFAULT_BUDGETS[item.k].toFixed(2);
        const inp = document.createElement('input');
        inp.type='text';
        inp.value=state.budgets[item.k];
        inp.oninput = (e)=>{ state.budgets[item.k] = e.target.value; saveState(); updateSummary(); };
        row.appendChild(inp);

        const btn = document.createElement('button');
        btn.className='budget-default-btn';
        btn.innerText='Default';
        btn.onclick = ()=>{
          state.budgets[item.k] = DEFAULT_BUDGETS[item.k].toFixed(2);
          saveState();
          makeGrid();
          updateSummary();
        };
        row.appendChild(btn);

        card.appendChild(row);
      });
    }

    grid.appendChild(card);
  }

  saveState();
}

/* ---------- Summary/calculation with coloured diff ---------- */
function updateSummary(){
  const week = state.selectedWeek;
  let curWeek = 0;
  for(let d=0; d<6; d++){
    const mainType = (d===6) ? 'lunch' : (state.dayChoice[`${week}-w${d}`] || 'breakfast');
    const selKey = `sel-${week}-${d}-${mainType}`;
    const sel = state.weeks[week][selKey] || 'skip';
    curWeek += priceForSelection(mainType, sel, week, d);
    const dk = `sel-${week}-${d}-dinner`;
    const dsel = state.weeks[week][dk] || 'skip';
    curWeek += priceForSelection('dinner', dsel, week, d);
  }

  let sunTotal=0;
  for(let w=1; w<=4; w++){
    const s1 = state.weeks[w][`sel-${w}-6-lunch`] || 'skip';
    const s2 = state.weeks[w][`sel-${w}-6-dinner`] || 'skip';
    sunTotal += priceForSelection('lunch', s1, w, 6);
    sunTotal += priceForSelection('dinner', s2, w, 6);
  }

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

  const grand = weekdaysTotal + sunTotal;

  const bWeekly   = state.budgets.weekly    || DEFAULT_BUDGETS.weekly;
  const bSunday   = state.budgets.sunday    || DEFAULT_BUDGETS.sunday;
  const bWeekdays = state.budgets.weekdays  || DEFAULT_BUDGETS.weekdays;
  const bGrand    = state.budgets.grandTotal || DEFAULT_BUDGETS.grandTotal;

  document.getElementById('curWeekVal').innerHTML =
    '₹ '+curWeek.toFixed(2) + diffHtml(curWeek, bWeekly);
  document.getElementById('sunTotalVal').innerHTML =
    '₹ '+sunTotal.toFixed(2) + diffHtml(sunTotal, bSunday);
  document.getElementById('wdTotalVal').innerHTML =
    '₹ '+weekdaysTotal.toFixed(2) + diffHtml(weekdaysTotal, bWeekdays);
  document.getElementById('grandVal').innerHTML =
    '₹ '+grand.toFixed(2) + diffHtml(grand, bGrand);
}

/* ---------- Init ---------- */
function ensureStructure(){
  for(let w=1; w<=4; w++){
    if(!state.weeks[w]) state.weeks[w] = {};
  }
  if(!state.budgets) state.budgets = {};
  if(!state.modified) state.modified = {};
  saveState();
}

ensureStructure();
makeWeekButtons();
makeGrid();
updateSummary();
window.mealsyncState = state;
</script>
</body>
</html>
"""

components.html(html, height=900, scrolling=True)
