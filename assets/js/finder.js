/* Treatment finder: filters the treatment list by the concerns ticked and the downtime the visitor can plan for,
   and carries the matches into the booking link (?t=slug,slug). Without JavaScript every treatment stays listed.
   Nothing is sent anywhere: it all runs in the browser. */
(function () {
  "use strict";
  var box = document.getElementById("finder");
  if (!box) return;
  var form = box.querySelector(".fd-f"), items = box.querySelectorAll(".fr"), count = document.getElementById("fd-n"),
      none = document.getElementById("fd-none"), book = document.getElementById("fd-book"), base = book.getAttribute("href");
  var total = items.length;
  function update() {
    var picked = Array.prototype.map.call(form.querySelectorAll('input[name=c]:checked'), function (i) { return i.value; });
    var dtEl = form.querySelector('input[name=dt]:checked'), maxDt = dtEl ? Number(dtEl.value) : 9;
    var shown = [], n = 0;
    Array.prototype.forEach.call(items, function (li) {
      var cs = li.getAttribute("data-c").split(" ");
      var hit = (!picked.length || picked.some(function (p) { return cs.indexOf(p) > -1; })) && Number(li.getAttribute("data-dt")) <= maxDt;
      var was = li.hidden;
      li.hidden = !hit;
      if (hit) {
        n++;
        // rank: more matching concerns first
        li.style.order = String(10 - cs.filter(function (c) { return picked.indexOf(c) > -1; }).length);
        if (was) { li.classList.remove("pop"); void li.offsetWidth; li.classList.add("pop"); }
        var a = li.querySelector("a"), slug = a.getAttribute("href").replace(/\/$/, "").split("/").pop();
        shown.push(slug);
      }
    });
    count.textContent = (!picked.length && maxDt > 0) ? "All " + total + " treatments" : (n === 1 ? "1 treatment matches" : n + " treatments match");
    none.hidden = n > 0;
    book.setAttribute("href", base + (picked.length && n ? "?t=" + shown.join(",") : ""));
  }
  form.addEventListener("change", update);
  update();
})();
