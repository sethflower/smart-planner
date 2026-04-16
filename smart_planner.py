"""
Smart Planner Pro — Windows Desktop Application
Requires: pip install pywebview
"""
import webview
import database as db
from api import Api
import os
import sys

def get_html():
    """Return the full HTML for the application, with pywebview.api bridge."""
    return r'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smart Planner Pro</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600;700&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{
--bg:#F0F4FA;--bg2:#FFFFFF;--bg3:#F6F8FC;--bg4:#EDF1F7;
--card:#FFFFFF;--card2:#F8FAFD;--card-hover:#F2F5FB;
--accent:#4361EE;--accent2:#3A56D4;--accent3:#5B76F0;--accent-bg:rgba(67,97,238,.08);
--green:#10B981;--green2:#059669;--green-bg:rgba(16,185,129,.08);
--amber:#F59E0B;--amber2:#D97706;--amber-bg:rgba(245,158,11,.08);
--red:#EF4444;--red2:#DC2626;--red-bg:rgba(239,68,68,.08);
--cyan:#06B6D4;--cyan2:#0891B2;--cyan-bg:rgba(6,182,212,.08);
--pink:#EC4899;--pink2:#DB2777;--pink-bg:rgba(236,72,153,.08);
--orange:#F97316;--orange2:#EA580C;--orange-bg:rgba(249,115,22,.08);
--text:#1E293B;--text2:#475569;--text3:#94A3B8;--text4:#CBD5E1;
--border:#E2E8F0;--border2:#CBD5E1;
--radius:14px;--radius-lg:20px;
--shadow:0 1px 3px rgba(0,0,0,.06),0 2px 8px rgba(0,0,0,.04);--shadow-lg:0 8px 32px rgba(0,0,0,.1);
--font:'DM Sans',system-ui,-apple-system,sans-serif;--mono:'IBM Plex Mono',monospace;
--gradient:linear-gradient(135deg,#4361EE,#7C3AED);
--gradient2:linear-gradient(135deg,#10B981,#06B6D4);
--gradient3:linear-gradient(135deg,#4361EE 0%,#7C3AED 50%,#EC4899 100%);
}
html{font-family:var(--font);background:var(--bg);color:var(--text);font-size:14px;-webkit-font-smoothing:antialiased;line-height:1.5}
body{background:var(--bg);min-height:100vh}
button{font-family:var(--font);cursor:pointer;transition:all .2s ease}
input,select,textarea{font-family:var(--font)}
button:active{transform:scale(.96)}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border2);border-radius:8px}
::-webkit-scrollbar-thumb:hover{background:var(--accent)}
::selection{background:var(--accent);color:#fff}
.hdr{background:#FFFFFF;box-shadow:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);padding:0 32px;display:flex;align-items:center;height:64px;position:sticky;top:0;z-index:100;gap:16px;border-bottom:1px solid var(--border)}
.hdr-brand{display:flex;align-items:center;gap:12px;margin-right:auto}
.hdr-logo{width:38px;height:38px;border-radius:12px;background:var(--gradient);display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 4px 12px rgba(67,97,238,.3)}
.hdr-brand h1{color:var(--text);font-size:16px;font-weight:700;letter-spacing:-.3px}
.hdr-brand small{color:var(--text3);font-size:11px;font-weight:400}
.tabs{display:flex;height:64px;align-items:stretch;gap:2px}
.tab{padding:0 18px;border:none;background:0;color:var(--text3);font-weight:500;font-size:13px;position:relative;display:flex;align-items:center;gap:6px;border-radius:10px 10px 0 0;transition:all .2s}
.tab:hover{color:var(--text2);background:var(--bg)}
.tab.on{color:var(--accent);font-weight:700}
.tab.on::after{content:"";position:absolute;bottom:0;left:8px;right:8px;height:3px;background:var(--gradient);border-radius:3px 3px 0 0}
.tab .tab-icon{font-size:15px}
.add-b{height:38px;padding:0 20px;border-radius:12px;border:none;background:var(--gradient);color:#fff;font-weight:600;font-size:13px;display:flex;align-items:center;gap:6px;box-shadow:0 2px 10px rgba(67,97,238,.25);letter-spacing:.2px}
.add-b:hover{box-shadow:0 4px 16px rgba(67,97,238,.35);transform:translateY(-1px)}
.set-b{width:38px;height:38px;border-radius:12px;border:1px solid var(--border);background:var(--bg);color:var(--text3);font-size:16px;display:flex;align-items:center;justify-content:center}
.set-b:hover{background:var(--bg4);color:var(--text);border-color:var(--border2)}
.main{padding:28px 32px;max-width:1400px;margin:0 auto}
.card{background:var(--card);border-radius:var(--radius-lg);border:1px solid var(--border);padding:22px;transition:all .2s;position:relative;overflow:hidden}
.card:hover{border-color:var(--border2)}
.card::before{content:"";position:absolute;top:0;left:0;right:0;height:1px;background:var(--gradient);opacity:0;transition:opacity .3s}
.card:hover::before{opacity:.5}
.card-glow{box-shadow:0 0 40px rgba(67,97,238,.04)}
.stitle{font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:1.2px;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.stitle-icon{font-size:14px}
.kpi-r{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:24px}
.kpi{background:var(--card);border-radius:var(--radius);border:1px solid var(--border);padding:20px;position:relative;overflow:hidden;transition:all .3s}
.kpi:hover{transform:translateY(-2px);box-shadow:var(--shadow-lg)}
.kpi-glow{position:absolute;top:-20px;right:-20px;width:80px;height:80px;border-radius:50%;opacity:.06;filter:blur(20px);pointer-events:none}
.kpi-l{font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:1.2px}
.kpi-v{font-size:32px;font-weight:800;margin-top:6px;font-family:var(--mono);color:var(--accent)}
.kpi-v.green{color:var(--green)}
.kpi-v.plain{color:var(--text)}
.bdg{display:inline-flex;padding:3px 10px;border-radius:8px;font-size:11px;font-weight:600;white-space:nowrap;letter-spacing:.2px}
.pw{position:relative;width:100%;height:8px;background:var(--bg4);border-radius:10px;cursor:pointer;overflow:hidden;transition:height .2s}
.pw:hover{height:14px}
.pf{height:100%;border-radius:10px;transition:width .3s ease;pointer-events:none;position:relative}
.pf::after{content:attr(data-p);position:absolute;right:4px;top:50%;transform:translateY(-50%);font-size:9px;font-weight:700;color:#fff;opacity:0;transition:opacity .2s;font-family:var(--mono)}
.pw:hover .pf::after{opacity:1}
.tr{background:var(--card);border-radius:var(--radius);border:1px solid var(--border);padding:14px 16px;display:flex;align-items:center;gap:12px;cursor:pointer;transition:all .25s}
.tr:hover{border-color:var(--accent);box-shadow:0 4px 20px rgba(67,97,238,.1);transform:translateY(-1px)}
.tr.done{opacity:.35}
.task-left{width:4px;align-self:stretch;border-radius:4px;flex-shrink:0}
.seg{display:flex;border:1px solid var(--border);border-radius:10px;overflow:hidden;background:var(--card)}
.seg button{padding:8px 16px;border:none;background:transparent;color:var(--text3);font-size:12px;font-weight:600;border-right:1px solid var(--border);transition:all .2s}
.seg button:last-child{border:none}
.seg button:hover{color:var(--text2);background:var(--bg)}
.seg button.on{background:var(--accent);color:#fff}
.mo{position:fixed;inset:0;background:rgba(30,41,59,.5);display:flex;align-items:center;justify-content:center;z-index:1000;backdrop-filter:blur(8px);animation:fi .2s}
.md{background:#FFFFFF;border-radius:var(--radius-lg);width:min(560px,94vw);max-height:90vh;overflow:hidden;box-shadow:var(--shadow-lg);animation:su .25s;display:flex;flex-direction:column;border:1px solid var(--border)}
.mh{padding:20px 24px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;background:var(--bg3)}
.mh h3{font-size:17px;font-weight:700;display:flex;align-items:center;gap:8px}
.mb{padding:24px;overflow-y:auto;flex:1}
.mc{width:32px;height:32px;border-radius:10px;border:1px solid var(--border);background:var(--card);font-size:18px;color:var(--text3);display:flex;align-items:center;justify-content:center}
.mc:hover{background:var(--bg4);color:var(--text)}
@keyframes fi{from{opacity:0}to{opacity:1}}
@keyframes su{from{opacity:0;transform:translateY(16px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}
.fl{display:flex;flex-direction:column;gap:6px}
.fl label{font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.6px}
.fl input,.fl select,.fl textarea{padding:10px 14px;border-radius:10px;border:1.5px solid var(--border);font-size:14px;color:var(--text);background:#FFFFFF;outline:none;width:100%;transition:all .2s}
.fl input:focus,.fl select:focus,.fl textarea:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(67,97,238,.1)}
.fl textarea{resize:vertical;min-height:64px}
.fl select{cursor:pointer}
.fl select option{background:#fff;color:var(--text)}
.bp{padding:12px 24px;border-radius:12px;border:none;background:var(--gradient);color:#fff;font-size:14px;font-weight:700;width:100%;letter-spacing:.3px;box-shadow:0 2px 10px rgba(67,97,238,.25)}
.bp:hover{box-shadow:0 4px 16px rgba(67,97,238,.35);transform:translateY(-1px)}
.bo{padding:8px 16px;border-radius:10px;border:1px solid var(--border);background:#FFFFFF;font-size:13px;font-weight:500;color:var(--text2);transition:all .2s}
.bo:hover{background:var(--bg);border-color:var(--border2);color:var(--text)}
.bd{padding:8px 16px;border-radius:10px;border:1px solid var(--red-bg);background:var(--red-bg);font-size:13px;font-weight:600;color:var(--red)}
.bd:hover{background:rgba(239,68,68,.12)}
.bs{padding:12px 24px;border-radius:12px;border:none;background:var(--gradient2);color:#fff;font-size:14px;font-weight:700;box-shadow:0 2px 10px rgba(16,185,129,.25)}
.bs:hover{box-shadow:0 4px 16px rgba(16,185,129,.35)}
.dp{position:fixed;right:0;top:0;bottom:0;width:min(460px,100vw);background:#FFFFFF;box-shadow:-4px 0 24px rgba(0,0,0,.08);z-index:999;display:flex;flex-direction:column;animation:sl .25s;border-left:1px solid var(--border)}
@keyframes sl{from{transform:translateX(100%)}to{transform:translateX(0)}}
.co{position:fixed;inset:0;background:rgba(30,41,59,.4);display:flex;align-items:center;justify-content:center;z-index:2000;backdrop-filter:blur(6px)}
.cb{background:#FFFFFF;border-radius:var(--radius-lg);padding:30px;width:min(380px,90vw);text-align:center;border:1px solid var(--border);box-shadow:var(--shadow-lg)}
.cb h4{font-size:16px;font-weight:700;margin-bottom:8px}
.cb p{color:var(--text2);font-size:14px;margin-bottom:20px}
.chip{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:10px;border:1px solid var(--border);font-size:13px;font-weight:500;background:#FFFFFF;transition:all .2s}
.chip:hover{border-color:var(--border2)}
.chip button{background:none;border:none;color:var(--text4);font-size:14px;padding:0;line-height:1}
.chip button:hover{color:var(--red)}
.sw{border:1px solid var(--border);border-radius:var(--radius-lg);overflow:auto;background:var(--card)}
.sg{display:grid;font-size:12px}
.sh{padding:12px 8px;background:var(--accent);color:#fff;text-align:center;font-weight:600;font-size:11px;border-bottom:1px solid var(--border)}
.sh.td{background:#7C3AED;color:#fff}
.st{padding:8px 4px;font-size:10px;font-weight:600;color:var(--accent);text-align:center;background:#FFFFFF;border-right:1px solid var(--border);border-bottom:1px solid var(--border);font-family:var(--mono)}
.sc{padding:2px 3px;border-right:1px solid var(--border);border-bottom:1px solid var(--border);min-height:36px;background:#FFFFFF}
.sc.td{background:rgba(67,97,238,.04)}
.sch{padding:3px 6px;border-radius:6px;font-size:10px;font-weight:600;display:block;margin:1px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer;transition:all .2s}
.sch:hover{transform:scale(1.02);box-shadow:0 2px 8px rgba(0,0,0,.1)}
.ht{width:100%;border-collapse:collapse;font-size:12px}
.ht th{padding:10px 4px;background:var(--accent);color:#fff;font-size:10px;font-weight:600;position:sticky;top:0;z-index:2;border-bottom:1px solid var(--border)}
.ht th:first-child{text-align:left;padding-left:14px;min-width:140px;position:sticky;left:0;z-index:3}
.ht th.today-th{background:#7C3AED;color:#fff}
.ht td{border-bottom:1px solid var(--border)}
.ht td:first-child{position:sticky;left:0;z-index:1;background:inherit;border-right:1px solid var(--border);padding:6px 12px}
.ht tr:hover td{background:var(--bg)}
.filter-bar{display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-wrap:wrap}
.toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#FFFFFF;color:var(--text);padding:12px 24px;border-radius:12px;font-size:13px;font-weight:600;z-index:3000;border:1px solid var(--border);box-shadow:var(--shadow-lg);animation:toast-in .3s ease}
.toast.error{border-color:var(--red);color:var(--red);background:var(--red-bg)}
@keyframes toast-in{from{opacity:0;transform:translateX(-50%) translateY(20px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
.meeting-time{display:inline-flex;align-items:center;gap:4px;padding:3px 8px;border-radius:6px;font-size:11px;font-weight:600;background:var(--cyan-bg);color:var(--cyan2)}
.analytics-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.chart-card{background:var(--card);border-radius:var(--radius-lg);border:1px solid var(--border);padding:22px;position:relative}
.chart-card .chart-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.chart-card .chart-title{font-size:13px;font-weight:700;color:var(--text)}
.chart-toggle{width:32px;height:18px;border-radius:10px;border:none;background:var(--border);position:relative;cursor:pointer;transition:all .2s}
.chart-toggle.on{background:var(--accent)}
.chart-toggle::after{content:"";position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;background:#fff;transition:all .2s;box-shadow:0 1px 3px rgba(0,0,0,.15)}
.chart-toggle.on::after{left:16px}
.bar-chart{display:flex;align-items:flex-end;gap:6px;height:140px;padding-top:10px}
.bar-col{display:flex;flex-direction:column;align-items:center;gap:4px;flex:1}
.bar-fill{width:100%;border-radius:6px 6px 0 0;transition:height .5s ease;min-width:20px;position:relative}
.bar-label{font-size:9px;color:var(--text3);font-weight:600;text-align:center}
.bar-value{font-size:10px;font-weight:700;color:var(--text2);font-family:var(--mono)}
.donut-container{display:flex;align-items:center;justify-content:center;gap:20px}
.donut-legend{display:flex;flex-direction:column;gap:6px}
.donut-legend-item{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--text2)}
.donut-legend-dot{width:10px;height:10px;border-radius:3px;flex-shrink:0}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border)}
.stat-row:last-child{border-bottom:none}
.heatmap-cell{border-radius:3px;aspect-ratio:1;transition:all .2s}
.heatmap-cell:hover{transform:scale(1.3);z-index:1}
@media(max-width:768px){
.hdr{padding:0 14px;gap:8px;height:auto;flex-wrap:wrap;padding:12px 14px}
.tabs{overflow-x:auto;height:auto;gap:0}
.tab{padding:10px 12px;font-size:12px}
.tab.on::after{bottom:-2px}
.main{padding:16px 14px}
.kpi-r{grid-template-columns:repeat(2,1fr)}
.two-col{grid-template-columns:1fr!important}
.analytics-grid{grid-template-columns:1fr}
.dp{width:100vw}
}
</style>
</head>
<body>
<div id="root"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.3.1/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.24.7/babel.min.js"></script>
<script type="text/babel">
/* ===== BRIDGE: wait for pywebview API ===== */
async function callApi(method, ...args) {
    while (!window.pywebview || !window.pywebview.api) {
        await new Promise(r => setTimeout(r, 50));
    }
    return window.pywebview.api[method](...args);
}

const {useState,useEffect,useMemo,useCallback,useRef}=React;
const uid=()=>Date.now().toString(36)+Math.random().toString(36).slice(2,7);
const td=()=>new Date().toISOString().split("T")[0];
const fmt=d=>{if(!d)return"\u2014";const t=new Date(d);return`${String(t.getDate()).padStart(2,"0")}.${String(t.getMonth()+1).padStart(2,"0")}.${t.getFullYear()}`};
const fmtS=d=>{if(!d)return"";const t=new Date(d);return`${String(t.getDate()).padStart(2,"0")}.${String(t.getMonth()+1).padStart(2,"0")}`};
const diffD=(a,b)=>Math.round((new Date(a)-new Date(b))/864e5);
const TABS=["Панель","Задачи","Сегодня","Расписание","Журнал","Аналитика","Экспорт"];
const TAB_ICONS={"Панель":"\ud83d\udcca","Задачи":"\ud83d\udccb","Сегодня":"\u2600\ufe0f","Расписание":"\ud83d\udcc5","Журнал":"\ud83d\udcd3","Аналитика":"\ud83d\udcc8","Экспорт":"\ud83d\udcc4"};
const dayN=["Пн","Вт","Ср","Чт","Пт","Сб","Вс"];
const hours=Array.from({length:15},(_,i)=>`${String(i+7).padStart(2,"0")}:00`);
const monthN=["","Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"];
const CC={"Рабочая":"#4361EE","Совещание":"#0891B2","Проект":"#059669","Обучение":"#DB2777","Личная":"#EA580C","Рутина":"#64748B"};
const PC={"Высокий":"#EF4444","Средний":"#F59E0B","Низкий":"#10B981"};
const PB={"Высокий":"var(--red-bg)","Средний":"var(--amber-bg)","Низкий":"var(--green-bg)"};
const gc=n=>CC[n]||"#636E72";const gp=n=>PC[n]||"#636E72";const gb=n=>PB[n]||"var(--bg3)";
function getS(t,now){if(!t.name)return{l:" ",i:"",c:"var(--text3)"};if(t.progress>=100)return{l:"Выполнено",i:"\u2705",c:"var(--green)"};if(t.deadline&&t.deadline<now&&t.progress<100)return{l:"Просрочено",i:"\ud83d\udd34",c:"var(--red)"};if(t.deadline){const dl=diffD(t.deadline,now);if(dl>=0&&dl<=2)return{l:"Горит",i:"\u26a0\ufe0f",c:"var(--amber)"};}if(t.progress>0)return{l:"В работе",i:"\ud83d\udd04",c:"var(--accent)"};return{l:"Новая",i:"\ud83c\udd95",c:"var(--text3)"};}

const Bdg=({children,color,bg})=><span className="bdg" style={{color,background:bg||color+"18"}}>{children}</span>;
const KPI=({label,value,sub,color})=><div className="kpi"><div className="kpi-glow" style={{background:color}}/><div className="kpi-l">{label}</div><div className="kpi-v" style={{color}}>{value}</div><div className="kpi-s">{sub}</div></div>;

function PBar({value=0,color="var(--accent)",onChange,size=8}){
const ref=useRef(null);
const hc=e=>{if(!onChange||!ref.current)return;const r=ref.current.getBoundingClientRect();const p=Math.round(Math.max(0,Math.min(100,((e.clientX-r.left)/r.width)*100))/5)*5;onChange(p)};
return<div className="pw" ref={ref} onClick={hc} style={{height:size}} title={`${value}%`}><div className="pf" data-p={`${value}%`} style={{width:`${Math.min(value,100)}%`,background:value>=100?'var(--gradient2)':color,height:size}}/></div>}

function Confirm({title,text,onYes,onNo,yesLabel="Да",noLabel="Отмена",yesColor}){
return<div className="co" onClick={onNo}><div className="cb" onClick={e=>e.stopPropagation()}>
<h4>{title}</h4><p>{text}</p>
<div style={{display:"flex",gap:10,justifyContent:"center"}}>
<button className="bo" onClick={onNo}>{noLabel}</button>
<button style={{padding:"10px 24px",borderRadius:12,border:"none",background:yesColor||"var(--gradient)",color:"#fff",fontWeight:700,fontSize:14}} onClick={onYes}>{yesLabel}</button>
</div></div></div>}

function Toast({msg,type,onDone}){useEffect(()=>{const t=setTimeout(onDone,2500);return()=>clearTimeout(t)},[]);return<div className={`toast ${type||""}`}>{msg}</div>}

function KpiDrill({kpi,tasks,now,onClose,onOpenTask}){
const titles={total:"Все задачи",done:"Выполненные задачи",active:"Задачи в работе",burn:"Горящие задачи",over:"Просроченные задачи"};
const icons={total:"📋",done:"✅",active:"🔄",burn:"⚠️",over:"🔴"};
const colors={total:"var(--accent)",done:"var(--green)",active:"var(--accent)",burn:"var(--amber)",over:"var(--red)"};
const filter={
total:t=>t.name,
done:t=>t.name&&getS(t,now).l==="Выполнено",
active:t=>{if(!t.name)return false;const s=getS(t,now).l;return s!=="Выполнено"},
burn:t=>t.name&&getS(t,now).l==="Горит",
over:t=>t.name&&getS(t,now).l==="Просрочено",
}[kpi];
const filtered=tasks.filter(filter);
return<div className="mo" onClick={onClose}><div className="md" onClick={e=>e.stopPropagation()} style={{width:"min(720px,94vw)",maxHeight:"85vh"}}>
<div className="mh" style={{borderTop:`4px solid ${colors[kpi]}`}}>
<h3>{icons[kpi]} {titles[kpi]} <span style={{fontWeight:500,fontSize:13,color:"var(--text3)",marginLeft:8}}>({filtered.length})</span></h3>
<button className="mc" onClick={onClose}>×</button>
</div>
<div className="mb" style={{padding:16}}>
{filtered.length===0?<div style={{textAlign:"center",padding:50,color:"var(--text4)"}}>
<div style={{fontSize:44,marginBottom:10}}>🎉</div>
<div style={{fontWeight:700,fontSize:15}}>Нет задач в этой категории</div>
</div>:<div style={{display:"flex",flexDirection:"column",gap:6}}>
{filtered.map(t=>{const st=getS(t,now);const dl=t.deadline?diffD(t.deadline,now):null;const isMtg=t.cat==="Совещание";
return<div key={t.id} className="tr" onClick={()=>{onClose();onOpenTask(t)}}>
<div className="task-left" style={{background:gp(t.pri)}}/>
<div style={{flex:1,minWidth:0}}>
<div style={{fontWeight:600,fontSize:14}}>{t.name}</div>
<div style={{display:"flex",gap:5,marginTop:5,flexWrap:"wrap",alignItems:"center"}}>
<Bdg color={gc(t.cat)}>{t.cat}</Bdg>
<Bdg color={gp(t.pri)} bg={gb(t.pri)}>{t.pri}</Bdg>
{isMtg&&t.timeStart&&<span className="meeting-time">🕐 {t.timeStart}–{t.timeEnd||"?"}</span>}
{t.deadline&&<span style={{fontSize:11,color:dl<0?"var(--red)":dl<=2?"var(--amber)":"var(--text3)"}}>📅 {fmt(t.deadline)}{dl!==null&&dl<0?` (+${Math.abs(dl)}д)`:""}</span>}
</div>
</div>
<div style={{textAlign:"right",flexShrink:0}}>
<Bdg color={st.c}>{st.i} {st.l}</Bdg>
<div style={{fontSize:13,fontWeight:700,color:st.c,fontFamily:"var(--mono)",marginTop:3}}>{t.progress}%</div>
</div>
</div>})}
</div>}
</div>
</div></div>
}

function TForm({onClose,initial,onSubmit,cats,pris}){
const[f,setF]=useState(initial?{...initial}:{name:"",cat:cats[0]||"",pri:pris[1]||pris[0]||"",desc:"",start:td(),deadline:"",progress:0,notes:"",timeStart:"",timeEnd:""});
const s=(k,v)=>setF(p=>({...p,[k]:v}));const isMeeting=f.cat==="Совещание";
const go=()=>{if(!f.name.trim())return;onSubmit({...f,progress:parseInt(f.progress)||0});onClose()};
return<div className="mo" onClick={onClose}><div className="md" onClick={e=>e.stopPropagation()}>
<div className="mh"><h3>✨ {initial?"Редактировать":"Новая задача"}</h3><button className="mc" onClick={onClose}>×</button></div>
<div className="mb"><div style={{display:"flex",flexDirection:"column",gap:14}}>
<div className="fl"><label>Название *</label><input value={f.name} onChange={e=>s("name",e.target.value)} placeholder="Что нужно сделать?" autoFocus/></div>
<div className="fl"><label>Описание</label><textarea value={f.desc} onChange={e=>s("desc",e.target.value)} placeholder="Детали задачи..."/></div>
<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
<div className="fl"><label>Категория</label><select value={f.cat} onChange={e=>s("cat",e.target.value)}>{cats.map(c=><option key={c}>{c}</option>)}</select></div>
<div className="fl"><label>Приоритет</label><select value={f.pri} onChange={e=>s("pri",e.target.value)}>{pris.map(p=><option key={p}>{p}</option>)}</select></div>
</div>
<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
<div className="fl"><label>Дата начала</label><input type="date" value={f.start} onChange={e=>s("start",e.target.value)}/></div>
<div className="fl"><label>Дедлайн</label><input type="date" value={f.deadline} onChange={e=>s("deadline",e.target.value)}/></div>
</div>
{isMeeting&&<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12,padding:14,background:"var(--cyan-bg)",borderRadius:12,border:"1px solid rgba(6,182,212,.2)"}}>
<div className="fl"><label style={{color:"var(--cyan)"}}>🕐 Время начала</label><input type="time" value={f.timeStart||""} onChange={e=>s("timeStart",e.target.value)}/></div>
<div className="fl"><label style={{color:"var(--cyan)"}}>🕐 Время окончания</label><input type="time" value={f.timeEnd||""} onChange={e=>s("timeEnd",e.target.value)}/></div>
</div>}
<div className="fl"><label>Заметки</label><textarea value={f.notes} onChange={e=>s("notes",e.target.value)} placeholder="Примечания..."/></div>
<button className="bp" onClick={go} style={{marginTop:6}}>{initial?"💾 Сохранить":"➕ Добавить"}</button>
</div></div></div></div>}

function TDetail({task,onClose,onEdit,onDelete,onProg,now}){
const st=getS(task,now);const dl=task.deadline?diffD(task.deadline,now):null;
const[cd,setCd]=useState(false);const[cf,setCf]=useState(false);const[full,setFull]=useState(false);
const isMeeting=task.cat==="Совещание";
const panelStyle=full?{position:"fixed",inset:0,width:"100%",background:"#fff",boxShadow:"none",zIndex:999,display:"flex",flexDirection:"column",animation:"fi .2s",borderLeft:"none"}:{};
return<><div style={{position:"fixed",inset:0,background:"rgba(0,0,0,.4)",zIndex:998}} onClick={onClose}/>
<div className={full?"":"dp"} style={full?panelStyle:{}}>
<div style={{padding:"20px 24px",borderBottom:"1px solid var(--border)",display:"flex",alignItems:"center",justifyContent:"space-between",background:"var(--bg3)"}}>
<h3 style={{fontSize:15,fontWeight:700,display:"flex",alignItems:"center",gap:8}}>📋 Детали задачи</h3>
<div style={{display:"flex",gap:6}}>
<button className="mc" onClick={()=>setFull(f=>!f)} title={full?"Свернуть":"На весь экран"}>{full?"⊡":"⛶"}</button>
<button className="mc" onClick={onClose}>×</button>
</div></div>
<div style={{padding:24,overflowY:"auto",flex:1,...(full?{maxWidth:800,margin:"0 auto",width:"100%"}:{})}}>
<div style={{display:"flex",gap:6,marginBottom:12,flexWrap:"wrap"}}>
<Bdg color={gc(task.cat)} bg={gc(task.cat)+"20"}>{task.cat}</Bdg>
<Bdg color={gp(task.pri)} bg={gb(task.pri)}>{task.pri}</Bdg>
<Bdg color={st.c}>{st.i} {st.l}</Bdg>
</div>
<h2 style={{fontSize:20,fontWeight:800,lineHeight:1.3,marginBottom:8}}>{task.name}</h2>
{task.desc&&<p style={{color:"var(--text2)",fontSize:14,lineHeight:1.6,marginBottom:18}}>{task.desc}</p>}
<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16,marginBottom:20}}>
<div style={{background:"var(--bg)",borderRadius:12,padding:14}}><div style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginBottom:4}}>Начало</div><div style={{fontSize:15,fontWeight:600}}>{fmt(task.start)}</div></div>
<div style={{background:"var(--bg)",borderRadius:12,padding:14}}><div style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginBottom:4}}>Дедлайн</div><div style={{fontSize:15,fontWeight:600,color:dl!==null&&dl<0?"var(--red)":dl!==null&&dl<=2?"var(--amber)":"var(--text)"}}>{fmt(task.deadline)}{dl!==null&&dl<0?` (+${Math.abs(dl)}д)`:dl!==null&&dl>=0?` (${dl}д)`:""}</div></div>
</div>
{isMeeting&&(task.timeStart||task.timeEnd)&&<div style={{background:"var(--cyan-bg)",borderRadius:12,padding:14,marginBottom:20,border:"1px solid rgba(6,182,212,.2)"}}>
<div style={{fontSize:10,fontWeight:700,color:"var(--cyan)",textTransform:"uppercase",marginBottom:6}}>🕐 Время совещания</div>
<div style={{display:"flex",gap:16}}>
<div><span style={{color:"var(--text3)",fontSize:12}}>Начало: </span><span style={{fontWeight:700,fontSize:16,color:"var(--cyan2)"}}>{task.timeStart||"\u2014"}</span></div>
<div><span style={{color:"var(--text3)",fontSize:12}}>Конец: </span><span style={{fontWeight:700,fontSize:16,color:"var(--cyan2)"}}>{task.timeEnd||"\u2014"}</span></div>
</div></div>}
<div style={{marginBottom:20}}>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:8}}>
<span style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase"}}>Прогресс</span>
<span style={{fontSize:20,fontWeight:800,color:st.c,fontFamily:"var(--mono)"}}>{task.progress}%</span>
</div>
<PBar value={task.progress} color={st.c} onChange={p=>onProg(task.id,p)} size={14}/>
</div>
{task.notes&&<div style={{marginBottom:18}}><div style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginBottom:6}}>Заметки</div><div style={{background:"var(--bg)",borderRadius:12,padding:14,fontSize:14,color:"var(--text2)",lineHeight:1.6,border:"1px solid var(--border)"}}>{task.notes}</div></div>}
</div>
<div style={{padding:"16px 24px",borderTop:"1px solid var(--border)",display:"flex",gap:10,justifyContent:"flex-end"}}>
<button className="bd" onClick={()=>setCd(true)}>🗑 Удалить</button>
<button className="bo" onClick={()=>onEdit(task)}>✏️ Редактировать</button>
{task.progress<100&&<button className="bs" onClick={()=>setCf(true)}>Завершить ✅</button>}
</div></div>
{cd&&<Confirm title="Удалить задачу?" text={`«${task.name}» будет удалена.`} onNo={()=>setCd(false)} onYes={()=>{onDelete(task.id);onClose()}} yesLabel="Удалить" yesColor="var(--red)"/>}
{cf&&<Confirm title="Завершить задачу?" text={`Отметить «${task.name}» как выполненную?`} onNo={()=>setCf(false)} onYes={()=>{onProg(task.id,100);setCf(false)}} yesLabel="Завершить" yesColor="var(--green)"/>}
</>}

function Settings({data,onUpdate,onClose,showToast,protectedCats}){
const[nc,setNc]=useState("");const[np,setNp]=useState("");
const tryDeleteCat=async c=>{
if(protectedCats.includes(c)){showToast(`Категорию «${c}» нельзя удалить — она является системной`,"error");return}
const res=await callApi("delete_category",c);
if(res==="protected"){showToast(`Категорию «${c}» нельзя удалить — она является системной`,"error");return}
onUpdate();
};
const doAddCat=async()=>{
if(!nc.trim())return;
await callApi("add_category",nc.trim());
setNc("");onUpdate();
};
const doAddPri=async()=>{
if(!np.trim())return;
await callApi("add_priority",np.trim());
setNp("");onUpdate();
};
const doDelPri=async p=>{
await callApi("delete_priority",p);
onUpdate();
};
return<div className="mo" onClick={onClose}><div className="md" onClick={e=>e.stopPropagation()}>
<div className="mh"><h3>⚙️ Настройки</h3><button className="mc" onClick={onClose}>×</button></div>
<div className="mb">
<div style={{marginBottom:24}}>
<div className="stitle"><span className="stitle-icon">🏷️</span> Категории</div>
<div style={{display:"flex",flexWrap:"wrap",gap:6,marginBottom:10}}>
{data.categories.map(c=><div key={c} className="chip" style={protectedCats.includes(c)?{borderColor:"var(--cyan)",background:"var(--cyan-bg)"}:{}}>
<span style={{width:8,height:8,borderRadius:4,background:gc(c)}}/>{c}
{protectedCats.includes(c)?<span style={{fontSize:10,color:"var(--cyan)"}}>🔒</span>
:<button onClick={()=>tryDeleteCat(c)}>×</button>}
</div>)}
</div>
<div style={{display:"flex",gap:8}}>
<input value={nc} onChange={e=>setNc(e.target.value)} placeholder="Новая категория..." style={{flex:1,padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:13,background:"var(--bg)",color:"var(--text)"}} onKeyDown={e=>{if(e.key==="Enter")doAddCat()}}/>
<button className="bo" onClick={doAddCat}>+</button>
</div></div>
<div style={{marginBottom:24}}>
<div className="stitle"><span className="stitle-icon">🎯</span> Приоритеты</div>
<div style={{display:"flex",flexWrap:"wrap",gap:6,marginBottom:10}}>
{data.priorities.map(p=><div key={p} className="chip"><span style={{width:8,height:8,borderRadius:4,background:gp(p)}}/>{p}<button onClick={()=>doDelPri(p)}>×</button></div>)}
</div>
<div style={{display:"flex",gap:8}}>
<input value={np} onChange={e=>setNp(e.target.value)} placeholder="Новый приоритет..." style={{flex:1,padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:13,background:"var(--bg)",color:"var(--text)"}} onKeyDown={e=>{if(e.key==="Enter")doAddPri()}}/>
<button className="bo" onClick={doAddPri}>+</button>
</div></div>
</div></div></div>}

/* DonutChart */
function DonutChart({segments,size=140,thickness=24}){const r=size/2;const cr=r-thickness/2;const circ=2*Math.PI*cr;let offset=0;
return<svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
{segments.map((seg,i)=>{const dash=circ*seg.pct/100;const gap=circ-dash;const rot=-90+offset*360/100;offset+=seg.pct;
return<circle key={i} cx={r} cy={r} r={cr} fill="none" stroke={seg.color} strokeWidth={thickness} strokeDasharray={`${dash} ${gap}`} transform={`rotate(${rot} ${r} ${r})`} style={{transition:"all .5s ease"}}/>})}
<text x={r} y={r-6} textAnchor="middle" fill="var(--text)" fontFamily="var(--mono)" fontSize="22" fontWeight="800">{segments.reduce((a,s)=>a+s.value,0)}</text>
<text x={r} y={r+12} textAnchor="middle" fill="var(--text2)" fontFamily="var(--font)" fontSize="10" fontWeight="600">ВСЕГО</text>
</svg>}

/* ===== MAIN APP ===== */
function App(){
const[data,setData]=useState({categories:[],priorities:[],tasks:[],protectedCats:[]});
const[loading,setLoading]=useState(true);
const[tab,setTab]=useState("Панель");
const now=td();
const[showForm,setShowForm]=useState(false);
const[editTask,setEditTask]=useState(null);
const[detailTask,setDetailTask]=useState(null);
const[showSettings,setShowSettings]=useState(false);
const[filter,setFilter]=useState("active");
const[sortBy,setSortBy]=useState("deadline");
const[schedDate,setSchedDate]=useState(now);
const[habMonth,setHabMonth]=useState(()=>{const d=new Date();return`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`});
const[toast,setToast]=useState(null);
const showToast=(msg,type)=>setToast({msg,type});
const[drillKpi,setDrillKpi]=useState(null);
/* Analytics state */
const[anPeriod,setAnPeriod]=useState("all");
const[anCat,setAnCat]=useState("");
const[anPri,setAnPri]=useState("");
const[anCharts,setAnCharts]=useState({kpis:true,status:true,category:true,priority:true,productivity:true,timeline:true,heatmap:true,catPri:true,avgProg:true,completion:true,onTime:true,upcoming:true});
const[anShowSettings,setAnShowSettings]=useState(false);

/* Load data from SQLite via Python bridge */
const reload=useCallback(async()=>{
const raw=await callApi("get_data");
setData(JSON.parse(raw));
setLoading(false);
},[]);

useEffect(()=>{reload()},[reload]);

const addT=async t=>{
await callApi("add_task",JSON.stringify(t));
reload();
};
const updT=async(id,patch)=>{
await callApi("update_task",id,JSON.stringify(patch));
reload();
};
const delT=async id=>{
await callApi("delete_task",id);
setDetailTask(null);
reload();
};
const setProg=async(id,p)=>{
const patch=p>=100?{progress:p,completedAt:td()}:{progress:p,completedAt:null};
await callApi("update_task",id,JSON.stringify(patch));
if(detailTask&&detailTask.id===id)setDetailTask(prev=>({...prev,...patch}));
reload();
};

const stats=useMemo(()=>{const s={total:0,done:0,active:0,burn:0,over:0};data.tasks.forEach(t=>{if(!t.name)return;s.total++;const st=getS(t,now);if(st.l==="Выполнено")s.done++;else if(st.l==="В работе")s.active++;else if(st.l==="Горит"){s.burn++;s.active++}else if(st.l==="Просрочено")s.over++;else s.active++});s.pct=s.total>0?Math.round(s.done/s.total*100):0;return s},[data.tasks,now]);

const filtered=useMemo(()=>{let l=[...data.tasks].filter(t=>t.name);if(filter==="active")l=l.filter(t=>getS(t,now).l!=="Выполнено");else if(filter==="completed")l=l.filter(t=>getS(t,now).l==="Выполнено");
if(sortBy==="deadline")l.sort((a,b)=>(a.deadline||"9999").localeCompare(b.deadline||"9999"));
else if(sortBy==="priority"){const o={};data.priorities.forEach((p,i)=>o[p]=i);l.sort((a,b)=>(o[a.pri]??99)-(o[b.pri]??99)||(a.deadline||"9999").localeCompare(b.deadline||"9999"))}
else if(sortBy==="category")l.sort((a,b)=>(a.cat||"").localeCompare(b.cat||"")||(a.deadline||"9999").localeCompare(b.deadline||"9999"));
else if(sortBy==="created")l.sort((a,b)=>(b.createdAt||"").localeCompare(a.createdAt||""));
return l},[data.tasks,data.priorities,filter,sortBy,now]);

const todayL=useMemo(()=>data.tasks.filter(t=>{if(!t.name)return false;const st=getS(t,now);if(st.l==="Выполнено")return false;if(!t.start||t.start>now)return false;if(st.l==="Просрочено")return true;if(!t.deadline||t.deadline>=now)return true;return false}).sort((a,b)=>{const o={};data.priorities.forEach((p,i)=>o[p]=i);return(o[a.pri]??99)-(o[b.pri]??99)}),[data.tasks,data.priorities,now]);

const urgent=useMemo(()=>data.tasks.filter(t=>{const s=getS(t,now).l;return s==="Просрочено"||s==="Горит"}),[data.tasks,now]);

const getMon=d=>{const dt=new Date(d);const dw=dt.getDay();const diff=dt.getDate()-dw+(dw===0?-6:1);return new Date(dt.setDate(diff)).toISOString().split("T")[0]};
const weekD=useMemo(()=>{const m=getMon(schedDate);return Array.from({length:7},(_,i)=>{const d=new Date(m);d.setDate(d.getDate()+i);return d.toISOString().split("T")[0]})},[schedDate]);

const getMeetingsForDay=useCallback(day=>data.tasks.filter(t=>{if(!t.name||t.cat!=="Совещание")return false;if(getS(t,now).l==="Выполнено")return false;if(t.start&&t.start<=day&&t.deadline&&t.deadline>=day)return true;if(t.start===day||t.deadline===day)return true;return false}).sort((a,b)=>(a.timeStart||"99:99").localeCompare(b.timeStart||"99:99")),[data.tasks,now]);

const daysInM=useMemo(()=>{const[y,m]=habMonth.split("-").map(Number);return new Date(y,m,0).getDate()},[habMonth]);

/* Export page state */
const[expFrom,setExpFrom]=useState(()=>{const d=new Date();d.setMonth(d.getMonth()-1);return d.toISOString().split("T")[0]});
const[expTo,setExpTo]=useState(td());
const[expCats,setExpCats]=useState([]);const[expPris,setExpPris]=useState([]);const[expStat,setExpStat]=useState([]);
const[expPreview,setExpPreview]=useState(null);const[expGen,setExpGen]=useState(false);
const toggleA=(a,s,v)=>s(p=>p.includes(v)?p.filter(x=>x!==v):[...p,v]);
const statuses=["Выполнено","В работе","Горит","Просрочено","Новая"];

const expFiltered=useMemo(()=>data.tasks.filter(t=>{if(!t.name)return false;if(t.start&&t.start>expTo)return false;if(t.deadline&&t.deadline<expFrom&&getS(t,now).l!=="Просрочено")return false;if(expCats.length&&!expCats.includes(t.cat))return false;if(expPris.length&&!expPris.includes(t.pri))return false;if(expStat.length&&!expStat.includes(getS(t,now).l))return false;return true}),[data.tasks,expFrom,expTo,expCats,expPris,expStat,now]);
const expStats=useMemo(()=>{const s={total:expFiltered.length,done:0,active:0,overdue:0,burning:0};expFiltered.forEach(t=>{const st=getS(t,now);if(st.l==="Выполнено")s.done++;else if(st.l==="Просрочено")s.overdue++;else if(st.l==="Горит")s.burning++;else s.active++});s.pct=s.total?Math.round(s.done/s.total*100):0;s.avgProg=s.total?Math.round(expFiltered.reduce((a,t)=>a+(t.progress||0),0)/s.total):0;return s},[expFiltered,now]);

const genReport=()=>{setExpGen(true);setTimeout(()=>{
const catBr={};expFiltered.forEach(t=>{catBr[t.cat]=(catBr[t.cat]||0)+1});
const priBr={};expFiltered.forEach(t=>{priBr[t.pri]=(priBr[t.pri]||0)+1});
const done=expFiltered.filter(t=>getS(t,now).l==="Выполнено");
const active=expFiltered.filter(t=>getS(t,now).l!=="Выполнено");
const overdue=expFiltered.filter(t=>getS(t,now).l==="Просрочено");
const burning=expFiltered.filter(t=>getS(t,now).l==="Горит");
const inprog=expFiltered.filter(t=>getS(t,now).l==="В работе");

/* Advanced metrics */
const onTimeDone=done.filter(t=>!t.deadline||t.completedAt<=t.deadline).length;
const onTimeRate=done.length?Math.round(onTimeDone/done.length*100):null;
const latDone=done.filter(t=>t.deadline&&t.completedAt>t.deadline).length;
const avgTimeDays=(()=>{const ts=done.filter(t=>t.completedAt&&t.start);if(!ts.length)return null;return Math.round(ts.reduce((s,t)=>s+Math.max(0,diffD(t.completedAt,t.start)),0)/ts.length*10)/10})();
const avgProg=expStats.avgProg;

/* Status breakdown */
const statuses=[
{label:"Выполнено",count:done.length,color:"#10B981",icon:"✓"},
{label:"В работе",count:inprog.length,color:"#4361EE",icon:"⟳"},
{label:"Горит",count:burning.length,color:"#F59E0B",icon:"⚠"},
{label:"Просрочено",count:overdue.length,color:"#EF4444",icon:"✕"},
].filter(s=>s.count>0);

/* Assessment */
const assessment=expStats.pct>=75?{text:"🏆 Отличный результат",color:"#10B981"}:expStats.pct>=50?{text:"✓ Хороший прогресс",color:"#4361EE"}:expStats.pct>=25?{text:"⚠ Требуется внимание",color:"#F59E0B"}:{text:"⚠ Низкая эффективность",color:"#EF4444"};

const escapeHTML=s=>String(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");

const taskRow=(t,showDeadline=false)=>{const st=getS(t,now);return `<tr><td><strong>${escapeHTML(t.name)}</strong>${t.desc?'<div style="color:#64748B;font-size:11px;margin-top:2px">'+escapeHTML(t.desc)+'</div>':''}</td><td><span class="bdg" style="color:${gc(t.cat)};background:${gc(t.cat)}15">${escapeHTML(t.cat)}</span></td><td><span class="bdg" style="color:${gp(t.pri)};background:${gp(t.pri)}15">${escapeHTML(t.pri)}</span></td>${showDeadline?`<td>${fmt(t.deadline)}</td>`:''}<td style="color:${st.c==='var(--green)'?'#10B981':st.c==='var(--red)'?'#EF4444':st.c==='var(--amber)'?'#F59E0B':'#4361EE'};font-weight:600">${st.i} ${st.l}</td><td><div style="display:flex;align-items:center;gap:8px"><div style="flex:1;height:8px;background:#F0F4FA;border-radius:4px;overflow:hidden;min-width:60px"><div style="width:${t.progress}%;height:100%;background:${st.c==='var(--green)'?'#10B981':st.c==='var(--red)'?'#EF4444':st.c==='var(--amber)'?'#F59E0B':'#4361EE'}"></div></div><span style="font-family:'IBM Plex Mono';font-weight:700;font-size:11px;min-width:32px;text-align:right">${t.progress}%</span></div></td>${t.completedAt?`<td style="color:#10B981;font-weight:600">${fmt(t.completedAt)}</td>`:''}</tr>`};

const html=`<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Отчёт Smart Planner</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@500;600;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box;font-family:'DM Sans',sans-serif}
body{padding:40px;color:#1E293B;font-size:13px;line-height:1.6;background:#fff}
@media print{body{padding:20px}@page{margin:15mm;size:A4}.page-break{page-break-before:always}.no-break{page-break-inside:avoid}}
.header{position:relative;margin-bottom:32px;padding:28px;background:linear-gradient(135deg,#4361EE 0%,#7C3AED 100%);border-radius:16px;color:#fff;overflow:hidden}
.header::before{content:"";position:absolute;top:-50%;right:-10%;width:300px;height:300px;border-radius:50%;background:rgba(255,255,255,.1);filter:blur(40px)}
.header::after{content:"";position:absolute;bottom:-30%;left:-5%;width:200px;height:200px;border-radius:50%;background:rgba(236,72,153,.25);filter:blur(40px)}
.header-content{position:relative;z-index:1;display:flex;justify-content:space-between;align-items:flex-start;gap:20px;flex-wrap:wrap}
.header h1{font-size:28px;font-weight:800;letter-spacing:-.5px;margin-bottom:4px}
.header .subtitle{font-size:14px;font-weight:500;opacity:.85}
.header .period{text-align:right}
.header .period .label{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;opacity:.7;margin-bottom:4px}
.header .period .dates{font-size:16px;font-weight:700;font-family:'IBM Plex Mono',monospace}
.header .period .gen{font-size:11px;opacity:.7;margin-top:6px}
.assess-box{margin-bottom:24px;padding:20px 24px;border-radius:14px;border-left:5px solid ${assessment.color};background:${assessment.color}12;display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
.assess-box .main-text{font-size:18px;font-weight:700;color:${assessment.color}}
.assess-box .sub{font-size:12px;color:#64748B;margin-top:4px}
.assess-box .big-pct{font-size:36px;font-weight:800;color:${assessment.color};font-family:'IBM Plex Mono',monospace}
.kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:10px;margin-bottom:24px}
.kpi-box{border:1.5px solid #E2E8F0;border-radius:12px;padding:14px 12px;text-align:center;position:relative;background:#fff}
.kpi-box::before{content:"";position:absolute;top:0;left:12%;right:12%;height:3px;border-radius:0 0 4px 4px}
.kpi-box .num{font-size:24px;font-weight:800;font-family:'IBM Plex Mono',monospace;line-height:1}
.kpi-box .lbl{font-size:9px;font-weight:700;color:#94A3B8;text-transform:uppercase;letter-spacing:.8px;margin-top:8px}
.kpi-box .sub{font-size:10px;color:#94A3B8;margin-top:2px}
.blue{color:#4361EE}.blue::before{background:#4361EE}.grn{color:#10B981}.grn::before{background:#10B981}.amb{color:#F59E0B}.amb::before{background:#F59E0B}.red{color:#EF4444}.red::before{background:#EF4444}.cyan{color:#0891B2}.cyan::before{background:#06B6D4}.pnk{color:#DB2777}.pnk::before{background:#EC4899}
.summary{background:#F8FAFD;border:1px solid #E2E8F0;border-radius:14px;padding:20px 22px;margin-bottom:28px}
.summary-title{font-size:13px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:1px;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.summary-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px 32px;font-size:13px}
.summary-item{padding:10px 0;border-bottom:1px dashed #E2E8F0}
.summary-item:last-child{border-bottom:none}
.summary-item .sum-label{color:#64748B;font-size:12px;margin-bottom:2px}
.summary-item .sum-value{font-weight:700;color:#1E293B}
.sum-value.pos{color:#10B981}.sum-value.neg{color:#EF4444}.sum-value.warn{color:#F59E0B}
.narrative{margin-top:16px;padding:14px 16px;background:#fff;border-radius:10px;border:1px solid #E2E8F0;color:#475569;line-height:1.7;font-size:13px}
.section{margin-bottom:28px}
.section h2{font-size:16px;font-weight:700;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #E2E8F0;color:#1E293B;display:flex;align-items:center;gap:8px}
.section h2 .count{font-size:12px;color:#94A3B8;font-weight:500;margin-left:auto;font-family:'IBM Plex Mono',monospace}
.stat-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:24px}
.stat-card{padding:16px;background:#F8FAFD;border-radius:12px;text-align:center;border:1px solid #E2E8F0}
.stat-card .v{font-size:22px;font-weight:800;font-family:'IBM Plex Mono',monospace;color:#4361EE}
.stat-card .lb{font-size:10px;color:#64748B;margin-top:4px;text-transform:uppercase;letter-spacing:.5px}
.bar-section{display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:24px}
.bar-group{background:#F8FAFD;border-radius:12px;padding:18px;border:1px solid #E2E8F0}
.bar-group-title{font-weight:700;font-size:12px;margin-bottom:14px;text-transform:uppercase;letter-spacing:.8px;color:#475569}
.bar-item{margin-bottom:10px}
.bar-label-row{display:flex;justify-content:space-between;font-size:11px;margin-bottom:4px;align-items:center}
.bar-track{height:10px;background:#E2E8F0;border-radius:5px;overflow:hidden}
.bar-inner{height:100%;border-radius:5px;transition:width .5s}
.status-row{display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap}
.status-pill{flex:1;min-width:140px;padding:12px 14px;border-radius:10px;display:flex;align-items:center;gap:10px;font-size:12px;border:1px solid}
.status-pill .sp-icon{font-size:20px;font-weight:700}
.status-pill .sp-count{font-size:20px;font-weight:800;font-family:'IBM Plex Mono',monospace}
.status-pill .sp-label{font-size:10px;text-transform:uppercase;letter-spacing:.5px;opacity:.8}
table{width:100%;border-collapse:collapse;font-size:12px;margin-bottom:8px;background:#fff;border:1px solid #E2E8F0;border-radius:10px;overflow:hidden}
th{background:#F0F4FA;color:#475569;font-weight:700;text-align:left;padding:11px 12px;font-size:10px;text-transform:uppercase;letter-spacing:.5px;border-bottom:2px solid #E2E8F0}
td{padding:11px 12px;border-bottom:1px solid #F0F4FA;vertical-align:top}
tr:last-child td{border-bottom:none}
.bdg{display:inline-block;padding:3px 9px;border-radius:6px;font-size:10px;font-weight:600;white-space:nowrap}
.footer{margin-top:40px;padding-top:20px;border-top:2px solid #E2E8F0;font-size:11px;color:#94A3B8;display:flex;justify-content:space-between;align-items:center}
.footer .logo-footer{font-weight:700;color:#4361EE;display:flex;align-items:center;gap:6px}
</style></head><body>

<div class="header">
<div class="header-content">
<div><h1>⚡ Smart Planner</h1><div class="subtitle">Отчёт о выполнении задач</div></div>
<div class="period">
<div class="label">Отчётный период</div>
<div class="dates">${fmt(expFrom)} — ${fmt(expTo)}</div>
<div class="gen">Сформировано: ${fmt(now)}</div>
</div></div></div>

<div class="assess-box">
<div><div class="main-text">${assessment.text}</div><div class="sub">Коэффициент завершения задач за отчётный период</div></div>
<div class="big-pct">${expStats.pct}%</div>
</div>

<div class="kpis">
<div class="kpi-box blue"><div class="num">${expStats.total}</div><div class="lbl">Всего</div><div class="sub">задач</div></div>
<div class="kpi-box grn"><div class="num">${done.length}</div><div class="lbl">Выполнено</div><div class="sub">завершены</div></div>
<div class="kpi-box blue"><div class="num">${inprog.length}</div><div class="lbl">В работе</div><div class="sub">активных</div></div>
<div class="kpi-box amb"><div class="num">${burning.length}</div><div class="lbl">Горит</div><div class="sub">≤ 2 дня</div></div>
<div class="kpi-box red"><div class="num">${overdue.length}</div><div class="lbl">Просрочено</div><div class="sub">срок вышел</div></div>
<div class="kpi-box pnk"><div class="num">${avgProg}%</div><div class="lbl">Прогресс</div><div class="sub">средний</div></div>
</div>

<div class="summary">
<div class="summary-title">📊 Подробная сводка</div>
<div class="summary-grid">
<div class="summary-item"><div class="sum-label">Всего задач в отчёте</div><div class="sum-value">${expStats.total}</div></div>
<div class="summary-item"><div class="sum-label">Коэффициент завершения</div><div class="sum-value ${expStats.pct>=70?'pos':expStats.pct>=40?'warn':'neg'}">${expStats.pct}% (${done.length} из ${expStats.total})</div></div>
<div class="summary-item"><div class="sum-label">Средний прогресс</div><div class="sum-value">${avgProg}%</div></div>
<div class="summary-item"><div class="sum-label">Активных задач</div><div class="sum-value">${active.length}</div></div>
<div class="summary-item"><div class="sum-label">Задач в критической зоне</div><div class="sum-value ${burning.length+overdue.length>0?'warn':'pos'}">${burning.length+overdue.length} (горит ${burning.length} + просрочено ${overdue.length})</div></div>
<div class="summary-item"><div class="sum-label">Пунктуальность</div><div class="sum-value ${onTimeRate===null?'':onTimeRate>=80?'pos':onTimeRate>=50?'warn':'neg'}">${onTimeRate!==null?onTimeRate+'% задач выполнено в срок':'нет завершённых для оценки'}</div></div>
<div class="summary-item"><div class="sum-label">Скорость выполнения</div><div class="sum-value">${avgTimeDays!==null?avgTimeDays+' дн. в среднем на задачу':'нет данных'}</div></div>
<div class="summary-item"><div class="sum-label">Задач с нарушением срока</div><div class="sum-value ${latDone>0?'warn':'pos'}">${latDone} ${latDone>0?'(сдано с опозданием)':''}</div></div>
</div>
<div class="narrative">
<strong>Ключевые выводы:</strong> За отчётный период с ${fmt(expFrom)} по ${fmt(expTo)} было обработано <strong>${expStats.total}</strong> задач. Из них <strong>${done.length}</strong> успешно завершены (${expStats.pct}% от общего числа). ${onTimeRate!==null?'В срок выполнено <strong>'+onTimeRate+'%</strong> из завершённых задач. ':''}${avgTimeDays!==null?'Средняя продолжительность выполнения — <strong>'+avgTimeDays+'</strong> дн. ':''}
${overdue.length>0?'⚠ <strong>Требуют особого внимания:</strong> '+overdue.length+' просроченных задач. ':''}
${burning.length>0?'🔥 <strong>Приближаются дедлайны:</strong> '+burning.length+' горящих задач. ':''}
${overdue.length===0&&burning.length===0?'✓ Критических задач не обнаружено — все сроки под контролем. ':''}
${expStats.pct>=75?'Команда демонстрирует высокую эффективность.':expStats.pct>=50?'Результаты в пределах нормы, есть потенциал для роста.':'Необходимо пересмотреть распределение ресурсов и приоритеты.'}
</div></div>

<div class="section no-break">
<h2>📈 Распределение по статусам <span class="count">${expStats.total} задач</span></h2>
<div class="status-row">
${statuses.map(s=>`<div class="status-pill" style="background:${s.color}0F;border-color:${s.color}40;color:${s.color}"><div class="sp-icon">${s.icon}</div><div><div class="sp-count">${s.count}</div><div class="sp-label">${s.label} · ${Math.round(s.count/expStats.total*100)}%</div></div></div>`).join('')}
</div></div>

${expStats.total>0?`<div class="section no-break">
<h2>🔀 Структура задач</h2>
<div class="bar-section">
<div class="bar-group"><div class="bar-group-title">🏷️ По категориям</div>
${Object.entries(catBr).sort((a,b)=>b[1]-a[1]).map(([c,n])=>`<div class="bar-item"><div class="bar-label-row"><span style="font-weight:600;color:${CC[c]||'#64748B'}">${escapeHTML(c)}</span><span style="font-family:IBM Plex Mono;font-weight:700">${n} · ${Math.round(n/expStats.total*100)}%</span></div><div class="bar-track"><div class="bar-inner" style="width:${(n/expStats.total)*100}%;background:${CC[c]||'#64748B'}"></div></div></div>`).join('')}
</div>
<div class="bar-group"><div class="bar-group-title">🎯 По приоритетам</div>
${Object.entries(priBr).sort((a,b)=>b[1]-a[1]).map(([p,n])=>`<div class="bar-item"><div class="bar-label-row"><span style="font-weight:600;color:${PC[p]||'#64748B'}">${escapeHTML(p)}</span><span style="font-family:IBM Plex Mono;font-weight:700">${n} · ${Math.round(n/expStats.total*100)}%</span></div><div class="bar-track"><div class="bar-inner" style="width:${(n/expStats.total)*100}%;background:${PC[p]||'#64748B'}"></div></div></div>`).join('')}
</div></div></div>`:''}

${overdue.length?`<div class="section page-break"><h2 style="color:#EF4444">⚠ Просроченные задачи <span class="count">${overdue.length}</span></h2>
<table><thead><tr><th>Задача</th><th>Категория</th><th>Приоритет</th><th>Дедлайн</th><th>Статус</th><th>Прогресс</th></tr></thead><tbody>${overdue.map(t=>taskRow(t,true)).join('')}</tbody></table></div>`:''}

${burning.length?`<div class="section"><h2 style="color:#F59E0B">🔥 Горящие задачи <span class="count">${burning.length}</span></h2>
<table><thead><tr><th>Задача</th><th>Категория</th><th>Приоритет</th><th>Дедлайн</th><th>Статус</th><th>Прогресс</th></tr></thead><tbody>${burning.map(t=>taskRow(t,true)).join('')}</tbody></table></div>`:''}

${inprog.length?`<div class="section"><h2 style="color:#4361EE">⟳ Задачи в работе <span class="count">${inprog.length}</span></h2>
<table><thead><tr><th>Задача</th><th>Категория</th><th>Приоритет</th><th>Дедлайн</th><th>Статус</th><th>Прогресс</th></tr></thead><tbody>${inprog.map(t=>taskRow(t,true)).join('')}</tbody></table></div>`:''}

${done.length?`<div class="section page-break"><h2 style="color:#10B981">✓ Выполненные задачи <span class="count">${done.length}</span></h2>
<table><thead><tr><th>Задача</th><th>Категория</th><th>Приоритет</th><th>Статус</th><th>Прогресс</th><th>Завершено</th></tr></thead><tbody>${done.map(t=>taskRow(t,false)).join('')}</tbody></table></div>`:''}

<div class="footer">
<div class="logo-footer">⚡ Smart Planner</div>
<div>Автоматический отчёт · ${fmt(now)}</div>
</div></body></html>`;
setExpPreview(html);setExpGen(false)},200)};

const printReport=async()=>{if(!expPreview)return;await callApi("save_pdf_report",expPreview)};

if(loading)return<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100vh",fontSize:18,color:"var(--text3)"}}>Загрузка...</div>;

return<div>
<div className="hdr"><div className="hdr-brand"><div className="hdr-logo">⚡</div><div><h1>Smart Planner</h1><small>{fmt(now)}</small></div></div>
<div className="tabs">{TABS.map(t=><button key={t} className={`tab ${tab===t?"on":""}`} onClick={()=>setTab(t)}><span className="tab-icon">{TAB_ICONS[t]}</span>{t}</button>)}</div>
<div style={{display:"flex",gap:8}}><button className="add-b" onClick={()=>{setEditTask(null);setShowForm(true)}}><span>+</span> Задача</button><button className="set-b" onClick={()=>setShowSettings(true)} title="Настройки">⚙</button></div></div>

<div className="main">
{/* ПАНЕЛЬ */}
{tab==="Панель"&&<><div className="kpi-r">
<div className="kpi" style={{cursor:"pointer"}} onClick={()=>setDrillKpi("total")}><div className="kpi-glow" style={{background:"var(--accent)"}}/><div className="kpi-l">Всего</div><div className="kpi-v" style={{color:"var(--accent)"}}>{stats.total}</div><div className="kpi-s">задач · клик для списка</div></div>
<div className="kpi" style={{cursor:"pointer"}} onClick={()=>setDrillKpi("done")}><div className="kpi-glow" style={{background:"var(--green)"}}/><div className="kpi-l">Выполнено</div><div className="kpi-v" style={{color:"var(--green)"}}>{stats.done}</div><div className="kpi-s">{stats.pct}% · клик для списка</div></div>
<div className="kpi" style={{cursor:"pointer"}} onClick={()=>setDrillKpi("active")}><div className="kpi-glow" style={{background:"var(--accent)"}}/><div className="kpi-l">В работе</div><div className="kpi-v" style={{color:"var(--accent)"}}>{stats.active}</div><div className="kpi-s">активных · клик</div></div>
<div className="kpi" style={{cursor:"pointer"}} onClick={()=>setDrillKpi("burn")}><div className="kpi-glow" style={{background:"var(--amber)"}}/><div className="kpi-l">Горит</div><div className="kpi-v" style={{color:"var(--amber)"}}>{stats.burn}</div><div className="kpi-s">≤ 2 дня · клик</div></div>
<div className="kpi" style={{cursor:"pointer"}} onClick={()=>setDrillKpi("over")}><div className="kpi-glow" style={{background:"var(--red)"}}/><div className="kpi-l">Просрочено</div><div className="kpi-v" style={{color:"var(--red)"}}>{stats.over}</div><div className="kpi-s">срок вышел · клик</div></div>
</div>
<div className="card card-glow" style={{marginBottom:22}}><div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:10}}><span className="stitle" style={{margin:0}}>🚀 Общий прогресс</span><span style={{fontWeight:800,fontSize:22,color:"var(--accent)",fontFamily:"var(--mono)"}}>{stats.pct}%</span></div><PBar value={stats.pct} size={12} color="var(--accent)"/></div>
<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16,marginBottom:22}} className="two-col">
<div className="card"><div className="stitle"><span className="stitle-icon">🎯</span> По приоритетам</div>{data.priorities.map(p=>{const c=data.tasks.filter(t=>t.name&&t.pri===p).length;return<div key={p} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"7px 0",borderBottom:"1px solid var(--border)"}}><Bdg color={gp(p)} bg={gb(p)}>{p}</Bdg><span style={{fontWeight:800,fontSize:18,color:gp(p),fontFamily:"var(--mono)"}}>{c}</span></div>})}</div>
<div className="card"><div className="stitle"><span className="stitle-icon">🏷️</span> По категориям</div>{data.categories.map(c=>{const n=data.tasks.filter(t=>t.name&&t.cat===c).length;if(!n)return null;return<div key={c} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"7px 0",borderBottom:"1px solid var(--border)"}}><Bdg color={gc(c)}>{c}</Bdg><span style={{fontWeight:800,fontSize:18,color:gc(c),fontFamily:"var(--mono)"}}>{n}</span></div>})}</div>
</div>
{urgent.length>0&&<div className="card" style={{borderLeft:"3px solid var(--red)"}}><div className="stitle" style={{color:"var(--red)"}}>🔥 Требуют внимания</div>{urgent.map(t=>{const st=getS(t,now);return<div key={t.id} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"10px 0",borderBottom:"1px solid var(--border)",cursor:"pointer"}} onClick={()=>setDetailTask(t)}><div><div style={{fontWeight:600}}>{t.name}</div><div style={{fontSize:12,color:"var(--text3)"}}>{t.cat} · {fmt(t.deadline)}</div></div><Bdg color={st.c}>{st.i} {st.l}</Bdg></div>})}</div>}</>}

{/* ЗАДАЧИ */}
{tab==="Задачи"&&<><div className="filter-bar"><div className="seg">{[["active","Активные"],["all","Все"],["completed","Готовые"]].map(([k,l])=><button key={k} className={filter===k?"on":""} onClick={()=>setFilter(k)}>{l}</button>)}</div>
<select value={sortBy} onChange={e=>setSortBy(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:12,background:"var(--bg3)",color:"var(--text)"}}><option value="deadline">По дедлайну</option><option value="priority">По приоритету</option><option value="category">По категории</option><option value="created">По дате создания</option></select>
<span style={{fontSize:12,color:"var(--text4)",marginLeft:"auto"}}>{filtered.length} задач</span></div>
<div style={{display:"flex",flexDirection:"column",gap:6}}>{filtered.map(t=>{const st=getS(t,now);const dl=t.deadline?diffD(t.deadline,now):null;const isMtg=t.cat==="Совещание";
return<div key={t.id} className={`tr ${st.l==="Выполнено"?"done":""}`} onClick={()=>setDetailTask(t)}><div className="task-left" style={{background:gp(t.pri)}}/><div style={{flex:1,minWidth:0}}>
<div style={{fontWeight:600,fontSize:14,textDecoration:st.l==="Выполнено"?"line-through":"none",color:st.l==="Выполнено"?"var(--text3)":"var(--text)"}}>{t.name}</div>
<div style={{display:"flex",gap:5,marginTop:5,flexWrap:"wrap",alignItems:"center"}}><Bdg color={gc(t.cat)}>{t.cat}</Bdg><Bdg color={gp(t.pri)} bg={gb(t.pri)}>{t.pri}</Bdg>
{isMtg&&t.timeStart&&<span className="meeting-time">🕐 {t.timeStart}–{t.timeEnd||"?"}</span>}
{t.deadline&&<span style={{fontSize:11,color:dl<0?"var(--red)":dl<=2?"var(--amber)":"var(--text3)"}}>📅 {fmt(t.deadline)}{dl!==null&&dl<0?` (+${Math.abs(dl)}д)`:""}</span>}</div>
<div style={{marginTop:6}} onClick={e=>e.stopPropagation()}><PBar value={t.progress} color={st.c} onChange={p=>setProg(t.id,p)}/></div></div>
<div style={{textAlign:"right",flexShrink:0}}><Bdg color={st.c}>{st.i} {st.l}</Bdg><div style={{fontSize:14,fontWeight:700,color:st.c,fontFamily:"var(--mono)",marginTop:4}}>{t.progress}%</div></div></div>})}
{filtered.length===0&&<div style={{textAlign:"center",padding:60,color:"var(--text4)"}}><div style={{fontSize:44,marginBottom:10}}>📋</div><div style={{fontWeight:700,fontSize:16}}>Нет задач</div></div>}</div></>}

{/* СЕГОДНЯ */}
{tab==="Сегодня"&&<><div style={{marginBottom:16}}><div style={{fontWeight:800,fontSize:22,color:"var(--accent)"}}>{fmt(now)}</div><div style={{color:"var(--text3)",fontSize:13,marginTop:2}}>{todayL.length} активных задач</div></div>
{todayL.map(t=>{const st=getS(t,now);const isMtg=t.cat==="Совещание";return<div key={t.id} className="card" style={{marginBottom:8,borderLeft:`3px solid ${gp(t.pri)}`,cursor:"pointer"}} onClick={()=>setDetailTask(t)}>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",gap:12,flexWrap:"wrap"}}><div style={{flex:1}}><div style={{fontWeight:700,fontSize:16}}>{t.name}</div>{t.desc&&<div style={{fontSize:13,color:"var(--text2)",marginTop:3}}>{t.desc}</div>}
<div style={{display:"flex",gap:6,marginTop:8,flexWrap:"wrap",alignItems:"center"}}><Bdg color={gc(t.cat)}>{t.cat}</Bdg><Bdg color={st.c}>{st.i} {st.l}</Bdg>{isMtg&&t.timeStart&&<span className="meeting-time">🕐 {t.timeStart}–{t.timeEnd||"?"}</span>}</div></div>
<div style={{fontSize:20,fontWeight:800,color:st.c,fontFamily:"var(--mono)"}}>{t.progress}%</div></div>
<div style={{marginTop:12}} onClick={e=>e.stopPropagation()}><PBar value={t.progress} color={st.c} onChange={p=>setProg(t.id,p)} size={10}/></div></div>})}
{todayL.length===0&&<div style={{textAlign:"center",padding:60,color:"var(--text4)"}}><div style={{fontSize:52,marginBottom:12}}>🎉</div><div style={{fontSize:18,fontWeight:700}}>Всё выполнено!</div></div>}</>}

{/* РАСПИСАНИЕ */}
{tab==="Расписание"&&<><div style={{display:"flex",alignItems:"center",gap:8,marginBottom:16,flexWrap:"wrap"}}>
<button className="bo" style={{padding:"6px 12px"}} onClick={()=>{const d=new Date(schedDate);d.setDate(d.getDate()-7);setSchedDate(d.toISOString().split("T")[0])}}>←</button>
<input type="date" value={schedDate} onChange={e=>setSchedDate(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:13,fontWeight:600,background:"var(--bg3)",color:"var(--text)"}}/>
<button className="bo" style={{padding:"6px 12px"}} onClick={()=>{const d=new Date(schedDate);d.setDate(d.getDate()+7);setSchedDate(d.toISOString().split("T")[0])}}>→</button>
<button className="bo" onClick={()=>setSchedDate(td())} style={{fontSize:12}}>Сегодня</button>
<span style={{fontSize:12,color:"var(--text3)",marginLeft:8}}>📅 Только совещания</span></div>
<div className="sw"><div className="sg" style={{gridTemplateColumns:`60px repeat(7,minmax(100px,1fr))`}}>
<div className="sh" style={{fontSize:9}}>Время</div>
{weekD.map((d,i)=><div key={d} className={`sh ${d===now?"td":""}`}><div>{dayN[i]}</div><div style={{fontSize:10,opacity:.7,fontWeight:400}}>{fmtS(d)}</div></div>)}
{hours.map(h=><React.Fragment key={h}><div className="st">{h}</div>
{weekD.map(d=>{const mt=getMeetingsForDay(d);const hN=parseInt(h);const match=mt.filter(m=>m.timeStart&&parseInt(m.timeStart.split(":")[0])===hN);
return<div key={d} className={`sc ${d===now?"td":""}`}>{match.map(m=><span key={m.id} className="sch" style={{background:gc("Совещание")+"20",color:gc("Совещание"),padding:"4px 6px",fontSize:10}} onClick={()=>setDetailTask(m)}>{m.timeStart&&<span style={{fontWeight:700}}>{m.timeStart} </span>}{m.name}</span>)}</div>})}</React.Fragment>)}
</div></div></>}

{/* ЖУРНАЛ */}
{tab==="Журнал"&&<><div style={{display:"flex",alignItems:"center",gap:8,marginBottom:16,flexWrap:"wrap"}}>
<button className="bo" style={{padding:"6px 12px"}} onClick={()=>{const[y,m]=habMonth.split("-").map(Number);const d=new Date(y,m-2,1);setHabMonth(`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`)}}>←</button>
<input type="month" value={habMonth} onChange={e=>setHabMonth(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:13,fontWeight:600,background:"var(--bg3)",color:"var(--text)"}}/>
<button className="bo" style={{padding:"6px 12px"}} onClick={()=>{const[y,m]=habMonth.split("-").map(Number);const d=new Date(y,m,1);setHabMonth(`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`)}}>→</button>
<span style={{fontWeight:700,fontSize:16}}>{monthN[parseInt(habMonth.split("-")[1])]} {habMonth.split("-")[0]}</span>
<span style={{fontSize:12,color:"var(--text4)",marginLeft:8}}>{data.tasks.filter(t=>t.completedAt&&t.completedAt.startsWith(habMonth)).length} завершённых</span></div>
<div className="card" style={{padding:0,overflow:"auto"}}><table className="ht"><thead><tr><th>Задача</th><th style={{minWidth:70}}>Категория</th>
{Array.from({length:daysInM},(_,i)=>{const dk=`${habMonth}-${String(i+1).padStart(2,"0")}`;return<th key={i} className={dk===now?"today-th":""} style={{minWidth:30}}>{i+1}</th>})}</tr></thead>
<tbody>{(()=>{const completed=data.tasks.filter(t=>t.completedAt&&t.completedAt.startsWith(habMonth));
if(!completed.length)return<tr><td colSpan={daysInM+2} style={{textAlign:"center",padding:50,color:"var(--text4)"}}>📓 Нет завершённых задач</td></tr>;
return completed.map((t,i)=><tr key={t.id||i} style={{background:i%2===0?"#FFFFFF":"var(--bg)",cursor:"pointer"}} onClick={()=>setDetailTask(t)}>
<td><div style={{fontWeight:600,fontSize:12}}>{t.name}</div></td><td style={{textAlign:"center"}}><Bdg color={gc(t.cat)}>{t.cat}</Bdg></td>
{Array.from({length:daysInM},(_,di)=>{const dk=`${habMonth}-${String(di+1).padStart(2,"0")}`;return<td key={di} style={{textAlign:"center",padding:2}}>{t.completedAt===dk&&<span style={{display:"inline-flex",width:28,height:28,borderRadius:8,background:"var(--gradient2)",color:"#fff",alignItems:"center",justifyContent:"center",fontSize:14,fontWeight:700}}>✓</span>}</td>})}
</tr>)})()}</tbody></table></div></>}

{/* АНАЛИТИКА — мощный инструмент */}
{tab==="Аналитика"&&(()=>{
/* Filter tasks by period */
const anFiltered=data.tasks.filter(t=>{
if(!t.name)return false;
if(anCat&&t.cat!==anCat)return false;
if(anPri&&t.pri!==anPri)return false;
if(anPeriod==="all")return true;
const nd=new Date();let from;
if(anPeriod==="week"){from=new Date(nd);from.setDate(from.getDate()-7)}
else if(anPeriod==="month"){from=new Date(nd);from.setMonth(from.getMonth()-1)}
else if(anPeriod==="quarter"){from=new Date(nd);from.setMonth(from.getMonth()-3)}
else if(anPeriod==="year"){from=new Date(nd);from.setFullYear(from.getFullYear()-1)}
const fISO=from.toISOString().split("T")[0];
return(t.start&&t.start>=fISO)||(t.deadline&&t.deadline>=fISO)||(t.completedAt&&t.completedAt>=fISO)||(t.createdAt&&t.createdAt>=fISO);
});

const anStats={total:0,done:0,active:0,burn:0,over:0,newT:0};
anFiltered.forEach(t=>{anStats.total++;const st=getS(t,now).l;
if(st==="Выполнено")anStats.done++;
else if(st==="Просрочено")anStats.over++;
else if(st==="Горит")anStats.burn++;
else if(st==="В работе")anStats.active++;
else anStats.newT++});
const anPct=anStats.total?Math.round(anStats.done/anStats.total*100):0;
const anAvgProg=anStats.total?Math.round(anFiltered.reduce((a,t)=>a+(t.progress||0),0)/anStats.total):0;

/* On-time rate: завершено до дедлайна */
const onTimeRate=(()=>{
const completed=anFiltered.filter(t=>t.completedAt);
if(!completed.length)return null;
const onTime=completed.filter(t=>!t.deadline||t.completedAt<=t.deadline).length;
return Math.round(onTime/completed.length*100);
})();

/* Average completion time (days from start to completedAt) */
const avgCompTime=(()=>{
const done=anFiltered.filter(t=>t.completedAt&&t.start);
if(!done.length)return null;
const total=done.reduce((s,t)=>s+Math.max(0,diffD(t.completedAt,t.start)),0);
return Math.round(total/done.length*10)/10;
})();

/* Heatmap 12 weeks */
const heatmap=[];
for(let w=11;w>=0;w--){const week=[];for(let d=0;d<7;d++){const dt=new Date();dt.setDate(dt.getDate()-w*7-d);const ds=dt.toISOString().split("T")[0];const count=data.tasks.filter(t=>t.completedAt===ds).length;week.push({date:ds,count})}heatmap.push(week)}
const maxHeat=Math.max(...heatmap.flat().map(c=>c.count),1);

/* Timeline 14 days */
const timeline=[];
for(let i=13;i>=0;i--){const dt=new Date();dt.setDate(dt.getDate()-i);const ds=dt.toISOString().split("T")[0];
timeline.push({day:ds,created:data.tasks.filter(t=>t.createdAt&&t.createdAt.startsWith(ds)).length,completed:data.tasks.filter(t=>t.completedAt===ds).length})}
const maxTL=Math.max(...timeline.map(d=>Math.max(d.created,d.completed)),1);

/* Upcoming deadlines (next 7 days) */
const upcoming=data.tasks.filter(t=>{const st=getS(t,now).l;if(st==="Выполнено")return false;if(!t.deadline)return false;const dl=diffD(t.deadline,now);return dl>=0&&dl<=7}).sort((a,b)=>(a.deadline||"").localeCompare(b.deadline||""));

/* Category x Priority matrix */
const catPri={};data.categories.forEach(c=>{catPri[c]={};data.priorities.forEach(p=>{catPri[c][p]=anFiltered.filter(t=>t.cat===c&&t.pri===p).length})});

/* Avg progress per category */
const apc={};data.categories.forEach(c=>{const ts=anFiltered.filter(t=>t.cat===c);apc[c]=ts.length?Math.round(ts.reduce((a,t)=>a+(t.progress||0),0)/ts.length):0});

const statusSegs=[
{label:"Выполнено",value:anStats.done,color:"#10B981"},
{label:"В работе",value:anStats.active,color:"#4361EE"},
{label:"Горит",value:anStats.burn,color:"#F59E0B"},
{label:"Просрочено",value:anStats.over,color:"#EF4444"},
{label:"Новая",value:anStats.newT,color:"#94A3B8"},
].filter(s=>s.value>0).map(s=>({...s,pct:anStats.total?s.value/anStats.total*100:0}));

const chartNames={kpis:"KPI метрики",status:"Статусы",category:"Категории",priority:"Приоритеты",productivity:"Продуктивность",timeline:"Таймлайн 14 дней",heatmap:"Тепловая карта",catPri:"Матрица кат×приор",avgProg:"Прогресс по кат.",completion:"Скорость",onTime:"Пунктуальность",upcoming:"Ближайшие дедлайны"};

return<div>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",marginBottom:20,flexWrap:"wrap",gap:12}}>
<div><div style={{fontSize:22,fontWeight:800}}>📈 Аналитика</div><div style={{color:"var(--text3)",fontSize:13,marginTop:2}}>Мощный инструмент анализа задач · {anFiltered.length} в выборке</div></div>
<div style={{display:"flex",gap:8,flexWrap:"wrap"}}>
<div className="seg">{[["all","Всё время"],["week","Неделя"],["month","Месяц"],["quarter","Квартал"],["year","Год"]].map(([k,l])=><button key={k} className={anPeriod===k?"on":""} onClick={()=>setAnPeriod(k)}>{l}</button>)}</div>
<select value={anCat} onChange={e=>setAnCat(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:12,background:"#fff"}}>
<option value="">Все категории</option>{data.categories.map(c=><option key={c}>{c}</option>)}
</select>
<select value={anPri} onChange={e=>setAnPri(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:12,background:"#fff"}}>
<option value="">Все приоритеты</option>{data.priorities.map(p=><option key={p}>{p}</option>)}
</select>
<button className="bo" onClick={()=>setAnShowSettings(!anShowSettings)}>⚙️ Виджеты</button>
</div></div>

{anShowSettings&&<div className="card" style={{marginBottom:16,padding:16}}>
<div className="stitle" style={{marginBottom:10}}>Управление виджетами</div>
<div style={{display:"flex",flexWrap:"wrap",gap:8}}>
{Object.entries(chartNames).map(([k,nm])=><button key={k} onClick={()=>setAnCharts(p=>({...p,[k]:!p[k]}))} style={{padding:"6px 14px",borderRadius:10,border:`1px solid ${anCharts[k]?"var(--accent)":"var(--border)"}`,background:anCharts[k]?"var(--accent-bg)":"#fff",color:anCharts[k]?"var(--accent)":"var(--text3)",fontSize:12,fontWeight:600,cursor:"pointer"}}>{anCharts[k]?"✓ ":"○ "}{nm}</button>)}
</div></div>}

{/* KPI row */}
{anCharts.kpis&&<div style={{display:"grid",gridTemplateColumns:"repeat(6,1fr)",gap:12,marginBottom:20}}>
<div className="kpi"><div className="kpi-glow" style={{background:"var(--accent)"}}/><div className="kpi-l">Всего</div><div className="kpi-v" style={{color:"var(--accent)"}}>{anStats.total}</div><div className="kpi-s">в выборке</div></div>
<div className="kpi"><div className="kpi-glow" style={{background:"var(--green)"}}/><div className="kpi-l">Выполнено</div><div className="kpi-v" style={{color:"var(--green)"}}>{anPct}%</div><div className="kpi-s">{anStats.done} задач</div></div>
<div className="kpi"><div className="kpi-glow" style={{background:"var(--amber)"}}/><div className="kpi-l">Ср. прогресс</div><div className="kpi-v" style={{color:"var(--amber)"}}>{anAvgProg}%</div><div className="kpi-s">по всем</div></div>
<div className="kpi"><div className="kpi-glow" style={{background:"var(--red)"}}/><div className="kpi-l">Просрочено</div><div className="kpi-v" style={{color:"var(--red)"}}>{anStats.over}</div><div className="kpi-s">срок вышел</div></div>
<div className="kpi"><div className="kpi-glow" style={{background:"var(--cyan)"}}/><div className="kpi-l">Пунктуальность</div><div className="kpi-v" style={{color:"var(--cyan2)"}}>{onTimeRate!==null?onTimeRate+"%":"—"}</div><div className="kpi-s">в срок</div></div>
<div className="kpi"><div className="kpi-glow" style={{background:"#EC4899"}}/><div className="kpi-l">Ср. срок</div><div className="kpi-v" style={{color:"#DB2777"}}>{avgCompTime!==null?avgCompTime:"—"}</div><div className="kpi-s">дней на задачу</div></div>
</div>}

<div className="analytics-grid">
{anCharts.status&&<div className="chart-card">
<div className="chart-header"><span className="chart-title">📊 Статусы задач</span></div>
{statusSegs.length?<div className="donut-container"><DonutChart segments={statusSegs} size={150} thickness={26}/>
<div className="donut-legend">{statusSegs.map(s=><div key={s.label} className="donut-legend-item"><div className="donut-legend-dot" style={{background:s.color}}/><span>{s.label}</span><span style={{fontFamily:"var(--mono)",fontWeight:700,marginLeft:"auto",paddingLeft:12}}>{s.value} ({Math.round(s.pct)}%)</span></div>)}</div>
</div>:<div style={{textAlign:"center",padding:30,color:"var(--text4)"}}>Нет данных</div>}
</div>}

{anCharts.category&&<div className="chart-card">
<div className="chart-header"><span className="chart-title">🏷️ По категориям</span></div>
{(()=>{const cd={};anFiltered.forEach(t=>{cd[t.cat]=(cd[t.cat]||0)+1});const entries=Object.entries(cd).sort((a,b)=>b[1]-a[1]);const mx=Math.max(...entries.map(e=>e[1]),1);
return entries.length?<div className="bar-chart">{entries.map(([c,n])=><div key={c} className="bar-col"><div className="bar-value">{n}</div><div className="bar-fill" style={{height:`${(n/mx)*100}%`,background:gc(c),minHeight:4}}/><div className="bar-label">{c}</div></div>)}</div>:<div style={{textAlign:"center",padding:30,color:"var(--text4)"}}>Нет данных</div>})()}
</div>}

{anCharts.priority&&<div className="chart-card">
<div className="chart-header"><span className="chart-title">🎯 По приоритетам</span></div>
{data.priorities.map(p=>{const c=anFiltered.filter(t=>t.pri===p).length;const tot=anFiltered.length||1;return<div key={p} style={{marginBottom:12}}>
<div style={{display:"flex",justifyContent:"space-between",marginBottom:4}}><span style={{fontSize:12,fontWeight:600,color:gp(p)}}>{p}</span><span style={{fontSize:12,fontWeight:700,fontFamily:"var(--mono)"}}>{c} ({Math.round(c/tot*100)}%)</span></div>
<div style={{width:"100%",height:10,background:"var(--bg4)",borderRadius:6,overflow:"hidden"}}><div style={{width:`${(c/tot)*100}%`,height:"100%",background:gp(p),borderRadius:6,transition:"width .5s"}}/></div>
</div>})}
</div>}

{anCharts.productivity&&<div className="chart-card">
<div className="chart-header"><span className="chart-title">⚡ Продуктивность</span></div>
<div className="stat-row"><span style={{color:"var(--text2)"}}>Всего задач</span><span style={{fontWeight:700,fontFamily:"var(--mono)"}}>{anStats.total}</span></div>
<div className="stat-row"><span style={{color:"var(--text2)"}}>Завершено</span><span style={{fontWeight:700,fontFamily:"var(--mono)",color:"var(--green)"}}>{anStats.done}</span></div>
<div className="stat-row"><span style={{color:"var(--text2)"}}>В работе</span><span style={{fontWeight:700,fontFamily:"var(--mono)",color:"var(--accent)"}}>{anStats.active}</span></div>
<div className="stat-row"><span style={{color:"var(--text2)"}}>Горящих</span><span style={{fontWeight:700,fontFamily:"var(--mono)",color:"var(--amber)"}}>{anStats.burn}</span></div>
<div className="stat-row"><span style={{color:"var(--text2)"}}>Просрочено</span><span style={{fontWeight:700,fontFamily:"var(--mono)",color:"var(--red)"}}>{anStats.over}</span></div>
<div className="stat-row"><span style={{color:"var(--text2)"}}>Коэф. завершения</span><span style={{fontWeight:700,fontFamily:"var(--mono)",color:anPct>=70?"var(--green)":anPct>=40?"var(--amber)":"var(--red)"}}>{anPct}%</span></div>
</div>}

{anCharts.timeline&&<div className="chart-card" style={{gridColumn:"1/-1"}}>
<div className="chart-header"><span className="chart-title">📅 Активность (14 дней): создано vs завершено</span></div>
<div className="bar-chart" style={{height:140}}>
{timeline.map(d=><div key={d.day} className="bar-col">
<div className="bar-value" style={{fontSize:9}}>{d.created||d.completed?`+${d.created}/✓${d.completed}`:""}</div>
<div style={{display:"flex",gap:2,alignItems:"flex-end",width:"100%",height:"100%"}}>
<div style={{flex:1,height:`${(d.created/maxTL)*100}%`,background:"var(--accent)",borderRadius:"4px 4px 0 0",minHeight:d.created?4:0}}/>
<div style={{flex:1,height:`${(d.completed/maxTL)*100}%`,background:"var(--green)",borderRadius:"4px 4px 0 0",minHeight:d.completed?4:0}}/>
</div>
<div className="bar-label" style={{fontSize:8}}>{fmtS(d.day)}</div>
</div>)}
</div>
<div style={{display:"flex",gap:16,justifyContent:"center",marginTop:10}}>
<div style={{display:"flex",alignItems:"center",gap:4,fontSize:11,color:"var(--text3)"}}><div style={{width:10,height:10,borderRadius:3,background:"var(--accent)"}}/> Создано</div>
<div style={{display:"flex",alignItems:"center",gap:4,fontSize:11,color:"var(--text3)"}}><div style={{width:10,height:10,borderRadius:3,background:"var(--green)"}}/> Завершено</div>
</div></div>}

{anCharts.heatmap&&<div className="chart-card" style={{gridColumn:"1/-1"}}>
<div className="chart-header"><span className="chart-title">🔥 Тепловая карта завершений (12 недель)</span></div>
<div style={{display:"flex",gap:8,alignItems:"flex-start"}}>
<div style={{display:"flex",flexDirection:"column",gap:3,paddingTop:2}}>
{dayN.map(d=><div key={d} style={{height:18,fontSize:9,color:"var(--text4)",display:"flex",alignItems:"center"}}>{d}</div>)}
</div>
<div style={{display:"grid",gridTemplateColumns:`repeat(${heatmap.length},1fr)`,gap:3,flex:1}}>
{heatmap.map((week,wi)=><div key={wi} style={{display:"flex",flexDirection:"column",gap:3}}>
{week.map((cell,di)=>{const intensity=cell.count/maxHeat;return<div key={di} className="heatmap-cell" title={`${fmt(cell.date)}: ${cell.count} завершений`} style={{height:18,background:cell.count===0?"var(--bg4)":`rgba(16,185,129,${Math.max(.15,intensity)})`,borderRadius:3}}/>})}
</div>)}
</div></div>
<div style={{display:"flex",gap:4,alignItems:"center",justifyContent:"flex-end",marginTop:8}}>
<span style={{fontSize:9,color:"var(--text4)"}}>Меньше</span>
{[0,.25,.5,.8].map((o,i)=><div key={i} style={{width:14,height:14,borderRadius:3,background:o===0?"var(--bg4)":`rgba(16,185,129,${o})`}}/>)}
<span style={{fontSize:9,color:"var(--text4)"}}>Больше</span>
</div></div>}

{anCharts.catPri&&<div className="chart-card">
<div className="chart-header"><span className="chart-title">🔀 Матрица Категория × Приоритет</span></div>
<div style={{overflowX:"auto"}}>
<table style={{width:"100%",borderCollapse:"collapse",fontSize:12}}>
<thead><tr><th style={{textAlign:"left",padding:"8px",color:"var(--text3)",fontWeight:600,fontSize:10,textTransform:"uppercase"}}></th>
{data.priorities.map(p=><th key={p} style={{padding:"8px",textAlign:"center",color:gp(p),fontWeight:600,fontSize:10}}>{p}</th>)}
</tr></thead>
<tbody>{data.categories.map(c=><tr key={c}>
<td style={{padding:"8px",fontWeight:600,color:gc(c),fontSize:12}}>{c}</td>
{data.priorities.map(p=>{const v=catPri[c]?.[p]||0;return<td key={p} style={{textAlign:"center",padding:"8px"}}>
<span style={{display:"inline-flex",width:32,height:32,borderRadius:8,alignItems:"center",justifyContent:"center",fontWeight:700,fontFamily:"var(--mono)",fontSize:13,background:v?gc(c)+"20":"var(--bg4)",color:v?gc(c):"var(--text4)"}}>{v}</span>
</td>})}
</tr>)}</tbody></table>
</div></div>}

{anCharts.avgProg&&<div className="chart-card">
<div className="chart-header"><span className="chart-title">📊 Средний прогресс по категориям</span></div>
{data.categories.map(c=>{const v=apc[c];if(!anFiltered.some(t=>t.cat===c))return null;return<div key={c} style={{marginBottom:12}}>
<div style={{display:"flex",justifyContent:"space-between",marginBottom:4}}><span style={{fontSize:12,fontWeight:600,color:gc(c)}}>{c}</span><span style={{fontSize:12,fontWeight:700,fontFamily:"var(--mono)"}}>{v}%</span></div>
<div style={{width:"100%",height:10,background:"var(--bg4)",borderRadius:6,overflow:"hidden"}}><div style={{width:`${v}%`,height:"100%",background:gc(c),borderRadius:6,transition:"width .5s"}}/></div>
</div>})}
</div>}

{anCharts.completion&&<div className="chart-card">
<div className="chart-header"><span className="chart-title">⏱ Скорость выполнения</span></div>
<div style={{textAlign:"center",padding:"20px 0"}}>
<div style={{fontSize:48,fontWeight:800,fontFamily:"var(--mono)",color:avgCompTime!==null?(avgCompTime<=3?"var(--green)":avgCompTime<=7?"var(--amber)":"var(--red)"):"var(--text4)"}}>{avgCompTime!==null?avgCompTime:"—"}</div>
<div style={{fontSize:12,color:"var(--text3)",marginTop:4}}>дней в среднем на задачу</div>
<div style={{marginTop:20,padding:12,background:"var(--bg)",borderRadius:10,fontSize:12,color:"var(--text2)",lineHeight:1.6}}>
{avgCompTime===null?"Нет завершённых задач со стартом для расчёта":
avgCompTime<=3?"🚀 Отличная скорость работы!":
avgCompTime<=7?"👍 Нормальный темп работы":
"⚠️ Задачи выполняются медленно"}
</div></div></div>}

{anCharts.onTime&&<div className="chart-card">
<div className="chart-header"><span className="chart-title">🎯 Пунктуальность</span></div>
<div style={{textAlign:"center",padding:"20px 0"}}>
<div style={{fontSize:48,fontWeight:800,fontFamily:"var(--mono)",color:onTimeRate!==null?(onTimeRate>=80?"var(--green)":onTimeRate>=50?"var(--amber)":"var(--red)"):"var(--text4)"}}>{onTimeRate!==null?onTimeRate+"%":"—"}</div>
<div style={{fontSize:12,color:"var(--text3)",marginTop:4}}>задач завершено в срок</div>
<div style={{marginTop:20,padding:12,background:"var(--bg)",borderRadius:10,fontSize:12,color:"var(--text2)",lineHeight:1.6}}>
{onTimeRate===null?"Нет данных о завершениях":
onTimeRate>=80?"🏆 Превосходная дисциплина!":
onTimeRate>=50?"👌 Есть куда расти":
"📉 Часто срываются сроки"}
</div></div></div>}

{anCharts.upcoming&&<div className="chart-card" style={{gridColumn:"1/-1"}}>
<div className="chart-header"><span className="chart-title">⏰ Ближайшие дедлайны (7 дней)</span></div>
{upcoming.length?<div style={{display:"flex",flexDirection:"column",gap:6}}>
{upcoming.map(t=>{const st=getS(t,now);const dl=diffD(t.deadline,now);return<div key={t.id} className="tr" onClick={()=>setDetailTask(t)} style={{cursor:"pointer"}}>
<div className="task-left" style={{background:gp(t.pri)}}/>
<div style={{flex:1,minWidth:0}}><div style={{fontWeight:600,fontSize:14}}>{t.name}</div>
<div style={{display:"flex",gap:5,marginTop:5,flexWrap:"wrap",alignItems:"center"}}><Bdg color={gc(t.cat)}>{t.cat}</Bdg><Bdg color={gp(t.pri)} bg={gb(t.pri)}>{t.pri}</Bdg><span style={{fontSize:11,color:dl===0?"var(--red)":dl<=2?"var(--amber)":"var(--text3)"}}>📅 {fmt(t.deadline)} · {dl===0?"сегодня":`через ${dl} д.`}</span></div></div>
<div style={{textAlign:"right",flexShrink:0}}><Bdg color={st.c}>{st.i} {st.l}</Bdg><div style={{fontSize:13,fontWeight:700,color:st.c,fontFamily:"var(--mono)",marginTop:3}}>{t.progress}%</div></div>
</div>})}
</div>:<div style={{textAlign:"center",padding:30,color:"var(--text4)"}}>🎉 Нет срочных дедлайнов на неделю</div>}
</div>}

</div></div>})()}

{/* ЭКСПОРТ */}
{tab==="Экспорт"&&<div><div style={{fontSize:20,fontWeight:800,marginBottom:6}}>📄 Экспорт отчёта</div><div style={{color:"var(--text3)",fontSize:13,marginBottom:20}}>Сформируйте отчёт для руководителя</div>
<div style={{display:"grid",gridTemplateColumns:"340px 1fr",gap:20}} className="two-col">
<div className="card" style={{alignSelf:"flex-start"}}>
<div className="stitle"><span className="stitle-icon">🔍</span> Параметры</div>
<div style={{marginBottom:16}}><div className="fl"><label>Период от</label><input type="date" value={expFrom} onChange={e=>setExpFrom(e.target.value)}/></div></div>
<div style={{marginBottom:16}}><div className="fl"><label>Период до</label><input type="date" value={expTo} onChange={e=>setExpTo(e.target.value)}/></div></div>
<div style={{marginBottom:16}}><label style={{fontSize:11,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",letterSpacing:".6px",marginBottom:6,display:"block"}}>Категории</label>
<div style={{display:"flex",flexWrap:"wrap",gap:4}}>{data.categories.map(c=><button key={c} onClick={()=>toggleA(expCats,setExpCats,c)} style={{padding:"4px 10px",borderRadius:8,border:`1px solid ${expCats.includes(c)?gc(c):"var(--border)"}`,background:expCats.includes(c)?gc(c)+"15":"#fff",color:expCats.includes(c)?gc(c):"var(--text3)",fontSize:11,fontWeight:600,cursor:"pointer"}}>{c}</button>)}</div></div>
<div style={{marginBottom:16}}><label style={{fontSize:11,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",letterSpacing:".6px",marginBottom:6,display:"block"}}>Приоритеты</label>
<div style={{display:"flex",flexWrap:"wrap",gap:4}}>{data.priorities.map(p=><button key={p} onClick={()=>toggleA(expPris,setExpPris,p)} style={{padding:"4px 10px",borderRadius:8,border:`1px solid ${expPris.includes(p)?gp(p):"var(--border)"}`,background:expPris.includes(p)?gp(p)+"15":"#fff",color:expPris.includes(p)?gp(p):"var(--text3)",fontSize:11,fontWeight:600,cursor:"pointer"}}>{p}</button>)}</div></div>
<div style={{marginBottom:20}}><label style={{fontSize:11,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",letterSpacing:".6px",marginBottom:6,display:"block"}}>Статусы</label>
<div style={{display:"flex",flexWrap:"wrap",gap:4}}>{statuses.map(s=><button key={s} onClick={()=>toggleA(expStat,setExpStat,s)} style={{padding:"4px 10px",borderRadius:8,border:`1px solid ${expStat.includes(s)?"var(--accent)":"var(--border)"}`,background:expStat.includes(s)?"var(--accent-bg)":"#fff",color:expStat.includes(s)?"var(--accent)":"var(--text3)",fontSize:11,fontWeight:600,cursor:"pointer"}}>{s}</button>)}</div></div>
<div style={{background:"var(--bg)",borderRadius:10,padding:12,marginBottom:16}}>
<div style={{display:"flex",justifyContent:"space-between",fontSize:12,marginBottom:4}}><span style={{color:"var(--text3)"}}>В выборке:</span><span style={{fontWeight:700,fontFamily:"var(--mono)"}}>{expFiltered.length}</span></div>
<div style={{display:"flex",justifyContent:"space-between",fontSize:12}}><span style={{color:"var(--text3)"}}>Выполнено:</span><span style={{fontWeight:700,fontFamily:"var(--mono)",color:"var(--green)"}}>{expStats.done}</span></div></div>
<button className="bp" onClick={genReport} disabled={expGen||!expFiltered.length} style={{opacity:expFiltered.length?1:.5}}>{expGen?"⏳ ...":"📄 Сформировать отчёт"}</button>
</div>
<div>{!expPreview?<div className="card" style={{textAlign:"center",padding:60}}><div style={{fontSize:48,marginBottom:12}}>📋</div><div style={{fontWeight:700,fontSize:16}}>Предварительный просмотр</div><div style={{color:"var(--text3)",fontSize:13}}>Настройте фильтры и нажмите «Сформировать отчёт»</div></div>
:<div><div style={{display:"flex",gap:8,marginBottom:12}}><button className="bp" onClick={printReport} style={{width:"auto",padding:"10px 24px"}}>🖨️ Печать / Сохранить PDF</button><button className="bo" onClick={()=>setExpPreview(null)}>Сбросить</button></div>
<div className="card" style={{padding:0,overflow:"hidden"}}><iframe srcDoc={expPreview} style={{width:"100%",height:"calc(100vh - 200px)",border:"none",borderRadius:16}} title="report"/></div></div>}</div>
</div></div>}
</div>

{showForm&&<TForm onClose={()=>{setShowForm(false);setEditTask(null)}} initial={editTask} cats={data.categories} pris={data.priorities} onSubmit={t=>{if(editTask)updT(editTask.id,t);else addT(t)}}/>}
{detailTask&&<TDetail task={data.tasks.find(x=>x.id===detailTask.id)||detailTask} onClose={()=>setDetailTask(null)} now={now} onEdit={t=>{setDetailTask(null);setEditTask(t);setShowForm(true)}} onDelete={delT} onProg={setProg}/>}
{showSettings&&<Settings data={data} onUpdate={reload} onClose={()=>setShowSettings(false)} showToast={showToast} protectedCats={data.protectedCats}/>}
{toast&&<Toast msg={toast.msg} type={toast.type} onDone={()=>setToast(null)}/>}
{drillKpi&&<KpiDrill kpi={drillKpi} tasks={data.tasks} now={now} onClose={()=>setDrillKpi(null)} onOpenTask={t=>setDetailTask(t)}/>}
</div>}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
</script>
</body>
</html>'''


def main():
    # Init database
    db.init_db()

    # Create API bridge
    api = Api()

    # Create window
    window = webview.create_window(
        title="Smart Planner Pro",
        html=get_html(),
        js_api=api,
        width=1400,
        height=900,
        min_size=(900, 600),
        text_select=True,
    )

    # Start webview
    webview.start(debug=False)


if __name__ == "__main__":
    main()
