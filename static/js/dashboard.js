document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('readinessGrid');
  if (!grid) return;

  const items = [
    ['Profile Fit', '8/10'],
    ['Resume Match', '82%'],
    ['Portfolio', '2/3'],
    ['Interview Prep', '5/7'],
    ['Skill Growth', 'High'],
    ['Job Search', 'Active']
  ];

  grid.innerHTML = items.map(([label, value]) => `
    <div class="pill">
      <span>${label}</span>
      <strong>${value}</strong>
    </div>
  `).join('');
});
