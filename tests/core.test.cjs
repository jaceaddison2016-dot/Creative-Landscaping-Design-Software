const { test } = require('node:test');
const assert = require('node:assert/strict');
const L = require('../core.js');
const near = (actual, expected, tolerance = 0.001) =>
  assert.ok(
    Math.abs(actual - expected) < tolerance,
    `${actual} is not within ${tolerance} of ${expected}`,
  );

test('imperial inputs normalize to whole inches', () => {
  assert.equal(L.parseLength('10\' 6"'), 126);
  assert.equal(L.parseLength('10 ft 6 in'), 126);
  assert.equal(L.parseLength('10′ 6″'), 126);
  assert.equal(L.parseLength('10.5'), 126);
  assert.equal(L.formatInches(126), '10′ 6″');
  assert.equal(L.formatInches(11.8), '1′ 0″');
  for (let inches = 0; inches <= 12000; inches += 17)
    assert.equal(L.parseLength(L.inputLength(inches)), inches);
});
test('invalid and ambiguous dimensions are rejected', () => {
  for (const text of ['-1', 'abc', '10\' 12"', 'Infinity', '', '1001', '1e3', "5' garbage"])
    assert.throws(() => L.parseLength(text));
});
test('dimension distance uses both coordinates', () => {
  assert.equal(L.distance({ x: 0, y: 0 }, { x: 36, y: 48 }), 60);
});
test('demo and blank projects survive exact file round trips', () => {
  for (const p of [L.newProject(), L.demoProject()])
    assert.deepEqual(L.parseProject(L.serialize(p)), p);
});
test('project validation rejects malformed files without silently coercing data', () => {
  assert.throws(() => L.parseProject('{'));
  for (const change of [
    (p) => {
      p.version = 2;
    },
    (p) => {
      p.width = 0;
    },
    (p) => {
      p.name = '';
    },
    (p) => {
      p.site.latitude = 91;
    },
    (p) => {
      p.site.date = '2026-02-30';
    },
    (p) => {
      p.plants[0].height = -1;
    },
    (p) => {
      p.plants[0].x = p.width + 1;
    },
    (p) => {
      p.plants[0].x = 1.5;
    },
    (p) => {
      p.plants[0].diameter = '10';
    },
    (p) => {
      p.plants[0].id = p.plants[1].id;
    },
    (p) => {
      p.dimensions[0].a.y = -10;
    },
    (p) => {
      p.site = null;
    },
  ]) {
    const p = L.demoProject();
    change(p);
    assert.throws(() => L.validateProject(p));
  }
});
test('project limits prevent oversized object collections', () => {
  const p = L.newProject();
  p.plants = Array.from({ length: 501 }, (_, i) => ({
    ...L.demoProject().plants[0],
    id: `item-${i}`,
  }));
  assert.throws(() => L.validateProject(p));
  assert.throws(() => L.parseProject(' '.repeat(2000001)));
});
test('unknown fields do not enter the canonical project', () => {
  const p = L.demoProject();
  p.extra = 'ignored';
  p.plants[0].onclick = 'ignored';
  assert.equal(L.validateProject(p).extra, undefined);
  assert.equal(L.validateProject(p).plants[0].onclick, undefined);
});
test('explicit UTC offsets handle day boundaries and fractional zones', () => {
  assert.equal(L.localToUTC('2026-06-21', '15:00', -4).toISOString(), '2026-06-21T19:00:00.000Z');
  assert.equal(L.localToUTC('2026-01-01', '00:15', 5.5).toISOString(), '2025-12-31T18:45:00.000Z');
  assert.equal(L.localToUTC('2026-12-31', '23:00', -5).toISOString(), '2027-01-01T04:00:00.000Z');
  assert.throws(() => L.localToUTC('2026-02-29', '12:00', 0));
  assert.throws(() => L.localToUTC('2026-01-01', '24:00', 0));
  assert.doesNotThrow(() => L.localToUTC('2024-02-29', '12:00', 0));
});
test('solar approximation agrees within 0.5 degrees with the NREL SPA example', () => {
  // NREL SPA report NREL/TP-560-34302, example: 2003-10-17 12:30:30 UTC-7,
  // lat 39.742476, lon -105.1786, zenith 50.11162°, azimuth 194.34024°.
  const s = L.solarPosition(39.742476, -105.1786, new Date('2003-10-17T19:30:30Z'));
  near(s.elevation, 90 - 50.11162, 0.5);
  near(s.azimuth, 194.34024, 0.5);
});
test('solar seasons, night, and hemispheres satisfy independent physical expectations', () => {
  const summer = L.solarPosition(40, 0, new Date('2026-06-21T12:00:00Z'));
  const winter = L.solarPosition(40, 0, new Date('2026-12-21T12:00:00Z'));
  near(summer.elevation, 73.44, 0.5);
  near(winter.elevation, 26.56, 0.5);
  assert.ok(summer.elevation > winter.elevation);
  assert.equal(L.solarPosition(40, 0, new Date('2026-06-21T00:00:00Z')).daylight, false);
  assert.ok(L.solarPosition(80, 0, new Date('2026-06-21T00:00:00Z')).daylight);
  assert.equal(L.solarPosition(80, 0, new Date('2026-12-21T12:00:00Z')).daylight, false);
  const south = L.solarPosition(-40, 0, new Date('2026-12-21T12:00:00Z'));
  near(south.elevation, 73.44, 0.5);
  assert.ok(south.azimuth < 5 || south.azimuth > 355);
});
test('morning sun is east and afternoon sun west', () => {
  const morning = L.solarPosition(40, 0, new Date('2026-06-21T09:00:00Z'));
  const afternoon = L.solarPosition(40, 0, new Date('2026-06-21T15:00:00Z'));
  assert.ok(morning.azimuth > 0 && morning.azimuth < 180);
  assert.ok(afternoon.azimuth > 180 && afternoon.azimuth < 360);
});
test('shadows have the expected length and point opposite sunlight in screen coordinates', () => {
  const north = L.shadowVector(120, 45, 180);
  near(north.length, 120);
  near(north.dx, 0);
  near(north.dy, -120);
  const west = L.shadowVector(120, 45, 90);
  near(west.dx, -120);
  near(west.dy, 0);
  assert.ok(L.shadowVector(120, 20, 90).length > L.shadowVector(120, 60, 90).length);
  assert.equal(L.shadowVector(120, -10, 90), null);
  assert.equal(L.shadowVector(120, 0.5, 90), null);
});
