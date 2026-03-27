/**
 * ACM Lite - 前端交互逻辑
 */

// ==================== 全局状态 ====================
let editor = null;
let currentProblem = null;
let currentMode = 'acm';       // 'acm' | 'core'
let savedCode = { acm: '', core: '' };
let _draftTimer = null;
let editorFontSize = parseInt(localStorage.getItem('editor_font_size') || '13');

// 难度对应的样式（全局复用）
const DIFF_STYLE = {
    Easy:   'bg-green-100 text-green-700',
    Medium: 'bg-amber-100 text-amber-700',
    Hard:   'bg-red-100 text-red-700',
};

// ==================== 草稿自动保存 ====================
function draftKey(pid, mode) { return `draft_${pid}_${mode}`; }

function saveDraft() {
    if (!currentProblem || !editor) return;
    const code = editor.getValue();
    const tmpl = currentMode === 'core' ? (currentProblem.lc_template || '') : (currentProblem.template_code || '');
    // 内容与模板相同则不存草稿
    if (code === tmpl) { localStorage.removeItem(draftKey(currentProblem.id, currentMode)); return; }
    localStorage.setItem(draftKey(currentProblem.id, currentMode), code);
}

function loadDraft(pid, mode) {
    return localStorage.getItem(draftKey(pid, mode)) || '';
}

function clearDraft(pid, mode) {
    localStorage.removeItem(draftKey(pid, mode));
}

function scheduleDraftSave() {
    clearTimeout(_draftTimer);
    _draftTimer = setTimeout(saveDraft, 1000);
}

// ==================== 页面路由 ====================
function navigate(page, data) {
    // 离开做题页前保存草稿
    if (currentProblem && editor) saveDraft();

    document.querySelectorAll('.page').forEach(p => { p.classList.add('hidden'); p.classList.remove('block'); });
    const el = document.getElementById('page-' + page);
    if (el) { el.classList.remove('hidden'); el.classList.add('block'); }

    if (page === 'home') loadHome();
    if (page === 'solve' && data) loadProblem(data);
}

// ==================== 主页加载 ====================
async function loadHome() {
    loadDaily();
    loadStats();
    loadTags();
    loadProblems();
}

async function loadTags() {
    try {
        const tags = await (await fetch('/api/tags')).json();
        const sel = document.getElementById('filter-tag');
        if (!sel) return;
        const current = sel.value;
        sel.innerHTML = '<option value="">全部标签</option>' + tags.map(t => `<option value="${esc(t)}"${t===current?' selected':''}>${esc(t)}</option>`).join('');
    } catch {}
}

// -- 每日一题
async function loadDaily() {
    const container = document.getElementById('daily-card');
    try {
        const res = await fetch('/api/daily');
        if (!res.ok) { container.innerHTML = '<div class="text-sm text-slate-400">题库为空，请先添加题目</div>'; return; }
        const data = await res.json();
        const p = data.problem;
        const done = data.is_completed;
        const diffColor = DIFF_STYLE;
        // 已完成时卡片左边框变绿
        container.className = container.className.replace(/border-green-400|border-l-4/g, '').trim();
        if (done) container.className += ' border-l-4 border-green-400';
        container.innerHTML = `
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div class="space-y-3">
                    <div class="flex items-center gap-2">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${diffColor[p.difficulty] || ''}">${p.difficulty}</span>
                        ${done ? '<span class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-700"><span class="material-symbols-outlined text-[14px]">check_circle</span>已完成</span>' : ''}
                    </div>
                    <h3 class="text-2xl font-bold tracking-tight">${esc(p.title)}</h3>
                    <p class="text-slate-500 max-w-md text-sm">${esc((p.tags || []).join(' · '))}${p.source ? ' · ' + esc(p.source) : ''}</p>
                </div>
                <div class="flex items-center gap-3 shrink-0">
                    <button onclick="refreshDaily()" class="px-4 py-3 rounded-lg border border-slate-200 text-slate-500 hover:bg-slate-50 text-sm font-semibold transition-colors">
                        <span class="material-symbols-outlined text-[18px]">refresh</span>
                    </button>
                    <button onclick="navigate('solve', ${p.id})" class="inline-flex items-center justify-center px-8 py-3 rounded-lg bg-primary text-white font-semibold text-sm transition-all hover:bg-primary/90 focus:ring-4 focus:ring-primary/20">
                        ${done ? '查看题目' : '开始做题'}
                    </button>
                </div>
            </div>`;
    } catch { container.innerHTML = '<div class="text-sm text-slate-400">加载失败</div>'; }
}

async function refreshDaily() {
    await fetch('/api/daily/refresh', { method: 'POST' });
    loadDaily();
}

// -- 统计
async function loadStats() {
    const res = await fetch('/api/stats');
    const s = await res.json();
    document.getElementById('stats-cards').innerHTML = `
        <div class="p-5 rounded-lg border border-slate-100 bg-slate-50/50">
            <div class="flex items-center gap-2 mb-1.5">
                <span class="material-symbols-outlined text-primary text-sm">task_alt</span>
                <p class="text-xs font-medium text-slate-400">已通过</p>
            </div>
            <p class="text-2xl font-bold">${s.ac_count} <span class="text-sm font-normal text-slate-400">/ ${s.total_problems} 题</span></p>
        </div>
        <div class="p-5 rounded-lg border border-slate-100 bg-slate-50/50">
            <div class="flex items-center gap-2 mb-1.5">
                <span class="material-symbols-outlined text-primary text-sm">send</span>
                <p class="text-xs font-medium text-slate-400">总提交</p>
            </div>
            <p class="text-2xl font-bold">${s.total_submissions}</p>
        </div>
        <div class="p-5 rounded-lg border border-slate-100 bg-slate-50/50">
            <div class="flex items-center gap-2 mb-1.5">
                <span class="material-symbols-outlined text-primary text-sm">percent</span>
                <p class="text-xs font-medium text-slate-400">通过率</p>
            </div>
            <p class="text-2xl font-bold">${s.total_problems > 0 ? Math.round(s.ac_count / s.total_problems * 100) : 0}%</p>
        </div>
        <div class="p-5 rounded-lg border border-slate-100 bg-slate-50/50">
            <div class="flex items-center gap-2 mb-1.5">
                <span class="material-symbols-outlined text-primary text-sm">bar_chart</span>
                <p class="text-xs font-medium text-slate-400">难度分布</p>
            </div>
            ${renderDiffBar(s)}
        </div>`;
}

// -- 题库列表
async function loadProblems() { filterProblems(); }

async function filterProblems() {
    const keyword = document.getElementById('search-input').value;
    const difficulty = document.getElementById('filter-difficulty').value;
    const tag = document.getElementById('filter-tag')?.value || '';
    const sortOrder = document.getElementById('sort-order').value;
    const params = new URLSearchParams();
    if (keyword) params.set('keyword', keyword);
    if (difficulty) params.set('difficulty', difficulty);
    if (tag) params.set('tag', tag);

    const res = await fetch('/api/problems?' + params);
    let problems = await res.json();

    // 前端排序
    if (sortOrder === 'id_asc') problems.sort((a, b) => a.id - b.id);
    else if (sortOrder === 'status') problems.sort((a, b) => (a.best_status === 'Accepted' ? 1 : 0) - (b.best_status === 'Accepted' ? 1 : 0));
    // id_desc 是默认顺序，无需排序

    renderProblems(problems);
}

function renderProblems(problems) {
    const container = document.getElementById('problems-list');
    if (!problems.length) {
        container.innerHTML = `<div class="text-center py-16 text-slate-400 text-sm">题库为空，点击上方「添加题目」开始</div>`;
        return;
    }

    // 按来源分为真题和 LeetCode 两组
    const isReal = p => p.source && !p.source.startsWith('LeetCode');
    const realProblems = problems.filter(isReal);
    const lcProblems = problems.filter(p => !isReal(p));

    container.innerHTML =
        renderGroup('面试真题', 'work', 'border-l-orange-500 bg-orange-50/40', realProblems) +
        renderGroup('LeetCode 原题', 'code', 'border-l-blue-500 bg-blue-50/40', lcProblems);
}

function renderGroup(title, icon, borderClass, problems) {
    if (!problems.length) return '';
    const diffColor = DIFF_STYLE;

    const header = `
        <div class="flex items-center gap-3 px-4 py-3 rounded-lg border-l-4 ${borderClass} mb-3 mt-6 first:mt-0">
            <span class="material-symbols-outlined text-[20px]">${icon}</span>
            <span class="font-bold text-sm">${title}</span>
            <span class="text-xs text-slate-400 font-medium">${problems.length} 题</span>
        </div>`;

    const cards = problems.map(p => {
        const statusIcon = p.best_status === 'Accepted'
            ? '<span class="material-symbols-outlined text-green-500 text-[18px]">check_circle</span>'
            : p.best_status
                ? '<span class="material-symbols-outlined text-amber-400 text-[18px]">pending</span>'
                : '<span class="material-symbols-outlined text-slate-300 text-[18px]">radio_button_unchecked</span>';

        return `
        <div class="group flex items-center gap-4 p-4 rounded-xl border border-slate-100 bg-white hover:border-slate-200 hover:shadow-sm transition-all cursor-pointer" onclick="navigate('solve', ${p.id})">
            <div class="shrink-0">${statusIcon}</div>
            <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2 mb-1">
                    <span class="text-xs text-slate-400 font-medium">#${p.id}</span>
                    <span class="font-semibold text-sm truncate">${esc(p.title)}</span>
                </div>
                <div class="flex items-center gap-2">
                    <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${diffColor[p.difficulty]||''}">${p.difficulty}</span>
                    ${(p.tags||[]).slice(0,3).map(t => `<span class="text-[11px] text-slate-400">${esc(t)}</span>`).join('<span class="text-slate-200">·</span>')}
                </div>
            </div>
            <div class="shrink-0 flex items-center gap-2">
                ${p.source ? `<span class="text-xs text-slate-400 hidden sm:inline">${esc(p.source)}</span>` : ''}
                <button onclick="event.stopPropagation();editProblem(${p.id})" class="p-1.5 text-slate-300 hover:text-slate-500 opacity-0 group-hover:opacity-100 transition-all">
                    <span class="material-symbols-outlined text-[16px]">edit</span>
                </button>
                <button onclick="event.stopPropagation();deleteProblem(${p.id},'${esc(p.title)}')" class="p-1.5 text-slate-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all">
                    <span class="material-symbols-outlined text-[16px]">delete</span>
                </button>
            </div>
        </div>`;
    }).join('');

    return header + cards;
}

// ==================== 做题页 ====================
async function loadProblem(pid) {
    const res = await fetch(`/api/problems/${pid}`);
    currentProblem = await res.json();
    const p = currentProblem;

    document.getElementById('solve-title').textContent = `${p.id}. ${p.title}`;

    // Meta
    const diffColor = DIFF_STYLE;
    const tagsHtml = (p.tags||[]).map(t => `<span class="text-slate-500 text-sm">${esc(t)}</span>`).join('<span class="text-slate-300">·</span>');
    document.getElementById('solve-meta').innerHTML = `
        <span class="px-2 py-0.5 rounded text-xs font-bold uppercase tracking-wider ${diffColor[p.difficulty]||''}">${p.difficulty}</span>
        <span class="text-slate-300">|</span>
        ${tagsHtml}`;

    // Description
    document.getElementById('solve-description').innerHTML = marked.parse(p.description || '暂无题目描述');

    // Source tags
    const srcEl = document.getElementById('solve-source-tags');
    if (p.source) {
        srcEl.innerHTML = `<span class="px-3 py-1 bg-white border border-slate-200 rounded-full text-xs font-medium">${esc(p.source)}</span>`;
        if (p.source_url) srcEl.innerHTML += `<a href="${p.source_url}" target="_blank" class="px-3 py-1 bg-white border border-slate-200 rounded-full text-xs font-medium text-primary hover:bg-primary/5">原题链接 ↗</a>`;
    } else {
        srcEl.innerHTML = '<span class="text-xs text-slate-400">无</span>';
    }

    // 获取提交历史（统计 + 恢复上次代码和模式）
    const subs = await (await fetch(`/api/submissions?problem_id=${pid}&limit=50`)).json();
    const acCount = subs.filter(s => s.status === 'Accepted').length;
    document.getElementById('solve-submission-count').textContent = `${acCount} AC / ${subs.length} 次提交`;

    const lastCode = subs.length > 0 ? subs[0].code : '';

    // 从代码内容检测上次使用的模式
    let lastMode = 'acm';
    if (lastCode && p.lc_template) {
        const sig = p.lc_template.match(/^(?:def|class)\s+\w+/m);
        if (sig && lastCode.includes(sig[0]) && !lastCode.includes('sys.stdin')) {
            lastMode = 'core';
        }
    }

    currentMode = lastCode ? lastMode : 'acm';
    savedCode = { acm: '', core: '' };
    if (lastCode) savedCode[currentMode] = lastCode;
    updateModeUI();
    renderTestCases(p.test_cases || []);

    // 优先级：localStorage 草稿 > 上次提交 > 模板
    const draft = loadDraft(p.id, currentMode);
    const initialCode = draft || lastCode || (currentMode === 'core' ? (p.lc_template || '') : (p.template_code || getDefaultTemplate()));
    initEditor(initialCode);

    // Reset result panel & custom input
    document.getElementById('result-panel').classList.add('hidden');
    toggleCustomInput(true);
}

function renderTestCases(cases) {
    const container = document.getElementById('testcases-list');
    if (!cases.length) { container.innerHTML = '<p class="text-sm text-slate-400">暂无测试用例</p>'; return; }

    if (currentMode === 'core') {
        // 核心代码模式：格式化输入为可读参数 + 期望输出
        const fmt = currentProblem?.lc_input_fmt || '';
        container.innerHTML = cases.map((tc, i) => {
            const displayInput = fmtCoreInput(tc.input, fmt);
            return `
            <div class="bg-slate-50 border border-slate-100 p-4 rounded-lg text-sm space-y-2">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-semibold text-slate-400 uppercase">样例 ${i+1}</span>
                    <button onclick="deleteTestCase(${tc.id})" class="text-slate-300 hover:text-red-400 transition-colors" title="删除">
                        <span class="material-symbols-outlined text-[16px]">delete</span>
                    </button>
                </div>
                <div>
                    <p class="text-[10px] text-slate-400 mb-0.5 font-sans uppercase">输入</p>
                    <pre class="text-xs whitespace-pre-wrap text-slate-700 font-mono">${esc(displayInput)}</pre>
                </div>
                <div>
                    <p class="text-[10px] text-slate-400 mb-0.5 font-sans uppercase">输出</p>
                    <pre class="text-xs whitespace-pre-wrap text-slate-700 font-mono">${esc(tc.expected_output)}</pre>
                </div>
            </div>`;
        }).join('');
    } else {
        // ACM 模式：显示完整输入和输出
        container.innerHTML = cases.map((tc, i) => `
            <div class="bg-slate-50 border border-slate-100 p-4 rounded-lg font-mono text-sm space-y-2">
                <div class="flex items-center justify-between">
                    <span class="text-xs font-semibold text-slate-400 uppercase">用例 ${i+1}</span>
                    <button onclick="deleteTestCase(${tc.id})" class="text-slate-300 hover:text-red-400 transition-colors" title="删除">
                        <span class="material-symbols-outlined text-[16px]">delete</span>
                    </button>
                </div>
                <div class="grid grid-cols-2 gap-3">
                    <div>
                        <p class="text-[10px] text-slate-400 mb-0.5 font-sans uppercase">输入</p>
                        <pre class="text-xs whitespace-pre-wrap text-slate-700">${esc(tc.input)}</pre>
                    </div>
                    <div>
                        <p class="text-[10px] text-slate-400 mb-0.5 font-sans uppercase">期望输出</p>
                        <pre class="text-xs whitespace-pre-wrap text-slate-700">${esc(tc.expected_output)}</pre>
                    </div>
                </div>
            </div>
        `).join('');
    }
}

function getDefaultTemplate() {
    return `import sys
input = sys.stdin.readline

def solve():
    # 在这里写你的解法
    pass

T = int(input())
for _ in range(T):
    solve()
`;
}

// ==================== Monaco Editor ====================
function initEditor(code) {
    const container = document.getElementById('monaco-editor');
    if (editor) { editor.setValue(code); return; }

    require(['vs/editor/editor.main'], function () {
        editor = monaco.editor.create(container, {
            value: code,
            language: 'python',
            theme: 'vs',
            fontSize: editorFontSize,
            fontFamily: "'JetBrains Mono', 'SF Mono', 'Consolas', monospace",
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            wordWrap: 'on',
            padding: { top: 16 },
            lineNumbers: 'on',
            renderLineHighlight: 'line',
            overviewRulerLanes: 0,
            hideCursorInOverviewRuler: true,
            scrollbar: { vertical: 'hidden', horizontal: 'auto' },
        });
        editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter, () => submitCode());
        editor.addCommand(monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter, () => runCode());
        // 编辑时自动保存草稿
        editor.onDidChangeModelContent(() => scheduleDraftSave());
    });
}

function resetCode() {
    if (!currentProblem || !editor) return;
    if (!confirm('确定要重置代码吗？')) return;
    const tmpl = currentMode === 'core'
        ? (currentProblem.lc_template || '# 该题暂无核心代码模板\n')
        : (currentProblem.template_code || getDefaultTemplate());
    editor.setValue(tmpl);
    savedCode[currentMode] = '';
    clearDraft(currentProblem.id, currentMode);
}

function setFontSize(delta) {
    editorFontSize = Math.max(11, Math.min(20, editorFontSize + delta));
    localStorage.setItem('editor_font_size', editorFontSize);
    if (editor) editor.updateOptions({ fontSize: editorFontSize });
    const label = document.getElementById('font-size-label');
    if (label) label.textContent = editorFontSize;
}

// ==================== 运行 & 提交 ====================
async function runCode() {
    if (!currentProblem || !editor) return;
    const btn = document.getElementById('btn-run');
    btn.disabled = true; btn.textContent = '运行中...';
    try {
        const body = { code: editor.getValue(), mode: currentMode };
        if (document.getElementById('use-custom-input').checked) body.custom_input = document.getElementById('custom-input').value;
        const res = await fetch(`/api/run/${currentProblem.id}`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(body) });
        showResult(await res.json());
    } catch(e) { alert('运行出错: ' + e.message); }
    finally { btn.disabled = false; btn.textContent = '运行'; }
}

async function submitCode() {
    if (!currentProblem || !editor) return;
    const btn = document.getElementById('btn-submit');
    btn.disabled = true; btn.textContent = '判题中...';
    try {
        const res = await fetch(`/api/submit/${currentProblem.id}`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ code: editor.getValue(), mode: currentMode }) });
        const result = await res.json();
        showResult(result);
        // 提交后更新提交计数
        const subRes = await fetch(`/api/submissions?problem_id=${currentProblem.id}&limit=50`);
        const subs = await subRes.json();
        const acCount = subs.filter(s => s.status === 'Accepted').length;
        document.getElementById('solve-submission-count').textContent = `${acCount} AC / ${subs.length} 次提交`;
        // AC 时清除草稿并显示通过提示
        if (result.status === 'Accepted') {
            clearDraft(currentProblem.id, currentMode);
            showAcceptedBanner();
        }
    } catch(e) { alert('提交出错: ' + e.message); }
    finally { btn.disabled = false; btn.textContent = '提交'; }
}

function showAcceptedBanner() {
    // 已有 banner 则跳过
    if (document.getElementById('ac-banner')) return;
    const banner = document.createElement('div');
    banner.id = 'ac-banner';
    banner.className = 'fixed top-0 left-0 right-0 z-50 flex items-center justify-center py-3 bg-green-500 text-white font-bold text-sm transition-opacity duration-500';
    banner.textContent = 'Accepted — 全部用例通过!';
    document.body.appendChild(banner);
    setTimeout(() => { banner.style.opacity = '0'; }, 2000);
    setTimeout(() => { banner.remove(); }, 2500);
}

function showResult(result) {
    const panel = document.getElementById('result-panel');
    panel.classList.remove('hidden');

    const statusStyle = {
        'Accepted': 'text-green-600',
        'Wrong Answer': 'text-red-600',
        'Time Limit Exceeded': 'text-amber-600',
        'Runtime Error': 'text-orange-600',
    };

    document.getElementById('result-status').className = `text-sm font-bold ${statusStyle[result.status] || 'text-slate-600'}`;
    document.getElementById('result-status').textContent = result.status;
    document.getElementById('result-stats').textContent = `${result.passed_cases}/${result.total_cases} 通过 · ${result.total_time_ms.toFixed(0)}ms`;

    document.getElementById('result-detail').innerHTML = (result.detail||[]).map((c, i) => {
        const color = c.status === 'AC' ? 'text-green-600' : c.status === 'WA' ? 'text-red-600' : c.status === 'TLE' ? 'text-amber-600' : 'text-orange-600';
        const showDiff = c.status !== 'AC';
        return `
        <div class="bg-slate-50 rounded-lg p-3 text-xs">
            <div class="flex items-center gap-3 mb-1">
                <span class="font-bold ${color}">${c.status}</span>
                <span class="text-slate-400">用例 ${i+1}</span>
                <span class="text-slate-300">${c.time_ms.toFixed(1)}ms</span>
            </div>
            ${showDiff ? `<div class="grid grid-cols-2 gap-2 mt-2 font-mono">
                <div><p class="text-[10px] text-slate-400 uppercase mb-0.5">期望</p>${expandablePre(c.expected||'')}</div>
                <div><p class="text-[10px] text-slate-400 uppercase mb-0.5">${c.error?'错误':'实际'}</p>${expandablePre(c.error||c.actual||'')}</div>
            </div>` : ''}
        </div>`;
    }).join('');
}

// ==================== 自定义输入 ====================
function toggleCustomInput(forceClose) {
    const cb = document.getElementById('use-custom-input');
    if (forceClose === true) cb.checked = false;
    const show = cb.checked;
    document.getElementById('custom-input-panel').classList.toggle('hidden', !show);
    if (show) updateCustomInputHint();
}

function updateCustomInputHint() {
    const hint = document.getElementById('custom-input-hint');
    if (!hint || !currentProblem) return;
    // 取第一个测试用例的输入作为格式参考
    const tc = (currentProblem.test_cases || [])[0];
    if (tc) {
        const example = tc.input.length > 60 ? tc.input.substring(0, 60) + '...' : tc.input;
        hint.textContent = '格式参考: ' + example.replace(/\n/g, ' ↵ ');
    }
}

// ==================== 做题模式切换 ====================
function switchMode(mode) {
    if (mode === currentMode || !currentProblem) return;
    if (editor) { savedCode[currentMode] = editor.getValue(); saveDraft(); }
    currentMode = mode;
    updateModeUI();
    renderTestCases(currentProblem.test_cases || []);
    if (editor) {
        // 优先级：内存缓存 > localStorage 草稿 > 上次提交的代码由 loadProblem 已存 > 模板
        const draft = loadDraft(currentProblem.id, mode);
        const code = savedCode[mode] || draft || (mode === 'core'
            ? (currentProblem.lc_template || '# 该题暂无核心代码模板\n')
            : (currentProblem.template_code || getDefaultTemplate()));
        editor.setValue(code);
    }
}

function updateModeUI() {
    const acmBtn = document.getElementById('mode-btn-acm');
    const coreBtn = document.getElementById('mode-btn-core');
    const on = 'bg-white text-slate-900 shadow-sm';
    const off = 'text-slate-500 hover:text-slate-700';
    acmBtn.className = `px-3 py-1 rounded-md text-xs font-semibold transition-colors ${currentMode === 'acm' ? on : off}`;
    coreBtn.className = `px-3 py-1 rounded-md text-xs font-semibold transition-colors ${currentMode === 'core' ? on : off}`;
    // 仅当题目配置了核心代码模板时显示切换按钮
    const hasCore = currentProblem && currentProblem.lc_template;
    document.getElementById('mode-toggle').style.display = hasCore ? '' : 'none';
}

// ==================== 弹窗: 添加/编辑题目 ====================
function showAddModal() {
    document.getElementById('modal-title').textContent = '添加题目';
    document.getElementById('edit-problem-id').value = '';
    document.getElementById('form-title').value = '';
    document.getElementById('form-difficulty').value = 'Medium';
    document.getElementById('form-source').value = '';
    document.getElementById('form-source-url').value = '';
    document.getElementById('form-tags').value = '';
    document.getElementById('form-description').value = '';
    document.getElementById('form-template').value = '';
    document.getElementById('form-lc-template').value = '';
    document.getElementById('form-lc-wrapper').value = '';
    document.getElementById('form-testcases').innerHTML = '';
    addTcFormRow();
    document.getElementById('modal-overlay').classList.remove('hidden');
}

async function editProblem(pid) {
    const p = await (await fetch(`/api/problems/${pid}`)).json();
    document.getElementById('modal-title').textContent = '编辑题目';
    document.getElementById('edit-problem-id').value = pid;
    document.getElementById('form-title').value = p.title;
    document.getElementById('form-difficulty').value = p.difficulty;
    document.getElementById('form-source').value = p.source || '';
    document.getElementById('form-source-url').value = p.source_url || '';
    document.getElementById('form-tags').value = (p.tags||[]).join(', ');
    document.getElementById('form-description').value = p.description || '';
    document.getElementById('form-template').value = p.template_code || '';
    document.getElementById('form-lc-template').value = p.lc_template || '';
    document.getElementById('form-lc-wrapper').value = p.lc_wrapper || '';
    const tcContainer = document.getElementById('form-testcases');
    tcContainer.innerHTML = '';
    (p.test_cases||[]).forEach(tc => addTcFormRow(tc.input, tc.expected_output));
    if (!p.test_cases?.length) addTcFormRow();
    document.getElementById('modal-overlay').classList.remove('hidden');
}

function addTcFormRow(inp, out) {
    const div = document.createElement('div');
    div.className = 'flex gap-2 items-start';
    div.innerHTML = `
        <textarea class="tc-inp flex-1 px-2 py-1.5 rounded border border-slate-200 text-xs font-mono resize-none" rows="2" placeholder="输入">${esc(inp||'')}</textarea>
        <textarea class="tc-out flex-1 px-2 py-1.5 rounded border border-slate-200 text-xs font-mono resize-none" rows="2" placeholder="期望输出">${esc(out||'')}</textarea>
        <button onclick="this.parentElement.remove()" class="mt-1 text-slate-300 hover:text-red-500"><span class="material-symbols-outlined text-[16px]">close</span></button>`;
    document.getElementById('form-testcases').appendChild(div);
}

async function saveProblem() {
    const pid = document.getElementById('edit-problem-id').value;
    const title = document.getElementById('form-title').value.trim();
    if (!title) { alert('请输入题目标题'); return; }

    const tagsStr = document.getElementById('form-tags').value;
    const tags = tagsStr ? tagsStr.split(/[,，]/).map(t => t.trim()).filter(Boolean) : [];
    const testCases = [];
    document.querySelectorAll('#form-testcases > div').forEach(row => {
        const inp = row.querySelector('.tc-inp').value;
        const out = row.querySelector('.tc-out').value;
        if (inp || out) testCases.push({ input: inp, expected_output: out });
    });

    const data = {
        title, description: document.getElementById('form-description').value,
        difficulty: document.getElementById('form-difficulty').value, tags,
        source: document.getElementById('form-source').value.trim(),
        source_url: document.getElementById('form-source-url').value.trim(),
        template_code: document.getElementById('form-template').value,
        lc_template: document.getElementById('form-lc-template').value,
        lc_wrapper: document.getElementById('form-lc-wrapper').value,
        test_cases: testCases,
    };

    if (pid) {
        await fetch(`/api/problems/${pid}`, { method:'PUT', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) });
        const old = await (await fetch(`/api/problems/${pid}/testcases`)).json();
        for (const tc of old) await fetch(`/api/testcases/${tc.id}`, { method:'DELETE' });
        if (testCases.length) await fetch(`/api/problems/${pid}/testcases`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(testCases) });
    } else {
        await fetch('/api/problems', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) });
    }
    closeModal();
    loadHome();
}

async function deleteProblem(pid, title) {
    if (!confirm(`确定删除「${title}」？`)) return;
    await fetch(`/api/problems/${pid}`, { method:'DELETE' });
    loadHome();
}

function closeModal(e) {
    // 点击背景关闭时，检查表单是否有内容
    if (e && e.target !== e.currentTarget) return;
    if (e && modalHasContent() && !confirm('表单内容尚未保存，确定关闭？')) return;
    document.getElementById('modal-overlay').classList.add('hidden');
}
function modalHasContent() {
    return !!(document.getElementById('form-title').value.trim() || document.getElementById('form-description').value.trim());
}

// ==================== 弹窗: 添加测试用例 ====================
function showAddTcModal() {
    document.getElementById('tc-form-input').value = '';
    document.getElementById('tc-form-output').value = '';
    // 根据当前题目的已有用例生成格式提示
    const hint = document.getElementById('tc-format-hint');
    const tc = (currentProblem?.test_cases || [])[0];
    if (tc) {
        const inputLines = tc.input.split('\n');
        const numbered = inputLines.map(l => `<code class="bg-white px-1 rounded">${esc(l)}</code>`).join('<br>');
        hint.innerHTML = `
            <p class="font-semibold text-slate-600">输入格式参考（参照已有用例）:</p>
            <div class="font-mono mt-1">${numbered}</div>
            <p class="mt-1.5">对应输出: <code class="bg-white px-1 rounded font-mono">${esc(tc.expected_output)}</code></p>
            <p class="mt-1.5 text-slate-400">按相同格式填写新的测试数据即可。每行对应一组输入参数。</p>`;
        hint.classList.remove('hidden');
    } else {
        hint.innerHTML = `<p class="text-slate-400">该题暂无已有用例可参考，请按 ACM 格式填写：每行一组数据，通过标准输入读取。</p>`;
        hint.classList.remove('hidden');
    }
    document.getElementById('tc-modal').classList.remove('hidden');
}
function closeTcModal(e) {
    if (e && e.target !== e.currentTarget) return;
    document.getElementById('tc-modal').classList.add('hidden');
}

async function saveTestCase() {
    if (!currentProblem) return;
    await fetch(`/api/problems/${currentProblem.id}/testcases`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ input: document.getElementById('tc-form-input').value, expected_output: document.getElementById('tc-form-output').value }) });
    closeTcModal();
    currentProblem = await (await fetch(`/api/problems/${currentProblem.id}`)).json();
    renderTestCases(currentProblem.test_cases||[]);
}

async function deleteTestCase(id) {
    if (!confirm('删除此测试用例？')) return;
    await fetch(`/api/testcases/${id}`, { method:'DELETE' });
    currentProblem = await (await fetch(`/api/problems/${currentProblem.id}`)).json();
    renderTestCases(currentProblem.test_cases||[]);
}

// ==================== 导入导出 ====================
async function exportProblems() {
    const data = await (await fetch('/api/export')).json();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([JSON.stringify(data,null,2)], {type:'application/json'}));
    a.download = `acm_problems_${new Date().toISOString().slice(0,10)}.json`;
    a.click();
}

async function importProblems(e) {
    const file = e.target.files[0]; if(!file) return;
    try {
        const data = JSON.parse(await file.text());
        const res = await fetch('/api/import', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) });
        const r = await res.json();
        alert(r.message || r.error);
    } catch { alert('JSON 格式错误'); }
    e.target.value = '';
    loadHome();
}

// ==================== 工具 ====================
function esc(s) { if(!s) return ''; return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }

/** 可展开的 pre 块：超过 200 字符时截断并提供展开按钮 */
function expandablePre(text, limit = 200) {
    if (text.length <= limit) return `<pre class="whitespace-pre-wrap text-slate-600">${esc(text)}</pre>`;
    const id = 'exp_' + Math.random().toString(36).slice(2, 8);
    return `<pre id="${id}" class="whitespace-pre-wrap text-slate-600">${esc(text.substring(0, limit))}…</pre>
        <button onclick="document.getElementById('${id}').textContent=decodeURIComponent('${encodeURIComponent(text)}');this.remove()"
            class="text-primary text-[10px] hover:underline mt-0.5">展开全部</button>`;
}

/** 难度分布 AC 进度条 */
function renderDiffBar(s) {
    const levels = [
        { key: 'Easy', label: 'E', color: 'bg-green-400', bg: 'bg-green-100' },
        { key: 'Medium', label: 'M', color: 'bg-amber-400', bg: 'bg-amber-100' },
        { key: 'Hard', label: 'H', color: 'bg-red-400', bg: 'bg-red-100' },
    ];
    return levels.map(l => {
        const total = s.difficulty_counts?.[l.key] || 0;
        const ac = s.ac_by_difficulty?.[l.key] || 0;
        const pct = total > 0 ? Math.round(ac / total * 100) : 0;
        return `<div class="flex items-center gap-2 mt-1">
            <span class="text-[10px] text-slate-500 w-3 font-bold">${l.label}</span>
            <div class="flex-1 h-1.5 ${l.bg} rounded-full overflow-hidden">
                <div class="${l.color} h-full rounded-full transition-all" style="width:${pct}%"></div>
            </div>
            <span class="text-[10px] text-slate-500 w-8 text-right">${ac}/${total}</span>
        </div>`;
    }).join('');
}

/**
 * 核心代码模式：将原始输入按格式模板转为可读参数
 * 语法: {N} 整行, {N:M} 第N行第M个token, {N[]} 格式化为数组, {N..} 第N行起全部, {N..mat} 每行作为子数组
 */
function fmtCoreInput(raw, fmt) {
    if (!fmt) return raw;
    const L = raw.trim().split('\n').map(l => l.trim());
    return fmt.replace(/\{(\d+)(\.\.(?:mat)?)?(\[\])?(?::(\d+))?\}/g, (_, n, range, arr, tok) => {
        const idx = parseInt(n) - 1;
        if (range) {
            const rest = L.slice(idx);
            if (range === '..mat')
                return '[' + rest.map(l => '[' + l.split(/\s+/).join(', ') + ']').join(', ') + ']';
            return rest.join('\n');
        }
        const line = L[idx] || '';
        if (tok !== undefined) return line.split(/\s+/)[parseInt(tok) - 1] || '';
        if (arr) return '[' + line.split(/\s+/).join(', ') + ']';
        return line;
    });
}

// ==================== 初始化 ====================
document.addEventListener('DOMContentLoaded', () => {
    const lbl = document.getElementById('font-size-label');
    if (lbl) lbl.textContent = editorFontSize;
    navigate('home');
    // Escape 关闭弹窗
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') {
            const modal = document.getElementById('modal-overlay');
            const tcModal = document.getElementById('tc-modal');
            if (!tcModal.classList.contains('hidden')) { closeTcModal(); return; }
            if (!modal.classList.contains('hidden')) { closeModal(); }
        }
    });
    // 页面关闭前保存草稿
    window.addEventListener('beforeunload', saveDraft);
});
