const test = require("node:test");
const assert = require("node:assert/strict");

require("../data/trening.js");
const core = require("./trening-core.js");
const plans = globalThis.TRAINING_PLANS;

test("selects a dated week before a monthly template", () => {
    const selected = core.selectBaseWeek(plans, "u17", "2026-10-01");
    assert.equal(selected.source, "exact");
    assert.equal(selected.plan.start, "2026-09-28");
});

test("selects the monthly template outside dated blocks", () => {
    const selected = core.selectBaseWeek(plans, "u15", "2026-03-12");
    assert.equal(selected.source, "template");
    assert.deepEqual(selected.plan.months, [3]);
});

test("returns no plan for a month without source material", () => {
    assert.equal(core.selectBaseWeek(plans, "u17", "2026-01-12"), null);
});

test("moves a movable workout to the nearest available day", () => {
    const profile = core.defaultProfile("u15");
    profile.availability[1] = { dayIndex: 1, available: false, maxHours: 0, activity: "Skole" };
    const result = core.buildWeek(plans, profile, "2026-03-10");
    const moved = result.days.map(day => day.workout).find(workout => workout && workout.originalDayIndex === 1);
    assert.ok(moved);
    assert.notEqual(moved.dayIndex, 1);
    assert.equal(moved.moved, true);
});

test("reports a conflict rather than increasing available time", () => {
    const profile = core.defaultProfile("u19");
    profile.availability = profile.availability.map(slot => ({ ...slot, maxHours: 0.5 }));
    const result = core.buildWeek(plans, profile, "2026-07-01");
    assert.ok(result.conflicts.length > 0);
    assert.ok(result.days.every(day => !day.workout || day.workout.maxHours <= 0.5));
});

test("creates stable date-specific completion keys", () => {
    assert.equal(core.completionKey("u17", "2026-10-01", "workout-1"), "u17:2026-10-01:workout-1");
});

test("invalid or old storage data resets safely", () => {
    assert.equal(core.parseState("not json", plans).version, core.STORAGE_VERSION);
    assert.deepEqual(core.parseState('{"version":0}', plans).completions, {});
});