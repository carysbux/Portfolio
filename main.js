(function () {
  const buttons = document.querySelectorAll(".nav-tile[data-section]");
  const sections = {
    home: document.getElementById("section-home"),
    projects: document.getElementById("section-projects"),
    about: document.getElementById("section-about"),
    contact: document.getElementById("section-contact"),
  };

  function showSection(id, updateHash) {
    const active = sections[id];
    if (!active) return;

    Object.entries(sections).forEach(([key, el]) => {
      if (!el) return;
      const on = key === id;
      el.hidden = !on;
      el.classList.toggle("is-visible", on);
    });

    buttons.forEach((btn) => {
      const isCurrent = btn.dataset.section === id;
      btn.classList.toggle("is-active", isCurrent);
      if (isCurrent) btn.setAttribute("aria-current", "page");
      else btn.removeAttribute("aria-current");
    });

    if (updateHash !== false) {
      const newHash = id === "home" ? "" : "#" + id;
      if (window.location.hash !== newHash) {
        history.replaceState(null, "", newHash || window.location.pathname);
      }
    }
  }

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => showSection(btn.dataset.section));
  });

  document.querySelectorAll("a[data-from='projects']").forEach((a) => {
    a.addEventListener("click", () => {
      if (window.location.hash !== "#projects") {
        history.replaceState(null, "", "#projects");
      }
    });
  });

  document.getElementById("logo-home")?.addEventListener("click", (e) => {
    e.preventDefault();
    showSection("home");
  });

  function fromHash() {
    const h = (window.location.hash || "").replace("#", "");
    return sections[h] ? h : "home";
  }

  window.addEventListener("hashchange", () => showSection(fromHash(), false));

  showSection(fromHash(), false);
})();
