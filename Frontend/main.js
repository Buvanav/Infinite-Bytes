const dots = document.querySelectorAll('.dot');
const nextBtn = document.getElementById('nextBtn');
console.log('dots length:', dots.length);
console.log('nextBtn:', nextBtn);

let currentIndex = 0;

nextBtn.addEventListener('click', () => {
  console.log('Next clicked');   // test
  dots[currentIndex].classList.remove('dot-active');
  currentIndex = (currentIndex + 1) % dots.length;
  dots[currentIndex].classList.add('dot-active');

  setTimeout(() => {
    window.location.href = 'signup.html';
  }, 400);
});





