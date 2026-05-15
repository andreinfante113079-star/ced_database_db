<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Primary Structures — Dashboard</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root {
    --brown: #7a4a23; --brown-dark: #5e3818;
    --navy: #18345b; --navy-light: #2a4a7a;
    --bg: #f5f7fa; --card: #ffffff; --border: #e4e8ef;
    --text: #1a1f2e; --text-muted: #6b7280; --text-soft: #9aa3b2;
    --accent: #c47a36; --completed: #18345b;
    --shadow-sm: 0 1px 2px rgba(15,23,42,.04), 0 1px 3px rgba(15,23,42,.04);
    --shadow-md: 0 2px 6px rgba(15,23,42,.06), 0 4px 12px rgba(15,23,42,.04);
    --radius: 12px; --sidebar-w: 260px;
  }
  [data-theme="dark"] {
    --bg: #0f1420; --card: #1a2030; --border: #2a3245;
    --text: #e8ecf3; --text-muted: #9aa3b2; --text-soft: #6b7280;
    --shadow-sm: 0 1px 2px rgba(0,0,0,.3); --shadow-md: 0 4px 12px rgba(0,0,0,.35);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Inter', -apple-system, sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; transition: background .25s ease, color .25s ease; }
  h1, h2, h3, h4 { font-family: 'Plus Jakarta Sans', sans-serif; letter-spacing: -0.02em; }
  .layout { display: grid; grid-template-columns: 1fr var(--sidebar-w); min-height: 100vh; }
  .main { display: flex; flex-direction: column; min-width: 0; }
  .topbar { background: linear-gradient(135deg, var(--brown) 0%, var(--brown-dark) 100%); color: #fff; padding: 22px 36px; display: flex; align-items: center; justify-content: space-between; box-shadow: var(--shadow-sm); }
  .topbar h1 { font-size: 22px; font-weight: 700; }
  .topbar-actions { display: flex; gap: 10px; align-items: center; }
  .icon-btn { width: 38px; height: 38px; background: rgba(255,255,255,.95); border: none; border-radius: 8px; cursor: pointer; display: grid; place-items: center; color: var(--brown-dark); transition: all .15s ease; }
  .icon-btn:hover { transform: translateY(-1px); background: #fff; }
  .icon-btn svg { width: 18px; height: 18px; }
  .rebuild-btn { background: rgba(255,255,255,.95); color: var(--brown-dark); border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 13px; display: inline-flex; align-items: center; gap: 7px; transition: all .15s ease; font-family: inherit; text-decoration: none; }
  .rebuild-btn:hover { transform: translateY(-1px); background: #fff; }
  .rebuild-btn svg { width: 14px; height: 14px; }
  .content { flex: 1; padding: 36px; overflow-x: hidden; }
  .greeting { margin-bottom: 28px; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 12px; }
  .greeting h2 { font-size: 38px; font-weight: 800; margin-bottom: 4px; }
  .greeting p { color: var(--text-muted); font-size: 15px; }
  .last-updated { font-size: 12px; color: var(--text-soft); }
  .last-updated b { color: var(--text-muted); font-weight: 600; }
  .card { background: var(--card); border: 1px solid var(--border); border-radius: var(--radius); padding: 24px; box-shadow: var(--shadow-sm); transition: box-shadow .2s ease; }
  .card:hover { box-shadow: var(--shadow-md); }
  .card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 18px; }
  .card-title { font-size: 12px; font-weight: 700; letter-spacing: 0.08em; color: var(--text-muted); text-transform: uppercase; }
  .card-sub { font-size: 13px; color: var(--text-soft); margin-top: 2px; }
  .card-icon { color: var(--accent); opacity: .85; }
  .grid-top, .grid-mid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
  .stat-number { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 56px; font-weight: 800; line-height: 1; color: var(--text); margin: 8px 0 6px; }
  .stat-label { font-size: 11px; letter-spacing: 0.1em; color: var(--text-soft); text-transform: uppercase; font-weight: 600; }
  .stat-mini { display: flex; gap: 18px; margin-top: 14px; padding-top: 14px; border-top: 1px dashed var(--border); flex-wrap: wrap; }
  .stat-mini > div { font-size: 11px; color: var(--text-muted); }
  .stat-mini strong { display: block; font-size: 15px; color: var(--text); margin-bottom: 1px; font-family: 'Plus Jakarta Sans'; font-weight: 700; }
  .chart-wrap { position: relative; height: 240px; width: 100%; }
  .chart-wrap.tall { height: 280px; }
  .activities { display: flex; flex-direction: column; gap: 12px; }
  .row { display: flex; align-items: center; gap: 16px; padding: 16px 20px; border: 1px solid var(--border); border-radius: 10px; background: var(--card); transition: all .15s ease; }
  .row:hover { border-color: var(--navy); transform: translateX(2px); }
  .row .ico { width: 44px; height: 44px; border-radius: 10px; background: rgba(24,52,91,.08); color: var(--navy); display: grid; place-items: center; flex-shrink: 0; }
  [data-theme="dark"] .row .ico { background: rgba(196,122,54,.15); color: var(--accent); }
  .row .info { flex: 1; min-width: 0; }
  .row .name { font-weight: 700; font-size: 14px; letter-spacing: 0.02em; }
  .row .meta { font-size: 12px; color: var(--text-soft); margin-top: 3px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .badge { background: var(--completed); color: #fff; font-size: 11px; padding: 5px 12px; border-radius: 999px; font-weight: 600; letter-spacing: 0.03em; }
  .btn-view { background: transparent; border: 1px solid var(--border); color: var(--text-muted); font-size: 12px; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-weight: 600; font-family: inherit; transition: all .15s ease; }
  .btn-view:hover { background: var(--bg); color: var(--text); }
  .show-more { background: transparent; border: 1px dashed var(--border); color: var(--text-muted); padding: 10px; border-radius: 8px; cursor: pointer; font-family: inherit; font-size: 13px; margin-top: 4px; transition: all .15s ease; }
  .show-more:hover { background: var(--bg); color: var(--text); border-style: solid; }
  .search-card { margin-bottom: 24px; }
  .search-header { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
  .search-header h3 { font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-muted); }
  .search-card .desc { color: var(--text-soft); font-size: 13px; margin-bottom: 20px; }
  .filter-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 18px; }
  .filter-field label { display: block; font-size: 10px; letter-spacing: 0.1em; color: var(--text-muted); text-transform: uppercase; font-weight: 700; margin-bottom: 6px; }
  .filter-field select { width: 100%; padding: 10px 12px; background: var(--card); border: 1px solid var(--border); border-radius: 8px; font-size: 13px; font-family: inherit; color: var(--text); cursor: pointer; appearance: none; background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='12' fill='none' stroke='%236b7280' stroke-width='2' viewBox='0 0 24 24'%3E%3Cpath d='M6 9l6 6 6-6'/%3E%3C/svg%3E"); background-repeat: no-repeat; background-position: right 12px center; padding-right: 32px; }
  .filter-field select:focus { outline: none; border-color: var(--navy); box-shadow: 0 0 0 3px rgba(24,52,91,.08); }
  .btn-search { background: var(--navy); color: #fff; border: none; padding: 11px 22px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 13px; display: inline-flex; align-items: center; gap: 8px; transition: all .15s ease; font-family: inherit; }
  .btn-search:hover { background: var(--navy-light); transform: translateY(-1px); }
  .btn-search svg { width: 14px; height: 14px; }
  .btn-reset { background: transparent; color: var(--text-muted); border: 1px solid var(--border); padding: 11px 18px; border-radius: 8px; cursor: pointer; font-size: 13px; font-weight: 500; font-family: inherit; margin-left: 8px; transition: all .15s ease; }
  .btn-reset:hover { background: var(--bg); color: var(--text); }
  .search-results { margin-top: 18px; padding-top: 18px; border-top: 1px dashed var(--border); font-size: 13px; color: var(--text-muted); }
  .result-list { margin-top: 14px; display: flex; flex-direction: column; gap: 8px; max-height: 380px; overflow-y: auto; padding-right: 4px; }
  .result-list::-webkit-scrollbar { width: 6px; }
  .result-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
  .sidebar { background: var(--card); border-left: 1px solid var(--border); display: flex; flex-direction: column; position: sticky; top: 0; height: 100vh; overflow-y: auto; }
  .sb-brand { padding: 22px 24px; display: flex; align-items: center; gap: 12px; border-bottom: 1px solid var(--border); }
  .sb-brand .logo { width: 36px; height: 36px; background: var(--card); border: 1.5px solid var(--text); border-radius: 8px; display: grid; place-items: center; transform: rotate(45deg); }
  .sb-brand .logo span { transform: rotate(-45deg); font-weight: 800; font-family: 'Plus Jakarta Sans', sans-serif; color: var(--text); font-size: 15px; }
  .sb-brand h4 { font-size: 15px; font-weight: 700; }
  .sb-nav { flex: 1; padding: 16px 14px; display: flex; flex-direction: column; gap: 2px; }
  .nav-item { display: flex; align-items: center; gap: 12px; padding: 10px 12px; border-radius: 8px; color: var(--text-muted); font-size: 14px; font-weight: 500; cursor: pointer; transition: all .15s ease; border: none; background: none; width: 100%; text-align: left; font-family: inherit; }
  .nav-item:hover { background: var(--bg); color: var(--text); }
  .nav-item.active { color: var(--text); background: var(--bg); }
  .nav-item svg { width: 18px; height: 18px; flex-shrink: 0; }
  .nav-item .chev { margin-left: auto; transition: transform .2s ease; }
  .nav-item.open .chev { transform: rotate(180deg); }
  .nav-children { display: none; padding-left: 24px; flex-direction: column; gap: 2px; margin-top: 2px; }
  .nav-group.open .nav-children { display: flex; }
  .nav-child { padding: 8px 12px; color: var(--text-muted); font-size: 13px; border-radius: 6px; cursor: pointer; transition: all .15s ease; }
  .nav-child:hover { background: var(--bg); color: var(--text); }
  .sb-user { padding: 16px 18px; border-top: 1px solid var(--border); display: flex; align-items: center; gap: 12px; }
  .sb-user .avatar { width: 36px; height: 36px; background: var(--bg); border: 1px solid var(--border); border-radius: 8px; display: grid; place-items: center; font-weight: 700; font-size: 12px; color: var(--text); }
  .sb-user .name { font-size: 13px; font-weight: 600; }
  .sb-user .role { font-size: 11px; color: var(--text-soft); }
  .modal-overlay { position: fixed; inset: 0; background: rgba(15,23,42,.55); display: none; align-items: center; justify-content: center; z-index: 100; padding: 20px; }
  .modal-overlay.show { display: flex; animation: fadeIn .2s ease; }
  .modal { background: var(--card); border-radius: 14px; max-width: 720px; width: 100%; max-height: 88vh; overflow-y: auto; box-shadow: 0 25px 60px rgba(0,0,0,.3); animation: rise .25s ease; }
  .modal-head { padding: 22px 26px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; gap: 16px; }
  .modal-head h3 { font-size: 18px; font-weight: 800; }
  .modal-head .sub { font-size: 12px; color: var(--text-soft); margin-top: 4px; }
  .modal-close { background: none; border: none; cursor: pointer; color: var(--text-muted); font-size: 24px; padding: 0 4px; }
  .modal-body { padding: 22px 26px; display: grid; grid-template-columns: 1fr 1fr; gap: 14px 24px; }
  .field { font-size: 12px; }
  .field .lbl { color: var(--text-soft); text-transform: uppercase; letter-spacing: 0.06em; font-size: 10px; font-weight: 700; margin-bottom: 3px; }
  .field .val { color: var(--text); font-size: 13px; font-weight: 500; }
  .ratios-block { grid-column: span 2; margin-top: 8px; padding-top: 16px; border-top: 1px dashed var(--border); }
  .ratios-block h4 { font-size: 11px; letter-spacing: 0.1em; color: var(--text-muted); text-transform: uppercase; margin-bottom: 10px; }
  .ratios-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
  .ratio { background: var(--bg); border-radius: 8px; padding: 12px; }
  .ratio .v { font-family: 'Plus Jakarta Sans'; font-weight: 700; font-size: 17px; color: var(--text); }
  .ratio .k { font-size: 10px; color: var(--text-soft); text-transform: uppercase; letter-spacing: 0.06em; margin-top: 2px; }
  .loading { padding: 60px 20px; text-align: center; color: var(--text-muted); }
  .loading-spinner { width: 32px; height: 32px; border: 3px solid var(--border); border-top-color: var(--navy); border-radius: 50%; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
  .error { padding: 30px; text-align: center; color: #b91c1c; background: #fef2f2; border: 1px solid #fecaca; border-radius: 10px; margin: 20px 0; }
  [data-theme="dark"] .error { background: rgba(220,38,38,.1); color: #fca5a5; border-color: rgba(220,38,38,.3); }
  @media (max-width: 1100px) {
    .layout { grid-template-columns: 1fr; }
    .sidebar { display: none; }
    .grid-top, .grid-mid { grid-template-columns: 1fr; }
    .filter-grid { grid-template-columns: repeat(2, 1fr); }
    .content { padding: 24px; }
    .greeting h2 { font-size: 30px; }
    .modal-body { grid-template-columns: 1fr; }
    .ratios-block { grid-column: span 1; }
  }
  @media (max-width: 560px) {
    .filter-grid { grid-template-columns: 1fr; }
    .topbar { padding: 18px 22px; }
    .content { padding: 20px; }
    .row { flex-wrap: wrap; }
    .ratios-grid { grid-template-columns: repeat(2, 1fr); }
  }
  .card, .row { animation: rise .5s ease both; }
  @keyframes rise { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>
<div class="layout">
  <div class="main">
    <header class="topbar">
      <h1>Dashboard</h1>
      <div class="topbar-actions">
        <a id="rebuildLink" class="rebuild-btn" href="#" target="_blank" rel="noopener" title="Rebuild dashboard from latest Excel">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/><path d="M3 21v-5h5"/></svg>
          Rebuild
        </a>
        <button class="icon-btn" id="themeBtn" title="Toggle theme">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/></svg>
        </button>
      </div>
    </header>

    <div class="content">
      <div class="greeting">
        <div>
          <h2>Dashboard</h2>
          <p>Welcome back, Super Admin!</p>
        </div>
        <div class="last-updated" id="lastUpdated"></div>
      </div>

      <div id="loadingState" class="loading">
        <div class="loading-spinner"></div>
        <div>Loading project data...</div>
      </div>

      <div id="dashboardContent" style="display:none;">
        <div class="grid-top">
          <div class="card">
            <div class="card-header">
              <div class="card-title">Projects Uploaded</div>
              <div class="card-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9l-5 5"/><path d="m4 20 4-4"/><path d="m18 4 2 2"/><path d="m14 6 6 6-3 3-6-6 3-3"/></svg>
              </div>
            </div>
            <div class="stat-number" id="totalProjects">0</div>
            <div class="stat-label">Total Projects</div>
            <div class="stat-mini" id="topMetrics"></div>
          </div>

          <div class="card">
            <div class="card-header"><div class="card-title">Year</div></div>
            <div class="chart-wrap"><canvas id="yearChart"></canvas></div>
          </div>
        </div>

        <div class="grid-mid">
          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">Building Categories</div>
                <div class="card-sub">Projects per category (from project table)</div>
              </div>
            </div>
            <div class="chart-wrap tall"><canvas id="categoryChart"></canvas></div>
          </div>

          <div class="card">
            <div class="card-header">
              <div>
                <div class="card-title">Type of Occupancy</div>
                <div class="card-sub">Projects per type (from project table)</div>
              </div>
            </div>
            <div class="chart-wrap tall"><canvas id="occupancyChart"></canvas></div>
          </div>
        </div>

        <div class="card" style="margin-bottom:24px;">
          <div class="card-header">
            <div>
              <div class="card-title">Recent Activities</div>
              <div class="card-sub">Latest project updates</div>
            </div>
          </div>
          <div class="activities" id="activities"></div>
          <button class="show-more" id="showMoreBtn" style="display:none;">Show all projects</button>
        </div>

        <div class="card search-card">
          <div class="search-header">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="color:var(--text-muted)"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
            <h3>Search</h3>
          </div>
          <p class="desc">Filter projects by lookup table values, then open the projects list.</p>

          <div class="filter-grid">
            <div class="filter-field"><label>Type of Occupancy</label><select id="f-occupancy"></select></div>
            <div class="filter-field"><label>Building Category</label><select id="f-category"></select></div>
            <div class="filter-field"><label>Designer</label><select id="f-designer"></select></div>
            <div class="filter-field"><label>Type of Foundation</label><select id="f-foundation"></select></div>
            <div class="filter-field"><label>Construction Approach</label><select id="f-approach"></select></div>
          </div>

          <button class="btn-search" id="searchBtn">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
            Search projects
          </button>
          <button class="btn-reset" id="resetBtn">Reset filters</button>

          <div class="search-results" id="searchResults" style="display:none;"></div>
        </div>
      </div>
    </div>
  </div>

  <aside class="sidebar">
    <div class="sb-brand">
      <div class="logo"><span>S</span></div>
      <h4>Primary Structures</h4>
    </div>
    <nav class="sb-nav">
      <button class="nav-item active">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
        Dashboard
      </button>
      <button class="nav-item">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9l-5 5"/><path d="m4 20 4-4"/><path d="m18 4 2 2"/><path d="m14 6 6 6-3 3-6-6 3-3"/></svg>
        Projects
      </button>
      <div class="nav-group open" id="lookupGroup">
        <button class="nav-item open" onclick="toggleGroup('lookupGroup', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18M15 3v18"/></svg>
          Lookup Tables
          <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
        </button>
        <div class="nav-children">
          <div class="nav-child">Owners</div>
          <div class="nav-child">Type of Occupancy</div>
          <div class="nav-child">Building Category</div>
          <div class="nav-child">Designer</div>
          <div class="nav-child">Type of Foundation</div>
          <div class="nav-child">Construction Approach</div>
        </div>
      </div>
      <div class="nav-group" id="usersGroup">
        <button class="nav-item" onclick="toggleGroup('usersGroup', this)">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 11l-3 3-2-2"/></svg>
          Users and Roles
          <svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m6 9 6 6 6-6"/></svg>
        </button>
        <div class="nav-children">
          <div class="nav-child">Users</div>
          <div class="nav-child">Roles</div>
        </div>
      </div>
    </nav>
    <div class="sb-user">
      <div class="avatar">SA</div>
      <div>
        <div class="name">Super Admin</div>
        <div class="role">Super Admin</div>
      </div>
    </div>
  </aside>
</div>

<div class="modal-overlay" id="modal">
  <div class="modal">
    <div class="modal-head">
      <div>
        <h3 id="m-name"></h3>
        <div class="sub" id="m-sub"></div>
      </div>
      <button class="modal-close" onclick="closeModal()">×</button>
    </div>
    <div class="modal-body" id="m-body"></div>
  </div>
</div>

<!-- Configuration: edit the REBUILD_URL below to point at your GitHub Actions workflow page -->
<script>
  // CHANGE THIS to your GitHub Actions workflow URL after deploying
  // Example: https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/rebuild.yml
  const REBUILD_URL = 'REPLACE_WITH_YOUR_GITHUB_ACTIONS_URL';
</script>

<script>
let PROJECTS = [];
let UPDATED_AT = null;

document.getElementById('rebuildLink').href = REBUILD_URL;

document.getElementById('themeBtn').addEventListener('click', () => {
  const cur = document.body.getAttribute('data-theme');
  document.body.setAttribute('data-theme', cur === 'dark' ? '' : 'dark');
  if (PROJECTS.length) rebuildCharts();
});

function toggleGroup(id, btn) {
  document.getElementById(id).classList.toggle('open');
  btn.classList.toggle('open');
}

function fmt(n, d=0) {
  if (n === null || n === undefined || isNaN(n)) return '—';
  return Number(n).toLocaleString('en-US', { maximumFractionDigits: d, minimumFractionDigits: d });
}
function fmtCompact(n) {
  if (n === null || n === undefined || isNaN(n)) return '—';
  if (n >= 1e6) return (n/1e6).toFixed(1) + 'M';
  if (n >= 1e3) return (n/1e3).toFixed(1) + 'k';
  return Math.round(n).toString();
}

// Load data from projects.json with cache busting
async function loadData() {
  try {
    const res = await fetch('projects.json?t=' + Date.now());
    if (!res.ok) throw new Error('HTTP ' + res.status);
    const data = await res.json();
    PROJECTS = data.projects || [];
    UPDATED_AT = data.updatedAt;
    render();
  } catch (err) {
    document.getElementById('loadingState').innerHTML = `
      <div class="error">
        <strong>Could not load project data.</strong><br>
        ${err.message}<br><br>
        <small>Make sure projects.json has been generated. Click the Rebuild button to generate it from the latest Excel file.</small>
      </div>`;
  }
}

function render() {
  document.getElementById('loadingState').style.display = 'none';
  document.getElementById('dashboardContent').style.display = 'block';

  if (UPDATED_AT) {
    const d = new Date(UPDATED_AT);
    document.getElementById('lastUpdated').innerHTML =
      `<b>Last updated:</b> ${d.toLocaleString()}`;
  }

  document.getElementById('totalProjects').textContent = PROJECTS.length;
  const totalTFA = PROJECTS.reduce((s,p) => s + (p.tfa || 0), 0);
  const totalConcrete = PROJECTS.reduce((s,p) => s + (p.concrete || 0), 0);
  const totalRebar = PROJECTS.reduce((s,p) => s + (p.rebar || 0), 0);
  document.getElementById('topMetrics').innerHTML = `
    <div><strong>${fmtCompact(totalTFA)}</strong>Total TFA (sqm)</div>
    <div><strong>${fmtCompact(totalConcrete)}</strong>Concrete (cu.m)</div>
    <div><strong>${fmtCompact(totalRebar)}</strong>Rebar (kg)</div>
  `;

  renderActivities();
  buildCharts();
  populateFilters();
}

let activitiesExpanded = false;
function renderActivities() {
  const el = document.getElementById('activities');
  const more = document.getElementById('showMoreBtn');
  const list = activitiesExpanded ? PROJECTS : PROJECTS.slice(0, 5);
  el.innerHTML = list.map((p) => {
    const realIdx = PROJECTS.indexOf(p);
    return `
    <div class="row" data-idx="${realIdx}">
      <div class="ico"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9l-5 5"/><path d="m4 20 4-4"/><path d="m18 4 2 2"/><path d="m14 6 6 6-3 3-6-6 3-3"/></svg></div>
      <div class="info">
        <div class="name">${p.name || '—'}</div>
        <div class="meta">${[p.location, p.year, p.category].filter(Boolean).join(' • ')}</div>
      </div>
      <span class="badge">completed</span>
      <button class="btn-view" data-idx="${realIdx}">View</button>
    </div>`;
  }).join('');
  el.querySelectorAll('.btn-view, .row').forEach(elx => {
    elx.addEventListener('click', e => {
      e.stopPropagation();
      openModal(parseInt(elx.dataset.idx));
    });
  });
  more.style.display = PROJECTS.length > 5 ? 'block' : 'none';
  more.textContent = activitiesExpanded ? 'Show fewer' : `Show all ${PROJECTS.length} projects`;
}
document.getElementById('showMoreBtn').addEventListener('click', () => {
  activitiesExpanded = !activitiesExpanded;
  renderActivities();
});

function openModal(idx) {
  const p = PROJECTS[idx];
  if (!p) return;
  document.getElementById('m-name').textContent = p.name || '—';
  document.getElementById('m-sub').textContent = [p.owner, p.location].filter(Boolean).join(' · ');
  const fields = [
    ['Year', p.year], ['Occupancy', p.occupancy], ['Building Category', p.category],
    ['Designer', p.designer], ['TFA (sqm)', fmt(p.tfa, 2)], ['Footprint (sqm)', fmt(p.footprint, 2)],
    ['Units', fmt(p.units)], ['Height (m)', fmt(p.height, 1)], ['Levels', fmt(p.levels)],
    ['Foundation', p.foundation], ['Construction Approach', p.approach],
    ['Concrete (cu.m)', fmt(p.concrete, 2)], ['Rebar (kg)', fmt(p.rebar, 0)], ['Forms (sq.m)', fmt(p.forms, 2)],
  ];
  let html = fields.map(([k,v]) => `<div class="field"><div class="lbl">${k}</div><div class="val">${v || '—'}</div></div>`).join('');
  html += `
    <div class="ratios-block">
      <h4>Engineering Ratios</h4>
      <div class="ratios-grid">
        <div class="ratio"><div class="v">${fmt(p.cumTfa, 3)}</div><div class="k">cu.m / TFA</div></div>
        <div class="ratio"><div class="v">${fmt(p.kgTfa, 2)}</div><div class="k">kg / TFA</div></div>
        <div class="ratio"><div class="v">${fmt(p.sqmTfa, 3)}</div><div class="k">sq.m / TFA</div></div>
      </div>
    </div>`;
  document.getElementById('m-body').innerHTML = html;
  document.getElementById('modal').classList.add('show');
}
function closeModal() { document.getElementById('modal').classList.remove('show'); }
document.getElementById('modal').addEventListener('click', e => { if (e.target.id === 'modal') closeModal(); });
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

let yearChart, categoryChart, occupancyChart;

function chartText() { return getComputedStyle(document.body).getPropertyValue('--text-muted').trim() || '#6b7280'; }
function chartBorder() { return getComputedStyle(document.body).getPropertyValue('--border').trim() || '#e4e8ef'; }

function countBy(arr, key) {
  const out = {};
  arr.forEach(p => { const k = p[key]; if (k) out[k] = (out[k]||0) + 1; });
  return out;
}

function buildCharts() {
  const yearCounts = {};
  PROJECTS.forEach(p => {
    const y = p.yearStart || '—';
    yearCounts[y] = (yearCounts[y] || 0) + 1;
  });
  const yearKeys = Object.keys(yearCounts).sort((a,b) => {
    if (a === '—') return 1; if (b === '—') return -1;
    return Number(a) - Number(b);
  });

  yearChart = new Chart(document.getElementById('yearChart'), {
    type: 'bar',
    data: { labels: yearKeys, datasets: [{ data: yearKeys.map(k => yearCounts[k]), backgroundColor: '#18345b', borderRadius: 4, maxBarThickness: 28 }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } },
      scales: { x: { grid: { display: false }, ticks: { color: chartText(), font: { size: 10 } } },
                y: { beginAtZero: true, grid: { color: chartBorder() }, ticks: { color: chartText(), stepSize: 1, font: { size: 10 } } } } }
  });

  const cats = countBy(PROJECTS, 'category');
  const catLabels = Object.keys(cats);
  const palette = ['#7a4a23','#2d4555','#2f6fc6','#a86a30','#d8a93a','#c47a36','#8a5520','#3f6b8b','#5e3818'];
  categoryChart = new Chart(document.getElementById('categoryChart'), {
    type: 'pie',
    data: { labels: catLabels, datasets: [{ data: catLabels.map(k => cats[k]), backgroundColor: palette, borderWidth: 2, borderColor: getComputedStyle(document.body).getPropertyValue('--card').trim() || '#fff' }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: chartText(), font: { size: 11 }, padding: 10, boxWidth: 12 } } } }
  });

  const occ = countBy(PROJECTS, 'occupancy');
  const occLabels = Object.keys(occ);
  occupancyChart = new Chart(document.getElementById('occupancyChart'), {
    type: 'pie',
    data: { labels: occLabels, datasets: [{ data: occLabels.map(k => occ[k]), backgroundColor: palette, borderWidth: 2, borderColor: getComputedStyle(document.body).getPropertyValue('--card').trim() || '#fff' }] },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: chartText(), font: { size: 11 }, padding: 10, boxWidth: 12 } } } }
  });
}

function rebuildCharts() {
  [yearChart, categoryChart, occupancyChart].forEach(c => c && c.destroy());
  buildCharts();
}

function uniqueVals(key) {
  return [...new Set(PROJECTS.map(p => p[key]).filter(Boolean))].sort();
}
function fillSelect(id, vals) {
  document.getElementById(id).innerHTML =
    '<option value="">All</option>' + vals.map(v => `<option value="${v}">${v}</option>`).join('');
}
function populateFilters() {
  fillSelect('f-occupancy', uniqueVals('occupancy'));
  fillSelect('f-category', uniqueVals('category'));
  fillSelect('f-designer', uniqueVals('designer'));
  fillSelect('f-foundation', uniqueVals('foundation'));
  fillSelect('f-approach', uniqueVals('approach'));
}

document.getElementById('searchBtn').addEventListener('click', runSearch);
document.getElementById('resetBtn').addEventListener('click', () => {
  ['f-occupancy','f-category','f-designer','f-foundation','f-approach'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('searchResults').style.display = 'none';
});

function runSearch() {
  const f = {
    occupancy: document.getElementById('f-occupancy').value,
    category:  document.getElementById('f-category').value,
    designer:  document.getElementById('f-designer').value,
    foundation:document.getElementById('f-foundation').value,
    approach:  document.getElementById('f-approach').value,
  };
  const matches = PROJECTS.filter(p =>
    (!f.occupancy  || p.occupancy === f.occupancy) &&
    (!f.category   || p.category === f.category) &&
    (!f.designer   || p.designer === f.designer) &&
    (!f.foundation || p.foundation === f.foundation) &&
    (!f.approach   || p.approach === f.approach)
  );
  const active = Object.entries(f).filter(([,v]) => v).map(([k,v]) => `<strong>${k}</strong>: ${v}`).join(' · ') || '<em>No filters applied</em>';
  const out = document.getElementById('searchResults');
  out.style.display = 'block';
  let html = `<div style="margin-bottom:6px;">Filters → ${active}</div>
              <div>Found <strong style="color:var(--text)">${matches.length}</strong> project${matches.length===1?'':'s'}.</div>`;
  if (matches.length > 0) {
    html += `<div class="result-list">${matches.map((p) => {
      const realIdx = PROJECTS.indexOf(p);
      return `<div class="row" style="padding:12px 16px;">
        <div class="ico" style="width:36px;height:36px;"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 9l-5 5"/><path d="m4 20 4-4"/><path d="m18 4 2 2"/><path d="m14 6 6 6-3 3-6-6 3-3"/></svg></div>
        <div class="info"><div class="name" style="font-size:13px;">${p.name || '—'}</div><div class="meta">${[p.location, p.year].filter(Boolean).join(' • ')}</div></div>
        <button class="btn-view" data-idx="${realIdx}">View</button>
      </div>`;
    }).join('')}</div>`;
  }
  out.innerHTML = html;
  out.querySelectorAll('.btn-view').forEach(btn => {
    btn.addEventListener('click', () => openModal(parseInt(btn.dataset.idx)));
  });
}

loadData();
</script>
</body>
</html>
