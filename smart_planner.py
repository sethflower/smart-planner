"""
Smart Planner Pro — Windows Desktop Application
Requires: pip install pywebview
"""
import os
import json
import sqlite3
import datetime
import http.server

PORT = 5000
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "smart_planner.db")


def get_html():
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
.hdr{background:#FFFFFF;box-shadow:0 1px 3px rgba(0,0,0,.06);padding:0 32px;display:flex;align-items:center;height:64px;position:sticky;top:0;z-index:100;gap:16px;border-bottom:1px solid var(--border)}
.hdr-brand{display:flex;align-items:center;gap:12px;margin-right:auto}
.hdr-logo{width:38px;height:38px;border-radius:12px;background:var(--gradient);display:flex;align-items:center;justify-content:center;font-size:18px;box-shadow:0 4px 12px rgba(67,97,238,.3)}
.hdr-brand h1{color:var(--text);font-size:16px;font-weight:700;letter-spacing:-.3px}
.hdr-brand small{color:var(--text3);font-size:11px;font-weight:400}
.tabs{display:flex;height:64px;align-items:stretch;gap:2px}
.tab{padding:0 16px;border:none;background:0;color:var(--text3);font-weight:500;font-size:13px;position:relative;display:flex;align-items:center;gap:6px;border-radius:10px 10px 0 0;transition:all .2s}
.tab:hover{color:var(--text2);background:var(--bg)}
.tab.on{color:var(--accent);font-weight:700}
.tab.on::after{content:"";position:absolute;bottom:0;left:8px;right:8px;height:3px;background:var(--gradient);border-radius:3px 3px 0 0}
.tab .tab-icon{font-size:15px}
.add-b{height:38px;padding:0 18px;border-radius:12px;border:none;background:var(--gradient);color:#fff;font-weight:600;font-size:13px;display:flex;align-items:center;gap:6px;box-shadow:0 2px 10px rgba(67,97,238,.25)}
.add-b:hover{box-shadow:0 4px 16px rgba(67,97,238,.35);transform:translateY(-1px)}
.add-m{background:linear-gradient(135deg,#06B6D4,#0891B2);box-shadow:0 2px 10px rgba(6,182,212,.25)}
.add-m:hover{box-shadow:0 4px 16px rgba(6,182,212,.35)}
.set-b{width:38px;height:38px;border-radius:12px;border:1px solid var(--border);background:var(--bg);color:var(--text3);font-size:16px;display:flex;align-items:center;justify-content:center}
.set-b:hover{background:var(--bg4);color:var(--text);border-color:var(--border2)}
.main{padding:28px 32px;max-width:1400px;margin:0 auto}
.card{background:var(--card);border-radius:var(--radius-lg);border:1px solid var(--border);padding:22px;transition:all .2s;position:relative;overflow:hidden}
.card:hover{border-color:var(--border2)}
.card-glow{box-shadow:0 0 40px rgba(67,97,238,.04)}
.stitle{font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:1.2px;margin-bottom:14px;display:flex;align-items:center;gap:8px}
.stitle-icon{font-size:14px}
.kpi-r{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:24px}
.kpi{background:var(--card);border-radius:var(--radius);border:1px solid var(--border);padding:20px;position:relative;overflow:hidden;transition:all .3s}
.kpi:hover{transform:translateY(-2px);box-shadow:var(--shadow-lg)}
.kpi-glow{position:absolute;top:-20px;right:-20px;width:80px;height:80px;border-radius:50%;opacity:.06;filter:blur(20px);pointer-events:none}
.kpi-l{font-size:10px;color:var(--text3);font-weight:700;text-transform:uppercase;letter-spacing:1.2px}
.kpi-v{font-size:32px;font-weight:800;margin-top:6px;font-family:var(--mono);color:var(--accent)}
.kpi-s{font-size:11px;color:var(--text4);margin-top:4px}
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
.seg button{padding:8px 14px;border:none;background:transparent;color:var(--text3);font-size:12px;font-weight:600;border-right:1px solid var(--border);transition:all .2s}
.seg button:last-child{border:none}
.seg button:hover{color:var(--text2);background:var(--bg)}
.seg button.on{background:var(--accent);color:#fff}
.seg-cyan button.on{background:var(--cyan2)}
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
.bp{padding:12px 24px;border-radius:12px;border:none;background:var(--gradient);color:#fff;font-size:14px;font-weight:700;width:100%;letter-spacing:.3px;box-shadow:0 2px 10px rgba(67,97,238,.25)}
.bp:hover{box-shadow:0 4px 16px rgba(67,97,238,.35);transform:translateY(-1px)}
.bp-cyan{background:linear-gradient(135deg,#06B6D4,#0891B2);box-shadow:0 2px 10px rgba(6,182,212,.25)}
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
.chip{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:10px;border:1px solid var(--border);font-size:13px;font-weight:500;background:#FFFFFF}
.chip button{background:none;border:none;color:var(--text4);font-size:14px;padding:0;line-height:1}
.chip button:hover{color:var(--red)}
.sw{border:1px solid var(--border);border-radius:var(--radius-lg);overflow:auto;background:var(--card)}
.sg{display:grid;font-size:12px}
.sh{padding:12px 8px;background:var(--cyan2);color:#fff;text-align:center;font-weight:600;font-size:11px;border-bottom:1px solid var(--border)}
.sh.td{background:#7C3AED;color:#fff}
.st{padding:8px 4px;font-size:10px;font-weight:600;color:var(--cyan2);text-align:center;background:#FFFFFF;border-right:1px solid var(--border);border-bottom:1px solid var(--border);font-family:var(--mono)}
.sc{padding:2px 3px;border-right:1px solid var(--border);border-bottom:1px solid var(--border);min-height:36px;background:#FFFFFF}
.sc.td{background:rgba(6,182,212,.06)}
.sch{padding:3px 6px;border-radius:6px;font-size:10px;font-weight:600;display:block;margin:1px 0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer}
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
.toast.warning{border-color:var(--amber);color:var(--amber2);background:var(--amber-bg)}
.toast.meeting-notify{border-color:var(--cyan);color:var(--cyan2);background:var(--cyan-bg)}
@keyframes toast-in{from{opacity:0;transform:translateX(-50%) translateY(20px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}
.meeting-time{display:inline-flex;align-items:center;gap:4px;padding:3px 8px;border-radius:6px;font-size:11px;font-weight:600;background:var(--cyan-bg);color:var(--cyan2)}
.analytics-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.chart-card{background:var(--card);border-radius:var(--radius-lg);border:1px solid var(--border);padding:22px;position:relative}
.chart-card .chart-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:16px}
.chart-card .chart-title{font-size:13px;font-weight:700;color:var(--text)}
.bar-chart{display:flex;align-items:flex-end;gap:6px;height:140px;padding-top:10px}
.bar-col{display:flex;flex-direction:column;align-items:center;gap:4px;flex:1}
.bar-fill{width:100%;border-radius:6px 6px 0 0;transition:height .5s ease;min-width:20px}
.bar-label{font-size:9px;color:var(--text3);font-weight:600;text-align:center}
.bar-value{font-size:10px;font-weight:700;color:var(--text2);font-family:var(--mono)}
.donut-container{display:flex;align-items:center;justify-content:center;gap:20px}
.donut-legend{display:flex;flex-direction:column;gap:6px}
.donut-legend-item{display:flex;align-items:center;gap:8px;font-size:12px;color:var(--text2)}
.donut-legend-dot{width:10px;height:10px;border-radius:3px;flex-shrink:0}
.stat-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border)}
.stat-row:last-child{border-bottom:none}
.heatmap-cell{border-radius:3px;transition:all .2s}
.heatmap-cell:hover{transform:scale(1.3);z-index:1}
.notif-banner{position:fixed;top:74px;left:50%;transform:translateX(-50%);z-index:2500;display:flex;flex-direction:column;gap:8px;pointer-events:none;max-width:500px;width:90%}
.notif-item{pointer-events:all;padding:14px 20px;border-radius:14px;font-size:13px;font-weight:600;display:flex;align-items:center;gap:10px;box-shadow:var(--shadow-lg);animation:notif-slide .4s ease;cursor:pointer}
.notif-item.meeting{background:var(--cyan-bg);border:1.5px solid rgba(6,182,212,.3);color:var(--cyan2)}
.notif-item.overdue{background:var(--red-bg);border:1.5px solid rgba(239,68,68,.3);color:var(--red)}
.notif-close{margin-left:auto;background:none;border:none;font-size:16px;color:inherit;opacity:.6;cursor:pointer;padding:0 4px}
.notif-close:hover{opacity:1}
@keyframes notif-slide{from{opacity:0;transform:translateY(-20px)}to{opacity:1;transform:translateY(0)}}
@media(max-width:768px){.hdr{padding:0 14px;gap:8px;height:auto;flex-wrap:wrap;padding:12px 14px}.tabs{overflow-x:auto;height:auto;gap:0}.tab{padding:10px 12px;font-size:12px}.tab.on::after{bottom:-2px}.main{padding:16px 14px}.kpi-r{grid-template-columns:repeat(2,1fr)}.two-col{grid-template-columns:1fr!important}.analytics-grid{grid-template-columns:1fr}.dp{width:100vw}}
</style>
</head>
<body>
<div id="root"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.3.1/umd/react.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.3.1/umd/react-dom.production.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.24.7/babel.min.js"></script>
<script type="text/babel">
async function callApi(method,...args){while(!window.pywebview||!window.pywebview.api){await new Promise(r=>setTimeout(r,50))}return window.pywebview.api[method](...args)}

const {useState,useEffect,useMemo,useCallback,useRef}=React;
const td=()=>new Date().toISOString().split("T")[0];
const fmt=d=>{if(!d)return"\u2014";const t=new Date(d);return`${String(t.getDate()).padStart(2,"0")}.${String(t.getMonth()+1).padStart(2,"0")}.${t.getFullYear()}`};
const fmtS=d=>{if(!d)return"";const t=new Date(d);return`${String(t.getDate()).padStart(2,"0")}.${String(t.getMonth()+1).padStart(2,"0")}`};
const diffD=(a,b)=>Math.round((new Date(a)-new Date(b))/864e5);
const TABS=["Панель","Задачи","Совещания","Сегодня","Журнал","Аналитика","Экспорт"];
const TAB_ICONS={"Панель":"\ud83d\udcca","Задачи":"\ud83d\udccb","Совещания":"\ud83d\udd52","Сегодня":"\u2600\ufe0f","Журнал":"\ud83d\udcd3","Аналитика":"\ud83d\udcc8","Экспорт":"\ud83d\udcc4"};
const dayN=["Пн","Вт","Ср","Чт","Пт","Сб","Вс"];
const hours=Array.from({length:15},(_,i)=>`${String(i+7).padStart(2,"0")}:00`);
const monthN=["","Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"];
const CC={"Рабочая":"#4361EE","Проект":"#059669","Обучение":"#DB2777","Личная":"#EA580C","Рутина":"#64748B"};
const PC={"Высокий":"#EF4444","Средний":"#F59E0B","Низкий":"#10B981"};
const PB={"Высокий":"var(--red-bg)","Средний":"var(--amber-bg)","Низкий":"var(--green-bg)"};
const gc=n=>CC[n]||"#636E72";const gp=n=>PC[n]||"#636E72";const gb=n=>PB[n]||"var(--bg3)";
function getS(t,now){if(!t.name)return{l:" ",i:"",c:"var(--text3)"};if(t.progress>=100)return{l:"Выполнено",i:"\u2705",c:"var(--green)"};if(t.deadline&&t.deadline<now&&t.progress<100)return{l:"Просрочено",i:"\ud83d\udd34",c:"var(--red)"};if(t.deadline){const dl=diffD(t.deadline,now);if(dl>=0&&dl<=2)return{l:"Горит",i:"\u26a0\ufe0f",c:"var(--amber)"};}if(t.progress>0)return{l:"В работе",i:"\ud83d\udd04",c:"var(--accent)"};return{l:"Новая",i:"\ud83c\udd95",c:"var(--text3)"};}
function getMS(m,now){
if(!m.name)return{l:" ",c:"var(--text3)"};
const today=now;
if(m.progress>=100||m.completedAt)return{l:"Завершено",c:"var(--green)"};
if(m.deadline&&m.deadline<today)return{l:"Прошло",c:"var(--text3)"};
if(m.start===today||m.deadline===today)return{l:"Сегодня",c:"var(--amber)"};
if(m.start&&m.start>today)return{l:"Запланировано",c:"var(--cyan2)"};
return{l:"Активно",c:"var(--accent)"};
}
function periodRange(period){
const n=new Date();
if(period==="all")return[null,null];
if(period==="today"){const d=td();return[d,d]}
if(period==="week"){const d=new Date(n);d.setDate(d.getDate()-7);return[d.toISOString().split("T")[0],td()]}
if(period==="month"){const d=new Date(n);d.setMonth(d.getMonth()-1);return[d.toISOString().split("T")[0],td()]}
if(period==="quarter"){const d=new Date(n);d.setMonth(d.getMonth()-3);return[d.toISOString().split("T")[0],td()]}
if(period==="year"){const d=new Date(n);d.setFullYear(d.getFullYear()-1);return[d.toISOString().split("T")[0],td()]}
return[null,null]
}
function inPeriod(t,from,to){
if(!from&&!to)return true;
const dates=[t.start,t.deadline,t.createdAt&&t.createdAt.slice(0,10),t.completedAt].filter(Boolean);
if(!dates.length)return true;
return dates.some(d=>(!from||d>=from)&&(!to||d<=to));
}

const Bdg=({children,color,bg})=><span className="bdg" style={{color,background:bg||color+"18"}}>{children}</span>;
const KPI=({label,value,sub,color,onClick})=><div className="kpi" style={onClick?{cursor:"pointer"}:{}} onClick={onClick}><div className="kpi-glow" style={{background:color}}/><div className="kpi-l">{label}</div><div className="kpi-v" style={{color}}>{value}</div><div className="kpi-s">{sub}</div></div>;

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

function Toast({msg,type,onDone}){useEffect(()=>{const t=setTimeout(onDone,3500);return()=>clearTimeout(t)},[]);return<div className={`toast ${type||""}`}>{msg}</div>}

/* ─── Notification Banner ─── */
function NotifBanner({notifications,onDismiss,onClickNotif}){
if(!notifications.length)return null;
return<div className="notif-banner">{notifications.map(n=><div key={n.id} className={`notif-item ${n.type}`} onClick={()=>onClickNotif(n)}>
<span style={{fontSize:18}}>{n.type==="meeting"?"🕐":"🔴"}</span>
<div style={{flex:1}}><div>{n.title}</div><div style={{fontSize:11,opacity:.8,marginTop:2}}>{n.subtitle}</div></div>
<button className="notif-close" onClick={e=>{e.stopPropagation();onDismiss(n.id)}}>×</button>
</div>)}</div>}

/* ─── Task Form (regular task) ─── */
function TForm({onClose,initial,onSubmit,cats,pris}){
const[f,setF]=useState(initial?{...initial}:{name:"",cat:cats[0]||"",pri:pris[1]||pris[0]||"",desc:"",start:td(),deadline:"",progress:0,notes:""});
const s=(k,v)=>setF(p=>({...p,[k]:v}));
const go=()=>{if(!f.name.trim())return;onSubmit({...f,progress:parseInt(f.progress)||0,type:"task"});onClose()};
return<div className="mo" onClick={onClose}><div className="md" onClick={e=>e.stopPropagation()}>
<div className="mh"><h3>✨ {initial?"Редактировать задачу":"Новая задача"}</h3><button className="mc" onClick={onClose}>×</button></div>
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
<div className="fl"><label>Заметки</label><textarea value={f.notes} onChange={e=>s("notes",e.target.value)} placeholder="Примечания..."/></div>
<button className="bp" onClick={go} style={{marginTop:6}}>{initial?"💾 Сохранить":"➕ Добавить"}</button>
</div></div></div></div>}

/* ─── Meeting Form ─── */
function MForm({onClose,initial,onSubmit,pris}){
const[f,setF]=useState(initial?{...initial,result:initial.result||""}:{name:"",pri:pris[1]||pris[0]||"",desc:"",start:td(),deadline:td(),timeStart:"",timeEnd:"",progress:0,notes:"",result:""});
const s=(k,v)=>setF(p=>({...p,[k]:v}));
const go=()=>{if(!f.name.trim())return;onSubmit({...f,progress:parseInt(f.progress)||0,type:"meeting",cat:""});onClose()};
const isEdit=!!initial;
const isDone=isEdit&&(initial.progress>=100||initial.completedAt);
return<div className="mo" onClick={onClose}><div className="md" onClick={e=>e.stopPropagation()} style={{width:"min(620px,94vw)"}}>
<div className="mh" style={{background:"linear-gradient(135deg,rgba(6,182,212,.08),rgba(6,182,212,.02))"}}><h3>🕐 {isEdit?"Редактировать совещание":"Новое совещание"}</h3><button className="mc" onClick={onClose}>×</button></div>
<div className="mb"><div style={{display:"flex",flexDirection:"column",gap:14}}>
<div className="fl"><label>Название *</label><input value={f.name} onChange={e=>s("name",e.target.value)} placeholder="Название совещания..." autoFocus/></div>
<div className="fl"><label>Описание / повестка</label><textarea value={f.desc} onChange={e=>s("desc",e.target.value)} placeholder="Что обсуждаем..."/></div>
<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12}}>
<div className="fl"><label>Дата начала</label><input type="date" value={f.start} onChange={e=>s("start",e.target.value)}/></div>
<div className="fl"><label>Дата окончания</label><input type="date" value={f.deadline} onChange={e=>s("deadline",e.target.value)}/></div>
</div>
<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12,padding:14,background:"var(--cyan-bg)",borderRadius:12,border:"1px solid rgba(6,182,212,.2)"}}>
<div className="fl"><label style={{color:"var(--cyan2)"}}>🕐 Время начала</label><input type="time" value={f.timeStart||""} onChange={e=>s("timeStart",e.target.value)}/></div>
<div className="fl"><label style={{color:"var(--cyan2)"}}>🕐 Время окончания</label><input type="time" value={f.timeEnd||""} onChange={e=>s("timeEnd",e.target.value)}/></div>
</div>
<div className="fl"><label>Приоритет</label><select value={f.pri} onChange={e=>s("pri",e.target.value)}>{pris.map(p=><option key={p}>{p}</option>)}</select></div>
<div className="fl"><label>Заметки</label><textarea value={f.notes} onChange={e=>s("notes",e.target.value)} placeholder="Заметки по совещанию..."/></div>

{/* Result field — always visible for edit, allows entering results */}
{isEdit&&<div style={{padding:16,background:"linear-gradient(135deg,rgba(16,185,129,.06),rgba(6,182,212,.06))",borderRadius:14,border:"1px solid rgba(16,185,129,.2)"}}>
<div className="fl"><label style={{color:"var(--green2)"}}>📝 Результаты совещания</label>
<textarea value={f.result||""} onChange={e=>s("result",e.target.value)} placeholder="Запишите результаты, решения, действия по итогам совещания..." style={{minHeight:100}}/></div>
{!isDone&&<div style={{fontSize:11,color:"var(--text3)",marginTop:6}}>💡 Заполните результаты и нажмите «Сохранить». Чтобы отметить совещание завершённым, установите прогресс 100% в детальном просмотре.</div>}
</div>}

<button className="bp bp-cyan" onClick={go} style={{marginTop:6}}>{isEdit?"💾 Сохранить":"➕ Добавить совещание"}</button>
</div></div></div></div>}

/* ─── Result Modal (quick add result) ─── */
function ResultModal({task,onClose,onSave}){
const[result,setResult]=useState(task.result||"");
return<div className="mo" onClick={onClose}><div className="md" onClick={e=>e.stopPropagation()} style={{width:"min(520px,94vw)"}}>
<div className="mh" style={{background:"linear-gradient(135deg,rgba(16,185,129,.08),rgba(6,182,212,.06))"}}><h3>📝 Результаты совещания</h3><button className="mc" onClick={onClose}>×</button></div>
<div className="mb">
<div style={{marginBottom:12}}><div style={{fontWeight:700,fontSize:16}}>{task.name}</div>
{task.timeStart&&<div style={{fontSize:13,color:"var(--cyan2)",marginTop:4}}>🕐 {task.timeStart}–{task.timeEnd||"?"} · {fmt(task.start)}</div>}
{task.desc&&<div style={{fontSize:13,color:"var(--text2)",marginTop:6}}>{task.desc}</div>}
</div>
<div className="fl" style={{marginBottom:16}}>
<label style={{color:"var(--green2)"}}>Результаты, решения, следующие шаги</label>
<textarea value={result} onChange={e=>setResult(e.target.value)} placeholder="Опишите итоги совещания, принятые решения, ответственных..." style={{minHeight:140}} autoFocus/>
</div>
<div style={{display:"flex",gap:10}}>
<button className="bo" onClick={onClose} style={{flex:1}}>Отмена</button>
<button className="bs" onClick={()=>{onSave(task.id,result);onClose()}} style={{flex:2}}>💾 Сохранить результаты</button>
</div>
</div></div></div>}

/* ─── Task/Meeting Detail side panel ─── */
function TDetail({task,onClose,onEdit,onDelete,onProg,onAddResult,now}){
const st=getS(task,now);const dl=task.deadline?diffD(task.deadline,now):null;
const[cd,setCd]=useState(false);const[cf,setCf]=useState(false);const[full,setFull]=useState(false);
const isM=task.type==="meeting";
const ms=isM?getMS(task,now):null;
const panelStyle=full?{position:"fixed",inset:0,width:"100%",background:"#fff",boxShadow:"none",zIndex:999,display:"flex",flexDirection:"column",animation:"fi .2s",borderLeft:"none"}:{};
return<><div style={{position:"fixed",inset:0,background:"rgba(0,0,0,.4)",zIndex:998}} onClick={onClose}/>
<div className={full?"":"dp"} style={full?panelStyle:{}}>
<div style={{padding:"20px 24px",borderBottom:"1px solid var(--border)",display:"flex",alignItems:"center",justifyContent:"space-between",background:isM?"var(--cyan-bg)":"var(--bg3)"}}>
<h3 style={{fontSize:15,fontWeight:700,display:"flex",alignItems:"center",gap:8}}>{isM?"🕐 Детали совещания":"📋 Детали задачи"}</h3>
<div style={{display:"flex",gap:6}}>
<button className="mc" onClick={()=>setFull(f=>!f)} title={full?"Свернуть":"На весь экран"}>{full?"⊡":"⛶"}</button>
<button className="mc" onClick={onClose}>×</button>
</div></div>
<div style={{padding:24,overflowY:"auto",flex:1,...(full?{maxWidth:800,margin:"0 auto",width:"100%"}:{})}}>
<div style={{display:"flex",gap:6,marginBottom:12,flexWrap:"wrap"}}>
{isM?<Bdg color="var(--cyan2)" bg="var(--cyan-bg)">Совещание</Bdg>:<Bdg color={gc(task.cat)} bg={gc(task.cat)+"20"}>{task.cat}</Bdg>}
<Bdg color={gp(task.pri)} bg={gb(task.pri)}>{task.pri}</Bdg>
{isM?<Bdg color={ms.c}>{ms.l}</Bdg>:<Bdg color={st.c}>{st.i} {st.l}</Bdg>}
</div>
<h2 style={{fontSize:20,fontWeight:800,lineHeight:1.3,marginBottom:8}}>{task.name}</h2>
{task.desc&&<p style={{color:"var(--text2)",fontSize:14,lineHeight:1.6,marginBottom:18}}>{task.desc}</p>}
<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16,marginBottom:20}}>
<div style={{background:"var(--bg)",borderRadius:12,padding:14}}><div style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginBottom:4}}>{isM?"Дата":"Начало"}</div><div style={{fontSize:15,fontWeight:600}}>{fmt(task.start)}</div></div>
<div style={{background:"var(--bg)",borderRadius:12,padding:14}}><div style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginBottom:4}}>{isM?"Окончание":"Дедлайн"}</div><div style={{fontSize:15,fontWeight:600,color:!isM&&dl!==null&&dl<0?"var(--red)":!isM&&dl!==null&&dl<=2?"var(--amber)":"var(--text)"}}>{fmt(task.deadline)}{!isM&&dl!==null&&dl<0?` (+${Math.abs(dl)}д)`:!isM&&dl!==null&&dl>=0?` (${dl}д)`:""}</div></div>
</div>
{isM&&(task.timeStart||task.timeEnd)&&<div style={{background:"var(--cyan-bg)",borderRadius:12,padding:14,marginBottom:20,border:"1px solid rgba(6,182,212,.2)"}}>
<div style={{fontSize:10,fontWeight:700,color:"var(--cyan2)",textTransform:"uppercase",marginBottom:6}}>🕐 Время совещания</div>
<div style={{display:"flex",gap:16}}>
<div><span style={{color:"var(--text3)",fontSize:12}}>Начало: </span><span style={{fontWeight:700,fontSize:16,color:"var(--cyan2)"}}>{task.timeStart||"\u2014"}</span></div>
<div><span style={{color:"var(--text3)",fontSize:12}}>Конец: </span><span style={{fontWeight:700,fontSize:16,color:"var(--cyan2)"}}>{task.timeEnd||"\u2014"}</span></div>
</div></div>}
<div style={{marginBottom:20}}>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:8}}>
<span style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase"}}>Прогресс</span>
<span style={{fontSize:20,fontWeight:800,color:isM?ms.c:st.c,fontFamily:"var(--mono)"}}>{task.progress}%</span>
</div>
<PBar value={task.progress} color={isM?ms.c:st.c} onChange={p=>onProg(task.id,p)} size={14}/>
</div>
{task.notes&&<div style={{marginBottom:18}}><div style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginBottom:6}}>Заметки</div><div style={{background:"var(--bg)",borderRadius:12,padding:14,fontSize:14,color:"var(--text2)",lineHeight:1.6,border:"1px solid var(--border)"}}>{task.notes}</div></div>}

{/* Meeting result section */}
{isM&&<div style={{marginBottom:18}}>
<div style={{fontSize:10,fontWeight:700,color:"var(--green2)",textTransform:"uppercase",marginBottom:6,display:"flex",alignItems:"center",gap:6}}>📝 Результаты совещания</div>
{task.result?<div style={{background:"linear-gradient(135deg,rgba(16,185,129,.06),rgba(6,182,212,.06))",borderRadius:12,padding:14,fontSize:14,color:"var(--text2)",lineHeight:1.6,border:"1px solid rgba(16,185,129,.2)",whiteSpace:"pre-wrap"}}>{task.result}</div>
:<div style={{background:"var(--bg)",borderRadius:12,padding:20,textAlign:"center",border:"1px dashed var(--border)"}}>
<div style={{fontSize:28,marginBottom:6}}>📝</div>
<div style={{fontSize:13,color:"var(--text3)",marginBottom:10}}>Результаты ещё не внесены</div>
<button className="bo" onClick={()=>onAddResult(task)} style={{fontSize:12}}>+ Добавить результаты</button>
</div>}
</div>}

{task.completedAt&&<div style={{marginBottom:18}}><div style={{fontSize:10,fontWeight:700,color:"var(--green2)",textTransform:"uppercase",marginBottom:6}}>✅ Завершено</div><div style={{fontSize:15,fontWeight:600,color:"var(--green)"}}>{fmt(task.completedAt)}</div></div>}
</div>
<div style={{padding:"16px 24px",borderTop:"1px solid var(--border)",display:"flex",gap:10,justifyContent:"flex-end",flexWrap:"wrap"}}>
<button className="bd" onClick={()=>setCd(true)}>🗑 Удалить</button>
{isM&&<button className="bo" onClick={()=>onAddResult(task)} style={{borderColor:"rgba(16,185,129,.3)",color:"var(--green2)",background:"var(--green-bg)"}}>📝 Результаты</button>}
<button className="bo" onClick={()=>onEdit(task)}>✏️ Редактировать</button>
{task.progress<100&&<button className="bs" onClick={()=>setCf(true)}>Завершить ✅</button>}
</div></div>
{cd&&<Confirm title="Удалить?" text={`«${task.name}» будет удалено.`} onNo={()=>setCd(false)} onYes={()=>{onDelete(task.id);onClose()}} yesLabel="Удалить" yesColor="var(--red)"/>}
{cf&&<Confirm title="Завершить?" text={`Отметить «${task.name}» как выполненное?`} onNo={()=>setCf(false)} onYes={()=>{onProg(task.id,100);setCf(false)}} yesLabel="Завершить" yesColor="var(--green)"/>}
</>}

/* ─── Settings ─── */
function Settings({data,onClose,onUpdate,showToast}){
const[nc,setNc]=useState("");const[np,setNp]=useState("");
const doAddCat=async()=>{if(!nc.trim())return;if(nc.trim()==="Совещание"){showToast("Имя «Совещание» зарезервировано","error");return}await callApi("add_category",nc.trim());setNc("");onUpdate()};
const doDelCat=async c=>{await callApi("delete_category",c);onUpdate()};
const doAddPri=async()=>{if(!np.trim())return;await callApi("add_priority",np.trim());setNp("");onUpdate()};
const doDelPri=async p=>{await callApi("delete_priority",p);onUpdate()};
return<div className="mo" onClick={onClose}><div className="md" onClick={e=>e.stopPropagation()}>
<div className="mh"><h3>⚙️ Настройки</h3><button className="mc" onClick={onClose}>×</button></div>
<div className="mb">
<div style={{marginBottom:24}}>
<div className="stitle"><span className="stitle-icon">🏷️</span> Категории задач</div>
<div style={{display:"flex",flexWrap:"wrap",gap:6,marginBottom:10}}>
{data.categories.map(c=><div key={c} className="chip"><span style={{width:8,height:8,borderRadius:4,background:gc(c)}}/>{c}<button onClick={()=>doDelCat(c)}>×</button></div>)}
</div>
<div style={{display:"flex",gap:8}}>
<input value={nc} onChange={e=>setNc(e.target.value)} placeholder="Новая категория..." style={{flex:1,padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:13,background:"var(--bg)",color:"var(--text)"}} onKeyDown={e=>{if(e.key==="Enter")doAddCat()}}/>
<button className="bo" onClick={doAddCat}>+</button>
</div>
<div style={{fontSize:11,color:"var(--text3)",marginTop:8}}>💡 Совещания — отдельная сущность, не категория</div>
</div>
<div>
<div className="stitle"><span className="stitle-icon">🎯</span> Приоритеты</div>
<div style={{display:"flex",flexWrap:"wrap",gap:6,marginBottom:10}}>
{data.priorities.map(p=><div key={p} className="chip"><span style={{width:8,height:8,borderRadius:4,background:gp(p)}}/>{p}<button onClick={()=>doDelPri(p)}>×</button></div>)}
</div>
<div style={{display:"flex",gap:8}}>
<input value={np} onChange={e=>setNp(e.target.value)} placeholder="Новый приоритет..." style={{flex:1,padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:13,background:"var(--bg)",color:"var(--text)"}} onKeyDown={e=>{if(e.key==="Enter")doAddPri()}}/>
<button className="bo" onClick={doAddPri}>+</button>
</div></div>
</div></div></div>}

/* ─── KPI Drill-down ─── */
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
const f=tasks.filter(filter);
return<div className="mo" onClick={onClose}><div className="md" onClick={e=>e.stopPropagation()} style={{width:"min(720px,94vw)",maxHeight:"85vh"}}>
<div className="mh" style={{borderTop:`4px solid ${colors[kpi]}`}}>
<h3>{icons[kpi]} {titles[kpi]} <span style={{fontWeight:500,fontSize:13,color:"var(--text3)",marginLeft:8}}>({f.length})</span></h3>
<button className="mc" onClick={onClose}>×</button>
</div>
<div className="mb" style={{padding:16}}>
{f.length===0?<div style={{textAlign:"center",padding:50,color:"var(--text4)"}}><div style={{fontSize:44,marginBottom:10}}>🎉</div><div style={{fontWeight:700,fontSize:15}}>Нет задач</div></div>:
<div style={{display:"flex",flexDirection:"column",gap:6}}>
{f.map(t=>{const st=getS(t,now);const dl=t.deadline?diffD(t.deadline,now):null;return<div key={t.id} className="tr" onClick={()=>{onClose();onOpenTask(t)}}>
<div className="task-left" style={{background:gp(t.pri)}}/>
<div style={{flex:1,minWidth:0}}>
<div style={{fontWeight:600,fontSize:14}}>{t.name}</div>
<div style={{display:"flex",gap:5,marginTop:5,flexWrap:"wrap",alignItems:"center"}}>
<Bdg color={gc(t.cat)}>{t.cat}</Bdg><Bdg color={gp(t.pri)} bg={gb(t.pri)}>{t.pri}</Bdg>
{t.deadline&&<span style={{fontSize:11,color:dl<0?"var(--red)":dl<=2?"var(--amber)":"var(--text3)"}}>📅 {fmt(t.deadline)}{dl!==null&&dl<0?` (+${Math.abs(dl)}д)`:""}</span>}
</div></div>
<div style={{textAlign:"right",flexShrink:0}}><Bdg color={st.c}>{st.i} {st.l}</Bdg><div style={{fontSize:13,fontWeight:700,color:st.c,fontFamily:"var(--mono)",marginTop:3}}>{t.progress}%</div></div>
</div>})}
</div>}
</div></div></div>
}

/* ─── Donut chart ─── */
function DonutChart({segments,size=140,thickness=24}){const r=size/2;const cr=r-thickness/2;const circ=2*Math.PI*cr;let offset=0;
return<svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
{segments.map((seg,i)=>{const dash=circ*seg.pct/100;const gap=circ-dash;const rot=-90+offset*360/100;offset+=seg.pct;
return<circle key={i} cx={r} cy={r} r={cr} fill="none" stroke={seg.color} strokeWidth={thickness} strokeDasharray={`${dash} ${gap}`} transform={`rotate(${rot} ${r} ${r})`} style={{transition:"all .5s ease"}}/>})}
<text x={r} y={r-6} textAnchor="middle" fill="var(--text)" fontFamily="var(--mono)" fontSize="22" fontWeight="800">{segments.reduce((a,s)=>a+s.value,0)}</text>
<text x={r} y={r+12} textAnchor="middle" fill="var(--text2)" fontFamily="var(--font)" fontSize="10" fontWeight="600">ВСЕГО</text>
</svg>}

/* ═══════════════ MAIN APP ═══════════════ */
function App(){
const[data,setData]=useState({categories:[],priorities:[],tasks:[],protectedCats:[]});
const[loading,setLoading]=useState(true);
const[tab,setTab]=useState("Панель");
const now=td();
const[showForm,setShowForm]=useState(false);
const[showMForm,setShowMForm]=useState(false);
const[editTask,setEditTask]=useState(null);
const[detailTask,setDetailTask]=useState(null);
const[showSettings,setShowSettings]=useState(false);
const[showResultModal,setShowResultModal]=useState(null);
const[filter,setFilter]=useState("active");
const[sortBy,setSortBy]=useState("deadline");
const[todaySort,setTodaySort]=useState("priority");
const[mtgSort,setMtgSort]=useState("date");
const[mtgFilter,setMtgFilter]=useState("upcoming");
const[schedDate,setSchedDate]=useState(now);
const[habMonth,setHabMonth]=useState(()=>{const d=new Date();return`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`});
const[toast,setToast]=useState(null);
const showToast=(msg,type)=>setToast({msg,type});
const[drillKpi,setDrillKpi]=useState(null);
const[panelPeriod,setPanelPeriod]=useState("all");
const[anPeriod,setAnPeriod]=useState("all");
const[anCat,setAnCat]=useState("");
const[anPri,setAnPri]=useState("");

/* Notifications state */
const[notifications,setNotifications]=useState([]);
const notifiedIdsRef=useRef({meetings:new Set(),overdue:new Set()});

const reload=useCallback(async()=>{const raw=await callApi("get_data");setData(JSON.parse(raw));setLoading(false)},[]);
useEffect(()=>{reload()},[reload]);

const addT=async t=>{await callApi("add_task",JSON.stringify(t));reload()};
const updT=async(id,patch)=>{await callApi("update_task",id,JSON.stringify(patch));reload()};
const delT=async id=>{await callApi("delete_task",id);setDetailTask(null);reload()};
const setProg=async(id,p)=>{const patch=p>=100?{progress:p,completedAt:td()}:{progress:p,completedAt:null};await callApi("update_task",id,JSON.stringify(patch));if(detailTask&&detailTask.id===id)setDetailTask(prev=>({...prev,...patch}));reload()};
const saveResult=async(id,result)=>{await callApi("update_task",id,JSON.stringify({result}));reload()};

/* ─── Notification checker (every 30 sec) ─── */
useEffect(()=>{
const checkNotifications=async()=>{
try{
const timeData=JSON.parse(await callApi("get_current_time"));
const currentDate=timeData.date;
const currentTime=timeData.time;
const currentMinutes=parseInt(currentTime.split(":")[0])*60+parseInt(currentTime.split(":")[1]);
const newNotifs=[];

/* Check meetings starting in 5 minutes */
data.tasks.filter(t=>t.type==="meeting"&&t.progress<100).forEach(m=>{
if(!m.timeStart||!m.start)return;
/* Only check meetings today */
if(m.start!==currentDate&&m.deadline!==currentDate)return;
if(m.start>currentDate)return;
if(m.deadline&&m.deadline<currentDate)return;

const[h,min]=m.timeStart.split(":").map(Number);
const meetingMinutes=h*60+min;
const diff=meetingMinutes-currentMinutes;
/* 0 to 5 minutes before start */
if(diff>=0&&diff<=5&&!notifiedIdsRef.current.meetings.has(m.id)){
notifiedIdsRef.current.meetings.add(m.id);
/* Mark in DB so we don't re-notify after restart */
callApi("update_task",m.id,JSON.stringify({notifiedMeeting:1}));
newNotifs.push({id:"m_"+m.id,type:"meeting",taskId:m.id,title:`🕐 Совещание через ${diff} мин!`,subtitle:`${m.name} · ${m.timeStart}–${m.timeEnd||"?"}`});
}
});

/* Check overdue tasks (one-time notification) */
data.tasks.filter(t=>t.type!=="meeting"&&t.progress<100&&t.name).forEach(t=>{
if(!t.deadline)return;
if(t.deadline>=currentDate)return;
/* Task is overdue */
if(!notifiedIdsRef.current.overdue.has(t.id)&&!t.notifiedOverdue){
notifiedIdsRef.current.overdue.add(t.id);
callApi("update_task",t.id,JSON.stringify({notifiedOverdue:1}));
newNotifs.push({id:"o_"+t.id,type:"overdue",taskId:t.id,title:"🔴 Задача просрочена!",subtitle:`${t.name} · дедлайн ${fmt(t.deadline)}`});
}
});

if(newNotifs.length){setNotifications(prev=>[...prev,...newNotifs])}
}catch(e){console.error("Notification check error:",e)}
};

/* Pre-fill already notified IDs from DB */
data.tasks.forEach(t=>{
if(t.notifiedMeeting)notifiedIdsRef.current.meetings.add(t.id);
if(t.notifiedOverdue)notifiedIdsRef.current.overdue.add(t.id);
});

checkNotifications();
const interval=setInterval(checkNotifications,30000);
return()=>clearInterval(interval);
},[data.tasks]);

const dismissNotif=id=>setNotifications(prev=>prev.filter(n=>n.id!==id));
const clickNotif=n=>{dismissNotif(n.id);const task=data.tasks.find(t=>t.id===n.taskId);if(task)setDetailTask(task)};

/* Split tasks into regular and meetings */
const tasksOnly=useMemo(()=>data.tasks.filter(t=>t.type!=="meeting"),[data.tasks]);
const meetings=useMemo(()=>data.tasks.filter(t=>t.type==="meeting"),[data.tasks]);

const[pFrom,pTo]=periodRange(panelPeriod);
const panelTasks=useMemo(()=>tasksOnly.filter(t=>inPeriod(t,pFrom,pTo)),[tasksOnly,pFrom,pTo]);

const stats=useMemo(()=>{const s={total:0,done:0,active:0,burn:0,over:0};panelTasks.forEach(t=>{if(!t.name)return;s.total++;const st=getS(t,now);if(st.l==="Выполнено")s.done++;else if(st.l==="В работе")s.active++;else if(st.l==="Горит"){s.burn++;s.active++}else if(st.l==="Просрочено")s.over++;else s.active++});s.pct=s.total?Math.round(s.done/s.total*100):0;return s},[panelTasks,now]);

const urgent=useMemo(()=>panelTasks.filter(t=>{const s=getS(t,now).l;return s==="Просрочено"||s==="Горит"}),[panelTasks,now]);

const filtered=useMemo(()=>{
let l=[...tasksOnly].filter(t=>t.name);
if(filter==="active")l=l.filter(t=>getS(t,now).l!=="Выполнено");
else if(filter==="completed")l=l.filter(t=>getS(t,now).l==="Выполнено");
if(sortBy==="deadline")l.sort((a,b)=>(a.deadline||"9999").localeCompare(b.deadline||"9999"));
else if(sortBy==="priority"){const o={};data.priorities.forEach((p,i)=>o[p]=i);l.sort((a,b)=>(o[a.pri]??99)-(o[b.pri]??99)||(a.deadline||"9999").localeCompare(b.deadline||"9999"))}
else if(sortBy==="category")l.sort((a,b)=>(a.cat||"").localeCompare(b.cat||"")||(a.deadline||"9999").localeCompare(b.deadline||"9999"));
else if(sortBy==="created")l.sort((a,b)=>(b.createdAt||"").localeCompare(a.createdAt||""));
else if(sortBy==="completed")l.sort((a,b)=>(b.completedAt||"").localeCompare(a.completedAt||""));
return l
},[tasksOnly,data.priorities,filter,sortBy,now]);

const todayL=useMemo(()=>{
let l=tasksOnly.filter(t=>{if(!t.name)return false;const st=getS(t,now);if(st.l==="Выполнено")return false;if(!t.start||t.start>now)return false;if(st.l==="Просрочено")return true;if(!t.deadline||t.deadline>=now)return true;return false});
if(todaySort==="priority"){const o={};data.priorities.forEach((p,i)=>o[p]=i);l.sort((a,b)=>(o[a.pri]??99)-(o[b.pri]??99))}
else if(todaySort==="deadline")l.sort((a,b)=>(a.deadline||"9999").localeCompare(b.deadline||"9999"));
else if(todaySort==="category")l.sort((a,b)=>(a.cat||"").localeCompare(b.cat||""));
else if(todaySort==="created")l.sort((a,b)=>(b.createdAt||"").localeCompare(a.createdAt||""));
return l
},[tasksOnly,data.priorities,todaySort,now]);

const todayMeetings=useMemo(()=>meetings.filter(m=>{if(!m.name)return false;if(m.progress>=100)return false;if(m.start===now||m.deadline===now||(m.start&&m.start<=now&&m.deadline&&m.deadline>=now))return true;return false}).sort((a,b)=>(a.timeStart||"99:99").localeCompare(b.timeStart||"99:99")),[meetings,now]);

const getMon=d=>{const dt=new Date(d);const dw=dt.getDay();const diff=dt.getDate()-dw+(dw===0?-6:1);return new Date(dt.setDate(diff)).toISOString().split("T")[0]};
const weekD=useMemo(()=>{const m=getMon(schedDate);return Array.from({length:7},(_,i)=>{const d=new Date(m);d.setDate(d.getDate()+i);return d.toISOString().split("T")[0]})},[schedDate]);

const getMeetingsForDay=useCallback(day=>meetings.filter(m=>{if(!m.name||m.progress>=100)return false;if(m.start&&m.start<=day&&m.deadline&&m.deadline>=day)return true;if(m.start===day||m.deadline===day)return true;return false}).sort((a,b)=>(a.timeStart||"99:99").localeCompare(b.timeStart||"99:99")),[meetings]);

const daysInM=useMemo(()=>{const[y,m]=habMonth.split("-").map(Number);return new Date(y,m,0).getDate()},[habMonth]);

const mtgList=useMemo(()=>{
let l=[...meetings].filter(m=>m.name);
if(mtgFilter==="upcoming")l=l.filter(m=>m.progress<100&&(!m.deadline||m.deadline>=now));
else if(mtgFilter==="past")l=l.filter(m=>m.progress>=100||(m.deadline&&m.deadline<now));
else if(mtgFilter==="today")l=l.filter(m=>m.start===now||m.deadline===now||(m.start&&m.start<=now&&m.deadline&&m.deadline>=now));
if(mtgSort==="date")l.sort((a,b)=>(a.start||"").localeCompare(b.start||"")||(a.timeStart||"").localeCompare(b.timeStart||""));
else if(mtgSort==="date-desc")l.sort((a,b)=>(b.start||"").localeCompare(a.start||"")||(b.timeStart||"").localeCompare(a.timeStart||""));
else if(mtgSort==="priority"){const o={};data.priorities.forEach((p,i)=>o[p]=i);l.sort((a,b)=>(o[a.pri]??99)-(o[b.pri]??99))}
else if(mtgSort==="created")l.sort((a,b)=>(b.createdAt||"").localeCompare(a.createdAt||""));
return l
},[meetings,mtgFilter,mtgSort,data.priorities,now]);

/* Export state */
const[expFrom,setExpFrom]=useState(()=>{const d=new Date();d.setMonth(d.getMonth()-1);return d.toISOString().split("T")[0]});
const[expTo,setExpTo]=useState(td());
const[expCats,setExpCats]=useState([]);const[expPris,setExpPris]=useState([]);const[expStat,setExpStat]=useState([]);
const[expPreview,setExpPreview]=useState(null);const[expGen,setExpGen]=useState(false);
const toggleA=(a,s,v)=>s(p=>p.includes(v)?p.filter(x=>x!==v):[...p,v]);
const statuses=["Выполнено","В работе","Горит","Просрочено","Новая"];

const expFiltered=useMemo(()=>tasksOnly.filter(t=>{
if(!t.name)return false;
if(t.start&&t.start>expTo)return false;
if(t.deadline&&t.deadline<expFrom&&getS(t,now).l!=="Просрочено")return false;
if(expCats.length&&!expCats.includes(t.cat))return false;
if(expPris.length&&!expPris.includes(t.pri))return false;
if(expStat.length&&!expStat.includes(getS(t,now).l))return false;
return true
}),[tasksOnly,expFrom,expTo,expCats,expPris,expStat,now]);

/* Export meetings filtered by period */
const expMeetings=useMemo(()=>meetings.filter(m=>{
if(!m.name)return false;
const dates=[m.start,m.deadline].filter(Boolean);
if(!dates.length)return true;
return dates.some(d=>d>=expFrom&&d<=expTo);
}),[meetings,expFrom,expTo]);

const expStats=useMemo(()=>{const s={total:expFiltered.length,done:0,active:0,overdue:0,burning:0};expFiltered.forEach(t=>{const st=getS(t,now);if(st.l==="Выполнено")s.done++;else if(st.l==="Просрочено")s.overdue++;else if(st.l==="Горит")s.burning++;else s.active++});s.pct=s.total?Math.round(s.done/s.total*100):0;s.avgProg=s.total?Math.round(expFiltered.reduce((a,t)=>a+(t.progress||0),0)/s.total):0;return s},[expFiltered,now]);

const genReport=()=>{setExpGen(true);setTimeout(()=>{
const catBr={};expFiltered.forEach(t=>{catBr[t.cat]=(catBr[t.cat]||0)+1});
const priBr={};expFiltered.forEach(t=>{priBr[t.pri]=(priBr[t.pri]||0)+1});
const done=expFiltered.filter(t=>getS(t,now).l==="Выполнено");
const overdue=expFiltered.filter(t=>getS(t,now).l==="Просрочено");
const burning=expFiltered.filter(t=>getS(t,now).l==="Горит");
const inprog=expFiltered.filter(t=>getS(t,now).l==="В работе");
const onTimeDone=done.filter(t=>!t.deadline||t.completedAt<=t.deadline).length;
const onTimeRate=done.length?Math.round(onTimeDone/done.length*100):null;
const latDone=done.filter(t=>t.deadline&&t.completedAt>t.deadline).length;
const avgTimeDays=(()=>{const ts=done.filter(t=>t.completedAt&&t.start);if(!ts.length)return null;return Math.round(ts.reduce((s,t)=>s+Math.max(0,diffD(t.completedAt,t.start)),0)/ts.length*10)/10})();
const avgProg=expStats.avgProg;
const statusList=[
{label:"Выполнено",count:done.length,color:"#10B981",icon:"✓"},
{label:"В работе",count:inprog.length,color:"#4361EE",icon:"⟳"},
{label:"Горит",count:burning.length,color:"#F59E0B",icon:"⚠"},
{label:"Просрочено",count:overdue.length,color:"#EF4444",icon:"✕"},
].filter(s=>s.count>0);
const esc=s=>String(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
const taskRow=(t,showDeadline=false)=>{const st=getS(t,now);const cc=st.c==='var(--green)'?'#10B981':st.c==='var(--red)'?'#EF4444':st.c==='var(--amber)'?'#F59E0B':'#4361EE';return`<tr><td><strong>${esc(t.name)}</strong>${t.desc?'<div style="color:#64748B;font-size:11px;margin-top:2px">'+esc(t.desc)+'</div>':''}</td><td><span class="bdg" style="color:${gc(t.cat)};background:${gc(t.cat)}15">${esc(t.cat)}</span></td><td><span class="bdg" style="color:${gp(t.pri)};background:${gp(t.pri)}15">${esc(t.pri)}</span></td>${showDeadline?`<td>${fmt(t.deadline)}</td>`:''}<td style="color:${cc};font-weight:600">${st.i} ${st.l}</td><td><div style="display:flex;align-items:center;gap:8px"><div style="flex:1;height:8px;background:#F0F4FA;border-radius:4px;overflow:hidden;min-width:60px"><div style="width:${t.progress}%;height:100%;background:${cc}"></div></div><span style="font-family:'IBM Plex Mono';font-weight:700;font-size:11px;min-width:32px;text-align:right">${t.progress}%</span></div></td>${t.completedAt?`<td style="color:#10B981;font-weight:600">${fmt(t.completedAt)}</td>`:''}</tr>`};

/* Meeting row for report */
const meetingRow=(m)=>{
const ms=getMS(m,now);
const msColor=ms.c==='var(--green)'?'#10B981':ms.c==='var(--cyan2)'?'#0891B2':ms.c==='var(--amber)'?'#F59E0B':'#64748B';
return`<tr>
<td><strong>${esc(m.name)}</strong>${m.desc?'<div style="color:#64748B;font-size:11px;margin-top:2px">'+esc(m.desc)+'</div>':''}</td>
<td>${fmt(m.start)}</td>
<td>${m.timeStart?m.timeStart+'–'+(m.timeEnd||'?'):'—'}</td>
<td><span class="bdg" style="color:${gp(m.pri)};background:${gp(m.pri)}15">${esc(m.pri)}</span></td>
<td style="color:${msColor};font-weight:600">${ms.l}</td>
<td>${m.result?'<div style="max-width:250px;font-size:11px;line-height:1.5;color:#1E293B">'+esc(m.result)+'</div>':'<span style="color:#CBD5E1;font-style:italic">Нет результатов</span>'}</td>
</tr>`};

/* Meeting stats for report */
const mtgTotal=expMeetings.length;
const mtgDone=expMeetings.filter(m=>m.progress>=100||m.completedAt).length;
const mtgWithResult=expMeetings.filter(m=>m.result&&m.result.trim()).length;
const mtgUpcoming=expMeetings.filter(m=>m.progress<100&&m.start&&m.start>now).length;
const mtgPast=expMeetings.filter(m=>(m.progress>=100)||(m.deadline&&m.deadline<now)).length;

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
.compl-box{margin-bottom:24px;padding:20px 24px;border-radius:14px;border-left:5px solid #4361EE;background:rgba(67,97,238,.08);display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap}
.compl-box .title{font-size:14px;font-weight:700;color:#475569;text-transform:uppercase;letter-spacing:1px}
.compl-box .sub{font-size:12px;color:#64748B;margin-top:4px}
.compl-box .big-pct{font-size:36px;font-weight:800;color:#4361EE;font-family:'IBM Plex Mono',monospace}
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
.narrative{margin-top:16px;padding:14px 16px;background:#fff;border-radius:10px;border:1px solid #E2E8F0;color:#475569;line-height:1.7;font-size:13px}
.section{margin-bottom:28px}
.section h2{font-size:16px;font-weight:700;margin-bottom:14px;padding-bottom:8px;border-bottom:2px solid #E2E8F0;color:#1E293B;display:flex;align-items:center;gap:8px}
.section h2 .count{font-size:12px;color:#94A3B8;font-weight:500;margin-left:auto;font-family:'IBM Plex Mono',monospace}
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
.footer .logo-footer{font-weight:700;color:#4361EE}
.mtg-header{position:relative;margin-bottom:24px;padding:22px;background:linear-gradient(135deg,#06B6D4 0%,#0891B2 100%);border-radius:14px;color:#fff}
.mtg-kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:20px}
.mtg-kpi{border:1.5px solid rgba(6,182,212,.3);border-radius:10px;padding:14px;text-align:center;background:rgba(6,182,212,.04)}
.mtg-kpi .num{font-size:22px;font-weight:800;font-family:'IBM Plex Mono',monospace;color:#0891B2}
.mtg-kpi .lbl{font-size:9px;font-weight:700;color:#64748B;text-transform:uppercase;margin-top:4px}
.result-box{margin-top:8px;padding:10px 14px;background:#F0FDF4;border:1px solid #BBF7D0;border-radius:8px;font-size:12px;line-height:1.6}
.result-label{font-size:10px;font-weight:700;color:#059669;text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px}
</style></head><body>

<div class="header"><div class="header-content">
<div><h1>⚡ Smart Planner</h1><div class="subtitle">Отчёт о выполнении задач</div></div>
<div class="period">
<div class="label">Отчётный период</div>
<div class="dates">${fmt(expFrom)} — ${fmt(expTo)}</div>
<div class="gen">Сформировано: ${fmt(now)}</div>
</div></div></div>

<div class="compl-box">
<div><div class="title">Коэффициент завершения задач</div><div class="sub">за отчётный период</div></div>
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
<div class="summary-item"><div class="sum-label">Коэффициент завершения</div><div class="sum-value">${expStats.pct}% (${done.length} из ${expStats.total})</div></div>
<div class="summary-item"><div class="sum-label">Средний прогресс</div><div class="sum-value">${avgProg}%</div></div>
<div class="summary-item"><div class="sum-label">Активных задач</div><div class="sum-value">${expStats.total-done.length}</div></div>
<div class="summary-item"><div class="sum-label">Задач в критической зоне</div><div class="sum-value">${burning.length+overdue.length} (горит ${burning.length} + просрочено ${overdue.length})</div></div>
<div class="summary-item"><div class="sum-label">Выполнено в срок</div><div class="sum-value">${onTimeRate!==null?onTimeRate+'% задач':'нет завершённых'}</div></div>
<div class="summary-item"><div class="sum-label">Средняя скорость выполнения</div><div class="sum-value">${avgTimeDays!==null?avgTimeDays+' дн. на задачу':'нет данных'}</div></div>
<div class="summary-item"><div class="sum-label">Сдано с опозданием</div><div class="sum-value">${latDone} задач</div></div>
</div>
<div class="narrative">
<strong>Ключевые факты:</strong> За отчётный период с ${fmt(expFrom)} по ${fmt(expTo)} было обработано <strong>${expStats.total}</strong> задач. Из них <strong>${done.length}</strong> успешно завершены (${expStats.pct}% от общего числа). ${onTimeRate!==null?'В срок выполнено <strong>'+onTimeRate+'%</strong> из завершённых задач. ':''}${avgTimeDays!==null?'Средняя продолжительность выполнения — <strong>'+avgTimeDays+'</strong> дн. ':''}${overdue.length>0?'Просроченных задач: <strong>'+overdue.length+'</strong>. ':''}${burning.length>0?'Горящих задач: <strong>'+burning.length+'</strong>. ':''}${overdue.length===0&&burning.length===0?'Критических задач не обнаружено — все сроки под контролем. ':''}
</div></div>

<div class="section no-break">
<h2>📈 Распределение по статусам <span class="count">${expStats.total} задач</span></h2>
<div class="status-row">
${statusList.map(s=>`<div class="status-pill" style="background:${s.color}0F;border-color:${s.color}40;color:${s.color}"><div class="sp-icon">${s.icon}</div><div><div class="sp-count">${s.count}</div><div class="sp-label">${s.label} · ${Math.round(s.count/expStats.total*100)}%</div></div></div>`).join('')}
</div></div>

${expStats.total>0?`<div class="section no-break">
<h2>🔀 Структура задач</h2>
<div class="bar-section">
<div class="bar-group"><div class="bar-group-title">🏷️ По категориям</div>
${Object.entries(catBr).sort((a,b)=>b[1]-a[1]).map(([c,n])=>`<div class="bar-item"><div class="bar-label-row"><span style="font-weight:600;color:${CC[c]||'#64748B'}">${esc(c)}</span><span style="font-family:IBM Plex Mono;font-weight:700">${n} · ${Math.round(n/expStats.total*100)}%</span></div><div class="bar-track"><div class="bar-inner" style="width:${(n/expStats.total)*100}%;background:${CC[c]||'#64748B'}"></div></div></div>`).join('')}
</div>
<div class="bar-group"><div class="bar-group-title">🎯 По приоритетам</div>
${Object.entries(priBr).sort((a,b)=>b[1]-a[1]).map(([p,n])=>`<div class="bar-item"><div class="bar-label-row"><span style="font-weight:600;color:${PC[p]||'#64748B'}">${esc(p)}</span><span style="font-family:IBM Plex Mono;font-weight:700">${n} · ${Math.round(n/expStats.total*100)}%</span></div><div class="bar-track"><div class="bar-inner" style="width:${(n/expStats.total)*100}%;background:${PC[p]||'#64748B'}"></div></div></div>`).join('')}
</div></div></div>`:''}

${overdue.length?`<div class="section page-break"><h2 style="color:#EF4444">⚠ Просроченные задачи <span class="count">${overdue.length}</span></h2>
<table><thead><tr><th>Задача</th><th>Категория</th><th>Приоритет</th><th>Дедлайн</th><th>Статус</th><th>Прогресс</th></tr></thead><tbody>${overdue.map(t=>taskRow(t,true)).join('')}</tbody></table></div>`:''}

${burning.length?`<div class="section"><h2 style="color:#F59E0B">🔥 Горящие задачи <span class="count">${burning.length}</span></h2>
<table><thead><tr><th>Задача</th><th>Категория</th><th>Приоритет</th><th>Дедлайн</th><th>Статус</th><th>Прогресс</th></tr></thead><tbody>${burning.map(t=>taskRow(t,true)).join('')}</tbody></table></div>`:''}

${inprog.length?`<div class="section"><h2 style="color:#4361EE">⟳ Задачи в работе <span class="count">${inprog.length}</span></h2>
<table><thead><tr><th>Задача</th><th>Категория</th><th>Приоритет</th><th>Дедлайн</th><th>Статус</th><th>Прогресс</th></tr></thead><tbody>${inprog.map(t=>taskRow(t,true)).join('')}</tbody></table></div>`:''}

${done.length?`<div class="section page-break"><h2 style="color:#10B981">✓ Выполненные задачи <span class="count">${done.length}</span></h2>
<table><thead><tr><th>Задача</th><th>Категория</th><th>Приоритет</th><th>Статус</th><th>Прогресс</th><th>Завершено</th></tr></thead><tbody>${done.map(t=>taskRow(t,false)).join('')}</tbody></table></div>`:''}

<!-- ═══ MEETINGS SECTION ═══ -->
<div class="page-break"></div>
<div class="mtg-header">
<div style="font-size:22px;font-weight:800;margin-bottom:4px">🕐 Совещания за период</div>
<div style="font-size:13px;opacity:.85">${fmt(expFrom)} — ${fmt(expTo)} · ${mtgTotal} совещаний</div>
</div>

<div class="mtg-kpis">
<div class="mtg-kpi"><div class="num">${mtgTotal}</div><div class="lbl">Всего</div></div>
<div class="mtg-kpi"><div class="num">${mtgDone}</div><div class="lbl">Проведено</div></div>
<div class="mtg-kpi"><div class="num">${mtgWithResult}</div><div class="lbl">С результатами</div></div>
<div class="mtg-kpi"><div class="num">${mtgUpcoming}</div><div class="lbl">Предстоящие</div></div>
</div>

${mtgTotal>0?`<div class="section">
<h2 style="color:#0891B2">📋 Детальная информация по совещаниям <span class="count">${mtgTotal}</span></h2>
<table>
<thead><tr><th>Совещание</th><th>Дата</th><th>Время</th><th>Приоритет</th><th>Статус</th><th>Результаты</th></tr></thead>
<tbody>${expMeetings.sort((a,b)=>(a.start||'').localeCompare(b.start||'')).map(m=>meetingRow(m)).join('')}</tbody>
</table>
</div>

${(()=>{const withRes=expMeetings.filter(m=>m.result&&m.result.trim());
if(!withRes.length)return'';
return'<div class="section page-break"><h2 style="color:#059669">📝 Результаты совещаний <span class="count">'+withRes.length+'</span></h2>'+
withRes.map(m=>'<div style="margin-bottom:16px;border:1px solid #E2E8F0;border-radius:12px;overflow:hidden" class="no-break">'+
'<div style="padding:14px 16px;background:#F8FAFD;border-bottom:1px solid #E2E8F0;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px">'+
'<div><strong style="font-size:14px">'+esc(m.name)+'</strong>'+
(m.desc?'<div style="color:#64748B;font-size:11px;margin-top:2px">'+esc(m.desc)+'</div>':'')+
'</div>'+
'<div style="display:flex;gap:8px;align-items:center;flex-shrink:0">'+
'<span style="font-size:11px;color:#0891B2;font-weight:600">'+fmt(m.start)+(m.timeStart?' · '+m.timeStart+'–'+(m.timeEnd||'?'):'')+'</span>'+
'<span class="bdg" style="color:'+gp(m.pri)+';background:'+gp(m.pri)+'15">'+esc(m.pri)+'</span>'+
'</div></div>'+
'<div class="result-box"><div class="result-label">📝 Результаты / решения</div>'+
'<div style="white-space:pre-wrap">'+esc(m.result)+'</div></div>'+
'</div>').join('')+'</div>'})()}

${(()=>{const noRes=expMeetings.filter(m=>!m.result||!m.result.trim());
if(!noRes.length)return'';
return'<div class="section"><h2 style="color:#94A3B8">⏳ Совещания без результатов <span class="count">'+noRes.length+'</span></h2>'+
'<table><thead><tr><th>Совещание</th><th>Дата</th><th>Время</th><th>Приоритет</th><th>Статус</th></tr></thead><tbody>'+
noRes.map(m=>{const ms2=getMS(m,now);const msC=ms2.c==="var(--green)"?"#10B981":ms2.c==="var(--cyan2)"?"#0891B2":ms2.c==="var(--amber)"?"#F59E0B":"#64748B";
return'<tr><td><strong>'+esc(m.name)+'</strong>'+(m.desc?'<div style="color:#64748B;font-size:11px;margin-top:2px">'+esc(m.desc)+'</div>':'')+'</td>'+
'<td>'+fmt(m.start)+'</td>'+
'<td>'+(m.timeStart?m.timeStart+'–'+(m.timeEnd||'?'):'—')+'</td>'+
'<td><span class="bdg" style="color:'+gp(m.pri)+';background:'+gp(m.pri)+'15">'+esc(m.pri)+'</span></td>'+
'<td style="color:'+msC+';font-weight:600">'+ms2.l+'</td></tr>'}).join('')+
'</tbody></table></div>'})()}`:''}

<div class="footer"><div class="logo-footer">⚡ Smart Planner</div><div>Автоматический отчёт · ${fmt(now)}</div></div>
</body></html>`;
setExpPreview(html);setExpGen(false)},200)};

const printReport=async()=>{if(!expPreview)return;await callApi("save_pdf_report",expPreview)};

if(loading)return<div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100vh",fontSize:18,color:"var(--text3)"}}>Загрузка...</div>;

const renderAddBtn=()=>{
if(tab==="Совещания")return<button className="add-b add-m" onClick={()=>{setEditTask(null);setShowMForm(true)}}><span>+</span> Совещание</button>;
return<button className="add-b" onClick={()=>{setEditTask(null);setShowForm(true)}}><span>+</span> Задача</button>;
};

return<div>
{/* Notification banner */}
<NotifBanner notifications={notifications} onDismiss={dismissNotif} onClickNotif={clickNotif}/>

<div className="hdr"><div className="hdr-brand"><div className="hdr-logo">⚡</div><div><h1>Smart Planner</h1><small>{fmt(now)}</small></div></div>
<div className="tabs">{TABS.map(t=><button key={t} className={`tab ${tab===t?"on":""}`} onClick={()=>setTab(t)}><span className="tab-icon">{TAB_ICONS[t]}</span>{t}</button>)}</div>
<div style={{display:"flex",gap:8}}>{renderAddBtn()}<button className="set-b" onClick={()=>setShowSettings(true)} title="Настройки">⚙</button></div></div>

<div className="main">

{/* ═════ ПАНЕЛЬ ═════ */}
{tab==="Панель"&&<>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:20,flexWrap:"wrap",gap:12}}>
<div><div style={{fontSize:22,fontWeight:800}}>📊 Панель</div><div style={{color:"var(--text3)",fontSize:13,marginTop:2}}>Общая картина по задачам {panelPeriod!=="all"?`· ${panelTasks.length} в выборке`:""}</div></div>
<div className="seg">
{[["all","Всё время"],["today","Сегодня"],["week","Неделя"],["month","Месяц"],["quarter","Квартал"],["year","Год"]].map(([k,l])=><button key={k} className={panelPeriod===k?"on":""} onClick={()=>setPanelPeriod(k)}>{l}</button>)}
</div></div>

<div className="kpi-r">
<KPI label="Всего" value={stats.total} sub="задач · клик для списка" color="var(--accent)" onClick={()=>setDrillKpi("total")}/>
<KPI label="Выполнено" value={stats.done} sub={`${stats.pct}% · клик для списка`} color="var(--green)" onClick={()=>setDrillKpi("done")}/>
<KPI label="В работе" value={stats.active} sub="активных · клик" color="var(--accent)" onClick={()=>setDrillKpi("active")}/>
<KPI label="Горит" value={stats.burn} sub="≤ 2 дня · клик" color="var(--amber)" onClick={()=>setDrillKpi("burn")}/>
<KPI label="Просрочено" value={stats.over} sub="срок вышел · клик" color="var(--red)" onClick={()=>setDrillKpi("over")}/>
</div>
<div className="card card-glow" style={{marginBottom:22}}><div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:10}}><span className="stitle" style={{margin:0}}>🚀 Общий прогресс</span><span style={{fontWeight:800,fontSize:22,color:"var(--accent)",fontFamily:"var(--mono)"}}>{stats.pct}%</span></div><PBar value={stats.pct} size={12} color="var(--accent)"/></div>
<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16,marginBottom:22}} className="two-col">
<div className="card"><div className="stitle"><span className="stitle-icon">🎯</span> По приоритетам</div>{data.priorities.map(p=>{const c=panelTasks.filter(t=>t.name&&t.pri===p).length;return<div key={p} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"7px 0",borderBottom:"1px solid var(--border)"}}><Bdg color={gp(p)} bg={gb(p)}>{p}</Bdg><span style={{fontWeight:800,fontSize:18,color:gp(p),fontFamily:"var(--mono)"}}>{c}</span></div>})}</div>
<div className="card"><div className="stitle"><span className="stitle-icon">🏷️</span> По категориям</div>{data.categories.map(c=>{const n=panelTasks.filter(t=>t.name&&t.cat===c).length;if(!n)return null;return<div key={c} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"7px 0",borderBottom:"1px solid var(--border)"}}><Bdg color={gc(c)}>{c}</Bdg><span style={{fontWeight:800,fontSize:18,color:gc(c),fontFamily:"var(--mono)"}}>{n}</span></div>})}</div>
</div>
{urgent.length>0&&<div className="card" style={{borderLeft:"3px solid var(--red)"}}><div className="stitle" style={{color:"var(--red)"}}>🔥 Требуют внимания</div>{urgent.map(t=>{const st=getS(t,now);return<div key={t.id} style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"10px 0",borderBottom:"1px solid var(--border)",cursor:"pointer"}} onClick={()=>setDetailTask(t)}><div><div style={{fontWeight:600}}>{t.name}</div><div style={{fontSize:12,color:"var(--text3)"}}>{t.cat} · {fmt(t.deadline)}</div></div><Bdg color={st.c}>{st.i} {st.l}</Bdg></div>})}</div>}
</>}

{/* ═════ ЗАДАЧИ ═════ */}
{tab==="Задачи"&&<>
<div className="filter-bar">
<div className="seg">{[["active","Активные"],["all","Все"],["completed","Готовые"]].map(([k,l])=><button key={k} className={filter===k?"on":""} onClick={()=>setFilter(k)}>{l}</button>)}</div>
<select value={sortBy} onChange={e=>setSortBy(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:12,background:"var(--bg3)",color:"var(--text)"}}>
<option value="deadline">По дедлайну</option>
<option value="priority">По приоритету</option>
<option value="category">По категории</option>
<option value="created">По дате создания</option>
{(filter==="all"||filter==="completed")&&<option value="completed">По дате завершения</option>}
</select>
<span style={{fontSize:12,color:"var(--text4)",marginLeft:"auto"}}>{filtered.length} задач</span>
</div>
<div style={{display:"flex",flexDirection:"column",gap:6}}>{filtered.map(t=>{const st=getS(t,now);const dl=t.deadline?diffD(t.deadline,now):null;
return<div key={t.id} className={`tr ${st.l==="Выполнено"?"done":""}`} onClick={()=>setDetailTask(t)}>
<div className="task-left" style={{background:gp(t.pri)}}/>
<div style={{flex:1,minWidth:0}}>
<div style={{fontWeight:600,fontSize:14,textDecoration:st.l==="Выполнено"?"line-through":"none",color:st.l==="Выполнено"?"var(--text3)":"var(--text)"}}>{t.name}</div>
<div style={{display:"flex",gap:5,marginTop:5,flexWrap:"wrap",alignItems:"center"}}>
<Bdg color={gc(t.cat)}>{t.cat}</Bdg><Bdg color={gp(t.pri)} bg={gb(t.pri)}>{t.pri}</Bdg>
{t.deadline&&<span style={{fontSize:11,color:dl<0?"var(--red)":dl<=2?"var(--amber)":"var(--text3)"}}>📅 {fmt(t.deadline)}{dl!==null&&dl<0?` (+${Math.abs(dl)}д)`:""}</span>}
{t.completedAt&&<span style={{fontSize:11,color:"var(--green)"}}>✓ {fmt(t.completedAt)}</span>}
</div>
<div style={{marginTop:6}} onClick={e=>e.stopPropagation()}><PBar value={t.progress} color={st.c} onChange={p=>setProg(t.id,p)}/></div>
</div>
<div style={{textAlign:"right",flexShrink:0}}><Bdg color={st.c}>{st.i} {st.l}</Bdg><div style={{fontSize:14,fontWeight:700,color:st.c,fontFamily:"var(--mono)",marginTop:4}}>{t.progress}%</div></div>
</div>})}
{filtered.length===0&&<div style={{textAlign:"center",padding:60,color:"var(--text4)"}}><div style={{fontSize:44,marginBottom:10}}>📋</div><div style={{fontWeight:700,fontSize:16}}>Нет задач</div></div>}
</div></>}

{/* ═════ СОВЕЩАНИЯ ═════ */}
{tab==="Совещания"&&<>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:20,flexWrap:"wrap",gap:12}}>
<div><div style={{fontSize:22,fontWeight:800,color:"var(--cyan2)"}}>🕐 Совещания</div><div style={{color:"var(--text3)",fontSize:13,marginTop:2}}>Отдельный модуль для планирования встреч</div></div>
</div>

<div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:12,marginBottom:24}}>
<div className="kpi"><div className="kpi-glow" style={{background:"var(--cyan)"}}/><div className="kpi-l">Всего</div><div className="kpi-v" style={{color:"var(--cyan2)"}}>{meetings.length}</div><div className="kpi-s">совещаний</div></div>
<div className="kpi"><div className="kpi-glow" style={{background:"var(--amber)"}}/><div className="kpi-l">Сегодня</div><div className="kpi-v" style={{color:"var(--amber)"}}>{todayMeetings.length}</div><div className="kpi-s">запланированы</div></div>
<div className="kpi"><div className="kpi-glow" style={{background:"var(--accent)"}}/><div className="kpi-l">Предстоящие</div><div className="kpi-v" style={{color:"var(--accent)"}}>{meetings.filter(m=>m.progress<100&&m.start&&m.start>now).length}</div><div className="kpi-s">впереди</div></div>
<div className="kpi"><div className="kpi-glow" style={{background:"var(--green)"}}/><div className="kpi-l">Проведено</div><div className="kpi-v" style={{color:"var(--green)"}}>{meetings.filter(m=>m.progress>=100).length}</div><div className="kpi-s">завершены</div></div>
</div>

<div style={{marginBottom:20}}>
<div className="stitle" style={{marginBottom:12}}><span className="stitle-icon">📅</span> Недельный календарь совещаний</div>
<div style={{display:"flex",alignItems:"center",gap:8,marginBottom:12,flexWrap:"wrap"}}>
<button className="bo" style={{padding:"6px 12px"}} onClick={()=>{const d=new Date(schedDate);d.setDate(d.getDate()-7);setSchedDate(d.toISOString().split("T")[0])}}>←</button>
<input type="date" value={schedDate} onChange={e=>setSchedDate(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:13,fontWeight:600,background:"var(--bg3)",color:"var(--text)"}}/>
<button className="bo" style={{padding:"6px 12px"}} onClick={()=>{const d=new Date(schedDate);d.setDate(d.getDate()+7);setSchedDate(d.toISOString().split("T")[0])}}>→</button>
<button className="bo" onClick={()=>setSchedDate(td())} style={{fontSize:12}}>Сегодня</button>
</div>
<div className="sw"><div className="sg" style={{gridTemplateColumns:`60px repeat(7,minmax(100px,1fr))`}}>
<div className="sh" style={{fontSize:9}}>Время</div>
{weekD.map((d,i)=><div key={d} className={`sh ${d===now?"td":""}`}><div>{dayN[i]}</div><div style={{fontSize:10,opacity:.7,fontWeight:400}}>{fmtS(d)}</div></div>)}
{hours.map(h=><React.Fragment key={h}><div className="st">{h}</div>
{weekD.map(d=>{const mt=getMeetingsForDay(d);const hN=parseInt(h);const match=mt.filter(m=>m.timeStart&&parseInt(m.timeStart.split(":")[0])===hN);
return<div key={d} className={`sc ${d===now?"td":""}`}>{match.map(m=><span key={m.id} className="sch" style={{background:"var(--cyan-bg)",color:"var(--cyan2)",padding:"4px 6px",fontSize:10}} onClick={()=>setDetailTask(m)}>{m.timeStart&&<span style={{fontWeight:700}}>{m.timeStart} </span>}{m.name}</span>)}</div>})}</React.Fragment>)}
</div></div></div>

<div className="filter-bar">
<div className="seg seg-cyan">{[["upcoming","Предстоящие"],["today","Сегодня"],["past","Прошедшие"],["all","Все"]].map(([k,l])=><button key={k} className={mtgFilter===k?"on":""} onClick={()=>setMtgFilter(k)}>{l}</button>)}</div>
<select value={mtgSort} onChange={e=>setMtgSort(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:12,background:"var(--bg3)"}}>
<option value="date">По дате ↑</option>
<option value="date-desc">По дате ↓</option>
<option value="priority">По приоритету</option>
<option value="created">По дате создания</option>
</select>
<span style={{fontSize:12,color:"var(--text4)",marginLeft:"auto"}}>{mtgList.length} совещаний</span>
</div>
<div style={{display:"flex",flexDirection:"column",gap:6}}>
{mtgList.map(m=>{const ms=getMS(m,now);return<div key={m.id} className="tr" onClick={()=>setDetailTask(m)} style={{borderLeft:"3px solid var(--cyan2)"}}>
<div style={{flex:1,minWidth:0}}>
<div style={{fontWeight:600,fontSize:14,textDecoration:m.progress>=100?"line-through":"none",color:m.progress>=100?"var(--text3)":"var(--text)"}}>{m.name}</div>
<div style={{display:"flex",gap:5,marginTop:5,flexWrap:"wrap",alignItems:"center"}}>
<Bdg color="var(--cyan2)" bg="var(--cyan-bg)">Совещание</Bdg>
<Bdg color={gp(m.pri)} bg={gb(m.pri)}>{m.pri}</Bdg>
{m.timeStart&&<span className="meeting-time">🕐 {m.timeStart}–{m.timeEnd||"?"}</span>}
{m.start&&<span style={{fontSize:11,color:"var(--text3)"}}>📅 {fmt(m.start)}</span>}
{m.result&&<span style={{fontSize:11,color:"var(--green2)",fontWeight:600}}>📝 Есть результаты</span>}
</div></div>
<div style={{textAlign:"right",flexShrink:0,display:"flex",flexDirection:"column",alignItems:"flex-end",gap:4}}>
<Bdg color={ms.c}>{ms.l}</Bdg>
<div style={{fontSize:14,fontWeight:700,color:ms.c,fontFamily:"var(--mono)"}}>{m.progress}%</div>
{(m.progress>=100||(m.deadline&&m.deadline<now))&&!m.result&&<button className="bo" style={{fontSize:10,padding:"3px 8px",borderColor:"rgba(16,185,129,.3)",color:"var(--green2)"}} onClick={e=>{e.stopPropagation();setShowResultModal(m)}}>+ Результат</button>}
</div>
</div>})}
{mtgList.length===0&&<div style={{textAlign:"center",padding:60,color:"var(--text4)"}}><div style={{fontSize:44,marginBottom:10}}>🕐</div><div style={{fontWeight:700,fontSize:16}}>Нет совещаний</div><div style={{fontSize:13,marginTop:4}}>Создайте первое — кнопка «+ Совещание» вверху</div></div>}
</div>
</>}

{/* ═════ СЕГОДНЯ ═════ */}
{tab==="Сегодня"&&<>
<div style={{marginBottom:16,display:"flex",justifyContent:"space-between",alignItems:"center",flexWrap:"wrap",gap:10}}>
<div><div style={{fontWeight:800,fontSize:22,color:"var(--accent)"}}>{fmt(now)}</div><div style={{color:"var(--text3)",fontSize:13,marginTop:2}}>{todayL.length} задач · {todayMeetings.length} совещаний</div></div>
<select value={todaySort} onChange={e=>setTodaySort(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:12,background:"var(--bg3)"}}>
<option value="priority">По приоритету</option>
<option value="deadline">По дедлайну</option>
<option value="category">По категории</option>
<option value="created">По дате создания</option>
</select>
</div>

{todayMeetings.length>0&&<div style={{marginBottom:20}}>
<div className="stitle" style={{color:"var(--cyan2)"}}><span className="stitle-icon">🕐</span> Совещания на сегодня</div>
{todayMeetings.map(m=><div key={m.id} className="card" style={{marginBottom:8,borderLeft:"3px solid var(--cyan2)",cursor:"pointer"}} onClick={()=>setDetailTask(m)}>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",gap:12,flexWrap:"wrap"}}>
<div style={{flex:1}}><div style={{fontWeight:700,fontSize:15}}>{m.name}</div>{m.desc&&<div style={{fontSize:13,color:"var(--text2)",marginTop:3}}>{m.desc}</div>}
<div style={{display:"flex",gap:6,marginTop:8,flexWrap:"wrap",alignItems:"center"}}><Bdg color="var(--cyan2)" bg="var(--cyan-bg)">Совещание</Bdg><Bdg color={gp(m.pri)} bg={gb(m.pri)}>{m.pri}</Bdg>{m.timeStart&&<span className="meeting-time">🕐 {m.timeStart}–{m.timeEnd||"?"}</span>}</div></div>
</div></div>)}
</div>}

{todayL.length>0&&<div className="stitle"><span className="stitle-icon">📋</span> Задачи на сегодня</div>}
{todayL.map(t=>{const st=getS(t,now);return<div key={t.id} className="card" style={{marginBottom:8,borderLeft:`3px solid ${gp(t.pri)}`,cursor:"pointer"}} onClick={()=>setDetailTask(t)}>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"flex-start",gap:12,flexWrap:"wrap"}}>
<div style={{flex:1}}><div style={{fontWeight:700,fontSize:16}}>{t.name}</div>{t.desc&&<div style={{fontSize:13,color:"var(--text2)",marginTop:3}}>{t.desc}</div>}
<div style={{display:"flex",gap:6,marginTop:8,flexWrap:"wrap",alignItems:"center"}}><Bdg color={gc(t.cat)}>{t.cat}</Bdg><Bdg color={st.c}>{st.i} {st.l}</Bdg></div></div>
<div style={{fontSize:20,fontWeight:800,color:st.c,fontFamily:"var(--mono)"}}>{t.progress}%</div></div>
<div style={{marginTop:12}} onClick={e=>e.stopPropagation()}><PBar value={t.progress} color={st.c} onChange={p=>setProg(t.id,p)} size={10}/></div>
</div>})}
{todayL.length===0&&todayMeetings.length===0&&<div style={{textAlign:"center",padding:60,color:"var(--text4)"}}><div style={{fontSize:52,marginBottom:12}}>🎉</div><div style={{fontSize:18,fontWeight:700}}>Всё чисто!</div></div>}
</>}

{/* ═════ ЖУРНАЛ ═════ */}
{tab==="Журнал"&&<>
<div style={{display:"flex",alignItems:"center",gap:8,marginBottom:16,flexWrap:"wrap"}}>
<button className="bo" style={{padding:"6px 12px"}} onClick={()=>{const[y,m]=habMonth.split("-").map(Number);const d=new Date(y,m-2,1);setHabMonth(`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`)}}>←</button>
<input type="month" value={habMonth} onChange={e=>setHabMonth(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:13,fontWeight:600,background:"var(--bg3)"}}/>
<button className="bo" style={{padding:"6px 12px"}} onClick={()=>{const[y,m]=habMonth.split("-").map(Number);const d=new Date(y,m,1);setHabMonth(`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,"0")}`)}}>→</button>
<span style={{fontWeight:700,fontSize:16}}>{monthN[parseInt(habMonth.split("-")[1])]} {habMonth.split("-")[0]}</span>
<span style={{fontSize:12,color:"var(--text4)",marginLeft:8}}>{tasksOnly.filter(t=>t.completedAt&&t.completedAt.startsWith(habMonth)).length} завершённых</span>
</div>
<div className="card" style={{padding:0,overflow:"auto"}}><table className="ht"><thead><tr><th>Задача</th><th style={{minWidth:70}}>Категория</th>
{Array.from({length:daysInM},(_,i)=>{const dk=`${habMonth}-${String(i+1).padStart(2,"0")}`;return<th key={i} className={dk===now?"today-th":""} style={{minWidth:30}}>{i+1}</th>})}</tr></thead>
<tbody>{(()=>{const completed=tasksOnly.filter(t=>t.completedAt&&t.completedAt.startsWith(habMonth));
if(!completed.length)return<tr><td colSpan={daysInM+2} style={{textAlign:"center",padding:50,color:"var(--text4)"}}>📓 Нет завершённых задач</td></tr>;
return completed.map((t,i)=><tr key={t.id||i} style={{background:i%2===0?"#FFFFFF":"var(--bg)",cursor:"pointer"}} onClick={()=>setDetailTask(t)}>
<td><div style={{fontWeight:600,fontSize:12}}>{t.name}</div></td><td style={{textAlign:"center"}}><Bdg color={gc(t.cat)}>{t.cat}</Bdg></td>
{Array.from({length:daysInM},(_,di)=>{const dk=`${habMonth}-${String(di+1).padStart(2,"0")}`;return<td key={di} style={{textAlign:"center",padding:2}}>{t.completedAt===dk&&<span style={{display:"inline-flex",width:28,height:28,borderRadius:8,background:"var(--gradient2)",color:"#fff",alignItems:"center",justifyContent:"center",fontSize:14,fontWeight:700}}>✓</span>}</td>})}
</tr>)})()}</tbody></table></div>
</>}

Продолжаю с `{/* ═════ АНАЛИТИКА ═════ */}`:

```python
{/* ═════ АНАЛИТИКА ═════ */}
{tab==="Аналитика"&&(()=>{
const anFiltered=tasksOnly.filter(t=>{
if(!t.name)return false;
if(anCat&&t.cat!==anCat)return false;
if(anPri&&t.pri!==anPri)return false;
const[f,to]=periodRange(anPeriod);
return inPeriod(t,f,to);
});
const anStats={total:0,done:0,active:0,burn:0,over:0,newT:0};
anFiltered.forEach(t=>{anStats.total++;const st=getS(t,now).l;
if(st==="Выполнено")anStats.done++;
else if(st==="В работе")anStats.active++;
else if(st==="Горит")anStats.burn++;
else if(st==="Просрочено")anStats.over++;
else anStats.newT++});
anStats.pct=anStats.total?Math.round(anStats.done/anStats.total*100):0;
anStats.avgProg=anStats.total?Math.round(anFiltered.reduce((s,t)=>s+(t.progress||0),0)/anStats.total):0;

const catData={};anFiltered.forEach(t=>{catData[t.cat]=(catData[t.cat]||0)+1});
const priData={};anFiltered.forEach(t=>{priData[t.pri]=(priData[t.pri]||0)+1});
const statusData=[
{label:"Выполнено",value:anStats.done,color:"#10B981"},
{label:"В работе",value:anStats.active,color:"#4361EE"},
{label:"Горит",value:anStats.burn,color:"#F59E0B"},
{label:"Просрочено",value:anStats.over,color:"#EF4444"},
{label:"Новые",value:anStats.newT,color:"#94A3B8"},
].filter(s=>s.value>0);
const statusSegs=statusData.map(s=>({...s,pct:anStats.total?s.value/anStats.total*100:0}));

/* Weekly completion trend (last 8 weeks) */
const weekTrend=useMemo(()=>{
const weeks=[];const d=new Date();
for(let i=7;i>=0;i--){
const wEnd=new Date(d);wEnd.setDate(wEnd.getDate()-i*7);
const wStart=new Date(wEnd);wStart.setDate(wStart.getDate()-6);
const ws=wStart.toISOString().split("T")[0];
const we=wEnd.toISOString().split("T")[0];
const count=anFiltered.filter(t=>t.completedAt&&t.completedAt>=ws&&t.completedAt<=we).length;
weeks.push({label:`${fmtS(ws)}`,value:count});
}return weeks},[anFiltered]);
const maxWeek=Math.max(...weekTrend.map(w=>w.value),1);

/* Category completion rates */
const catCompl=useMemo(()=>{
const res={};
data.categories.forEach(c=>{
const all=anFiltered.filter(t=>t.cat===c);
const done=all.filter(t=>getS(t,now).l==="Выполнено");
if(all.length)res[c]={total:all.length,done:done.length,pct:Math.round(done.length/all.length*100)};
});return res},[anFiltered,data.categories,now]);

/* Priority completion rates */
const priCompl=useMemo(()=>{
const res={};
data.priorities.forEach(p=>{
const all=anFiltered.filter(t=>t.pri===p);
const done=all.filter(t=>getS(t,now).l==="Выполнено");
if(all.length)res[p]={total:all.length,done:done.length,pct:Math.round(done.length/all.length*100)};
});return res},[anFiltered,data.priorities,now]);

/* On-time rate */
const doneFiltered=anFiltered.filter(t=>getS(t,now).l==="Выполнено");
const onTime=doneFiltered.filter(t=>!t.deadline||t.completedAt<=t.deadline).length;
const onTimeRate=doneFiltered.length?Math.round(onTime/doneFiltered.length*100):null;

/* Avg completion time */
const avgTime=(()=>{const ts=doneFiltered.filter(t=>t.completedAt&&t.start);if(!ts.length)return null;return Math.round(ts.reduce((s,t)=>s+Math.max(0,diffD(t.completedAt,t.start)),0)/ts.length*10)/10})();

/* Daily heatmap for current month */
const heatData=useMemo(()=>{
const m=new Date().getMonth();const y=new Date().getFullYear();
const dIM=new Date(y,m+1,0).getDate();
const res=[];
for(let i=1;i<=dIM;i++){
const dk=`${y}-${String(m+1).padStart(2,"0")}-${String(i).padStart(2,"0")}`;
const count=anFiltered.filter(t=>t.completedAt===dk).length;
res.push({day:i,date:dk,count});
}return res},[anFiltered]);
const maxHeat=Math.max(...heatData.map(h=>h.count),1);

/* Meeting stats for analytics */
const anMeetings=meetings.filter(m=>m.name);
const mtgDoneCount=anMeetings.filter(m=>m.progress>=100).length;
const mtgWithResult=anMeetings.filter(m=>m.result&&m.result.trim()).length;

return<>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:20,flexWrap:"wrap",gap:12}}>
<div><div style={{fontSize:22,fontWeight:800}}>📈 Аналитика</div><div style={{color:"var(--text3)",fontSize:13,marginTop:2}}>Детальный анализ выполнения · {anFiltered.length} задач в выборке</div></div>
</div>

<div className="filter-bar" style={{marginBottom:20}}>
<div className="seg">
{[["all","Всё время"],["week","Неделя"],["month","Месяц"],["quarter","Квартал"],["year","Год"]].map(([k,l])=><button key={k} className={anPeriod===k?"on":""} onClick={()=>setAnPeriod(k)}>{l}</button>)}
</div>
<select value={anCat} onChange={e=>setAnCat(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:12,background:"var(--bg3)"}}>
<option value="">Все категории</option>
{data.categories.map(c=><option key={c} value={c}>{c}</option>)}
</select>
<select value={anPri} onChange={e=>setAnPri(e.target.value)} style={{padding:"8px 12px",borderRadius:10,border:"1.5px solid var(--border)",fontSize:12,background:"var(--bg3)"}}>
<option value="">Все приоритеты</option>
{data.priorities.map(p=><option key={p} value={p}>{p}</option>)}
</select>
</div>

{/* Summary KPIs */}
<div style={{display:"grid",gridTemplateColumns:"repeat(6,1fr)",gap:10,marginBottom:24}} className="kpi-r">
<KPI label="Всего" value={anStats.total} sub="задач" color="var(--accent)"/>
<KPI label="Выполнено" value={anStats.done} sub={`${anStats.pct}%`} color="var(--green)"/>
<KPI label="Прогресс" value={`${anStats.avgProg}%`} sub="средний" color="var(--accent)"/>
<KPI label="В срок" value={onTimeRate!==null?`${onTimeRate}%`:"—"} sub="от завершённых" color="var(--cyan2)"/>
<KPI label="Скорость" value={avgTime!==null?`${avgTime}д`:"—"} sub="среднее на задачу" color="#7C3AED"/>
<KPI label="Совещания" value={anMeetings.length} sub={`${mtgWithResult} с результатами`} color="var(--cyan2)"/>
</div>

<div className="analytics-grid">

{/* Status donut */}
<div className="chart-card">
<div className="chart-header"><span className="chart-title">📊 Распределение по статусам</span></div>
{anStats.total>0?<div className="donut-container">
<DonutChart segments={statusSegs} size={150} thickness={26}/>
<div className="donut-legend">{statusData.map(s=><div key={s.label} className="donut-legend-item"><div className="donut-legend-dot" style={{background:s.color}}/><span style={{fontWeight:600}}>{s.value}</span> {s.label} ({anStats.total?Math.round(s.value/anStats.total*100):0}%)</div>)}</div>
</div>:<div style={{textAlign:"center",padding:40,color:"var(--text4)"}}>Нет данных</div>}
</div>

{/* Category donut */}
<div className="chart-card">
<div className="chart-header"><span className="chart-title">🏷️ По категориям</span></div>
{Object.keys(catData).length>0?<div className="donut-container">
<DonutChart segments={Object.entries(catData).map(([c,v])=>({label:c,value:v,pct:anStats.total?v/anStats.total*100:0,color:gc(c)}))} size={150} thickness={26}/>
<div className="donut-legend">{Object.entries(catData).sort((a,b)=>b[1]-a[1]).map(([c,v])=><div key={c} className="donut-legend-item"><div className="donut-legend-dot" style={{background:gc(c)}}/><span style={{fontWeight:600}}>{v}</span> {c}</div>)}</div>
</div>:<div style={{textAlign:"center",padding:40,color:"var(--text4)"}}>Нет данных</div>}
</div>

{/* Weekly trend bar chart */}
<div className="chart-card">
<div className="chart-header"><span className="chart-title">📈 Завершения по неделям</span></div>
<div className="bar-chart">{weekTrend.map((w,i)=><div key={i} className="bar-col">
<div className="bar-value">{w.value||""}</div>
<div className="bar-fill" style={{height:`${w.value?Math.max((w.value/maxWeek)*100,8):3}%`,background:w.value?'var(--gradient)':'var(--border)'}}/>
<div className="bar-label">{w.label}</div>
</div>)}</div>
</div>

{/* Priority bar chart */}
<div className="chart-card">
<div className="chart-header"><span className="chart-title">🎯 По приоритетам</span></div>
<div className="bar-chart">{data.priorities.map(p=>{const v=priData[p]||0;return<div key={p} className="bar-col">
<div className="bar-value">{v||""}</div>
<div className="bar-fill" style={{height:`${v?Math.max((v/Math.max(...Object.values(priData),1))*100,8):3}%`,background:v?gp(p):'var(--border)'}}/>
<div className="bar-label" style={{color:gp(p)}}>{p}</div>
</div>})}</div>
</div>

{/* Category completion rates */}
<div className="chart-card">
<div className="chart-header"><span className="chart-title">📊 Завершённость по категориям</span></div>
{Object.keys(catCompl).length>0?<div style={{display:"flex",flexDirection:"column",gap:10}}>
{Object.entries(catCompl).sort((a,b)=>b[1].pct-a[1].pct).map(([c,d])=><div key={c}>
<div style={{display:"flex",justifyContent:"space-between",fontSize:12,marginBottom:4}}>
<span style={{fontWeight:600,color:gc(c)}}>{c}</span>
<span style={{fontFamily:"var(--mono)",fontWeight:700,fontSize:11}}>{d.done}/{d.total} · {d.pct}%</span>
</div>
<PBar value={d.pct} color={gc(c)} size={8}/>
</div>)}</div>:<div style={{textAlign:"center",padding:40,color:"var(--text4)"}}>Нет данных</div>}
</div>

{/* Priority completion rates */}
<div className="chart-card">
<div className="chart-header"><span className="chart-title">🎯 Завершённость по приоритетам</span></div>
{Object.keys(priCompl).length>0?<div style={{display:"flex",flexDirection:"column",gap:10}}>
{Object.entries(priCompl).map(([p,d])=><div key={p}>
<div style={{display:"flex",justifyContent:"space-between",fontSize:12,marginBottom:4}}>
<span style={{fontWeight:600,color:gp(p)}}>{p}</span>
<span style={{fontFamily:"var(--mono)",fontWeight:700,fontSize:11}}>{d.done}/{d.total} · {d.pct}%</span>
</div>
<PBar value={d.pct} color={gp(p)} size={8}/>
</div>)}</div>:<div style={{textAlign:"center",padding:40,color:"var(--text4)"}}>Нет данных</div>}
</div>

{/* Daily heatmap */}
<div className="chart-card" style={{gridColumn:"span 2"}}>
<div className="chart-header"><span className="chart-title">🗓 Карта активности · {monthN[new Date().getMonth()+1]} {new Date().getFullYear()}</span></div>
<div style={{display:"grid",gridTemplateColumns:`repeat(${Math.min(heatData.length,31)},1fr)`,gap:3}}>
{heatData.map(h=><div key={h.day} title={`${h.date}: ${h.count} завершённых`}>
<div className="heatmap-cell" style={{width:"100%",aspectRatio:"1",borderRadius:4,background:h.count===0?"var(--border)":`rgba(16,185,129,${Math.max(0.15,h.count/maxHeat)})`,display:"flex",alignItems:"center",justifyContent:"center",fontSize:9,fontWeight:700,color:h.count?"#fff":"var(--text4)",cursor:"default"}}>{h.count||""}</div>
<div style={{textAlign:"center",fontSize:8,color:"var(--text4)",marginTop:2}}>{h.day}</div>
</div>)}</div>
<div style={{display:"flex",gap:8,justifyContent:"flex-end",marginTop:10,alignItems:"center"}}>
<span style={{fontSize:10,color:"var(--text4)"}}>Меньше</span>
{[0,.25,.5,.75,1].map((o,i)=><div key={i} style={{width:16,height:16,borderRadius:3,background:o===0?"var(--border)":`rgba(16,185,129,${Math.max(0.15,o)})`}}/>)}
<span style={{fontSize:10,color:"var(--text4)"}}>Больше</span>
</div>
</div>

{/* Meeting analytics */}
<div className="chart-card" style={{gridColumn:"span 2"}}>
<div className="chart-header"><span className="chart-title" style={{color:"var(--cyan2)"}}>🕐 Аналитика совещаний</span></div>
<div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:12}}>
<div style={{background:"var(--cyan-bg)",borderRadius:12,padding:16,textAlign:"center"}}>
<div style={{fontSize:28,fontWeight:800,color:"var(--cyan2)",fontFamily:"var(--mono)"}}>{anMeetings.length}</div>
<div style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginTop:4}}>Всего</div>
</div>
<div style={{background:"var(--green-bg)",borderRadius:12,padding:16,textAlign:"center"}}>
<div style={{fontSize:28,fontWeight:800,color:"var(--green)",fontFamily:"var(--mono)"}}>{mtgDoneCount}</div>
<div style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginTop:4}}>Проведено</div>
</div>
<div style={{background:"linear-gradient(135deg,rgba(16,185,129,.06),rgba(6,182,212,.06))",borderRadius:12,padding:16,textAlign:"center",border:"1px solid rgba(16,185,129,.15)"}}>
<div style={{fontSize:28,fontWeight:800,color:"var(--green2)",fontFamily:"var(--mono)"}}>{mtgWithResult}</div>
<div style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginTop:4}}>С результатами</div>
</div>
<div style={{background:"var(--bg)",borderRadius:12,padding:16,textAlign:"center"}}>
<div style={{fontSize:28,fontWeight:800,color:"var(--accent)",fontFamily:"var(--mono)"}}>{anMeetings.length?Math.round(mtgWithResult/anMeetings.length*100):0}%</div>
<div style={{fontSize:10,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginTop:4}}>Документировано</div>
</div>
</div>
</div>

</div>{/* end analytics-grid */}
</>})()}

{/* ═════ ЭКСПОРТ ═════ */}
{tab==="Экспорт"&&<>
<div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginBottom:20,flexWrap:"wrap",gap:12}}>
<div><div style={{fontSize:22,fontWeight:800}}>📄 Экспорт отчёта</div><div style={{color:"var(--text3)",fontSize:13,marginTop:2}}>Формирование детального PDF-отчёта с задачами и совещаниями</div></div>
</div>

<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:20,marginBottom:24}} className="two-col">
<div className="card">
<div className="stitle"><span className="stitle-icon">📅</span> Период</div>
<div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12,marginBottom:16}}>
<div className="fl"><label>С</label><input type="date" value={expFrom} onChange={e=>setExpFrom(e.target.value)}/></div>
<div className="fl"><label>По</label><input type="date" value={expTo} onChange={e=>setExpTo(e.target.value)}/></div>
</div>
<div style={{display:"flex",flexWrap:"wrap",gap:6}}>
{[["week","Неделя"],["month","Месяц"],["quarter","Квартал"],["year","Год"]].map(([k,l])=>{
const[f,t]=periodRange(k);return<button key={k} className="bo" style={{fontSize:11}} onClick={()=>{setExpFrom(f);setExpTo(t)}}>{l}</button>})}
</div>
</div>
<div className="card">
<div className="stitle"><span className="stitle-icon">🔍</span> Фильтры</div>
<div style={{marginBottom:12}}>
<div style={{fontSize:11,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginBottom:6}}>Категории</div>
<div style={{display:"flex",flexWrap:"wrap",gap:4}}>
{data.categories.map(c=><button key={c} className={`chip ${expCats.includes(c)?"":"" }`} onClick={()=>toggleA(expCats,setExpCats,c)} style={{cursor:"pointer",background:expCats.includes(c)?gc(c)+"20":"var(--bg)",color:expCats.includes(c)?gc(c):"var(--text3)",borderColor:expCats.includes(c)?gc(c)+"40":"var(--border)"}}>{c}</button>)}
</div>
</div>
<div style={{marginBottom:12}}>
<div style={{fontSize:11,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginBottom:6}}>Приоритеты</div>
<div style={{display:"flex",flexWrap:"wrap",gap:4}}>
{data.priorities.map(p=><button key={p} className="chip" onClick={()=>toggleA(expPris,setExpPris,p)} style={{cursor:"pointer",background:expPris.includes(p)?gp(p)+"20":"var(--bg)",color:expPris.includes(p)?gp(p):"var(--text3)",borderColor:expPris.includes(p)?gp(p)+"40":"var(--border)"}}>{p}</button>)}
</div>
</div>
<div>
<div style={{fontSize:11,fontWeight:700,color:"var(--text3)",textTransform:"uppercase",marginBottom:6}}>Статусы</div>
<div style={{display:"flex",flexWrap:"wrap",gap:4}}>
{statuses.map(s=><button key={s} className="chip" onClick={()=>toggleA(expStat,setExpStat,s)} style={{cursor:"pointer",background:expStat.includes(s)?"var(--accent)"+"20":"var(--bg)",color:expStat.includes(s)?"var(--accent)":"var(--text3)",borderColor:expStat.includes(s)?"var(--accent)"+"40":"var(--border)"}}>{s}</button>)}
</div>
</div>
</div>
</div>

<div style={{display:"grid",gridTemplateColumns:"repeat(5,1fr)",gap:10,marginBottom:24}} className="kpi-r">
<KPI label="Задач в отчёте" value={expStats.total} color="var(--accent)"/>
<KPI label="Выполнено" value={expStats.done} sub={`${expStats.pct}%`} color="var(--green)"/>
<KPI label="В работе" value={expStats.active} color="var(--accent)"/>
<KPI label="Просрочено" value={expStats.overdue} color="var(--red)"/>
<KPI label="Совещаний" value={expMeetings.length} sub={`${expMeetings.filter(m=>m.result).length} с рез.`} color="var(--cyan2)"/>
</div>

<div style={{display:"flex",gap:12,marginBottom:24}}>
<button className="bp" onClick={genReport} disabled={expGen} style={{maxWidth:280}}>{expGen?"⏳ Формирование...":"📊 Сформировать отчёт"}</button>
{expPreview&&<button className="bs" onClick={printReport} style={{maxWidth:280}}>💾 Сохранить PDF</button>}
{expPreview&&<button className="bo" onClick={()=>setExpPreview(null)}>Закрыть предпросмотр</button>}
</div>

{expPreview&&<div className="card" style={{padding:0,overflow:"hidden"}}>
<div style={{padding:"12px 20px",background:"var(--bg3)",borderBottom:"1px solid var(--border)",display:"flex",justifyContent:"space-between",alignItems:"center"}}>
<span style={{fontWeight:700,fontSize:14}}>📄 Предпросмотр отчёта</span>
<span style={{fontSize:12,color:"var(--text3)"}}>{expFiltered.length} задач · {expMeetings.length} совещаний</span>
</div>
<iframe srcDoc={expPreview} style={{width:"100%",height:"70vh",border:"none"}}/>
</div>}
</>}

</div>{/* end main */}

{/* ═════ MODALS & SIDE PANELS ═════ */}
{showForm&&<TForm cats={data.categories} pris={data.priorities} onClose={()=>{setShowForm(false);setEditTask(null)}} initial={editTask&&editTask.type!=="meeting"?editTask:null}
onSubmit={t=>{if(editTask&&editTask.type!=="meeting"){updT(editTask.id,t);setEditTask(null);showToast("Задача обновлена","");} else{addT(t);showToast("Задача добавлена","");}}}/>}

{showMForm&&<MForm pris={data.priorities} onClose={()=>{setShowMForm(false);setEditTask(null)}} initial={editTask&&editTask.type==="meeting"?editTask:null}
onSubmit={t=>{if(editTask&&editTask.type==="meeting"){updT(editTask.id,t);setEditTask(null);showToast("Совещание обновлено","");} else{addT(t);showToast("Совещание добавлено","");}}}/>}

{detailTask&&<TDetail task={detailTask} now={now} onClose={()=>setDetailTask(null)}
onEdit={t=>{setDetailTask(null);setEditTask(t);if(t.type==="meeting")setShowMForm(true);else setShowForm(true)}}
onDelete={id=>{delT(id);showToast("Удалено","")}}
onProg={(id,p)=>{setProg(id,p);if(p>=100)showToast("Завершено! ✅","")}}
onAddResult={t=>{setDetailTask(null);setShowResultModal(t)}}/>}

{showSettings&&<Settings data={data} onClose={()=>setShowSettings(false)} onUpdate={reload} showToast={showToast}/>}

{showResultModal&&<ResultModal task={showResultModal} onClose={()=>setShowResultModal(null)} onSave={(id,result)=>{saveResult(id,result);showToast("Результаты сохранены ✅","")}}/>}

{drillKpi&&<KpiDrill kpi={drillKpi} tasks={panelTasks} now={now} onClose={()=>setDrillKpi(null)} onOpenTask={t=>{setDrillKpi(null);setDetailTask(t)}}/>}

{toast&&<Toast msg={toast.msg} type={toast.type} onDone={()=>setToast(null)}/>}

</div>}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
</script>
</body></html>
'''

class Api:
    def __init__(self):
        self.db_path = DB_PATH
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL DEFAULT '',
            cat TEXT DEFAULT '',
            pri TEXT DEFAULT '',
            desc TEXT DEFAULT '',
            start TEXT DEFAULT '',
            deadline TEXT DEFAULT '',
            progress INTEGER DEFAULT 0,
            notes TEXT DEFAULT '',
            type TEXT DEFAULT 'task',
            timeStart TEXT DEFAULT '',
            timeEnd TEXT DEFAULT '',
            result TEXT DEFAULT '',
            completedAt TEXT DEFAULT '',
            createdAt TEXT DEFAULT '',
            notifiedMeeting INTEGER DEFAULT 0,
            notifiedOverdue INTEGER DEFAULT 0
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            protected INTEGER DEFAULT 0
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS priorities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            sort_order INTEGER DEFAULT 0
        )''')
        # Seed defaults
        defaults_cats = [("Рабочая", 1), ("Проект", 1), ("Обучение", 1), ("Личная", 1), ("Рутина", 1)]
        for cat, prot in defaults_cats:
            try:
                c.execute("INSERT INTO categories (name, protected) VALUES (?, ?)", (cat, prot))
            except sqlite3.IntegrityError:
                pass
        defaults_pris = [("Высокий", 1), ("Средний", 2), ("Низкий", 3)]
        for pri, order in defaults_pris:
            try:
                c.execute("INSERT INTO priorities (name, sort_order) VALUES (?, ?)", (pri, order))
            except sqlite3.IntegrityError:
                pass
        # Ensure columns exist (migration)
        existing = {row[1] for row in c.execute("PRAGMA table_info(tasks)").fetchall()}
        migrations = {
            "type": "TEXT DEFAULT 'task'",
            "timeStart": "TEXT DEFAULT ''",
            "timeEnd": "TEXT DEFAULT ''",
            "result": "TEXT DEFAULT ''",
            "completedAt": "TEXT DEFAULT ''",
            "createdAt": "TEXT DEFAULT ''",
            "notifiedMeeting": "INTEGER DEFAULT 0",
            "notifiedOverdue": "INTEGER DEFAULT 0",
        }
        for col, typedef in migrations.items():
            if col not in existing:
                c.execute(f"ALTER TABLE tasks ADD COLUMN {col} {typedef}")
        conn.commit()
        conn.close()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def get_data(self):
        conn = self._conn()
        c = conn.cursor()
        cats = [r[0] for r in c.execute("SELECT name FROM categories ORDER BY id").fetchall()]
        pris = [r[0] for r in c.execute("SELECT name FROM priorities ORDER BY sort_order, id").fetchall()]
        prot = [r[0] for r in c.execute("SELECT name FROM categories WHERE protected=1").fetchall()]
        rows = c.execute("SELECT * FROM tasks ORDER BY id").fetchall()
        cols = [d[0] for d in c.description]
        tasks = [dict(zip(cols, r)) for r in rows]
        conn.close()
        return json.dumps({"categories": cats, "priorities": pris, "protectedCats": prot, "tasks": tasks}, ensure_ascii=False)

    def add_task(self, task_json):
        t = json.loads(task_json)
        conn = self._conn()
        c = conn.cursor()
        today = datetime.date.today().isoformat()
        c.execute("""INSERT INTO tasks (name, cat, pri, desc, start, deadline, progress, notes, type, timeStart, timeEnd, result, completedAt, createdAt)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            t.get("name", ""),
            t.get("cat", ""),
            t.get("pri", ""),
            t.get("desc", ""),
            t.get("start", today),
            t.get("deadline", ""),
            t.get("progress", 0),
            t.get("notes", ""),
            t.get("type", "task"),
            t.get("timeStart", ""),
            t.get("timeEnd", ""),
            t.get("result", ""),
            t.get("completedAt", ""),
            today,
        ))
        conn.commit()
        task_id = c.lastrowid
        conn.close()
        return str(task_id)

    def update_task(self, task_id, patch_json):
        patch = json.loads(patch_json)
        conn = self._conn()
        c = conn.cursor()
        allowed = ["name", "cat", "pri", "desc", "start", "deadline", "progress",
                    "notes", "type", "timeStart", "timeEnd", "result", "completedAt",
                    "notifiedMeeting", "notifiedOverdue"]
        sets = []
        vals = []
        for k, v in patch.items():
            if k in allowed:
                sets.append(f"{k} = ?")
                vals.append(v)
        if sets:
            vals.append(int(task_id))
            c.execute(f"UPDATE tasks SET {', '.join(sets)} WHERE id = ?", vals)
            conn.commit()
        conn.close()
        return "ok"

    def delete_task(self, task_id):
        conn = self._conn()
        c = conn.cursor()
        c.execute("DELETE FROM tasks WHERE id = ?", (int(task_id),))
        conn.commit()
        conn.close()
        return "ok"

    def add_category(self, name):
        conn = self._conn()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO categories (name, protected) VALUES (?, 0)", (name,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        conn.close()
        return "ok"

    def delete_category(self, name):
        conn = self._conn()
        c = conn.cursor()
        c.execute("SELECT protected FROM categories WHERE name = ?", (name,))
        row = c.fetchone()
        if row and row[0] == 1:
            conn.close()
            return "protected"
        c.execute("DELETE FROM categories WHERE name = ? AND protected = 0", (name,))
        conn.commit()
        conn.close()
        return "ok"

    def add_priority(self, name):
        conn = self._conn()
        c = conn.cursor()
        max_order = c.execute("SELECT COALESCE(MAX(sort_order), 0) FROM priorities").fetchone()[0]
        try:
            c.execute("INSERT INTO priorities (name, sort_order) VALUES (?, ?)", (name, max_order + 1))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
        conn.close()
        return "ok"

    def delete_priority(self, name):
        conn = self._conn()
        c = conn.cursor()
        c.execute("DELETE FROM priorities WHERE name = ?", (name,))
        conn.commit()
        conn.close()
        return "ok"

    def get_current_time(self):
        now = datetime.datetime.now()
        return json.dumps({
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M"),
            "datetime": now.isoformat()
        })

    def save_pdf_report(self, html_content):
        """Save HTML report and open in browser for printing to PDF"""
        report_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
        os.makedirs(report_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"smart_planner_report_{timestamp}.html"
        filepath = os.path.join(report_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)
        # Open in default browser
        import webbrowser
        webbrowser.open(f"file://{os.path.abspath(filepath)}")
        return filepath


api = Api()


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            try:
                req = json.loads(body)
                method = req.get("method", "")
                args = req.get("args", [])

                if not hasattr(api, method):
                    raise ValueError(f"Unknown method: {method}")

                func = getattr(api, method)
                result = func(*args)

                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": True, "result": result}, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"ok": False, "error": str(e)}, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress default logging for cleaner console
        pass


def main():
    port = PORT
    server = http.server.HTTPServer(("0.0.0.0", port), RequestHandler)
    print(f"""
╔══════════════════════════════════════════════════╗
║           ⚡ Smart Planner v3.0                  ║
║──────────────────────────────────────────────────║
║  🌐 Откройте в браузере:                        ║
║     http://localhost:{port}                        ║
║                                                  ║
║  📋 Задачи + 🕐 Совещания + 📊 Аналитика        ║
║  📄 Экспорт отчётов (HTML/PDF)                   ║
║  🔔 Уведомления о совещаниях и просрочках        ║
║                                                  ║
║  💾 База данных: {DB_PATH:<31}║
║  🛑 Для остановки нажмите Ctrl+C                 ║
╚══════════════════════════════════════════════════╝
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⚡ Smart Planner остановлен. До встречи!")
        server.server_close()


if __name__ == "__main__":
    main()
