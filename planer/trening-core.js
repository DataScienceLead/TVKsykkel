(function (root, factory) {
    var api = factory();
    root.TrainingCore = api;
    if (typeof module === "object" && module.exports) module.exports = api;
}(globalThis, function () {
    "use strict";

    var STORAGE_VERSION = 1;
    var STORAGE_KEY = "tvk.trainingDiary";

    function localDate(value) {
        if (value instanceof Date) return new Date(value.getFullYear(), value.getMonth(), value.getDate());
        var parts = String(value).split("-").map(Number);
        return new Date(parts[0], parts[1] - 1, parts[2]);
    }

    function isoDate(value) {
        var date = localDate(value);
        return [date.getFullYear(), String(date.getMonth() + 1).padStart(2, "0"), String(date.getDate()).padStart(2, "0")].join("-");
    }

    function addDays(value, days) {
        var date = localDate(value);
        date.setDate(date.getDate() + days);
        return date;
    }

    function startOfWeek(value) {
        var date = localDate(value);
        var offset = (date.getDay() + 6) % 7;
        return addDays(date, -offset);
    }

    function defaultAvailability() {
        return [0, 1, 2, 3, 4, 5, 6].map(function (dayIndex) {
            return { dayIndex: dayIndex, available: true, maxHours: 8, activity: "" };
        });
    }

    function defaultProfile(groupId) {
        return { groupId: groupId || "u17", availability: defaultAvailability() };
    }

    function normalizeProfile(profile, plans) {
        var groupId = profile && plans.groups[profile.groupId] ? profile.groupId : "u17";
        var supplied = profile && Array.isArray(profile.availability) ? profile.availability : [];
        var availability = defaultAvailability().map(function (fallback) {
            var value = supplied.find(function (item) { return item.dayIndex === fallback.dayIndex; });
            if (!value) return fallback;
            return {
                dayIndex: fallback.dayIndex,
                available: value.available !== false,
                maxHours: Math.max(0, Number(value.maxHours) || 0),
                activity: String(value.activity || "").trim().slice(0, 80),
            };
        });
        return { groupId: groupId, availability: availability };
    }

    function selectBaseWeek(plans, groupId, value) {
        var date = localDate(value);
        var dateString = isoDate(date);
        var group = plans.groups[groupId];
        if (!group) return null;
        var exact = group.weeks.find(function (week) {
            return week.start <= dateString && week.end >= dateString;
        });
        if (exact) return { source: "exact", plan: exact };
        var month = date.getMonth() + 1;
        var matches = group.templates.filter(function (template) { return template.months.includes(month); });
        if (!matches.length) return null;
        var training = matches.find(function (template) { return template.variant === "training"; });
        return { source: "template", plan: training || matches[0] };
    }

    function isHard(day) {
        return day.intensity === "high" || day.intensity === "max";
    }

    function canPlace(day, dayIndex, availability, assigned) {
        var slot = availability[dayIndex];
        if (!slot.available || day.maxHours > slot.maxHours || assigned[dayIndex]) return false;
        if (isHard(day)) {
            if (assigned[dayIndex - 1] && isHard(assigned[dayIndex - 1])) return false;
            if (assigned[dayIndex + 1] && isHard(assigned[dayIndex + 1])) return false;
        }
        return true;
    }

    function candidateDays(originalIndex) {
        return [0, 1, 2, 3, 4, 5, 6].sort(function (left, right) {
            var distance = Math.abs(left - originalIndex) - Math.abs(right - originalIndex);
            return distance || left - right;
        });
    }

    function personalizeWeek(baseWeek, profile, weekStart) {
        var assigned = {};
        var conflicts = [];
        var availability = profile.availability;
        var work = baseWeek.days.slice().sort(function (left, right) {
            return right.priority - left.priority || Number(left.movable) - Number(right.movable) || left.dayIndex - right.dayIndex;
        });

        work.forEach(function (day) {
            var target = day.dayIndex;
            if (!canPlace(day, target, availability, assigned)) {
                target = -1;
                if (day.movable && day.category !== "rest") {
                    target = candidateDays(day.dayIndex).find(function (candidate) {
                        return canPlace(day, candidate, availability, assigned);
                    });
                    if (target === undefined) target = -1;
                }
            }
            if (target < 0) {
                if (day.category !== "rest") conflicts.push({ workout: day, reason: "Ingen tilgjengelig dag har nok tid og restitusjon." });
                return;
            }
            assigned[target] = Object.assign({}, day, {
                originalDayIndex: day.dayIndex,
                dayIndex: target,
                moved: target !== day.dayIndex,
                date: isoDate(addDays(weekStart, target)),
            });
        });

        var days = [0, 1, 2, 3, 4, 5, 6].map(function (dayIndex) {
            return {
                dayIndex: dayIndex,
                date: isoDate(addDays(weekStart, dayIndex)),
                availability: availability[dayIndex],
                workout: assigned[dayIndex] || null,
            };
        });
        return { days: days, conflicts: conflicts };
    }

    function buildWeek(plans, profileValue, value) {
        var profile = normalizeProfile(profileValue, plans);
        var weekStart = startOfWeek(value);
        var selected = selectBaseWeek(plans, profile.groupId, value);
        if (!selected) return { profile: profile, weekStart: isoDate(weekStart), source: null, base: null, days: [], conflicts: [] };
        var personalized = personalizeWeek(selected.plan, profile, weekStart);
        return Object.assign({
            profile: profile,
            weekStart: isoDate(weekStart),
            source: selected.source,
            base: selected.plan,
        }, personalized);
    }

    function completionKey(groupId, date, workoutId) {
        return [groupId, isoDate(date), workoutId].join(":");
    }

    function freshState(groupId) {
        return { version: STORAGE_VERSION, setupComplete: false, profile: defaultProfile(groupId), completions: {} };
    }

    function parseState(serialized, plans) {
        try {
            var state = JSON.parse(serialized);
            if (!state || state.version !== STORAGE_VERSION || typeof state.completions !== "object") return freshState();
            return {
                version: STORAGE_VERSION,
                setupComplete: state.setupComplete === true,
                profile: normalizeProfile(state.profile, plans),
                completions: state.completions,
            };
        } catch (error) {
            return freshState();
        }
    }

    return {
        STORAGE_KEY: STORAGE_KEY,
        STORAGE_VERSION: STORAGE_VERSION,
        addDays: addDays,
        buildWeek: buildWeek,
        completionKey: completionKey,
        defaultProfile: defaultProfile,
        isoDate: isoDate,
        normalizeProfile: normalizeProfile,
        parseState: parseState,
        personalizeWeek: personalizeWeek,
        selectBaseWeek: selectBaseWeek,
        startOfWeek: startOfWeek,
    };
}));