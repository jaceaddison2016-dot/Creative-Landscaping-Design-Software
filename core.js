/* Creative Landscaping prototype. Independent implementation; no Open Garden Planner code. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.Landscape = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const FORMAT = 'creative-landscape';
  const MAX_OBJECTS = 500;
  const CATALOG = [
    { kind: 'tree', name: 'Shade tree', diameter: 180, height: 300, color: '#46765b' },
    { kind: 'shrub', name: 'Evergreen shrub', diameter: 60, height: 48, color: '#81966b' },
    { kind: 'flower', name: 'Perennial', diameter: 24, height: 24, color: '#b47b89' },
  ];
  function formatInches(value) {
    const inches = Math.round(Math.abs(value));
    return `${value < 0 ? '−' : ''}${Math.floor(inches / 12)}′ ${inches % 12}″`;
  }
  // Accept decimal feet, 10' 6", or 10 ft 6 in. Store whole inches.
  function parseLength(text) {
    const value = String(text).trim().replaceAll('′', "'").replaceAll('″', '"');
    let inches;
    if (/^\d+(?:\.\d+)?$/.test(value)) inches = Number(value) * 12;
    else {
      const match = value.match(/^(\d+(?:\.\d+)?)\s*(?:'|ft)(?:\s*(\d+(?:\.\d+)?)\s*(?:"|in))?$/i);
      if (!match || Number(match[2] || 0) >= 12)
        throw new Error('Use feet, or feet and inches: 10\' 6".');
      inches = Number(match[1]) * 12 + Number(match[2] || 0);
    }
    if (!Number.isFinite(inches) || inches < 0 || inches > 12000)
      throw new Error('Length must be between 0 and 1,000 feet.');
    return Math.round(inches);
  }
  function inputLength(inches) {
    return `${Math.floor(inches / 12)}' ${inches % 12}"`;
  }
  function number(value, min, max, label) {
    if (typeof value !== 'number' || !Number.isFinite(value) || value < min || value > max)
      throw new Error(`${label} must be between ${min} and ${max}.`);
    return value;
  }
  function whole(value, min, max, label) {
    if (typeof value !== 'number' || !Number.isFinite(value) || value < min || value > max) {
      throw new Error(`${label} must be between ${formatInches(min)} and ${formatInches(max)}.`);
    }
    if (!Number.isInteger(value)) throw new Error(`${label} must be whole inches.`);
    return value;
  }
  function localToUTC(date, time, offset) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date) || !/^\d{2}:\d{2}$/.test(time))
      throw new Error('Enter a valid date and time.');
    const [year, month, day] = date.split('-').map(Number);
    const [hours, minutes] = time.split(':').map(Number);
    number(year, 1900, 2100, 'Year');
    number(hours, 0, 23, 'Hour');
    number(minutes, 0, 59, 'Minute');
    number(offset, -12, 14, 'UTC offset');
    const stamp = new Date(Date.UTC(year, month - 1, day, hours, minutes));
    if (
      stamp.getUTCFullYear() !== year ||
      stamp.getUTCMonth() !== month - 1 ||
      stamp.getUTCDate() !== day
    )
      throw new Error('Enter a valid calendar date.');
    return new Date(stamp.getTime() - offset * 3600000);
  }
  // NOAA's published fractional-year approximation. Geometric elevation (no refraction).
  // https://gml.noaa.gov/grad/solcalc/solareqns.PDF
  function solarPosition(latitude, longitude, instant) {
    number(latitude, -90, 90, 'Latitude');
    number(longitude, -180, 180, 'Longitude');
    if (!(instant instanceof Date) || !Number.isFinite(instant.getTime()))
      throw new Error('Invalid solar instant.');
    const rad = Math.PI / 180;
    const year = instant.getUTCFullYear();
    const day = Math.floor((instant - Date.UTC(year, 0, 1)) / 86400000) + 1;
    const days = (Date.UTC(year + 1, 0, 1) - Date.UTC(year, 0, 1)) / 86400000;
    const hour =
      instant.getUTCHours() + instant.getUTCMinutes() / 60 + instant.getUTCSeconds() / 3600;
    const gamma = ((2 * Math.PI) / days) * (day - 1 + (hour - 12) / 24);
    const eq =
      229.18 *
      (0.000075 +
        0.001868 * Math.cos(gamma) -
        0.032077 * Math.sin(gamma) -
        0.014615 * Math.cos(2 * gamma) -
        0.040849 * Math.sin(2 * gamma));
    const dec =
      0.006918 -
      0.399912 * Math.cos(gamma) +
      0.070257 * Math.sin(gamma) -
      0.006758 * Math.cos(2 * gamma) +
      0.000907 * Math.sin(2 * gamma) -
      0.002697 * Math.cos(3 * gamma) +
      0.00148 * Math.sin(3 * gamma);
    const minutes = (((hour * 60 + eq + 4 * longitude) % 1440) + 1440) % 1440;
    const angle = (minutes / 4 - 180) * rad;
    const lat = latitude * rad;
    const sinElevation =
      Math.sin(lat) * Math.sin(dec) + Math.cos(lat) * Math.cos(dec) * Math.cos(angle);
    const elevation = Math.asin(Math.max(-1, Math.min(1, sinElevation))) / rad;
    const azimuth =
      (Math.atan2(
        Math.sin(angle),
        Math.cos(angle) * Math.sin(lat) - Math.tan(dec) * Math.cos(lat),
      ) /
        rad +
        180 +
        360) %
      360;
    return { elevation, azimuth, daylight: elevation > 0 };
  }
  function shadowVector(height, elevation, azimuth) {
    if (elevation < 1 || height <= 0) return null; // Suppress near-horizon singularity.
    const rad = Math.PI / 180;
    const length = height / Math.tan(elevation * rad);
    // SVG y increases south; north is at the top of the plan.
    return { dx: -length * Math.sin(azimuth * rad), dy: length * Math.cos(azimuth * rad), length };
  }
  function distance(a, b) {
    return Math.hypot(a.x - b.x, a.y - b.y);
  }
  function validateProject(data) {
    if (!data || typeof data !== 'object' || data.format !== FORMAT || data.version !== 1)
      throw new Error('This is not a supported Creative Landscaping project (version 1).');
    if (typeof data.name !== 'string' || data.name.length < 1 || data.name.length > 100)
      throw new Error('Project name must contain 1–100 characters.');
    const width = whole(data.width, 120, 12000, 'Plot width');
    const depth = whole(data.depth, 120, 12000, 'Plot depth');
    const source = data.site;
    if (!source || typeof source !== 'object') throw new Error('Project is missing site settings.');
    const site = {
      latitude: number(source.latitude, -90, 90, 'Latitude'),
      longitude: number(source.longitude, -180, 180, 'Longitude'),
      utcOffset: number(source.utcOffset, -12, 14, 'UTC offset'),
      date: source.date,
      time: source.time,
    };
    localToUTC(site.date, site.time, site.utcOffset);
    if (
      !Array.isArray(data.plants) ||
      !Array.isArray(data.dimensions) ||
      data.plants.length + data.dimensions.length > MAX_OBJECTS
    )
      throw new Error(`Projects support up to ${MAX_OBJECTS} plants and dimensions combined.`);
    const ids = new Set();
    function id(value) {
      if (typeof value !== 'string' || !/^[a-zA-Z0-9-]{1,80}$/.test(value) || ids.has(value))
        throw new Error('Object IDs must be valid and unique.');
      ids.add(value);
      return value;
    }
    function point(p) {
      if (!p || typeof p !== 'object') throw new Error('Missing point.');
      return { x: whole(p.x, 0, width, 'X position'), y: whole(p.y, 0, depth, 'Y position') };
    }
    const plants = data.plants.map((p) => {
      if (
        !p ||
        !CATALOG.some((item) => item.kind === p.kind) ||
        typeof p.name !== 'string' ||
        p.name.length < 1 ||
        p.name.length > 80
      )
        throw new Error('Invalid plant type or name.');
      return {
        id: id(p.id),
        kind: p.kind,
        name: p.name,
        ...point(p),
        diameter: whole(p.diameter, 1, 1200, 'Plant diameter'),
        height: whole(p.height, 1, 2400, 'Plant height'),
      };
    });
    const dimensions = data.dimensions.map((d) => {
      if (!d) throw new Error('Invalid dimension.');
      return { id: id(d.id), a: point(d.a), b: point(d.b) };
    });
    return { format: FORMAT, version: 1, name: data.name, width, depth, site, plants, dimensions };
  }
  function serialize(project) {
    return JSON.stringify(validateProject(project), null, 2);
  }
  function parseProject(text) {
    if (typeof text !== 'string' || text.length > 2000000)
      throw new Error('Project file is too large (maximum 2 MB).');
    let data;
    try {
      data = JSON.parse(text);
    } catch {
      throw new Error('Project file is not valid JSON.');
    }
    return validateProject(data);
  }
  function newProject() {
    return {
      format: FORMAT,
      version: 1,
      name: 'My landscape',
      width: 960,
      depth: 720,
      site: {
        latitude: 42.33,
        longitude: -83.05,
        utcOffset: -4,
        date: '2026-06-21',
        time: '15:00',
      },
      plants: [],
      dimensions: [],
    };
  }
  function demoProject() {
    const p = newProject();
    p.name = 'Summer courtyard';
    p.plants = [
      { id: 'demo-tree-1', ...CATALOG[0], x: 250, y: 240 },
      { id: 'demo-tree-2', ...CATALOG[0], x: 700, y: 220, diameter: 144, height: 240 },
      ...[250, 350, 450, 550].map((x, i) => ({ id: `demo-shrub-${i}`, ...CATALOG[1], x, y: 550 })),
      ...[620, 665, 710, 755].map((x, i) => ({ id: `demo-flower-${i}`, ...CATALOG[2], x, y: 510 })),
    ].map(({ color, ...plant }) => plant);
    p.dimensions = [{ id: 'demo-dimension', a: { x: 250, y: 400 }, b: { x: 700, y: 400 } }];
    return p;
  }
  return {
    FORMAT,
    MAX_OBJECTS,
    CATALOG,
    formatInches,
    inputLength,
    parseLength,
    localToUTC,
    solarPosition,
    shadowVector,
    distance,
    validateProject,
    serialize,
    parseProject,
    newProject,
    demoProject,
  };
});
