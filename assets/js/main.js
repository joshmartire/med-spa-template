/* Med Spa Website Template: site interactions. No dependencies. */
(function () {
  "use strict";
  var d = document, root = d.documentElement;

  /* opening animation: once per browser session, skippable with a tap or any key */
  var intro = d.querySelector(".intro");
  if (intro && !root.classList.contains("no-intro")) {
    root.classList.add("intro-on");
    var done = false;
    var end = function () {
      if (done) return; done = true;
      try { sessionStorage.setItem("ms-intro", "1"); } catch (e) {}
      root.classList.remove("intro-on");
      if (intro.parentNode) intro.parentNode.removeChild(intro);
    };
    intro.addEventListener("click", end);
    d.addEventListener("keydown", end, { once: true });
    intro.addEventListener("animationend", function (e) { if (e.target === intro) end(); });
    setTimeout(end, 3600);
  } else if (intro) {
    intro.parentNode.removeChild(intro);
  }

  /* mobile menu */
  var burger = d.querySelector(".burger"), mp = d.getElementById("mp");
  if (burger && mp) {
    var setMenu = function (open) {
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
      mp.classList.toggle("open", open);
      d.body.classList.toggle("mp-on", open);
    };
    burger.addEventListener("click", function () { setMenu(burger.getAttribute("aria-expanded") !== "true"); });
    d.addEventListener("keydown", function (e) { if (e.key === "Escape" && mp.classList.contains("open")) { setMenu(false); burger.focus(); } });
    mp.addEventListener("click", function (e) { if (e.target.tagName === "A") setMenu(false); });
  }

  /* dropdowns: hover and focus open them in CSS; buttons toggle for touch and keyboard */
  var dds = d.querySelectorAll(".dd");
  Array.prototype.forEach.call(dds, function (dd) {
    var b = dd.querySelector(".ddb");
    b.addEventListener("click", function () {
      var open = !dd.classList.contains("open");
      Array.prototype.forEach.call(dds, function (o) { o.classList.remove("open"); o.querySelector(".ddb").setAttribute("aria-expanded", "false"); });
      dd.classList.toggle("open", open);
      b.setAttribute("aria-expanded", String(open));
    });
  });
  d.addEventListener("click", function (e) {
    if (!e.target.closest(".dd")) Array.prototype.forEach.call(dds, function (o) { o.classList.remove("open"); o.querySelector(".ddb").setAttribute("aria-expanded", "false"); });
  });
  d.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    Array.prototype.forEach.call(dds, function (o) { if (o.classList.contains("open")) { o.classList.remove("open"); var b = o.querySelector(".ddb"); b.setAttribute("aria-expanded", "false"); b.focus(); } });
  });

  /* reveal on scroll: each part of a section rises in turn */
  var els = d.querySelectorAll(".r");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, sibs = el.parentNode ? el.parentNode.querySelectorAll(":scope > .r") : [];
        var i = Array.prototype.indexOf.call(sibs, el);
        el.style.transitionDelay = Math.max(0, i) * 80 + "ms";
        el.classList.add("in");
        io.unobserve(el);
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    Array.prototype.forEach.call(els, function (el) { io.observe(el); });
  } else {
    Array.prototype.forEach.call(els, function (el) { el.classList.add("in"); });
  }

  /* booking form: tick treatments passed in the link (?t=slug,slug), then validate before sending */
  var form = d.querySelector("form[data-validate]");
  if (form) {
    try {
      var want = (new URLSearchParams(location.search).get("t") || "").split(",");
      want.forEach(function (slug) {
        if (!slug) return;
        var box = form.querySelector('input[data-slug="' + slug.replace(/[^a-z0-9-]/g, "") + '"]');
        if (box) box.checked = true;
      });
    } catch (e) {}
    var status = form.querySelector(".cf-status");
    var check = function (el) {
      var err = d.getElementById(el.id + "-error"), msg = "";
      var v = el.value.trim();
      if (el.required && !v) msg = "Please enter " + (el.getAttribute("data-label") || "this field") + ".";
      else if (el.type === "email" && v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = "Please enter a valid email address.";
      else if (el.type === "tel" && v && v.replace(/\D/g, "").length < 10) msg = "Please enter a phone number with area code.";
      el.setAttribute("aria-invalid", msg ? "true" : "false");
      if (err) err.textContent = msg;
      return !msg;
    };
    var fields = form.querySelectorAll("input[required], input[type=email], input[type=tel]");
    Array.prototype.forEach.call(fields, function (el) {
      el.addEventListener("blur", function () { if (el.value) check(el); });
      el.addEventListener("input", function () { if (el.getAttribute("aria-invalid") === "true") check(el); });
    });
    form.addEventListener("submit", function (e) {
      var bad = null;
      Array.prototype.forEach.call(fields, function (el) { if (!check(el) && !bad) bad = el; });
      if (bad) {
        e.preventDefault();
        status.className = "cf-status err";
        status.textContent = "Please check the highlighted fields.";
        bad.focus();
        return;
      }
      status.className = "cf-status";
      status.textContent = "Sending…";
      var btn = form.querySelector("button[type=submit]");
      if (btn) btn.disabled = true;
    });
  }
})();
