document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('assistantToggle');
  const panel = document.getElementById('assistantPanel');
  if (toggle && panel) {
    toggle.addEventListener('click', () => {
      panel.classList.toggle('open');
    });
  }

  document.querySelectorAll('[data-question]').forEach((button) => {
    button.addEventListener('click', () => {
      const out = document.getElementById('assistantOutput');
      if (out) {
        out.textContent = 'CareerPilot AI suggests: ' + button.dataset.question + '. Focus on skill development, resume improvement, and a consistent practice plan.';
      }
    });
  });

  const input = document.getElementById('assistantInput');
  const send = document.getElementById('assistantSend');
  if (input && send) {
    send.addEventListener('click', () => {
      const output = document.getElementById('assistantOutput');
      if (output) {
        output.textContent = input.value
          ? 'CareerPilot AI: ' + input.value + ' — build a focused plan around the highest-priority skill, resume updates, and weekly practice tasks.'
          : 'Ask about your roadmap, resume, or interview prep.';
      }
    });
  }
});
