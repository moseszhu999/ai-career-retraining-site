window.ProofSkillState = (() => {
  const storageKey = 'proofskill_v8_app_state';

  const initialState = {
    currentRole: 'learner',
    evidence: 'not_generated',
    hashesComputed: false,
    issuerReview: 'not_requested',
    evaluatorReview: 'not_assigned',
    evaluatorSetHash: null,
    proofStatus: 'not_registered',
    trustLevel: 'none',
    issuedCount: 0,
    issuerCount: 1,
    events: []
  };

  function load() {
    try {
      return JSON.parse(localStorage.getItem(storageKey)) || { ...initialState };
    } catch {
      return { ...initialState };
    }
  }

  let state = load();

  function save() {
    localStorage.setItem(storageKey, JSON.stringify(state));
  }

  function addEvent(message) {
    state.events.unshift(`${new Date().toLocaleTimeString()} · ${message}`);
    save();
  }

  function reset() {
    state = { ...initialState, events: [] };
    localStorage.removeItem(storageKey);
  }

  function mutate(mutator, eventMessage) {
    mutator(state);
    if (eventMessage) addEvent(eventMessage);
    save();
  }

  return {
    get state() {
      return state;
    },
    save,
    reset,
    mutate,
    addEvent
  };
})();
