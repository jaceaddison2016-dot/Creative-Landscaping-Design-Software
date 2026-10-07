/* Creative Landscaping · local-first prototype */
(function () {
  'use strict';
  const L = window.Landscape;
  const $ = (id) => document.getElementById(id);
  const svg = $('plan');
  const ns = 'http://www.w3.org/2000/svg';
  let project = L.demoProject();
  let selected = null,
    tool = 'select',
    anchor = null,
    drag = null,
    dirty = false;
  let undo = [],
    redo = [];
  let lastSaved = L.serialize(project);
  function node(tag, attrs = {}, content) {
    const element = document.createElementNS(ns, tag);
    for (const [key, value] of Object.entries(attrs)) element.setAttribute(key, String(value));
    if (content !== undefined) element.textContent = content;
    return element;
  }
  function status(message, error = false) {
    $('status').textContent = message;
    $('status').classList.toggle('error', error);
  }
  function snapshot() {
    return L.serialize(project);
  }
  function record(before) {
    if (before === snapshot()) return;
    undo.push(before);
    if (undo.length > 50) undo.shift();
    redo = [];
    dirty = snapshot() !== lastSaved;
  }
  function mutate(action) {
    const before = snapshot();
    try {
      action();
      project = L.validateProject(project);
      record(before);
      render();
      return true;
    } catch (error) {
      project = L.parseProject(before);
      status(error.message, true);
      return false;
    }
  }
  function id() {
    return 'item-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);
  }
  function boundedPoint(event) {
    const rect = svg.getBoundingClientRect();
    let x = ((event.clientX - rect.left) / rect.width) * project.width;
    let y = ((event.clientY - rect.top) / rect.height) * project.depth;
    const snap = $('snap').checked ? 6 : 1;
    x = Math.round(x / snap) * snap;
    y = Math.round(y / snap) * snap;
    return {
      x: Math.max(0, Math.min(project.width, x)),
      y: Math.max(0, Math.min(project.depth, y)),
    };
  }
  function chosenPlant() {
    return project.plants.find((p) => p.id === selected);
  }
  function setTool(value) {
    tool = value;
    anchor = null;
    $('select-tool').classList.toggle('active', tool === 'select');
    $('select-tool').setAttribute('aria-pressed', tool === 'select');
    $('measure-tool').classList.toggle('active', tool === 'measure');
    $('measure-tool').setAttribute('aria-pressed', tool === 'measure');
    document.querySelectorAll('.plant-option').forEach((button) => {
      button.classList.toggle('active', button.dataset.kind === tool);
      button.setAttribute('aria-pressed', button.dataset.kind === tool);
    });
    svg.classList.toggle('place-mode', tool !== 'select');
    $('tool-hint').textContent =
      tool === 'select'
        ? 'Select a plant to edit it. Drag to move.'
        : tool === 'measure'
          ? 'Click the start and end of a dimension. Escape cancels.'
          : 'Click the plan to place plants. Escape switches to select.';
    renderPlan();
  }
  // Convex hull of base and translated canopy approximates a solid vertical cylinder's shadow.
  function hull(points) {
    const sorted = points.slice().sort((a, b) => a.x - b.x || a.y - b.y);
    const cross = (a, b, c) => (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
    const lower = [],
      upper = [];
    for (const point of sorted) {
      while (lower.length > 1 && cross(lower.at(-2), lower.at(-1), point) <= 0) lower.pop();
      lower.push(point);
    }
    for (const point of sorted.slice().reverse()) {
      while (upper.length > 1 && cross(upper.at(-2), upper.at(-1), point) <= 0) upper.pop();
      upper.push(point);
    }
    return lower.slice(0, -1).concat(upper.slice(0, -1));
  }
  function solar() {
    const s = project.site;
    return L.solarPosition(s.latitude, s.longitude, L.localToUTC(s.date, s.time, s.utcOffset));
  }
  function drawSunReadout() {
    const sun = solar();
    $('sun-elevation').textContent = `${sun.elevation.toFixed(1)}°`;
    $('sun-azimuth').textContent = `${sun.azimuth.toFixed(1)}°`;
    $('sun-state').textContent = !sun.daylight
      ? 'SUN BELOW HORIZON'
      : sun.elevation < 1
        ? 'SUN AT HORIZON'
        : 'DAYLIGHT STUDY';
    $('shadow-summary').textContent =
      sun.elevation < 1
        ? 'Shadows hidden below 1° elevation.'
        : `10-foot plant → ${L.formatInches(L.shadowVector(120, sun.elevation, sun.azimuth).length)} shadow`;
  }
  function renderPlan() {
    svg.replaceChildren();
    svg.setAttribute('viewBox', `0 0 ${project.width} ${project.depth}`);
    const scale = project.width / 960;
    const defs = node('defs');
    const pattern = node('pattern', {
      id: 'grid',
      width: 60,
      height: 60,
      patternUnits: 'userSpaceOnUse',
    });
    pattern.append(
      node('path', {
        d: 'M 60 0 L 0 0 0 60',
        fill: 'none',
        stroke: '#dfe6d8',
        'stroke-width': scale,
      }),
    );
    defs.append(pattern);
    const clip = node('clipPath', { id: 'plot-clip' });
    clip.append(node('rect', { width: project.width, height: project.depth }));
    defs.append(clip);
    svg.append(defs);
    svg.append(node('rect', { width: project.width, height: project.depth, fill: 'url(#grid)' }));
    const contents = node('g', { 'clip-path': 'url(#plot-clip)' });
    svg.append(contents);
    if ($('show-shadows').checked) {
      const sun = solar();
      const shadows = node('g', {
        fill: '#466348',
        opacity: '.19',
        'pointer-events': 'none',
        'data-layer': 'shadows',
      });
      for (const p of project.plants) {
        const vector = L.shadowVector(p.height, sun.elevation, sun.azimuth);
        if (!vector) continue;
        const points = [];
        for (let i = 0; i < 32; i++) {
          const angle = (i * Math.PI) / 16;
          const x = p.x + (p.diameter / 2) * Math.cos(angle),
            y = p.y + (p.diameter / 2) * Math.sin(angle);
          points.push({ x, y }, { x: x + vector.dx, y: y + vector.dy });
        }
        shadows.append(
          node('polygon', {
            points: hull(points)
              .map((p) => `${p.x},${p.y}`)
              .join(' '),
          }),
        );
      }
      contents.append(shadows);
    }
    for (const p of project.plants) {
      const catalog = L.CATALOG.find((c) => c.kind === p.kind);
      const group = node('g', {
        class: 'plant',
        'data-id': p.id,
        tabindex: 0,
        role: 'button',
        'aria-label': `${p.name}, ${L.formatInches(p.diameter)} diameter, select to edit`,
      });
      const r = p.diameter / 2;
      group.append(
        node('circle', {
          cx: p.x,
          cy: p.y,
          r,
          fill: catalog.color,
          opacity: '.85',
          stroke: selected === p.id ? '#254d3d' : '#fffef4',
          'stroke-width': (selected === p.id ? 4 : 2) * scale,
        }),
      );
      if (p.kind === 'tree') {
        group.append(
          node('circle', {
            cx: p.x,
            cy: p.y,
            r: r * 0.76,
            fill: 'none',
            stroke: '#ffffff50',
            'stroke-width': scale,
            'stroke-dasharray': `${4 * scale} ${5 * scale}`,
          }),
        );
        for (let i = 0; i < 5; i++) {
          const a = (i * Math.PI * 2) / 5;
          group.append(
            node('path', {
              d: `M ${p.x} ${p.y} L ${p.x + Math.cos(a) * r * 0.53} ${p.y + Math.sin(a) * r * 0.53}`,
              stroke: '#ffffff35',
              'stroke-width': 2 * scale,
              fill: 'none',
            }),
          );
        }
      } else if (p.kind === 'flower') {
        group.append(node('circle', { cx: p.x, cy: p.y, r: r * 0.28, fill: '#eedac5' }));
      }
      group.append(node('circle', { cx: p.x, cy: p.y, r: 2.5 * scale, fill: '#fffde9' }));
      if (selected === p.id) {
        group.append(
          node(
            'text',
            {
              x: p.x,
              y: p.y + r + 20 * scale,
              'font-size': 13 * scale,
              'text-anchor': 'middle',
              fill: '#254d3d',
              'paint-order': 'stroke',
              stroke: '#fcfdf8',
              'stroke-width': 4 * scale,
            },
            p.name,
          ),
        );
      }
      contents.append(group);
    }
    for (const d of project.dimensions) {
      const group = node('g', {
        'data-id': d.id,
        class: 'dimension',
        tabindex: 0,
        role: 'button',
        'aria-label': `Dimension ${L.formatInches(L.distance(d.a, d.b))}, select to delete`,
      });
      const attrs = { x1: d.a.x, y1: d.a.y, x2: d.b.x, y2: d.b.y };
      group.append(node('line', { ...attrs, stroke: 'transparent', 'stroke-width': 20 * scale }));
      group.append(
        node('line', {
          ...attrs,
          stroke: selected === d.id ? '#a06c2b' : '#596e50',
          'stroke-width': 1.5 * scale,
        }),
      );
      for (const p of [d.a, d.b])
        group.append(node('circle', { cx: p.x, cy: p.y, r: 3.5 * scale, fill: '#596e50' }));
      group.append(
        node(
          'text',
          {
            x: (d.a.x + d.b.x) / 2,
            y: (d.a.y + d.b.y) / 2 - 10 * scale,
            'text-anchor': 'middle',
            'font-size': 14 * scale,
            fill: '#3d5536',
            'paint-order': 'stroke',
            stroke: '#fcfdf8',
            'stroke-width': 5 * scale,
          },
          L.formatInches(L.distance(d.a, d.b)),
        ),
      );
      contents.append(group);
    }
    if (anchor)
      contents.append(
        node('circle', { cx: anchor.x, cy: anchor.y, r: 5 * scale, fill: '#a06c2b' }),
      );
    const width = L.formatInches(project.width),
      depth = L.formatInches(project.depth);
    contents.append(
      node(
        'text',
        {
          x: 15 * scale,
          y: 25 * scale,
          'font-size': 12 * scale,
          fill: '#8b9981',
          'pointer-events': 'none',
        },
        `${width} × ${depth}  ·  Grid: 5′`,
      ),
    );
    $('plant-count').textContent =
      `${project.plants.length} plants · ${project.dimensions.length} dimensions`;
  }
  function renderSelection() {
    const p = chosenPlant();
    const dimension = project.dimensions.find((d) => d.id === selected);
    $('selection-empty').hidden = Boolean(p || dimension);
    $('plant-form').hidden = !p;
    $('dimension-selection').hidden = !dimension;
    $('delete-selection').hidden = !(p || dimension);
    if (p) {
      $('plant-name').value = p.name;
      for (const field of ['x', 'y', 'diameter', 'height'])
        $('plant-' + field).value = L.inputLength(p[field]);
    }
    if (dimension)
      $('dimension-value').textContent = L.formatInches(L.distance(dimension.a, dimension.b));
  }
  function render() {
    $('project-name').value = project.name;
    $('plot-width').value = L.inputLength(project.width);
    $('plot-depth').value = L.inputLength(project.depth);
    const s = project.site;
    $('sun-date').value = s.date;
    $('sun-time').value = s.time;
    $('latitude').value = s.latitude;
    $('longitude').value = s.longitude;
    $('utc-offset').value = s.utcOffset;
    const [h, m] = s.time.split(':').map(Number);
    $('time-slider').value = h * 60 + m;
    $('undo').disabled = undo.length === 0;
    $('redo').disabled = redo.length === 0;
    renderPlan();
    drawSunReadout();
    renderSelection();
  }
  svg.addEventListener('pointerdown', (event) => {
    if (event.button !== 0) return;
    const point = boundedPoint(event);
    if (tool === 'measure') {
      if (!anchor) {
        anchor = point;
        status('Now click the other end of the dimension.');
        renderPlan();
      } else if (L.distance(anchor, point) > 0) {
        const start = anchor;
        const added = mutate(() => {
          project.dimensions.push({ id: id(), a: start, b: point });
        });
        anchor = null;
        renderPlan();
        if (added) status('Dimension added. Click to start another.');
      }
      return;
    }
    const catalog = L.CATALOG.find((p) => p.kind === tool);
    if (catalog) {
      const added = mutate(() => {
        selected = id();
        project.plants.push({
          id: selected,
          kind: catalog.kind,
          name: catalog.name,
          diameter: catalog.diameter,
          height: catalog.height,
          ...point,
        });
      });
      if (added) status(`${catalog.name} placed. Choose Select & move to edit it.`);
      return;
    }
    selected = event.target.closest('[data-id]')?.dataset.id || null;
    const plant = chosenPlant();
    if (plant) {
      drag = {
        before: snapshot(),
        x: plant.x,
        y: plant.y,
        start: point,
        pointerId: event.pointerId,
      };
      svg.setPointerCapture(event.pointerId);
    }
    renderPlan();
    renderSelection();
  });
  svg.addEventListener('pointermove', (event) => {
    if (!drag || event.pointerId !== drag.pointerId) return;
    const p = chosenPlant();
    if (!p) return;
    const point = boundedPoint(event);
    p.x = Math.max(0, Math.min(project.width, drag.x + point.x - drag.start.x));
    p.y = Math.max(0, Math.min(project.depth, drag.y + point.y - drag.start.y));
    renderPlan();
    renderSelection();
  });
  function finishDrag(event, cancelled = false) {
    if (!drag || event.pointerId !== drag.pointerId) return;
    if (cancelled) project = L.parseProject(drag.before);
    else record(drag.before);
    drag = null;
    render();
  }
  svg.addEventListener('pointerup', (event) => finishDrag(event));
  svg.addEventListener('pointercancel', (event) => finishDrag(event, true));
  svg.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      const object = event.target.closest('[data-id]');
      if (object) {
        event.preventDefault();
        selected = object.dataset.id;
        renderPlan();
        renderSelection();
      }
    }
  });
  for (const item of L.CATALOG) {
    const button = document.createElement('button');
    button.className = 'plant-option';
    button.dataset.kind = item.kind;
    button.setAttribute('aria-pressed', 'false');
    const swatch = document.createElement('span');
    swatch.className = 'plant-swatch';
    swatch.style.setProperty('--plant-color', item.color);
    swatch.textContent = item.kind === 'flower' ? '✿' : '✳';
    swatch.setAttribute('aria-hidden', 'true');
    const info = document.createElement('span'),
      title = document.createElement('strong'),
      detail = document.createElement('small');
    title.textContent = item.name;
    detail.textContent = `${L.formatInches(item.diameter)} canopy`;
    info.append(title, detail);
    button.append(swatch, info);
    button.addEventListener('click', () => setTool(item.kind));
    $('catalog').append(button);
  }
  $('select-tool').onclick = () => setTool('select');
  $('measure-tool').onclick = () => setTool('measure');
  $('plant-form').onsubmit = (event) => {
    event.preventDefault();
    mutate(() => {
      const p = chosenPlant();
      if (!p) return;
      p.name = $('plant-name').value.trim();
      for (const field of ['x', 'y', 'diameter', 'height'])
        p[field] = L.parseLength($('plant-' + field).value);
    });
  };
  $('plot-form').onsubmit = (event) => {
    event.preventDefault();
    mutate(() => {
      project.width = L.parseLength($('plot-width').value);
      project.depth = L.parseLength($('plot-depth').value);
    });
  };
  $('project-name').onchange = () =>
    mutate(() => {
      project.name = $('project-name').value.trim();
    });
  function updateSite() {
    if (!$('sun-form').reportValidity()) return;
    mutate(() => {
      project.site = {
        latitude: Number($('latitude').value),
        longitude: Number($('longitude').value),
        utcOffset: Number($('utc-offset').value),
        date: $('sun-date').value,
        time: $('sun-time').value,
      };
    });
  }
  $('sun-form').onsubmit = (event) => {
    event.preventDefault();
    updateSite();
  };
  for (const field of ['sun-date', 'sun-time', 'latitude', 'longitude', 'utc-offset'])
    $(field).onchange = updateSite;
  $('time-slider').oninput = () => {
    const minutes = Number($('time-slider').value);
    $('sun-time').value =
      `${String(Math.floor(minutes / 60)).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}`;
  };
  $('time-slider').onchange = updateSite;
  $('show-shadows').onchange = renderPlan;
  $('delete-selection').onclick = () => {
    mutate(() => {
      project.plants = project.plants.filter((p) => p.id !== selected);
      project.dimensions = project.dimensions.filter((d) => d.id !== selected);
      selected = null;
    });
  };
  function history(forward) {
    if (drag) return;
    const from = forward ? redo : undo,
      to = forward ? undo : redo;
    if (!from.length) return;
    to.push(snapshot());
    project = L.parseProject(from.pop());
    selected = null;
    anchor = null;
    dirty = snapshot() !== lastSaved;
    render();
    status(forward ? 'Change restored.' : 'Change undone.');
  }
  $('undo').onclick = () => history(false);
  $('redo').onclick = () => history(true);
  async function replaceProject(next) {
    if (dirty) {
      const dialog = $('replace-dialog');
      const result = new Promise((resolve) =>
        dialog.addEventListener('close', () => resolve(dialog.returnValue), { once: true }),
      );
      dialog.showModal();
      if ((await result) !== 'replace') return;
    }
    project = L.validateProject(next);
    selected = null;
    anchor = null;
    undo = [];
    redo = [];
    dirty = false;
    lastSaved = snapshot();
    setTool('select');
    render();
    status('Plan opened. Save a project file to keep your changes.');
  }
  $('new-project').onclick = () => replaceProject(L.newProject());
  $('demo-project').onclick = () => replaceProject(L.demoProject());
  $('load-project').onclick = () => $('file-input').click();
  $('file-input').onchange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    try {
      if (file.size > 2000000) throw new Error('Project file is too large (maximum 2 MB).');
      const next = L.parseProject(await file.text());
      await replaceProject(next);
    } catch (error) {
      status(`Could not open project: ${error.message}`, true);
    } finally {
      $('file-input').value = '';
    }
  };
  $('save-project').onclick = () => {
    try {
      const data = snapshot();
      const url = URL.createObjectURL(new Blob([data], { type: 'application/json' }));
      const link = document.createElement('a');
      link.href = url;
      link.download =
        (project.name.replace(/[^a-z0-9_-]+/gi, '-').replace(/^-|-$/g, '') || 'landscape') + '.clp';
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 10000);
      lastSaved = data;
      dirty = false;
      status('Project download requested. Keep the .clp file and use Open to return to it.');
    } catch (error) {
      status(error.message, true);
    }
  };
  function zoom() {
    $('plan-paper').style.width = `${$('zoom').value}%`;
  }
  $('zoom').oninput = zoom;
  $('fit-view').onclick = () => {
    $('zoom').value = 100;
    zoom();
    $('canvas-area').scrollTo(0, 0);
  };
  document.addEventListener('keydown', (event) => {
    if (event.target.closest('input, textarea, select, dialog') || event.target.isContentEditable)
      return;
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'z') {
      event.preventDefault();
      history(event.shiftKey);
    } else if (event.key === 'Escape') {
      setTool('select');
    } else if (event.key.toLowerCase() === 'v') setTool('select');
    else if (event.key.toLowerCase() === 'm') setTool('measure');
    else if (event.key === 'Delete' || event.key === 'Backspace') {
      if (selected) {
        event.preventDefault();
        $('delete-selection').click();
      }
    }
  });
  window.addEventListener('beforeunload', (event) => {
    if (dirty) {
      event.preventDefault();
      event.returnValue = '';
    }
  });
  render();
})();
