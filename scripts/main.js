/* ============================================================
   Triage4US — Page scripts
   - Footer year
   - FAQ accordion (accessible, single-open behavior)
   - Smooth in-page scroll with reduced-motion fallback
   ============================================================ */

(function () {
  "use strict";

  /* ----- Footer year ----- */
  var yearEl = document.getElementById("year");
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* ----- Header transparent-over-hero state -----
     Default state on page load (set inline in HTML) is transparent. As soon
     as the user starts scrolling, the header flips to its frosted-white
     state. Switching back happens at the same low threshold. */
  var header = document.querySelector(".site-header");
  var SCROLL_THRESHOLD = 40;

  if (header) {
    var ticking = false;
    function syncHeaderState() {
      if (window.scrollY > SCROLL_THRESHOLD) {
        header.classList.remove("is-over-hero");
      } else {
        header.classList.add("is-over-hero");
      }
      ticking = false;
    }
    function onScroll() {
      if (!ticking) {
        window.requestAnimationFrame(syncHeaderState);
        ticking = true;
      }
    }
    window.addEventListener("scroll", onScroll, { passive: true });
    syncHeaderState();
  }

  /* ----- Floating donate CTA visibility -----
     Reveal the sticky donate button once the hero scrolls out of view.
     Uses IntersectionObserver against the hero section so the timing
     is anchored to actual layout, not a magic scroll threshold. */
  var floatingDonate = document.querySelector(".floating-donate");
  var heroSection = document.getElementById("hero");

  if (floatingDonate && heroSection && "IntersectionObserver" in window) {
    var donateObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        floatingDonate.setAttribute(
          "data-visible",
          String(!entry.isIntersecting)
        );
      });
    }, { rootMargin: "0px 0px -15% 0px", threshold: 0 });
    donateObserver.observe(heroSection);
  } else if (floatingDonate) {
    // No IntersectionObserver support — just show it always.
    floatingDonate.setAttribute("data-visible", "true");
  }

  /* ----- Below-fold image fade-in -----
     Mark each lazy image as loaded once it decodes. CSS handles the
     320ms opacity transition; reduced-motion users skip the dance. */
  document.querySelectorAll('img[loading="lazy"]').forEach(function (img) {
    if (img.complete && img.naturalHeight !== 0) {
      img.classList.add("is-loaded");
    } else {
      img.addEventListener("load", function () {
        img.classList.add("is-loaded");
      }, { once: true });
      img.addEventListener("error", function () {
        // Don't leave a permanently invisible image if it fails to load.
        img.classList.add("is-loaded");
      }, { once: true });
    }
  });

  /* ----- Mobile nav toggle -----
     Hamburger reveals a fixed drawer below the header on <768px. Closes
     on link click and on Escape. */
  var menuToggle = document.querySelector(".site-header_menu-toggle");
  var mobileNav = document.getElementById("mobile-nav");

  if (menuToggle && mobileNav) {
    function setMobileNavOpen(open) {
      menuToggle.setAttribute("aria-expanded", String(open));
      mobileNav.setAttribute("data-open", String(open));
      menuToggle.setAttribute(
        "aria-label",
        open ? "Close navigation menu" : "Open navigation menu"
      );
    }
    menuToggle.addEventListener("click", function () {
      var open = menuToggle.getAttribute("aria-expanded") === "true";
      setMobileNavOpen(!open);
    });
    mobileNav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () { setMobileNavOpen(false); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menuToggle.getAttribute("aria-expanded") === "true") {
        setMobileNavOpen(false);
        menuToggle.focus();
      }
    });
  }

  /* ----- FAQ accordion ----- */
  var triggers = document.querySelectorAll(".faq_trigger");

  function closePanel(trigger) {
    var panelId = trigger.getAttribute("aria-controls");
    var panel = document.getElementById(panelId);
    trigger.setAttribute("aria-expanded", "false");
    if (panel) panel.classList.remove("is-open");
  }

  function openPanel(trigger) {
    var panelId = trigger.getAttribute("aria-controls");
    var panel = document.getElementById(panelId);
    trigger.setAttribute("aria-expanded", "true");
    if (panel) panel.classList.add("is-open");
  }

  triggers.forEach(function (trigger) {
    trigger.addEventListener("click", function () {
      var isOpen = trigger.getAttribute("aria-expanded") === "true";

      // Single-open behavior: close all others first.
      triggers.forEach(function (other) {
        if (other !== trigger) closePanel(other);
      });

      if (isOpen) {
        closePanel(trigger);
      } else {
        openPanel(trigger);
      }
    });
  });

  /* ----- Donation selector -----
     Presets, custom amount, frequency toggle, reactive CTA copy. Custom
     and presets are mutually exclusive: picking one clears the other.
     Submit is a placeholder until payment integration ships — for now it
     scrolls to the final CTA so the page still flows. */
  var donationForm = document.getElementById("donation-form");
  if (donationForm) {
    var donationPresets = donationForm.querySelectorAll(".donation_preset");
    var donationFreqOptions = donationForm.querySelectorAll(".donation_freq-option");
    var donationCustomInput = document.getElementById("donation-custom-input");
    var donationCta = document.getElementById("donation-cta");
    var donationCtaLabel = donationCta.querySelector(".donation_cta-label");

    var donationState = { amount: null, frequency: "monthly" };

    function updateDonationCta() {
      if (!donationState.amount || donationState.amount < 1) {
        donationCta.disabled = true;
        donationCtaLabel.textContent = "Choose an amount";
        return;
      }
      donationCta.disabled = false;
      var word = donationState.frequency === "monthly" ? "monthly" : "once";
      donationCtaLabel.textContent =
        "Donate $" + donationState.amount + " " + word;
    }

    function clearPresetSelection() {
      donationPresets.forEach(function (btn) {
        btn.classList.remove("is-selected");
        btn.setAttribute("aria-checked", "false");
      });
    }

    donationPresets.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var amount = Number(btn.getAttribute("data-amount"));
        donationState.amount = amount;
        clearPresetSelection();
        btn.classList.add("is-selected");
        btn.setAttribute("aria-checked", "true");
        if (donationCustomInput.value !== "") donationCustomInput.value = "";
        updateDonationCta();
      });
    });

    donationFreqOptions.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var freq = btn.getAttribute("data-frequency");
        donationState.frequency = freq;
        donationFreqOptions.forEach(function (other) {
          var match = other === btn;
          other.classList.toggle("is-selected", match);
          other.setAttribute("aria-checked", String(match));
        });
        updateDonationCta();
      });
    });

    if (donationCustomInput) {
      donationCustomInput.addEventListener("input", function () {
        var n = parseInt(donationCustomInput.value, 10);
        donationState.amount = Number.isFinite(n) && n >= 1 ? n : null;
        clearPresetSelection();
        updateDonationCta();
      });
    }

    donationForm.addEventListener("submit", function (e) {
      e.preventDefault();
      if (donationCta.disabled) return;
      var target = document.getElementById("final-cta");
      if (!target) return;
      var reduceMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
      ).matches;
      target.scrollIntoView({
        behavior: reduceMotion ? "auto" : "smooth",
        block: "start"
      });
    });

    updateDonationCta();
  }

  /* ----- Smooth scroll for in-page anchors ----- */
  var prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (e) {
      var href = link.getAttribute("href");
      if (!href || href === "#") return;

      var target = document.querySelector(href);
      if (!target) return;

      e.preventDefault();
      target.scrollIntoView({
        behavior: prefersReducedMotion ? "auto" : "smooth",
        block: "start",
      });

      // Move focus to the target for keyboard users.
      if (!target.hasAttribute("tabindex")) {
        target.setAttribute("tabindex", "-1");
      }
      target.focus({ preventScroll: true });
    });
  });
})();
