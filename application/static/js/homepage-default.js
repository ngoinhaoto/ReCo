const swiper = new Swiper(".swiper", {
  // Optional parameters

  direction: "horizontal",
  loop: true,

  slidesPerView: 2,
  spaceBetween: 10,

  // If we need pagination
  pagination: {
    el: ".swiper-pagination",
  },

  // Navigation arrows
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },

  // And if we need scrollbar
  scrollbar: {
    el: ".swiper-scrollbar",
    dragClass: "swiper-scrollbar-drag",
  },
  autoplay: {
    delay: "500",
  },

  freeMode: {
    enabled: true,
  },
});
