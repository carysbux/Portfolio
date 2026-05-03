(function () {
  document.documentElement.classList.add("js-enabled");

  const scrollButtons = document.querySelectorAll("[data-scroll]");
  scrollButtons.forEach((button) => {
    button.addEventListener("click", () => {
      const targetId = button.getAttribute("data-scroll");
      const target = targetId ? document.getElementById(targetId) : null;
      if (!target) return;
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  const revealItems = document.querySelectorAll(".reveal-on-scroll");
  if (revealItems.length > 0) {
    const motionOkForReveal = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!motionOkForReveal || !("IntersectionObserver" in window)) {
      revealItems.forEach((item) => item.classList.add("is-visible"));
    } else {
      const ordered = Array.from(revealItems);
      let index = 0;
      const observer = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
            index += 1;
            if (index < ordered.length) {
              observer.observe(ordered[index]);
            }
          });
        },
        { threshold: 0.35, rootMargin: "0px 0px -10% 0px" }
      );
      observer.observe(ordered[0]);
    }
  }

  const roleImage = document.querySelector(".role-pill__img");
  const motionOk = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const designerPngs = [
    "imessage-blue_designer-c7b236e3-e7fb-4c5d-9215-797e2d02638e.png",
    "imessage-gray_designer-de9ca120-84ac-49f0-a1eb-2b8c1f255b6e.png",
    "instagram-dm_designer-de93ae65-d129-421a-b5be-34ae38214222.png",
    "ios-large-title_designer-300fbb84-c413-44dc-b297-eb409da6f172.png",
    "ios-highlight_designer-7f145aca-fa78-4d53-ac39-03e79e7bc876.png",
    "ios-link_designer-fabcd599-7558-411e-8773-09ebd7c7ddd9.png",
    "whatsapp-sent_designer-18eddb88-81a7-43c5-9edb-f12c64cdad82.png",
    "ios-selection-blue_designer-202f7c68-ef4d-485f-a93f-60bb748e5f77.png",
    "sms-green_designer-fe69c7ad-67e0-4e5a-b6dd-eb9412f5f75c.png",
    "tom-bubble_designer-c9d80025-8fbe-4a49-99be-4c72dccd4df4.png",
    "ios-selection-green_designer-5b4cee32-fe48-47a4-a339-61d080173105.png",
    "ios-mono_designer-7b3323e8-b796-4768-856f-7ba828054e51.png",
  ];

  if (roleImage && motionOk && designerPngs.length > 1) {
    const basePath = "assets/designer-word-selected/";
    const shuffle = (items) => {
      const next = [...items];
      for (let i = next.length - 1; i > 0; i -= 1) {
        const j = Math.floor(Math.random() * (i + 1));
        [next[i], next[j]] = [next[j], next[i]];
      }
      return next;
    };

    let queue = shuffle(designerPngs);
    let index = 0;
    roleImage.src = basePath + queue[index];

    window.setInterval(() => {
      if (document.hidden) return;

      index += 1;
      if (index >= queue.length) {
        const previous = queue[queue.length - 1];
        queue = shuffle(designerPngs);
        if (queue.length > 1 && queue[0] === previous) {
          [queue[0], queue[1]] = [queue[1], queue[0]];
        }
        index = 0;
      }

      roleImage.classList.add("role-pill__img--out");
      window.setTimeout(() => {
        roleImage.src = basePath + queue[index];
        roleImage.classList.remove("role-pill__img--out");
        roleImage.classList.add("role-pill__img--in");
        window.setTimeout(() => {
          roleImage.classList.remove("role-pill__img--in");
        }, 220);
      }, 160);
    }, 1800);
  }
})();
