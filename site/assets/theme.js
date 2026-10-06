/* Light / dark theme: the toggle, the remembered choice, and a way for canvases to follow.
   The attribute itself is set before first paint by _includes/theme-init.njk. Here:
   - the button (hidden until this script runs, since it needs JavaScript) switches the theme and remembers it in
     localStorage ("mizien.theme"; the choice stays in this browser only);
   - the browser's address-bar colour follows;
   - window.MizienTheme.get() gives the current theme and .colour(name) reads a token such as "--stage-a", so the
     claims web and the map can draw in the theme's colours; a "mizien:theme" event fires on window when it changes. */
(function () {
  var root = document.documentElement, KEY = "mizien.theme";
  function current() { return root.dataset.theme === "light" ? "light" : "dark"; }
  function token(name) { return getComputedStyle(root).getPropertyValue(name).trim(); }

  function apply(theme, remember) {
    root.dataset.theme = theme;
    if (remember) { try { localStorage.setItem(KEY, theme); } catch (e) { /* private mode: the choice lasts this visit */ } }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", token("--bg") || (theme === "light" ? "#e8efe8" : "#0e2a1f"));
    document.querySelectorAll(".theme-toggle").forEach(label);
    window.dispatchEvent(new CustomEvent("mizien:theme", { detail: { theme: theme } }));
  }
  function label(btn) {
    var next = current() === "light" ? "dark" : "light", text = "Switch to the " + next + " theme";
    btn.setAttribute("aria-label", text); btn.setAttribute("title", text);
  }

  window.MizienTheme = { get: current, colour: token, set: function (t) { apply(t === "light" ? "light" : "dark", true); } };

  function init() {
    document.querySelectorAll(".theme-toggle").forEach(function (btn) {
      btn.hidden = false; label(btn);
      btn.addEventListener("click", function () { apply(current() === "light" ? "dark" : "light", true); });
    });
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", token("--bg") || "#0e2a1f");
    // another tab changed the theme
    window.addEventListener("storage", function (e) { if (e.key === KEY && (e.newValue === "light" || e.newValue === "dark") && e.newValue !== current()) apply(e.newValue, false); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
