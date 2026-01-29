document.addEventListener('DOMContentLoaded', () => {
  const fadeElements = document.querySelectorAll('.fade-in');
  fadeElements.forEach((element) => {
    element.style.opacity = '0';
    element.offsetHeight;
    setTimeout(() => {
      element.style.opacity = '1';
    }, 10);
  });
});
