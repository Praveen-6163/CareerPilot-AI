document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('#careerForm');
  if (!form) return;
  const steps = [...document.querySelectorAll('.step')];
  const nextBtn = document.querySelector('#nextStep');
  const prevBtn = document.querySelector('#prevStep');
  const submitBtn = document.querySelector('#submitCareer');
  let currentStep = 0;

  function updateStepUI() {
    steps.forEach((step, index) => step.classList.toggle('active', index === currentStep));
    prevBtn.classList.toggle('hidden', currentStep === 0);
    nextBtn.classList.toggle('hidden', currentStep === steps.length - 1);
    submitBtn.classList.toggle('hidden', currentStep !== steps.length - 1);
  }

  nextBtn.addEventListener('click', () => {
    if (currentStep < steps.length - 1) currentStep += 1;
    updateStepUI();
  });

  prevBtn.addEventListener('click', () => {
    if (currentStep > 0) currentStep -= 1;
    updateStepUI();
  });

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(form).entries());
    alert('Career plan generated for ' + (data.targetRole || 'your target role') + ' using AI guidance.');
    console.log('Career form submission:', data);
  });

  updateStepUI();
});
