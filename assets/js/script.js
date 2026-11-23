'use strict';

// ==========================================
// 1. TEMPLATE UI LOGIC (NAVBAR & HEADER)
// ==========================================

/**
 * add event on element
 */
const addEventOnElem = function (elem, type, callback) {
  if (!elem) return;
  // NodeList / array-like (but not a single Element)
  if (elem instanceof NodeList || Array.isArray(elem)) {
    for (let i = 0; i < elem.length; i++) {
      elem[i].addEventListener(type, callback);
    }
  } else if (typeof elem.addEventListener === "function") {
    elem.addEventListener(type, callback);
  }
};

/**
 * toggle navbar
 */
const navbar = document.querySelector("[data-navbar]");
const navLinks = document.querySelectorAll("[data-nav-link]");
const navToggler = document.querySelector("[data-nav-toggler]");

const syncNavbarA11y = function (isOpen) {
  if (navToggler) {
    navToggler.setAttribute("aria-expanded", String(isOpen));
    navToggler.setAttribute("aria-label", isOpen ? "Close menu" : "Open menu");
  }
};

const toggleNavbar = function () {
  if (!navbar) return;
  navbar.classList.toggle("active");
  if (navToggler) navToggler.classList.toggle("active");
  syncNavbarA11y(navbar.classList.contains("active"));
};

if (navToggler) addEventOnElem(navToggler, "click", toggleNavbar);

const closeNavbar = function () {
  if (navbar) navbar.classList.remove("active");
  if (navToggler) navToggler.classList.remove("active");
  syncNavbarA11y(false);
};

if (navLinks.length > 0) addEventOnElem(navLinks, "click", closeNavbar);

// Escape closes the mobile menu (keyboard accessibility)
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape" && navbar && navbar.classList.contains("active")) {
    closeNavbar();
    if (navToggler) navToggler.focus();
  }
});

// Clicking outside the open menu closes it
document.addEventListener("click", function (event) {
  if (!navbar || !navbar.classList.contains("active")) return;
  if (navbar.contains(event.target) || (navToggler && navToggler.contains(event.target))) return;
  closeNavbar();
});

/**
 * header active
 */
const header = document.querySelector("[data-header]");

window.addEventListener("scroll", function () {
  if (header) {
    if (window.scrollY > 100) {
      header.classList.add("active");
    } else {
      header.classList.remove("active");
    }
  }
});


// ==========================================
// 2. CUSTOM FEATURES (PRELOADER, TIMELINE, CTF, FORM)
// ==========================================

document.addEventListener("DOMContentLoaded", () => {

  // --- A. MINIMALIST PRELOADER ---
  const preloader = document.getElementById("preloader");
  const typingTextElement = document.getElementById("typing-text");
  const textToType = "Establishing secure connection...";
  let index = 0;

  function typeString() {
    if (typingTextElement && index < textToType.length) {
      typingTextElement.textContent += textToType.charAt(index);
      index++;
      setTimeout(typeString, 50); 
    }
  }

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (preloader) {
    if (prefersReducedMotion) {
      preloader.classList.add("preloader-hidden");
      setTimeout(() => {
        if (preloader.parentNode) preloader.parentNode.removeChild(preloader);
      }, 100);
    } else {
      typeString(); // Start typing

      setTimeout(() => {
        preloader.classList.add("preloader-hidden");
        setTimeout(() => {
          if (preloader.parentNode) preloader.parentNode.removeChild(preloader);
        }, 500);
      }, 2500);
    }
  }

  // --- B. TIMELINE SCROLL REVEAL (Experience only; Education stays visible) ---
  const timelineSection = document.querySelector(".experience .timeline");
  const timelineItems = document.querySelectorAll(".experience .timeline-item");

  if (timelineSection && timelineItems.length > 0) {
    if (prefersReducedMotion) {
      timelineItems.forEach((item) => item.classList.add("show"));
    } else {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            timelineItems.forEach((item, index) => {
              setTimeout(() => {
                item.classList.add("show");
              }, index * 200);
            });
            observer.unobserve(entry.target);
          }
        });
      }, { threshold: 0.2 });

      observer.observe(timelineSection);
    }
  }

  // --- C. CTF CHALLENGE LOGIC ---
  const submitFlagBtn = document.getElementById("submit-flag");
  const flagInput = document.getElementById("flag-input");
  const ctfMessage = document.getElementById("ctf-message");
  const resumeDownload = document.getElementById("resume-download");
  const inputArea = document.getElementById("ctf-input-area");

  const terminalBox = document.querySelector(".terminal-box") || document.querySelector(".terminal-body");

  // SHA-256 of the correct flag (flag itself is not stored in plaintext).
  // Note: on a static site this only hides the flag from casual view-source;
  // the PDF remains publicly downloadable by design. For true gating, verify server-side.
  const FLAG_HASH = "7f5c0d5f5ddbcd96c88f19738e6661039d3c776cf698a5f3725a708a248b7e69";

  async function sha256Hex(text) {
    const data = new TextEncoder().encode(text);
    const hash = await crypto.subtle.digest("SHA-256", data);
    return Array.from(new Uint8Array(hash)).map((b) => b.toString(16).padStart(2, "0")).join("");
  }

  if (submitFlagBtn && flagInput) {
    submitFlagBtn.addEventListener("click", async () => {
      const userAnswer = flagInput.value.trim();
      let isCorrect = false;
      try {
        isCorrect = (await sha256Hex(userAnswer)) === FLAG_HASH;
      } catch (e) {
        isCorrect = false;
      }

      if (isCorrect) {
        // Success State
        ctfMessage.textContent = "";
        ctfMessage.classList.remove("error-text");
        inputArea.classList.add("hidden"); 
        resumeDownload.classList.remove("hidden"); 

        if (typeof confetti === "function") {
          confetti({
            particleCount: 150,
            spread: 100,
            origin: { y: 0.6 },
            colors: ['#27c93f', '#ff9c1a', '#ffffff']
          });
        }
      } else {
        // Error State (ACCESS DENIED)
        ctfMessage.textContent = "> ❌ ERROR: INCORRECT FLAG. ACCESS DENIED.";
        ctfMessage.classList.add("error-text");
        
        // Pure JavaScript Animation (Bypasses CSS entirely!)
        if (terminalBox) {
          terminalBox.animate([
            { transform: 'translateX(0)', borderColor: '#333', boxShadow: '0 15px 35px rgba(0, 0, 0, 0.8)' },
            { transform: 'translateX(-15px)', borderColor: '#ff5f56', boxShadow: '0 0 30px rgba(255, 95, 86, 0.6)' },
            { transform: 'translateX(15px)', borderColor: '#ff5f56', boxShadow: '0 0 30px rgba(255, 95, 86, 0.6)' },
            { transform: 'translateX(-15px)', borderColor: '#ff5f56', boxShadow: '0 0 30px rgba(255, 95, 86, 0.6)' },
            { transform: 'translateX(15px)', borderColor: '#ff5f56', boxShadow: '0 0 30px rgba(255, 95, 86, 0.6)' },
            { transform: 'translateX(0)', borderColor: '#333', boxShadow: '0 15px 35px rgba(0, 0, 0, 0.8)' }
          ], {
            duration: 400, // Takes exactly 0.4 seconds
            iterations: 1, // Plays once per click
            easing: 'ease-in-out'
          });
        }

        // Clear the input so they can try again
        flagInput.value = "";
      }
    });

    flagInput.addEventListener("keydown", function(event) {
      if (event.key === "Enter") {
        event.preventDefault();
        submitFlagBtn.click();
      }
    });
  }

});
