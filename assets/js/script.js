'use strict';

// ==========================================
// 1. TEMPLATE UI LOGIC (NAVBAR & HEADER)
// ==========================================

/**
 * add event on element
 */
const addEventOnElem = function (elem, type, callback) {
  if (elem.length > 1) {
    for (let i = 0; i < elem.length; i++) {
      elem[i].addEventListener(type, callback);
    }
  } else {
    elem.addEventListener(type, callback);
  }
};

/**
 * toggle navbar
 */
const navbar = document.querySelector("[data-navbar]");
const navLinks = document.querySelectorAll("[data-nav-link]");
const navToggler = document.querySelector("[data-nav-toggler]");

const toggleNavbar = function () {
  navbar.classList.toggle("active");
  navToggler.classList.toggle("active");
};

if (navToggler) addEventOnElem(navToggler, "click", toggleNavbar);

const closeNavbar = function () {
  navbar.classList.remove("active");
  navToggler.classList.remove("active");
};

if (navLinks.length > 0) addEventOnElem(navLinks, "click", closeNavbar);

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

  if (preloader) {
    typeString(); // Start typing
    
    setTimeout(() => {
      preloader.classList.add("preloader-hidden");
      setTimeout(() => {
        if (preloader.parentNode) preloader.parentNode.removeChild(preloader);
      }, 500);
    }, 2500);
  }

  // --- B. TIMELINE SCROLL REVEAL ---
  const timelineSection = document.querySelector(".timeline");
  const timelineItems = document.querySelectorAll(".timeline-item");

  if (timelineSection && timelineItems.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          timelineItems.forEach((item, index) => {
            setTimeout(() => {
              item.classList.add("show");
            }, index * 800); 
          });
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });

    observer.observe(timelineSection);
  }

  // --- C. CTF CHALLENGE LOGIC ---
// --- C. CTF CHALLENGE LOGIC ---
  const submitFlagBtn = document.getElementById("submit-flag");
  const flagInput = document.getElementById("flag-input");
  const ctfMessage = document.getElementById("ctf-message");
  const resumeDownload = document.getElementById("resume-download");
  const inputArea = document.getElementById("ctf-input-area");
  
  // THIS IS THE LINE THAT WAS LIKELY MISSING!
  const terminalBox = document.querySelector(".terminal-box"); 

  if (submitFlagBtn && flagInput) {
    submitFlagBtn.addEventListener("click", () => {
      const userAnswer = flagInput.value.trim();
      const correctFlag = "FLAG{F!nd_my_R3$um3_B3l0w}";

      if (userAnswer === correctFlag) {
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

    flagInput.addEventListener("keypress", function(event) {
      if (event.key === "Enter") {
        event.preventDefault();
        submitFlagBtn.click();
      }
    });
  }

  // --- D. CONTACT FORM (FLASK BACKEND) ---
  const contactForm = document.querySelector(".contact-form");

  if (contactForm) {
    contactForm.addEventListener("submit", async function (event) {
      event.preventDefault();

      const submitBtn = this.querySelector("button[type='submit']");
      const originalBtnText = submitBtn.textContent;

      let formData = {
        name: document.querySelector("[name='name']").value, 
        email: document.querySelector("[name='email_address']").value,
        message: document.querySelector("[name='message']").value
      };

      submitBtn.disabled = true;
      submitBtn.textContent = "Sending...";

      try {
        let response = await fetch("http://127.0.0.1:5000/send-email", { 
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok) {
          alert("Message sent successfully!");
          contactForm.reset();
        } else {
          alert("Failed: " + (result.error || "Unknown error"));
        }
      } catch (error) {
        console.error("Connection Error:", error);
        alert("Could not connect to the backend. Make sure app.py is running!");
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalBtnText;
      }
    });
  }

});