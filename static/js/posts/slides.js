document.addEventListener('DOMContentLoaded', function() {
  var elems = document.querySelectorAll('.materialboxed');
  var instances = M.Materialbox.init(elems);
});

let params = new URLSearchParams(document.location.search)
let slide = params.get("slide");
if (slide == null) {
  globalThis.slideIndex = 1;
}
else {
  globalThis.slideIndex = parseInt(slide);
};

showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
  window.location.href = `/post/view/?slide=${slideIndex}`;
}

function currentSlide(n) {
  showSlides(slideIndex = n);
  window.location.href = `/post/view/?slide=${slideIndex}`;
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {slideIndex = 1}    
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    let video = slides[i].querySelector("video");
    if (video) {
      video.pause();
      video.currentTime = 0;
    }
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
  let currentVideo = slides[slideIndex - 1].querySelector("video");
  if (currentVideo) {
    currentVideo.play().catch(err => console.log(err));
  }
}