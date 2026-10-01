(function () {
    "use strict";

    var plans = globalThis.TRAINING_PLANS;
    var core = globalThis.TrainingCore;
    var root = document.getElementById("trainingDiary");
    if (!plans || !core || !root) return;

    var dayNames = ["Mandag", "Tirsdag", "Onsdag", "Torsdag", "Fredag", "Lørdag", "Søndag"];
    var intensityNames = { rest: "Hvile", low: "Rolig", medium: "Moderat", high: "Hard", max: "Maks" };
    var categoryNames = { rest: "Hvile", race: "Ritt", strength: "Styrke", interval: "Intervall", endurance: "Langkjøring", easy: "Rolig økt" };
    var selectedDate = new Date();
    var activeView = "day";
    var state = loadState();

    function escapeHtml(value) {
        return String(value).replace(/[&<>'"]/g, function (character) {
            return { "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[character];
        });
    }

    function loadState() {
        try {
            var serialized = localStorage.getItem(core.STORAGE_KEY);
            return serialized ? core.parseState(serialized, plans) : core.parseState("", plans);
        } catch (error) {
            return core.parseState("", plans);
        }
    }

    function saveState() {
        try {
            localStorage.setItem(core.STORAGE_KEY, JSON.stringify(state));
        } catch (error) {
            showStorageMessage("Nettleseren kunne ikke lagre endringen. Planen kan fortsatt vises, men valgene forsvinner ved oppdatering.");
        }
    }

    function showStorageMessage(message) {
        var element = document.getElementById("diaryStorageMessage");
        element.textContent = message;
        element.hidden = !message;
    }

    function formatDate(value, options) {
        return new Intl.DateTimeFormat("nb-NO", options).format(value instanceof Date ? value : new Date(value + "T12:00:00"));
    }

    function formatWeekRange(start) {
        var end = core.addDays(start, 6);
        return formatDate(start, { day: "numeric", month: "short" }) + " – " +
            formatDate(end, { day: "numeric", month: "short", year: "numeric" });
    }

    function setupRows() {
        return state.profile.availability.map(function (slot) {
            return '<div class="availability-row">' +
                '<label class="availability-toggle"><input type="checkbox" data-field="available" data-day="' + slot.dayIndex + '"' + (slot.available ? " checked" : "") + '> <span>' + dayNames[slot.dayIndex] + '</span></label>' +
                '<label><span class="sr-only">Maks timer ' + dayNames[slot.dayIndex] + '</span><input class="hours-input" type="number" min="0" max="8" step="0.5" value="' + slot.maxHours + '" data-field="maxHours" data-day="' + slot.dayIndex + '" aria-label="Maks timer ' + dayNames[slot.dayIndex] + '"></label>' +
                '<label><span class="sr-only">Fast aktivitet ' + dayNames[slot.dayIndex] + '</span><input type="text" maxlength="80" value="' + escapeHtml(slot.activity) + '" data-field="activity" data-day="' + slot.dayIndex + '" placeholder="Skole eller annen aktivitet" aria-label="Fast aktivitet ' + dayNames[slot.dayIndex] + '"></label>' +
            '</div>';
        }).join("");
    }

    function renderSetup() {
        document.getElementById("diaryGroup").value = state.profile.groupId;
        document.getElementById("availabilityRows").innerHTML = setupRows();
        document.getElementById("diarySetup").hidden = false;
        document.getElementById("diaryDashboard").hidden = true;
    }

    function collectProfile() {
        var availability = dayNames.map(function (_, dayIndex) {
            var available = document.querySelector('[data-field="available"][data-day="' + dayIndex + '"]');
            var hours = document.querySelector('[data-field="maxHours"][data-day="' + dayIndex + '"]');
            var activity = document.querySelector('[data-field="activity"][data-day="' + dayIndex + '"]');
            return {
                dayIndex: dayIndex,
                available: available.checked,
                maxHours: Number(hours.value),
                activity: activity.value,
            };
        });
        return core.normalizeProfile({ groupId: document.getElementById("diaryGroup").value, availability: availability }, plans);
    }

    function workoutCard(day, compact) {
        if (!day.workout) {
            var reason = day.availability.available ? "Ingen planlagt økt" : "Ikke tilgjengelig";
            var activity = day.availability.activity ? " · " + escapeHtml(day.availability.activity) : "";
            return '<div class="diary-workout diary-workout-empty"><div><strong>' + reason + '</strong><span>' + activity + '</span></div></div>';
        }
        var workout = day.workout;
        var key = core.completionKey(state.profile.groupId, day.date, workout.id);
        var completed = state.completions[key] === true;
        var moved = workout.moved ? '<span class="moved-note">Flyttet fra ' + dayNames[workout.originalDayIndex].toLowerCase() + '</span>' : "";
        return '<article class="diary-workout intensity-border-' + workout.intensity + (completed ? " is-complete" : "") + '">' +
            '<div class="workout-main"><div class="workout-tags"><span class="activity-type type-' + (workout.category === "strength" ? "strength" : workout.category === "rest" ? "rest" : "ride") + '">' + escapeHtml(categoryNames[workout.category] || "Økt") + '</span>' +
            '<span class="intensity-badge intensity-' + workout.intensity + '">' + escapeHtml(intensityNames[workout.intensity]) + '</span>' + moved + '</div>' +
            '<h4>' + escapeHtml(workout.title) + '</h4>' +
            '<p>' + escapeHtml(workout.duration) + (day.availability.activity ? ' · Fast aktivitet: ' + escapeHtml(day.availability.activity) : "") + '</p></div>' +
            '<label class="complete-control"><input type="checkbox" data-completion="' + escapeHtml(key) + '"' + (completed ? " checked" : "") + '><span>' + (completed ? "Fullført" : "Marker fullført") + '</span></label>' +
        '</article>';
    }

    function renderDay(result) {
        var dateString = core.isoDate(selectedDate);
        var day = result.days.find(function (item) { return item.date === dateString; });
        if (!day) return '<div class="diary-empty"><strong>Ingen plan for denne dagen</strong><p>Velg en dato innenfor en publisert planperiode.</p></div>';
        return '<div class="day-focus"><div class="day-focus-date"><span>' + formatDate(day.date, { weekday: "long" }) + '</span><strong>' + formatDate(day.date, { day: "numeric", month: "long" }) + '</strong></div>' + workoutCard(day, false) + '</div>';
    }

    function renderWeek(result) {
        return '<div class="diary-week-list">' + result.days.map(function (day) {
            return '<section class="diary-day-row' + (day.date === core.isoDate(new Date()) ? " is-today" : "") + '"><div class="diary-day-heading"><strong>' + dayNames[day.dayIndex] + '</strong><span>' + formatDate(day.date, { day: "numeric", month: "short" }) + '</span></div>' + workoutCard(day, true) + '</section>';
        }).join("") + '</div>';
    }

    function renderConflicts(conflicts) {
        var element = document.getElementById("diaryConflicts");
        if (!conflicts.length) {
            element.hidden = true;
            element.innerHTML = "";
            return;
        }
        element.hidden = false;
        element.innerHTML = '<strong>' + conflicts.length + ' økt' + (conflicts.length === 1 ? "" : "er") + ' kunne ikke plasseres trygt.</strong><p>Juster tilgjengeligheten eller avklar tilpasningen med trener.</p><ul>' + conflicts.map(function (conflict) { return '<li>' + escapeHtml(conflict.workout.title) + '</li>'; }).join("") + '</ul>';
    }

    function renderDashboard() {
        var result = core.buildWeek(plans, state.profile, selectedDate);
        document.getElementById("diarySetup").hidden = true;
        document.getElementById("diaryDashboard").hidden = false;
        document.getElementById("profileSummary").textContent = plans.groups[state.profile.groupId].label + " · lagres på denne enheten";
        document.querySelectorAll("[data-view]").forEach(function (button) {
            var selected = button.dataset.view === activeView;
            button.classList.toggle("active", selected);
            button.setAttribute("aria-selected", String(selected));
        });
        document.getElementById("diaryPeriod").textContent = activeView === "day"
            ? formatDate(selectedDate, { weekday: "long", day: "numeric", month: "long", year: "numeric" })
            : formatWeekRange(core.startOfWeek(selectedDate));

        var content = document.getElementById("diaryContent");
        if (!result.base) {
            content.innerHTML = '<div class="diary-empty"><strong>Ingen publisert plan for denne perioden</strong><p>Planen inneholder ikke økter for denne måneden. Se PDF-planen eller kontakt trener.</p></div>';
            document.getElementById("diaryWeekMeta").textContent = "Ingen plandata";
            renderConflicts([]);
            return;
        }
        var completed = result.days.filter(function (day) {
            return day.workout && day.workout.category !== "rest" && state.completions[core.completionKey(state.profile.groupId, day.date, day.workout.id)];
        }).length;
        var workouts = result.days.filter(function (day) { return day.workout && day.workout.category !== "rest"; });
        var hours = workouts.reduce(function (sum, day) { return sum + day.workout.maxHours; }, 0);
        document.getElementById("diaryWeekMeta").textContent = result.base.phase + " · " + completed + "/" + workouts.length + " fullført · inntil " + String(hours).replace(".", ",") + " t";
        content.innerHTML = activeView === "day" ? renderDay(result) : renderWeek(result);
        renderConflicts(result.conflicts);
    }

    document.getElementById("saveProfile").addEventListener("click", function () {
        state.profile = collectProfile();
        state.setupComplete = true;
        saveState();
        renderDashboard();
    });

    document.getElementById("editProfile").addEventListener("click", renderSetup);
    document.getElementById("cancelProfile").addEventListener("click", function () {
        state.setupComplete ? renderDashboard() : renderSetup();
    });
    document.getElementById("resetDiary").addEventListener("click", function () {
        if (!confirm("Vil du slette lokal profil og all fullført-status på denne enheten?")) return;
        try { localStorage.removeItem(core.STORAGE_KEY); } catch (error) { /* Nothing else to clear. */ }
        state = core.parseState("", plans);
        selectedDate = new Date();
        renderSetup();
    });

    document.querySelectorAll("[data-view]").forEach(function (button) {
        button.addEventListener("click", function () {
            activeView = button.dataset.view;
            renderDashboard();
        });
    });

    document.querySelectorAll("[data-navigate]").forEach(function (button) {
        button.addEventListener("click", function () {
            var step = activeView === "day" ? 1 : 7;
            selectedDate = core.addDays(selectedDate, Number(button.dataset.navigate) * step);
            renderDashboard();
        });
    });
    document.getElementById("goToday").addEventListener("click", function () {
        selectedDate = new Date();
        renderDashboard();
    });

    document.getElementById("diaryContent").addEventListener("change", function (event) {
        if (!event.target.matches("[data-completion]")) return;
        state.completions[event.target.dataset.completion] = event.target.checked;
        saveState();
        renderDashboard();
    });

    if (state.setupComplete) renderDashboard(); else renderSetup();
}());