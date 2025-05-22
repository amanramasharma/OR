// Constants
const ANIMATION_DURATION = 2000;
const ANIMATION_STEPS = 60;
const SLIDER_INTERVAL = 5000;

// Utility functions
const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Navbar Module
const NavbarModule = {
  init() {
    // Add click event listeners to both menu toggle buttons
    const menuOpenButton = document.querySelector(".cursor-pointer");
    const menuCloseButton = document.querySelector("#mobileMenu div svg");
    const menuLinks = document.querySelectorAll("#mobileMenu a");

    if (menuOpenButton) {
      menuOpenButton.addEventListener("click", () => this.toggleMobileMenu());
    }

    if (menuCloseButton) {
      menuCloseButton.parentElement.addEventListener("click", () =>
        this.toggleMobileMenu()
      );
    }

    // Add click event listeners to all menu links
    menuLinks.forEach((link) => {
      link.addEventListener("click", () => this.toggleMobileMenu());
    });

    // Add click outside listener
    document.addEventListener("click", (e) => {
      const menu = document.getElementById("mobileMenu");
      const isClickInsideMenu = menu?.contains(e.target);
      const isClickOnToggle = menuOpenButton?.contains(e.target);

      if (
        menu &&
        !isClickInsideMenu &&
        !isClickOnToggle &&
        !menu.classList.contains("-right-full")
      ) {
        this.toggleMobileMenu();
      }
    });
  },

  toggleMobileMenu() {
    const menu = document.getElementById("mobileMenu");
    if (!menu) return;

    // Toggle the menu position
    if (menu.classList.contains("-right-full")) {
      menu.classList.remove("-right-full");
      menu.classList.add("right-0");
    } else {
      menu.classList.remove("right-0");
      menu.classList.add("-right-full");
    }
  },
};

// FAQ Module
const FAQModule = {
  init() {
    document.querySelectorAll('[id^="accordion"]').forEach((content) => {
      const button = content.previousElementSibling;
      if (button) {
        button.addEventListener("click", () =>
          this.toggleAccordion(content.id)
        );
      }
    });
  },

  toggleAccordion(id) {
    const content = document.getElementById(id);
    if (!content) return;

    const button = content.previousElementSibling;
    const svg = button?.querySelector("svg");
    const isHidden = content.classList.contains("hidden");

    // Close other accordions
    if (isHidden) {
      this.closeAllAccordions();
    }

    // Toggle current accordion
    content.classList.toggle("hidden", !isHidden);
    content.style.maxHeight = isHidden ? `${content.scrollHeight}px` : "0px";
    if (svg) {
      svg.style.transform = isHidden ? "rotate(180deg)" : "rotate(0)";
    }
  },

  closeAllAccordions() {
    document.querySelectorAll('[id^="accordion"]').forEach((el) => {
      if (!el.classList.contains("hidden")) {
        el.style.maxHeight = "0px";
        el.classList.add("hidden");
        const svg = el.previousElementSibling?.querySelector("svg");
        if (svg) {
          svg.style.transform = "rotate(0)";
        }
      }
    });
  },
};

// Counter Module
const CounterModule = {
  init() {
    this.setupCounter("counter", 36);
    this.setupProgressCounters();
  },

  setupCounter(elementId, targetNumber) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            this.animateCounter(element, targetNumber);
            observer.disconnect();
          }
        });
      },
      { threshold: 0.1 }
    );

    observer.observe(element);
  },

  setupProgressCounters() {
    this.createProgressCounter("progress1", 65);
    this.createProgressCounter("progress2", 75);
  },

  animateCounter(element, targetNumber, current = 0) {
    const increment = targetNumber / ANIMATION_STEPS;
    current += increment;

    if (current > targetNumber) {
      element.textContent = Math.round(targetNumber);
      return;
    }

    element.textContent = Math.round(current);
    requestAnimationFrame(() =>
      this.animateCounter(element, targetNumber, current)
    );
  },

  createProgressCounter(elementId, targetValue) {
    const element = document.getElementById(elementId);
    if (!element) return;

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            this.animateProgress(element, targetValue);
            observer.disconnect();
          }
        });
      },
      { threshold: 0.1 }
    );

    observer.observe(element);
  },

  animateProgress(element, targetValue, startTime = null) {
    const timestamp = performance.now();
    if (!startTime) startTime = timestamp;

    const progress = timestamp - startTime;
    const percentage = Math.min(progress / ANIMATION_DURATION, 1);
    const current = targetValue * percentage;

    element.textContent = `${Math.round(current)}%`;

    if (progress < ANIMATION_DURATION) {
      requestAnimationFrame(() =>
        this.animateProgress(element, targetValue, startTime)
      );
    }
  },
};

// Slider Module
const SliderModule = {
  currentIndex: 0,
  intervalId: null,

  init() {
    this.slides = document.querySelectorAll(".testimonial-slide");
    this.images = document.querySelectorAll(".testimonial-image");
    this.prevButton = document.querySelector(".prev-slide");
    this.nextButton = document.querySelector(".next-slide");

    if (!this.slides.length || !this.images.length) return;

    this.setupEventListeners();
    this.startAutoPlay();
  },

  setupEventListeners() {
    if (this.prevButton) {
      this.prevButton.addEventListener("click", () => this.prevSlide());
    }
    if (this.nextButton) {
      this.nextButton.addEventListener("click", () => this.nextSlide());
    }

    // Pause autoplay on hover
    const sliderContainer = document.querySelector(".testimonial-container");
    if (sliderContainer) {
      sliderContainer.addEventListener("mouseenter", () =>
        this.pauseAutoPlay()
      );
      sliderContainer.addEventListener("mouseleave", () =>
        this.startAutoPlay()
      );
    }
  },

  showSlide(index) {
    this.slides.forEach((slide) => slide.classList.remove("active"));
    this.images.forEach((image) => image.classList.remove("active"));

    this.slides[index].classList.add("active");
    this.images[index].classList.add("active");
  },

  nextSlide() {
    this.currentIndex = (this.currentIndex + 1) % this.slides.length;
    this.showSlide(this.currentIndex);
  },

  prevSlide() {
    this.currentIndex =
      (this.currentIndex - 1 + this.slides.length) % this.slides.length;
    this.showSlide(this.currentIndex);
  },

  startAutoPlay() {
    if (this.intervalId) return;
    this.intervalId = setInterval(() => this.nextSlide(), SLIDER_INTERVAL);
  },

  pauseAutoPlay() {
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
  },
};

// Initialize all modules when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  NavbarModule.init();
  FAQModule.init();
  CounterModule.init();
  SliderModule.init();
});

// AOS Animation
AOS.init({
  once: true,
});
