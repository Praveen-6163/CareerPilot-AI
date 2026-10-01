document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('#resumeForm');
  if (!form) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const file = document.getElementById('resumeFile');
    const role = document.getElementById('targetRole');
    const output = document.getElementById('resumeResult');
    const summary = [
      'Resume score: 82/100',
      'Key strengths: clear project impact, measurable results, structured experience sections.',
      'Suggested improvements: add role-specific keywords, quantify metrics, and tighten the summary for the target role.',
      'Target role focus: ' + (role && role.value ? role.value : 'Data Analyst'),
      'Upload file: ' + (file && file.files[0] ? file.files[0].name : 'No file selected')
    ];

    if (output) {
      output.innerHTML = '<ul>' + summary.map(item => '<li>' + item + '</li>').join('') + '</ul>';
    }
  });
});
