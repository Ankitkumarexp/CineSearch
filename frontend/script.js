// Connects the page to the CineSearch Flask API.
const API = "http://127.0.0.1:5000";
const $ = id => document.getElementById(id);
let currentMovies = [], timer;

function genresOf(movie) {
  const value = movie.genre ?? movie.genres ?? [];
  return Array.isArray(value) ? value : String(value).split(/[,|]/).map(x => x.trim()).filter(Boolean);
}
function ratingOf(movie) {
  const value = movie.rating ?? movie.vote_average;
  return value === undefined || value === null || value === "" ? null : Number(value);
}
function safe(value) {
  return String(value ?? "").replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
async function search(query) {
  const response = await fetch(`${API}/api/search?q=${encodeURIComponent(query)}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return Array.isArray(data.results) ? data.results : [];
}
function render() {
  const genre = $("genreFilter").value.toLowerCase(), min = Number($("ratingFilter").value);
  const rows = currentMovies.filter(m => {
    const genreOK = !genre || genresOf(m).some(g => g.toLowerCase() === genre);
    const rating = ratingOf(m);
    const ratingOK = min === 0 || (rating !== null && Number.isFinite(rating) && rating >= min);
    return genreOK && ratingOK;
  });
  $("resultCount").textContent = `${rows.length} movie${rows.length === 1 ? "" : "s"}`;
  if (!rows.length) { $("results").innerHTML = '<div class="empty">No movies match your search and filters.</div>'; return; }
  $("results").innerHTML = rows.map(m => {
    const rating = ratingOf(m), tags = genresOf(m).map(g => `<span>${safe(g)}</span>`).join("");
    return `<article class="card"><h3>${safe(m.title || "Untitled movie")}</h3>
      <div class="meta">${safe(m.year ?? m.release_year ?? "Year unavailable")}</div>
      <div class="tags">${tags || "<span>Genre unavailable</span>"}</div>
      <div class="rating-text ${rating == null ? "no-rating" : ""}">${rating == null ? "Rating not available" : `★ ${safe(rating)} / 10`}</div></article>`;
  }).join("");
}
function showSuggestions(movies) {
  const titles = [...new Set(movies.map(m => m.title).filter(Boolean))].slice(0,6);
  $("suggestions").innerHTML = titles.map(t => `<li tabindex="0">${safe(t)}</li>`).join("");
  $("suggestions").hidden = !titles.length;
  $("suggestions").querySelectorAll("li").forEach(li => {
    const choose = () => { $("searchInput").value = li.textContent; $("suggestions").hidden = true; runSearch(); };
    li.addEventListener("click", choose);
    li.addEventListener("keydown", e => { if (e.key === "Enter") choose(); });
  });
}
async function runSearch() {
  const query = $("searchInput").value.trim(); $("suggestions").hidden = true;
  if (!query) { currentMovies = []; render(); $("apiStatus").textContent = "Enter a movie title to search."; return; }
  $("apiStatus").textContent = "Searching…";
  try { currentMovies = await search(query); render(); $("apiStatus").textContent = "Connected to CineSearch backend."; }
  catch (e) { currentMovies = []; render(); $("apiStatus").textContent = `Could not reach backend: ${e.message}. Start Flask first.`; }
}
$("searchInput").addEventListener("input", () => {
  clearTimeout(timer); const q = $("searchInput").value.trim();
  if (!q) { $("suggestions").hidden = true; currentMovies = []; render(); return; }
  timer = setTimeout(async () => { try { showSuggestions(await search(q)); } catch { $("suggestions").hidden = true; } }, 250);
});
$("searchButton").addEventListener("click", runSearch);
$("searchInput").addEventListener("keydown", e => { if (e.key === "Enter") runSearch(); if (e.key === "Escape") $("suggestions").hidden = true; });
document.addEventListener("click", e => { if (!e.target.closest(".search")) $("suggestions").hidden = true; });
$("genreFilter").addEventListener("change", render);
$("ratingFilter").addEventListener("input", () => { const n = Number($("ratingFilter").value); $("ratingValue").textContent = n === 0 ? "Any" : `${n}+`; render(); });
$("clearFilters").addEventListener("click", () => { $("genreFilter").value = ""; $("ratingFilter").value = "0"; $("ratingValue").textContent = "Any"; render(); });
fetch(`${API}/api/health`).then(r => { if (!r.ok) throw Error(); $("apiStatus").textContent = "Connected to CineSearch backend."; })
.catch(() => $("apiStatus").textContent = "Backend not detected. Start Flask at 127.0.0.1:5000.");
