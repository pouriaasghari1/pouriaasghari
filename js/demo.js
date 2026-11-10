/* ==========================================================================
   Pouria Business — Product Demonstrations
   Working in-browser simulations of the catalog systems, running on clearly
   labelled sample data. Nothing here is a live business figure.
   ========================================================================== */
(function () {
  'use strict';

  var DEMOS = {
    inventory: {
      kicker: 'Inventory System',
      title: 'Stock command demo',
      lede: 'Watch reorder flags recalculate as you pick stock, sell units, or receive a delivery. Every number below is generated sample data.',
      kpis: [
        { label: 'Inventory value', get: function (s) { return money(s.reduce(function (t, p) { return t + p.onHand * p.cost; }, 0)); } },
        { label: 'Active SKUs', get: function (s) { return String(s.length); } },
        { label: 'Below reorder point', get: function (s) { return String(s.filter(function (p) { return p.onHand <= p.reorder; }).length); } },
        { label: 'Units on hand', get: function (s) { return num(s.reduce(function (t, p) { return t + p.onHand; }, 0)); } }
      ],
      columns: ['SKU', 'Product', 'On hand', 'Reorder at', 'Unit cost', 'Status', 'Action'],
      seed: function () {
        return [
          { sku: 'SKU-10482', name: 'Arctic Pro Headphones', onHand: 18, reorder: 40, cost: 46.5, lead: 6 },
          { sku: 'SKU-20915', name: 'Linen Blend Overshirt', onHand: 64, reorder: 90, cost: 18.2, lead: 12 },
          { sku: 'SKU-33107', name: 'Ceramic Pour-Over Set', onHand: 142, reorder: 80, cost: 12.4, lead: 9 },
          { sku: 'SKU-41860', name: 'Everyday Cotton Tote', onHand: 9, reorder: 120, cost: 4.8, lead: 4 },
          { sku: 'SKU-52240', name: 'Walnut Desk Organiser', onHand: 88, reorder: 60, cost: 22.9, lead: 15 }
        ];
      },
      row: function (p) {
        var status = p.onHand <= 0 ? ['Out of stock', 'danger']
          : p.onHand <= p.reorder * 0.5 ? ['Critical', 'danger']
          : p.onHand <= p.reorder ? ['Reorder now', 'warn']
          : ['Healthy', 'ok'];
        return {
          badge: status,
          cells: [p.sku, p.name, String(p.onHand), String(p.reorder), money(p.cost)],
          actions: [
            { id: 'sell', label: 'Sell 10' },
            { id: 'receive', label: 'Receive 50' }
          ]
        };
      },
      act: function (id, p) {
        if (id === 'sell') {
          if (p.onHand === 0) return 'This SKU is already out of stock.';
          p.onHand = Math.max(0, p.onHand - 10);
          return 'Recorded a sale of 10 units · status recalculated.';
        }
        if (id === 'receive') {
          p.onHand += 50;
          return 'Purchase order received: +50 units.';
        }
      },
      insight: [
        'The status column is driven by a single rule: on-hand against the reorder point.',
        'Lead time feeds the suggested order quantity — short-lead items reorder later, longer-lead items earlier.',
        'Change a reorder point and every flag, alert and dashboard card updates together.'
      ],
      schema: [['Table', 'tbl_Stock'], ['Key', 'SKU'], ['Reorder rule', 'on_hand < reorder_point'], ['Refresh', 'On edit + nightly sync']]
    },

    sales: {
      kicker: 'Sales System',
      title: 'Revenue demo',
      lede: 'Log sample sales and the KPIs, channel mix and top-products table update instantly. The logic mirrors a real sales workbook.',
      kpis: [
        { label: 'Net revenue', get: function (s) { return money(s.reduce(function (t, r) { return t + r.qty * r.price; }, 0)); } },
        { label: 'Orders logged', get: function (s) { return String(s.length); } },
        { label: 'Average order value', get: function (s) { return s.length ? money(s.reduce(function (t, r) { return t + r.qty * r.price; }, 0) / s.length) : money(0); } },
        { label: 'Units sold', get: function (s) { return num(s.reduce(function (t, r) { return t + r.qty; }, 0)); } }
      ],
      columns: ['Order', 'Product', 'Channel', 'Qty', 'Unit price', 'Total', ''],
      seed: function () {
        return [
          { id: 'SO-2041', product: 'Arctic Pro Headphones', channel: 'Retail', qty: 2, price: 129 },
          { id: 'SO-2042', product: 'Linen Blend Overshirt', channel: 'Online', qty: 3, price: 64 },
          { id: 'SO-2043', product: 'Ceramic Pour-Over Set', channel: 'Retail', qty: 1, price: 89 },
          { id: 'SO-2044', product: 'Walnut Desk Organiser', channel: 'Online', qty: 2, price: 74 }
        ];
      },
      row: function (r) {
        return {
          cells: [r.id, r.product, r.channel, String(r.qty), money(r.price), money(r.qty * r.price)],
          actions: [{ id: 'remove', label: 'Remove', tone: 'ghost' }]
        };
      },
      act: function (id, row, list) {
        if (id === 'remove') {
          list.splice(list.indexOf(row), 1);
          return 'Order removed — totals recalculated.';
        }
      },
      extra: function (s) {
        var byChannel = {};
        s.forEach(function (r) { byChannel[r.channel] = (byChannel[r.channel] || 0) + r.qty * r.price; });
        var total = s.reduce(function (t, r) { return t + r.qty * r.price; }, 0) || 1;
        var byProduct = {};
        s.forEach(function (r) {
          byProduct[r.product] = (byProduct[r.product] || 0) + r.qty * r.price;
        });
        return { byChannel: byChannel, total: total, byProduct: byProduct };
      },
      insight: [
        'Each order line is one row in tbl_Sales; KPIs are SUMIFS over that table.',
        'Channel mix is a pivot on the same table — no separate spreadsheet to maintain.',
        'Removing a line re-runs every formula, exactly like the real workbook.'
      ],
      schema: [['Table', 'tbl_Sales'], ['Key', 'Order ID'], ['KPI mode', 'SUMIFS / Pivot'], ['Refresh', 'On edit']]
    },

    wholesale: {
      kicker: 'Wholesale System',
      title: 'Purchase order demo',
      lede: 'Progress sample purchase orders through picking, transit and delivery. Fill rate and open-value totals recalculate as you go.',
      kpis: [
        { label: 'Open POs', get: function (s) { return String(s.filter(function (o) { return o.status !== 'Delivered'; }).length); } },
        { label: 'Open value', get: function (s) { return money(s.filter(function (o) { return o.status !== 'Delivered'; }).reduce(function (t, o) { return t + o.value; }, 0)); } },
        { label: 'Delivered value', get: function (s) { return money(s.filter(function (o) { return o.status === 'Delivered'; }).reduce(function (t, o) { return t + o.value; }, 0)); } },
        { label: 'Average fill rate', get: function (s) {
            var done = s.filter(function (o) { return o.status === 'Delivered'; });
            if (!done.length) return '—';
            return Math.round(done.reduce(function (t, o) { return t + o.fill; }, 0) / done.length) + '%';
          } }
      ],
      columns: ['PO', 'Account', 'Lines', 'Value', 'Fill rate', 'Status', 'Action'],
      seed: function () {
        return [
          { id: 'PO-20418', account: 'Marlow & Co.', lines: 42, value: 48260, fill: 96, status: 'In transit' },
          { id: 'PO-20417', account: 'Brightline Retail', lines: 18, value: 22910, fill: 88, status: 'Picking' },
          { id: 'PO-20412', account: 'Harbor Wholesale', lines: 64, value: 81430, fill: 0, status: 'Confirmed' },
          { id: 'PO-20405', account: 'Westgate Supply', lines: 9, value: 9640, fill: 0, status: 'Backorder' }
        ];
      },
      row: function (o) {
        var tone = o.status === 'Delivered' ? 'ok' : o.status === 'Backorder' ? 'danger'
          : o.status === 'In transit' ? 'info' : 'warn';
        return {
          badge: [o.status, tone],
          cells: [o.id, o.account, String(o.lines), money(o.value), o.fill ? o.fill + '%' : '—'],
          actions: [{ id: 'advance', label: o.status === 'Delivered' ? 'Reopen' : 'Advance', tone: o.status === 'Delivered' ? 'ghost' : 'solid' }]
        };
      },
      act: function (id, o) {
        var flow = ['Confirmed', 'Picking', 'In transit', 'Delivered'];
        if (id !== 'advance') return;
        var i = flow.indexOf(o.status);
        if (o.status === 'Backorder') { o.status = 'Confirmed'; return 'Backorder cleared — PO back in the active flow.'; }
        if (o.status === 'Delivered') { o.status = 'Confirmed'; o.fill = 0; return 'PO reopened for a new delivery cycle.'; }
        o.status = flow[Math.min(i + 1, flow.length - 1)];
        if (o.status === 'Delivered' && !o.fill) o.fill = 92 + Math.floor(Math.random() * 9);
        return 'PO moved to “' + o.status + '”.';
      },
      insight: [
        'Status is a data-validated list, so the workflow can never skip a stage silently.',
        'Fill rate is calculated: delivered lines ÷ ordered lines per PO.',
        'Open-value and delivered-value cards use the same table with different filters.'
      ],
      schema: [['Table', 'tbl_PurchaseOrders'], ['Key', 'PO number'], ['Status flow', 'Confirmed → Picking → Transit → Delivered'], ['Refresh', 'On edit']]
    },

    expenses: {
      kicker: 'Expense System',
      title: 'Budget demo',
      lede: 'Approve, hold or reject sample expenses and watch monthly spend against budget move in real time.',
      kpis: [
        { label: 'Approved spend', get: function (s) { return money(s.filter(function (e) { return e.status === 'Approved'; }).reduce(function (t, e) { return t + e.amount; }, 0)); } },
        { label: 'Budget', get: function () { return money(12000); } },
        { label: 'Budget used', get: function (s) {
            var a = s.filter(function (e) { return e.status === 'Approved'; }).reduce(function (t, e) { return t + e.amount; }, 0);
            return Math.round(a / 12000 * 100) + '%';
          } },
        { label: 'Awaiting review', get: function (s) { return String(s.filter(function (e) { return e.status === 'Pending'; }).length); } }
      ],
      columns: ['Ref', 'Vendor', 'Category', 'Amount', 'Status', 'Action'],
      seed: function () {
        return [
          { ref: 'INV-8841', vendor: 'Marlow & Co.', cat: 'Suppliers', amount: 2480, status: 'Approved' },
          { ref: 'INV-8839', vendor: 'Freight · Nordvik', cat: 'Logistics', amount: 326, status: 'Pending' },
          { ref: 'INV-8834', vendor: 'Studio light rebuild', cat: 'Operations', amount: 1180, status: 'Pending' },
          { ref: 'INV-8830', vendor: 'Ad spend · October', cat: 'Marketing', amount: 690, status: 'Pending' },
          { ref: 'INV-8826', vendor: 'Warehouse utilities', cat: 'Operations', amount: 2140, status: 'Approved' }
        ];
      },
      row: function (e) {
        var tone = e.status === 'Approved' ? 'ok' : e.status === 'Pending' ? 'warn' : 'danger';
        return {
          badge: [e.status, tone],
          cells: [e.ref, e.vendor, e.cat, money(e.amount)],
          actions: e.status === 'Pending'
            ? [{ id: 'approve', label: 'Approve' }, { id: 'reject', label: 'Reject', tone: 'ghost' }]
            : [{ id: 'reset', label: 'Reset', tone: 'ghost' }]
        };
      },
      act: function (id, e) {
        if (id === 'approve') { e.status = 'Approved'; return 'Expense approved — budget updated.'; }
        if (id === 'reject') { e.status = 'Rejected'; return 'Expense rejected — removed from spend.'; }
        if (id === 'reset') { e.status = 'Pending'; return 'Expense returned to the review queue.'; }
      },
      insight: [
        'Approved, pending and rejected rows are split with one status column — no copy-paste.',
        'Budget-used percentage is a single formula that feeds the KPI card and the progress bar.',
        'Rejected expenses never touch the spend total.'
      ],
      schema: [['Table', 'tbl_Expenses'], ['Key', 'Invoice ref'], ['Budget', 'Per month, per category'], ['Refresh', 'On edit']]
    },

    reporting: {
      kicker: 'Reporting System',
      title: 'Report builder demo',
      lede: 'Choose the period and the entities to include; the one-page summary rebuilds with the same aggregation logic a reporting workbook uses.',
      kpis: [
        { label: 'Selected entities', get: function (s) { return String(s.length); } },
        { label: 'Combined revenue', get: function (s) { return money(s.reduce(function (t, e) { return t + e.revenue; }, 0)); } },
        { label: 'Combined cost', get: function (s) { return money(s.reduce(function (t, e) { return t + e.cost; }, 0)); } },
        { label: 'Blended margin', get: function (s) {
            var rev = s.reduce(function (t, e) { return t + e.revenue; }, 0);
            var cost = s.reduce(function (t, e) { return t + e.cost; }, 0);
            return rev ? Math.round((rev - cost) / rev * 100) + '%' : '—';
          } }
      ],
      toggleMode: true,
      columns: ['Entity', 'Revenue', 'Cost', 'Gross profit', 'Margin', 'Include'],
      seed: function () {
        return [
          { name: 'Retail store', revenue: 132400, cost: 78100, on: true },
          { name: 'Online shop', revenue: 96800, cost: 54900, on: true },
          { name: 'Wholesale desk', revenue: 57230, cost: 41200, on: true },
          { name: 'Marketplace', revenue: 28400, cost: 19600, on: false }
        ];
      },
      row: function (e) {
        var margin = e.revenue ? Math.round((e.revenue - e.cost) / e.revenue * 100) : 0;
        return {
          cells: [e.name, money(e.revenue), money(e.cost), money(e.revenue - e.cost), margin + '%'],
          toggle: { id: 'toggle', on: e.on, label: e.on ? 'Included' : 'Excluded' }
        };
      },
      act: function (id, e) {
        if (id === 'toggle') { e.on = !e.on; return e.on ? e.name + ' added to the report.' : e.name + ' excluded from the report.'; }
      },
      filter: function (list) { return list.filter(function (e) { return e.on; }); },
      insight: [
        'Only the entities you include flow into the KPI cards and the summary line.',
        'Margin is calculated, never typed — it updates with every change.',
        'The same component exports to a one-page PDF board pack.'
      ],
      schema: [['Table', 'tbl_Entities'], ['Key', 'Entity name'], ['Mode', 'Toggle-driven consolidation'], ['Export', 'PDF / print-ready sheet']]
    }
  };

  /* ---------- helpers ---------- */
  function money(n) {
    return '$' + Math.round(n).toLocaleString('en-US');
  }
  function num(n) {
    return n.toLocaleString('en-US');
  }
  function badgeClass(tone) {
    return 'demo-badge demo-badge--' + (tone || 'ok');
  }

  var root = document.getElementById('demo-app');
  if (!root) return;

  var demo, state, id, logs = [];

  function paintChrome() {
    document.querySelectorAll('[data-demo-tab]').forEach(function (a) {
      var on = a.dataset.demoTab === id;
      a.classList.toggle('is-active', on);
      if (on) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    var titleEl = document.querySelector('[data-demo-title]');
    if (titleEl) titleEl.textContent = demo.kicker;
    document.title = demo.kicker + ' — Live demonstration · Pouria Business';
  }

  function visible() {
    return demo.filter ? demo.filter(state) : state;
  }

  function renderKpis() {
    var wrap = document.createElement('div');
    wrap.className = 'demo-kpis';
    var list = visible();
    demo.kpis.forEach(function (k) {
      var el = document.createElement('div');
      el.className = 'demo-kpi';
      el.innerHTML = '<span class="demo-kpi__label"></span><strong class="demo-kpi__value"></strong>';
      el.querySelector('.demo-kpi__label').textContent = k.label;
      el.querySelector('.demo-kpi__value').textContent = k.get(list);
      wrap.appendChild(el);
    });
    return wrap;
  }

  function renderTable() {
    var list = state;
    var wrap = document.createElement('div');
    wrap.className = 'demo-table-wrap';
    var table = document.createElement('table');
    table.className = 'demo-table';
    var thead = document.createElement('thead');
    var htr = document.createElement('tr');
    demo.columns.forEach(function (c) {
      var th = document.createElement('th');
      th.textContent = c;
      htr.appendChild(th);
    });
    thead.appendChild(htr);
    table.appendChild(thead);

    var tbody = document.createElement('tbody');
    list.forEach(function (row) {
      var spec = demo.row(row);
      var tr = document.createElement('tr');
      spec.cells.forEach(function (cell, i) {
        var td = document.createElement('td');
        td.dataset.label = demo.columns[i];
        if (i === 0) td.className = 'is-key';
        if (typeof cell === 'string' && /^[$\-0-9]/.test(cell)) td.className = 'is-num';
        td.textContent = cell;
        tr.appendChild(td);
      });
      if (spec.badge) {
        var td = document.createElement('td');
        td.dataset.label = 'Status';
        var b = document.createElement('span');
        b.className = badgeClass(spec.badge[1]);
        b.textContent = spec.badge[0];
        td.appendChild(b);
        tr.appendChild(td);
      }
      var actTd = document.createElement('td');
      actTd.dataset.label = 'Action';
      actTd.className = 'is-action';
      if (spec.toggle) {
        var tbtn = document.createElement('button');
        tbtn.type = 'button';
        tbtn.className = 'demo-toggle' + (spec.toggle.on ? ' is-on' : '');
        tbtn.innerHTML = '<span></span>';
        tbtn.setAttribute('aria-pressed', spec.toggle.on ? 'true' : 'false');
        tbtn.setAttribute('aria-label', spec.toggle.label);
        tbtn.addEventListener('click', function () { run(spec.toggle.id, row); });
        actTd.appendChild(tbtn);
        var lbl = document.createElement('em');
        lbl.textContent = spec.toggle.label;
        actTd.appendChild(lbl);
      }
      (spec.actions || []).forEach(function (a) {
        var btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'demo-btn' + (a.tone === 'ghost' ? ' demo-btn--ghost' : '');
        btn.textContent = a.label;
        btn.addEventListener('click', function () { run(a.id, row); });
        actTd.appendChild(btn);
      });
      tr.appendChild(actTd);
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    wrap.appendChild(table);
    return wrap;
  }

  function renderExtras() {
    if (!demo.extra) return null;
    var data = demo.extra(state);
    var box = document.createElement('div');
    box.className = 'demo-extra';
    box.innerHTML = '<h3>Channel mix</h3><div class="demo-bars"></div>';
    var bars = box.querySelector('.demo-bars');
    Object.keys(data.byChannel).forEach(function (key) {
      var pct = Math.round(data.byChannel[key] / data.total * 100);
      var row = document.createElement('div');
      row.className = 'demo-bar-row';
      row.innerHTML = '<span></span><div class="demo-bar"><i></i></div><b></b>';
      row.querySelector('span').textContent = key;
      row.querySelector('i').style.width = Math.max(4, pct) + '%';
      row.querySelector('b').textContent = money(data.byChannel[key]);
      bars.appendChild(row);
    });
    return box;
  }

  function render() {
    root.innerHTML = '';
    var head = document.createElement('div');
    head.className = 'demo-head';
    head.innerHTML = '<div><p class="demo-head__kicker">' + demo.kicker + ' · interactive demo</p>' +
      '<h2 class="demo-head__title">' + demo.title + '</h2>' +
      '<p class="demo-head__lede">' + demo.lede + '</p></div>' +
      '<div class="demo-head__actions">' +
      '<button type="button" class="btn btn--ghost btn--sm" data-reset>Reset demo data</button>' +
      '</div>';
    head.querySelector('[data-reset]').addEventListener('click', function () {
      state = demo.seed();
      log('Demo data reset to its starting state.');
      render();
    });
    root.appendChild(head);

    root.appendChild(renderKpis());
    root.appendChild(renderTable());
    var extra = renderExtras();
    if (extra) root.appendChild(extra);

    var foot = document.createElement('div');
    foot.className = 'demo-foot';
    foot.innerHTML =
      '<div class="demo-schema"><h3>Workbook structure</h3><dl>' +
      demo.schema.map(function (r) { return '<div><dt>' + r[0] + '</dt><dd>' + r[1] + '</dd></div>'; }).join('') +
      '</dl></div>' +
      '<div class="demo-log"><h3>Activity log</h3><ul data-log aria-live="polite"></ul></div>';
    root.appendChild(foot);

    var note = document.createElement('p');
    note.className = 'demo-disclaimer';
    note.textContent = 'Sample data only. This in-browser demo reproduces the calculation logic of the ' +
      demo.kicker + '; the delivered workbook is a separate Excel file built for your business.';
    root.appendChild(note);

    log('Demo loaded with ' + state.length + ' sample records.', true);
  }

  function log(msg, silent) {
    logs.unshift(msg);
    logs = logs.slice(0, 6);
    var ul = root.querySelector('[data-log]');
    if (!ul) return;
    ul.innerHTML = '';
    logs.forEach(function (m, i) {
      var li = document.createElement('li');
      li.textContent = m;
      if (i === 0 && !silent) li.className = 'is-new';
      ul.appendChild(li);
    });
  }

  function run(actionId, row) {
    var msg = demo.act(actionId, row, state);
    if (msg) log(msg);
    render();
  }

  function boot(animateScroll) {
    var wanted = (location.hash || '').replace('#', '') || 'inventory';
    if (!DEMOS[wanted]) wanted = 'inventory';
    if (wanted === id) return;
    id = wanted;
    demo = DEMOS[id];
    state = demo.seed();
    logs = [];
    paintChrome();
    render();
    if (animateScroll) root.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  boot(false);
  window.addEventListener('hashchange', function () {
    var wanted = (location.hash || '').replace('#', '') || 'inventory';
    if (DEMOS[wanted] && wanted !== id) boot(true);
  });
})();
