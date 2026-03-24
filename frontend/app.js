// ============================================================
// app.js - 前端交互逻辑
// ============================================================
// 开发顺序：HTML 和 CSS 写完后最后写
// 核心概念：
//   - DOM 操作：用 JS 读取/修改 HTML 元素
//   - fetch API：浏览器内置的 HTTP 请求工具
//   - async/await：处理异步操作（等待网络请求结果）
//   - marked.js：把 Markdown 字符串渲染成 HTML
// ============================================================

// 后端地址，开发时是本机8000端口，上线后改为真实服务器地址
const API_BASE = 'http://localhost:8000';

// ============================================================
// 功能切换
// ============================================================

/**
 * switchFeature - 切换激活的功能模块
 * 原理：
 *   1. 所有卡片移除 active → 点击的卡片加 active
 *   2. 所有面板移除 active → 对应面板加 active（显示）
 *   3. 隐藏上次的结果区
 */
function switchFeature(feature) {
  document.querySelectorAll('.feature-card').forEach(card => {
    card.classList.remove('active');
    // dataset.feature 读取 HTML 里的 data-feature 属性
    if (card.dataset.feature === feature) card.classList.add('active');
  });
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  const target = document.getElementById(`panel-${feature}`);
  if (target) target.classList.add('active');
  hideResult();
}

// 页面加载完成后，给每张功能卡片注册点击事件
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.feature-card').forEach(card => {
    card.addEventListener('click', () => switchFeature(card.dataset.feature));
  });
});


// ============================================================
// 通用工具函数
// ============================================================

function showLoading() {
  document.getElementById('loading').style.display = 'flex';
  document.getElementById('result-section').style.display = 'none';
}

function hideLoading() {
  document.getElementById('loading').style.display = 'none';
}

function hideResult() {
  document.getElementById('result-section').style.display = 'none';
  document.getElementById('loading').style.display = 'none';
}

/**
 * showResult - 把 AI 返回的 Markdown 渲染到页面
 * 原理：marked.parse() 把 Markdown 语法转换成 HTML 标签
 *       innerHTML 把 HTML 字符串插入到 DOM 中显示
 */
function showResult(markdownText) {
  hideLoading();
  const section = document.getElementById('result-section');
  const body = document.getElementById('result-body');
  body.innerHTML = marked.parse(markdownText);
  section.style.display = 'block';
  section.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function showError(message) {
  hideLoading();
  const section = document.getElementById('result-section');
  document.getElementById('result-body').innerHTML =
    `<div class="error-box">⚠️ 出错了：${message}</div>`;
  section.style.display = 'block';
  section.scrollIntoView({ behavior: 'smooth' });
}

/**
 * callAPI - 通用 API 调用函数
 * 原理：
 *   fetch() 发送 HTTP POST 请求
 *   async/await 让异步代码看起来像同步代码：
 *     await 暂停等待请求完成，再继续下一行
 *     比 .then().then() 链式写法更易读
 */
async function callAPI(endpoint, body) {
  showLoading();
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),   // JS对象 → JSON字符串
    });
    const data = await response.json();  // JSON字符串 → JS对象
    if (data.success) {
      showResult(data.data);
    } else {
      showError(data.error || '未知错误');
    }
  } catch (error) {
    // 网络错误（如后端未启动、断网）
    showError(`网络请求失败：${error.message}。请确认后端已启动（uvicorn app.main:app --reload）`);
  }
}


// ============================================================
// 各功能提交函数
// ============================================================

// .value 读取 input 的值，.trim() 去掉首尾空格
async function submitWeather() {
  const city = document.getElementById('weather-city').value.trim();
  if (!city) { alert('请输入城市名称'); return; }
  await callAPI('/api/weather', { city });
}

async function submitTravel() {
  const departure   = document.getElementById('travel-departure').value.trim();
  const destination = document.getElementById('travel-destination').value.trim();
  const days        = parseInt(document.getElementById('travel-days').value);
  const budget      = document.getElementById('travel-budget').value.trim();
  // querySelector 找到选中的单选按钮
  const preference  = document.querySelector('input[name="travel-pref"]:checked').value;
  if (!departure || !destination || !days || !budget) {
    alert('请填写出发城市、目的地、天数和预算'); return;
  }
  await callAPI('/api/travel', { departure, destination, days, budget, preference });
}

async function submitTranslate() {
  const text            = document.getElementById('translate-text').value.trim();
  const target_language = document.getElementById('translate-lang').value;
  const scene           = document.getElementById('translate-scene').value;
  if (!text) { alert('请输入需要翻译的内容'); return; }
  await callAPI('/api/translate', { text, target_language, scene });
}

async function submitRecipe() {
  const ingredients = document.getElementById('recipe-ingredients').value.trim();
  const taste       = document.getElementById('recipe-taste').value;
  const difficulty  = document.getElementById('recipe-difficulty').value;
  const cook_time   = parseInt(document.getElementById('recipe-time').value);
  await callAPI('/api/recipe', { ingredients, taste, cook_time, difficulty });
}

async function submitReply() {
  const message     = document.getElementById('reply-message').value.trim();
  const sender_role = document.getElementById('reply-role').value;
  const tone        = document.getElementById('reply-tone').value;
  const my_goal     = document.querySelector('input[name="reply-goal"]:checked').value;
  // || null：空字符串转为 null（后端 Optional 字段用 null 表示无值）
  const extra_context = document.getElementById('reply-context').value.trim() || null;
  if (!message) { alert('请输入对方发来的消息'); return; }
  await callAPI('/api/reply', { message, sender_role, tone, my_goal, extra_context });
}


// ============================================================
// 其他工具
// ============================================================

// 滑块实时更新时间显示
function updateTimeDisplay(value) {
  document.getElementById('time-display').textContent = value;
}

// 复制结果到剪贴板
async function copyResult() {
  const text = document.getElementById('result-body').innerText;
  try {
    await navigator.clipboard.writeText(text);
    const btn = document.querySelector('.copy-btn');
    btn.textContent = '✓ 已复制';
    setTimeout(() => { btn.textContent = '复制全部'; }, 1500);
  } catch (e) {
    alert('复制失败，请手动选中文字复制');
  }
}
