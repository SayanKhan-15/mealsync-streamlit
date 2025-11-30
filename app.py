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
      --bg:#020617;
      --card-inner:#0b1220;
      --muted:#9fb6c9;
      --accent:#2563EB;
      --green:#4ade80;
      --red:#fb7185;
      --text:#e6eef8;
      font-family: Inter, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
    }

    html,body {
      height:100%;
      margin:0;
      padding:0;
      background: var(--bg);
      color:var(--text);
    }

    .container { max-width:1200px; margin:18px auto; padding:18px; box-sizing:border-box; }

    h1 {
      text-align:center;
      color:#38bdf8;
      font-size:32px;
      margin:0 0 6px 0;
      font-weight:700;
      letter-spacing:0.04em;
    }
    p.subtitle { text-align:center; color: #9aaec0; margin:0 0 18px 0; }

    /* Week selector */
    .week-row {
      display:flex;
      justify-content:center;
      gap:12px;
      margin:18px 0 18px 0;
      flex-wrap:nowrap;
      overflow-x:auto;
      -webkit-overflow-scrolling:touch;
      padding-bottom:6px;
    }
    .week-btn {
      padding:8px 18px;
      border-radius:10px;
      border:1px solid rgba(148,163,184,0.6);
      background: #020617;
      color:var(--text);
      cursor:pointer;
      font-size:14px;
      flex:0 0 auto;
    }
    .week-btn.active {
      background: var(--accent);
      color:white;
      border-color:#1D4ED8;
    }

    /* 2x4 grid by default */
    .grid {
      display:grid;
      grid-template-columns:repeat(4,1fr);
      gap:18px;
      margin-top:8px;
    }

    /* Responsive breakpoints */
    @media (max-width: 1100px) {
      .grid { grid-template-columns:repeat(2,1fr); }
    }
    @media (max-width: 600px) {
      .container { padding:12px; max-width:100%; }
      h1 { font-size:26px; margin-bottom:6px; }
      .grid { grid-template-columns:1fr; gap:12px; }
      .week-row { gap:8px; margin:12px 0; }
      .week-btn { padding:7px 12px; font-size:13px; }
    }

    /* Cards (shared look) */
    .card {
      background: var(--card-inner);
      border-radius:12px;
      border:1px solid rgba(31,41,55,0.9);
      padding: 14px;
      box-sizing:border-box;
      height: 310px;
      display:flex;
      flex-direction:column;
      justify-content:flex-start;
    }

    /* On small screens make card height auto so content flows naturally */
    @media (max-width: 600px) {
      .card { height: auto; min-height: 220px; padding:12px; }
    }

    .day-header {
      display:flex;
      justify-content:space-between;
      align-items:center;
      margin-bottom:10px;
    }
    .day-title {
      font-weight:700;
      color:#3B82F6;
      font-size:18px;
    }
    .day-title.sunday { color:#F87171; }
    .day-title.budgets { color:#ffffff; }

    .toggle-btn {
      width:30px;
      height:30px;
      border-radius:999px;
      border:1px solid rgba(148,163,184,0.7);
      background: #020617;
      cursor:pointer;
      display:flex;
      align-items:center;
      justify-content:center;
      font-size:16px;
      color:#9ca3af;
      padding:0;
    }
    @media (max-width:600px){ .toggle-btn{ width:28px; height:28px; font-size:14px; } }

    /* Meal rows styled */
    .meal-row {
      position:relative;
      display:flex;
      align-items:center;
      justify-content:space-between;
      padding:10px 12px;
      margin-top:10px;
      border-radius:10px;
      background: #020617;
      border:1px solid rgba(51,65,85,0.9);
      box-sizing:border-box;
      min-height:48px;
    }
    @media (max-width:600px){
      .meal-row { padding:10px; min-height:46px; }
    }

    .meal-row-inner{
      display:flex;
      align-items:center;
      gap:10px;
      /* removed z-index so clicks go to the overlay select */
    }

    /* allows full text to show, wrapping if needed */
    .meal-label{
      font-size:14px;
      color:#e5e7eb;
      line-height:1.3;
    }
    .meal-label.muted{
      color:#9ca3af;
    }

    /* Invisible select overlay so the text stays visible but native control works */
    .meal-select {
      position:absolute;
      inset:0;
      opacity:0;
      cursor:pointer;
      width:100%;
      height:100%;
      z-index:1; /* ensure the whole row is clickable */
    }

    select option {
      background-color:#020617;
      color:#e6eef8;
    }

    .select-icon svg {
      width:24px;
      height:24px;
      display:block;
    }
    .select-icon-breakfast svg { color:#93C5FD; }
    .select-icon-lunch svg     { color:#FDE047; }
    .select-icon-dinner svg    { color:#C9A8EE; }

    .budget-label { font-size:13px; color:var(--muted); margin:5px 0 3px 0; }
    .budget-row { display:flex; gap:8px; align-items:center; margin-bottom:6px; }
    .budget-row input[type="text"] {
      flex:1; padding:7px 10px; border-radius:10px;
      background: #020617; border:1px solid rgba(51,65,85,0.9);
      color:var(--text);
      box-sizing:border-box; font-size:13px;
    }
    .budget-default-btn {
      padding:6px 10px; border-radius:999px; min-width:80px; white-space:nowrap; cursor:pointer;
      border:1px solid #1D4ED8; background: #2563EB; color:#e5f2ff; font-size:12px; font-weight:600;
    }

    /* Custom price input inside day cards */
    .custom-input {
      width:100%;
      box-sizing:border-box;
      padding:8px 10px;
      border-radius:8px;
      border:1px solid rgba(51,65,85,0.9);
      background:#020617;
      color:#e5e7eb;
      font-size:13px;
      margin-top:8px;
    }

    .summary {
      margin-top:16px; border-radius:10px; padding:14px; background: #020617;
      border:1px solid rgba(30,64,175,0.12);
    }
    .summary-row {
      display:flex;
      justify-content:space-between;
      margin-bottom:8px;
    }
    .summary-row .val {
      font-weight:700;
      color:#bfe6ff;
    }
    /* ensure label like "Current Week Total" stays on a single line */
    .summary-row > div:first-child {
      white-space: nowrap;
    }

    /* NOT bold for diff text */
    .diff-pos { color:var(--green); font-weight:400; }
    .diff-neg { color:var(--red);   font-weight:400; }

    .day-total-row{
      display:flex; justify-content:space-between; margin-top:8px; font-size:13px; color:#e5e7eb;
    }

    /* hide focus outline for the invisible select overlay for nicer look on mobile */
    .meal-select:focus { outline: none; }

    input::-webkit-outer-spin-button, input::-webkit-inner-spin-button { -webkit-appearance: none; margin: 0; }
  </style>
</head>
<body>
<div class="container">
  <h1>MealSync</h1>
  <p class="subtitle">Your weekly meal planning, simplified.</p>

  <div class="week-row" id="weekRow" aria-label="Week selector"></div>
  <div style="height:10px;"></div>
  <div class="grid" id="grid" aria-live="polite"></div>

  <div style="height:12px;"></div>
  <div class="summary" id="summary" role="region" aria-label="Cost summary">
    <div style="font-weight:700; margin-bottom:8px;">Cost Summary</div>
    <div class="summary-row"><div>Current Week Total:</div><div class="val" id="curWeekVal">₹ 0.00</div></div>
    <div class="summary-row"><div>Sunday Total:</div><div class="val" id="sunTotalVal">₹ 0.00</div></div>
    <hr style="border-color:rgba(255,255,255,0.04)"/>
    <div class="summary-row"><div>Weekdays Total:</div><div class="val" id="wdTotalVal">₹ 0.00</div></div>
    <div class="summary-row"><div>Grand Total:</div><div class="val" id="grandVal">₹ 0.00</div></div>
  </div>
</div>

<script>
(function() {
  /* ---------- Data ---------- */
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
    '1-1': BF_PAV, '3-2': BF_PAV, '1-3': BF_MAGGI, '1-5': BF_ALU,
    '4-3': BF_ALU, '2-3': BF_MAC, '2-4': BF_MAC, '4-5': BF_DAAL
  };
  const breakfastAll = [...breakfastBase, BF_PAV, BF_MAGGI, BF_ALU, BF_MAC, BF_DAAL];

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

  const DEFAULT_BUDGETS = { weekly:840, sunday:2140, weekdays:3360, grandTotal:5500 };
  const WEEK_DAYS = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];

  /* ---------- localStorage state helpers ---------- */
  function loadState(){
    const raw = localStorage.getItem('mealsync_state');
    if(raw){
      try{
        const parsed = JSON.parse(raw);
        if(!parsed.modified) parsed.modified = {};
        if(!parsed.budgets) parsed.budgets = {};
        if(!parsed.weeks) parsed.weeks = {};
        for(let w=1; w<=4; w++){ if(!parsed.weeks[w]) parsed.weeks[w] = {}; }
        return parsed;
      } catch(e){}
    }
    const s = { selectedWeek:1, weeks:{}, dayChoice:{}, budgets:{}, modified:{} };
    for(let w=1; w<=4; w++) s.weeks[w] = {};
    for(const k in DEFAULT_BUDGETS) s.budgets[k] = DEFAULT_BUDGETS[k].toFixed(2);
    localStorage.setItem('mealsync_state', JSON.stringify(s));
    return s;
  }
  function saveState(){ localStorage.setItem('mealsync_state', JSON.stringify(state)); }

  function priceForSelection(mealType, sel, week, day){
    if(sel==='skip') return 0;
    if(sel==='custom'){
      const key = `price-${week}-${day}-${mealType}`;
      const v = state.weeks[week][key];
      return parseFloat(v || 0) || 0;
    }
    let list = (mealType==='breakfast') ? breakfastAll : (mealType==='lunch' ? lunchOptions : dinnerOptions);
    const found = list.find(x=>x.id===sel);
    return found ? found.price : 0;
  }
  function getBreakfastConfig(week, dayIndex){
    const key = `${week}-${dayIndex}`;
    const special = specialBreakfastMap[key];
    if(special) return { defaultId: special.id, options: [special, ...breakfastBase] };
    return { defaultId: null, options: breakfastBase };
  }
  function createMealIcon(kind){
    if(kind === 'breakfast'){
      return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 10h13a3 3 0 0 0 0-6H4v6z"/><path d="M17 4v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V4"/><line x1="6" y1="18" x2="16" y2="18"/><line x1="8" y1="22" x2="14" y2="22"/></svg>';
    } else if(kind === 'lunch'){
      return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="4.93" y1="4.93" x2="6.34" y2="6.34"/><line x1="17.66" y1="17.66" x2="19.07" y2="19.07"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/><line x1="4.93" y1="19.07" x2="6.34" y2="17.66"/><line x1="17.66" y1="6.34" x2="19.07" y2="4.93"/></svg>';
    }
    return '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  }
  function diffHtml(cost, budgetVal){
    const b = parseFloat(budgetVal);
    if(isNaN(b)) return '';
    const diff = b - cost;
    if(Math.abs(diff) < 0.005) return '';
    const abs = Math.abs(diff).toFixed(2);
    const text = diff > 0 ? `+${abs}` : `-${abs}`;
    const cls = diff > 0 ? 'diff-pos' : 'diff-neg';
    return ` <span class="${cls}">(${text})</span>`;
  }

  const state = loadState();

  function makeWeekButtons(){
    const wr = document.getElementById('weekRow');
    if(!wr) return;
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
    if(!grid) return;
    grid.innerHTML = '';
    const week = state.selectedWeek;

    for(let cell=0; cell<8; cell++){
      const card = document.createElement('div');
      card.className = 'card';

      if(cell < 7){
        const day = cell;
        const hdr = document.createElement('div'); hdr.className='day-header';
        const title = document.createElement('div'); title.className='day-title';
        title.innerText = WEEK_DAYS[day];
        if(day === 6) title.className += ' sunday';
        hdr.appendChild(title);

        if(day !== 6){
          const key = `${week}-w${day}`;
          if(!state.dayChoice[key]) state.dayChoice[key] = 'breakfast';
          const tbtn = document.createElement('button');
          tbtn.className='toggle-btn';
          tbtn.innerText='⇄';
          tbtn.title='Toggle breakfast / lunch';
          tbtn.onclick = ()=>{
            state.dayChoice[key] = (state.dayChoice[key] === 'breakfast' ? 'lunch' : 'breakfast');
            saveState(); makeGrid(); updateSummary();
          };
          hdr.appendChild(tbtn);
        }
        card.appendChild(hdr);

        const mainType = (day === 6) ? 'lunch' : state.dayChoice[`${week}-w${day}`] || 'breakfast';

        // MAIN MEAL ROW
        const mainRow = document.createElement('div');
        mainRow.className = 'meal-row';
        const mainInner = document.createElement('div');
        mainInner.className = 'meal-row-inner';
        const mainIcon = document.createElement('span');
        mainIcon.className = 'select-icon select-icon-' + (mainType === 'breakfast' ? 'breakfast' : (mainType === 'lunch' ? 'lunch' : 'dinner'));
        mainIcon.innerHTML = createMealIcon(mainType);
        mainInner.appendChild(mainIcon);
        const mainLabel = document.createElement('span');
        mainLabel.className = 'meal-label';
        mainInner.appendChild(mainLabel);
        mainRow.appendChild(mainInner);

        const mainSelect = document.createElement('select');
        mainSelect.className = 'meal-select';
        const mainSelKey = `sel-${week}-${day}-${mainType}`;

        let opts = [];
        let defaultVal = 'skip';
        if(mainType === 'breakfast'){
          const cfg = getBreakfastConfig(week, day);
          opts = cfg.options;
          if(cfg.defaultId) defaultVal = cfg.defaultId;
        } else if(mainType === 'lunch'){
          if(day === 6) opts = []; else opts = lunchOptions;
        } else {
          if(day === 6) opts = []; else opts = dinnerOptions;
        }

        if(!(mainSelKey in state.weeks[week])){
          state.weeks[week][mainSelKey] = defaultVal;
        } else if(mainType === 'breakfast'){
          if(defaultVal && state.weeks[week][mainSelKey] === 'skip' && !state.modified[mainSelKey]){
            state.weeks[week][mainSelKey] = defaultVal;
          }
        }

        mainSelect.innerHTML = '';
        const addOption = (value, label) => {
          const o = document.createElement('option'); o.value = value; o.innerText = label;
          if(state.weeks[week][mainSelKey] === value) o.selected = true;
          mainSelect.appendChild(o);
        };
        addOption('skip','Not planned');
        opts.forEach(m => addOption(m.id, `${m.name} (₹ ${m.price.toFixed(2)})`));
        addOption('custom','Custom price (type ₹)');
        mainSelect.onchange = (e) => {
          state.weeks[week][mainSelKey] = e.target.value;
          state.modified[mainSelKey] = true;
          if(e.target.value === 'custom'){
            const pk = `price-${week}-${day}-${mainType}`;
            if(!(pk in state.weeks[week])) state.weeks[week][pk] = '0';
          }
          saveState(); makeGrid(); updateSummary();
        };
        mainRow.appendChild(mainSelect);
        card.appendChild(mainRow);

        if(state.weeks[week][mainSelKey] === 'custom'){
          const pk = `price-${week}-${day}-${mainType}`;
          if(!(pk in state.weeks[week])) state.weeks[week][pk] = '0';
          const input = document.createElement('input');
          input.type = 'text';
          input.value = state.weeks[week][pk];
          input.className = 'custom-input';
          input.oninput = (e) => { state.weeks[week][pk] = e.target.value; saveState(); updateSummary(); };
          card.appendChild(input);
        }

        // DINNER ROW
        const dinnerRow = document.createElement('div');
        dinnerRow.className = 'meal-row';
        const dinnerInner = document.createElement('div');
        dinnerInner.className = 'meal-row-inner';
        const dinnerIcon = document.createElement('span');
        dinnerIcon.className = 'select-icon select-icon-dinner';
        dinnerIcon.innerHTML = createMealIcon('dinner');
        dinnerInner.appendChild(dinnerIcon);
        const dinnerLabel = document.createElement('span');
        dinnerLabel.className = 'meal-label';
        dinnerInner.appendChild(dinnerLabel);
        dinnerRow.appendChild(dinnerInner);

        const dinnerKey = `sel-${week}-${day}-dinner`;
        if(!(dinnerKey in state.weeks[week])) state.weeks[week][dinnerKey] = 'skip';

        const dinnerSelect = document.createElement('select');
        dinnerSelect.className = 'meal-select';
        dinnerSelect.innerHTML = '';
        const addD = (v,l) => { const o = document.createElement('option'); o.value = v; o.innerText = l; if(state.weeks[week][dinnerKey]===v) o.selected = true; dinnerSelect.appendChild(o); };
        addD('skip','Not planned');
        if(day !== 6) dinnerOptions.forEach(m => addD(m.id, `${m.name} (₹ ${m.price.toFixed(2)})`));
        addD('custom','Custom price (type ₹)');
        dinnerSelect.onchange = (e) => {
          state.weeks[week][dinnerKey] = e.target.value;
          if(e.target.value === 'custom'){
            const pk = `price-${week}-${day}-dinner`;
            if(!(pk in state.weeks[week])) state.weeks[week][pk] = '0';
          }
          saveState(); makeGrid(); updateSummary();
        };
        dinnerRow.appendChild(dinnerSelect);
        card.appendChild(dinnerRow);

        if(state.weeks[week][dinnerKey] === 'custom'){
          const pk = `price-${week}-${day}-dinner`;
          if(!(pk in state.weeks[week])) state.weeks[week][pk] = '0';
          const input = document.createElement('input');
          input.type = 'text';
          input.value = state.weeks[week][pk];
          input.className = 'custom-input';
          input.oninput = (e) => { state.weeks[week][pk] = e.target.value; saveState(); updateSummary(); };
          card.appendChild(input);
        }

        // DAY TOTAL
        const mainSelVal = state.weeks[week][mainSelKey] || 'skip';
        const dinnerSelVal = state.weeks[week][dinnerKey] || 'skip';
        const dayTotal = priceForSelection(mainType, mainSelVal, week, day) + priceForSelection('dinner', dinnerSelVal, week, day);
        const dayLimit = (day === 6) ? 535 : 140;
        const totalRow = document.createElement('div');
        totalRow.className = 'day-total-row';
        const totalLabel = document.createElement('div'); totalLabel.textContent = 'Day total:';
        const totalVal = document.createElement('div'); totalVal.innerHTML = '₹ ' + dayTotal.toFixed(2) + diffHtml(dayTotal, dayLimit);
        totalRow.appendChild(totalLabel); totalRow.appendChild(totalVal);
        card.appendChild(totalRow);

        function labelForSelection(sel, type){
          if(sel==='skip') return 'Not planned';
          if(sel==='custom'){ const pk=`price-${week}-${day}-${type}`; const v=(state.weeks[week][pk]||'0').trim(); const n=parseFloat(v); return 'Custom (₹ '+(isNaN(n)?v:n.toFixed(2))+')'; }
          const list = (type==='breakfast') ? breakfastAll : (type==='lunch' ? lunchOptions : dinnerOptions);
          const found = list.find(x=>x.id===sel);
          return found ? `${found.name} (₹ ${found.price.toFixed(2)})` : 'Not planned';
        }
        mainLabel.textContent = labelForSelection(mainSelVal, mainType);
        if(mainSelVal==='skip') mainLabel.classList.add('muted');
        dinnerLabel.textContent = labelForSelection(dinnerSelVal, 'dinner');
        if(dinnerSelVal==='skip') dinnerLabel.classList.add('muted');

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
          const lab = document.createElement('div'); lab.className='budget-label'; lab.innerText = item.label;
          card.appendChild(lab);

          const row = document.createElement('div'); row.className='budget-row';
          if(!(item.k in state.budgets)) state.budgets[item.k] = DEFAULT_BUDGETS[item.k].toFixed(2);
          const inp = document.createElement('input'); inp.type='text'; inp.value = state.budgets[item.k];
          inp.oninput = (e)=>{ state.budgets[item.k] = e.target.value; saveState(); updateSummary(); };
          row.appendChild(inp);

          const btn = document.createElement('button'); btn.className='budget-default-btn'; btn.innerText='Default';
          btn.onclick = ()=>{
            state.budgets[item.k] = DEFAULT_BUDGETS[item.k].toFixed(2); saveState(); makeGrid(); updateSummary();
          };
          row.appendChild(btn);
          card.appendChild(row);
        });
      }

      grid.appendChild(card);
    }

    saveState();
  }

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

    let sunTotal = 0;
    for(let w=1; w<=4; w++){
      const s1 = state.weeks[w][`sel-${w}-6-lunch`] || 'skip';
      const s2 = state.weeks[w][`sel-${w}-6-dinner`] || 'skip';
      sunTotal += priceForSelection('lunch', s1, w, 6);
      sunTotal += priceForSelection('dinner', s2, w, 6);
    }

    let weekdaysTotal = 0;
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

    const cur = document.getElementById('curWeekVal');
    const sun = document.getElementById('sunTotalVal');
    const wd = document.getElementById('wdTotalVal');
    const gr = document.getElementById('grandVal');
    if(cur) cur.innerHTML = '₹ '+curWeek.toFixed(2) + diffHtml(curWeek, bWeekly);
    if(sun) sun.innerHTML = '₹ '+sunTotal.toFixed(2) + diffHtml(sunTotal, bSunday);
    if(wd) wd.innerHTML = '₹ '+weekdaysTotal.toFixed(2) + diffHtml(weekdaysTotal, bWeekdays);
    if(gr) gr.innerHTML = '₹ '+grand.toFixed(2) + diffHtml(grand, bGrand);
  }

  function ensureStructure(){
    for(let w=1; w<=4; w++){ if(!state.weeks[w]) state.weeks[w] = {}; }
    if(!state.budgets) state.budgets = {};
    if(!state.modified) state.modified = {};
    saveState();
  }

  window.addEventListener('DOMContentLoaded', function(){
    ensureStructure();
    makeWeekButtons();
    makeGrid();
    updateSummary();
    window.mealsyncState = state;
  });

})();
</script>
</body>
</html>
"""

# High height so everything scrolls nicely on mobile
components.html(html, height=1600, scrolling=True)
