(() => {
  const STORAGE_KEY = "gpu:progress:v1";

  function safeParse(value) {
    if (!value) return {};
    try {
      const parsed = JSON.parse(value);
      return typeof parsed === "object" && parsed ? parsed : {};
    } catch {
      return {};
    }
  }

  function nowIso() {
    return new Date().toISOString();
  }

  function load() {
    return safeParse(localStorage.getItem(STORAGE_KEY));
  }

  function save(state) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    window.dispatchEvent(new CustomEvent("gpu-progress-change"));
  }

  function getLesson(state, lessonId) {
    if (!state.lessons) state.lessons = {};
    if (!state.lessons[lessonId]) {
      state.lessons[lessonId] = {
        visitedAt: nowIso(),
        completedAt: "",
        checks: { ran: false, artifact: false },
      };
    }
    return state.lessons[lessonId];
  }

  function markVisited(lessonId) {
    const state = load();
    const lesson = getLesson(state, lessonId);
    if (!lesson.visitedAt) lesson.visitedAt = nowIso();
    save(state);
  }

  function setCheck(lessonId, checkName, checked) {
    const state = load();
    const lesson = getLesson(state, lessonId);
    lesson.checks = lesson.checks || {};
    lesson.checks[checkName] = checked;
    if (checked && !lesson.completedAt && lesson.checks.ran && lesson.checks.artifact) {
      lesson.completedAt = nowIso();
    }
    save(state);
  }

  function markComplete(lessonId) {
    const state = load();
    const lesson = getLesson(state, lessonId);
    if (!lesson.completedAt) lesson.completedAt = nowIso();
    lesson.checks = lesson.checks || {};
    lesson.checks.ran = true;
    lesson.checks.artifact = true;
    save(state);
  }

  function isComplete(lessonId) {
    const state = load();
    return Boolean(state?.lessons?.[lessonId]?.completedAt);
  }

  function reset() {
    localStorage.removeItem(STORAGE_KEY);
    window.dispatchEvent(new CustomEvent("gpu-progress-change"));
  }

  function getCompletedSet() {
    const state = load();
    const set = new Set();
    const lessons = state.lessons || {};
    Object.keys(lessons).forEach((lessonId) => {
      if (lessons[lessonId] && lessons[lessonId].completedAt) set.add(lessonId);
    });
    return set;
  }

  function renderHomeStats(catalog) {
    if (!catalog || !catalog.phases) return;
    const completed = getCompletedSet();
    const allLessons = catalog.phases.flatMap((phase) => phase.lessons || []);
    const totalLessons = allLessons.length;
    const completedCount = allLessons.filter((lesson) => completed.has(lesson.id)).length;

    const finished = document.getElementById("stat-lessons-finished");
    const finishedBar = document.getElementById("bar-lessons-finished");
    if (finished) finished.textContent = `${completedCount}/${totalLessons}`;
    if (finishedBar) finishedBar.style.width = `${totalLessons ? (completedCount / totalLessons) * 100 : 0}%`;

    let phasesStarted = 0;
    (catalog.phases || []).forEach((phase) => {
      const lessons = phase.lessons || [];
      const doneInPhase = lessons.filter((lesson) => completed.has(lesson.id)).length;
      if (doneInPhase > 0) phasesStarted += 1;
      const phaseNode = document.querySelector(`[data-phase-progress="${phase.id}"]`);
      if (phaseNode) phaseNode.textContent = `${doneInPhase}/${lessons.length}`;
    });

    const phaseStat = document.getElementById("stat-phases-started");
    const phaseBar = document.getElementById("bar-phases-started");
    if (phaseStat) phaseStat.textContent = `${phasesStarted}/${catalog.phase_count || 0}`;
    if (phaseBar) phaseBar.style.width = `${catalog.phase_count ? (phasesStarted / catalog.phase_count) * 100 : 0}%`;
  }

  function bindLessonControls() {
    const markButton = document.querySelector("[data-mark-complete]");
    if (!markButton) return;
    const lessonId = markButton.getAttribute("data-mark-complete") || "";
    if (!lessonId) return;

    markVisited(lessonId);
    const state = load();
    const lesson = getLesson(state, lessonId);
    save(state);

    document.querySelectorAll(`[data-lesson-id="${lessonId}"]`).forEach((input) => {
      const checkName = input.getAttribute("data-lesson-check");
      if (!(input instanceof HTMLInputElement) || !checkName) return;
      input.checked = Boolean(lesson.checks?.[checkName]);
      input.addEventListener("change", () => {
        setCheck(lessonId, checkName, input.checked);
      });
    });

    markButton.addEventListener("click", () => {
      markComplete(lessonId);
      document.querySelectorAll(`[data-lesson-id="${lessonId}"]`).forEach((input) => {
        if (input instanceof HTMLInputElement) input.checked = true;
      });
    });
  }

  window.GPUProgress = {
    bindLessonControls,
    isComplete,
    load,
    markComplete,
    renderHomeStats,
    reset,
  };
})();
