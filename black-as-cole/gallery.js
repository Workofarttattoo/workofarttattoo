(function () {
  var dialog = document.getElementById("bac-lightbox");
  if (!dialog) return;

  var img = document.getElementById("bac-lb-img");
  var titleEl = document.getElementById("bac-lb-title");
  var catEl = document.getElementById("bac-lb-cat");
  var noteEl = document.getElementById("bac-lb-note");
  var tiles = Array.prototype.slice.call(document.querySelectorAll("[data-bac-open]"));
  var index = 0;
  var lastFocus = null;
  var touchX = null;
  var touchY = null;

  function works() {
    var seen = Object.create(null);
    var list = [];
    tiles.forEach(function (tile) {
      var id = tile.getAttribute("data-bac-id");
      if (!id || seen[id]) return;
      seen[id] = true;
      list.push({
        id: id,
        src: tile.getAttribute("data-full"),
        alt: tile.getAttribute("data-alt") || "",
        title: tile.getAttribute("data-title") || "Untitled",
        category: tile.getAttribute("data-category") || "",
        note: tile.getAttribute("data-note") || "",
        width: tile.getAttribute("data-width") || "",
        height: tile.getAttribute("data-height") || ""
      });
    });
    return list;
  }

  var items = works();

  function show(next) {
    if (!items.length) return;
    index = (next + items.length) % items.length;
    var item = items[index];
    img.src = item.src;
    img.alt = item.alt;
    if (item.width) img.width = Number(item.width);
    if (item.height) img.height = Number(item.height);
    titleEl.textContent = item.title;
    catEl.textContent = item.category;
    noteEl.textContent = item.note;
    noteEl.hidden = !item.note;
  }

  function openAt(id, opener) {
    var next = 0;
    for (var i = 0; i < items.length; i += 1) {
      if (items[i].id === id) {
        next = i;
        break;
      }
    }
    lastFocus = opener || document.activeElement;
    show(next);
    if (typeof dialog.showModal === "function") {
      dialog.showModal();
    } else {
      dialog.setAttribute("open", "");
    }
    document.body.style.overflow = "hidden";
    var closeBtn = dialog.querySelector("[data-bac-close]");
    if (closeBtn) closeBtn.focus();
  }

  function closeDialog() {
    if (dialog.open && typeof dialog.close === "function") dialog.close();
    else dialog.removeAttribute("open");
    document.body.style.overflow = "";
    img.removeAttribute("src");
    if (lastFocus && typeof lastFocus.focus === "function") lastFocus.focus();
  }

  tiles.forEach(function (tile) {
    tile.addEventListener("click", function () {
      openAt(tile.getAttribute("data-bac-id"), tile);
    });
  });

  dialog.querySelector("[data-bac-close]").addEventListener("click", closeDialog);
  dialog.querySelector("[data-bac-prev]").addEventListener("click", function () {
    show(index - 1);
  });
  dialog.querySelector("[data-bac-next]").addEventListener("click", function () {
    show(index + 1);
  });

  dialog.addEventListener("cancel", function (event) {
    event.preventDefault();
    closeDialog();
  });

  dialog.addEventListener("click", function (event) {
    if (event.target === dialog) closeDialog();
  });

  document.addEventListener("keydown", function (event) {
    if (!dialog.open) return;
    if (event.key === "ArrowRight") {
      event.preventDefault();
      show(index + 1);
    } else if (event.key === "ArrowLeft") {
      event.preventDefault();
      show(index - 1);
    }
  });

  var stage = dialog.querySelector(".bac-lb-stage");
  stage.addEventListener(
    "touchstart",
    function (event) {
      if (!event.changedTouches || !event.changedTouches[0]) return;
      touchX = event.changedTouches[0].clientX;
      touchY = event.changedTouches[0].clientY;
    },
    { passive: true }
  );
  stage.addEventListener(
    "touchend",
    function (event) {
      if (touchX == null || !event.changedTouches || !event.changedTouches[0]) return;
      var dx = event.changedTouches[0].clientX - touchX;
      var dy = event.changedTouches[0].clientY - touchY;
      touchX = null;
      touchY = null;
      if (Math.abs(dx) < 48 || Math.abs(dx) < Math.abs(dy)) return;
      show(dx < 0 ? index + 1 : index - 1);
    },
    { passive: true }
  );
})();
