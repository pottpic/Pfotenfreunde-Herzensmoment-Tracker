// Pottpic Deck – baut das Deck aus kacheln.js zusammen.
// Hier musst du normalerweise nix ändern. Knöpfe stehen in kacheln.js.

const MERK_GRUPPE = "Heute anschauen";
const SPEICHER_SCHLUESSEL = "heuteAnschauen";

const deck = document.getElementById("deck");
const suche = document.getElementById("suche");
const nix = document.getElementById("nix");

let gemerkt = []; // Knöpfe aus „Heute anschauen“

function oeffnen(adresse) {
  chrome.tabs.create({ url: adresse });
  window.close();
}

function knopfBauen({ name, adresse, zeichen }, extraKlasse) {
  const k = document.createElement("button");
  k.className = "knopf" + (extraKlasse ? " " + extraKlasse : "");
  k.title = adresse ? name + " – " + adresse : name;
  k.dataset.suche = (name + " " + (adresse || "")).toLowerCase();

  const feld = document.createElement("span");
  feld.className = "feld";
  feld.textContent = zeichen || "🔗";

  const n = document.createElement("span");
  n.className = "knopf-name";
  n.textContent = name;

  k.append(feld, n);
  return k;
}

function gruppeBauen(gruppe) {
  const box = document.createElement("section");
  box.className = "gruppe";
  box.style.setProperty("--akzent", gruppe.farbe);

  const titel = document.createElement("h2");
  titel.className = "gruppe-titel";
  titel.textContent = `${gruppe.zeichen} ${gruppe.name}`;

  const reihe = document.createElement("div");
  reihe.className = "reihe";

  box.append(titel, reihe);
  return { box, reihe };
}

function merkReiheFuellen(reihe) {
  reihe.textContent = "";

  // ➕ – aktuelle Seite merken
  const plus = knopfBauen({ name: "Seite merken", zeichen: "➕" }, "plus");
  plus.dataset.immer = "1";
  plus.addEventListener("click", aktuelleSeiteMerken);
  reihe.append(plus);

  if (!gemerkt.length) {
    const leer = document.createElement("span");
    leer.className = "leer";
    leer.dataset.immer = "1";
    leer.textContent = "Noch nix gemerkt – geh auf 'ne Seite und klick auf ➕.";
    reihe.append(leer);
  }

  gemerkt.forEach((eintrag, i) => {
    const k = knopfBauen(eintrag, "merk");
    k.addEventListener("click", () => oeffnen(eintrag.adresse));

    const weg = document.createElement("span");
    weg.className = "weg";
    weg.textContent = "✕";
    weg.title = "Entfernen";
    weg.addEventListener("click", (e) => {
      e.stopPropagation();
      gemerkt.splice(i, 1);
      speichern();
      merkReiheFuellen(reihe);
      filtern();
    });
    k.append(weg);
    reihe.append(k);
  });
}

async function aktuelleSeiteMerken() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url || !/^https?:/.test(tab.url)) return;
  if (gemerkt.some((g) => g.adresse === tab.url)) return;

  let name = (tab.title || new URL(tab.url).hostname).trim();
  if (name.length > 40) name = name.slice(0, 40) + "…";

  gemerkt.push({ name, adresse: tab.url, zeichen: "📌" });
  speichern();
  merkReiheFuellen(document.querySelector('[data-gruppe="' + MERK_GRUPPE + '"] .reihe'));
  filtern();
}

function speichern() {
  chrome.storage.local.set({ [SPEICHER_SCHLUESSEL]: gemerkt });
}

function filtern() {
  const wort = suche.value.trim().toLowerCase();
  let treffer = 0;

  document.querySelectorAll(".gruppe").forEach((g) => {
    let sichtbar = 0;
    g.querySelectorAll(".knopf, .leer").forEach((k) => {
      const passt = !wort ? true : !k.dataset.immer && (k.dataset.suche || "").includes(wort);
      k.hidden = !passt;
      if (passt && !k.dataset.immer) sichtbar++;
    });
    g.hidden = wort && sichtbar === 0;
    treffer += sichtbar;
  });

  nix.hidden = !wort || treffer > 0;
}

// Enter öffnet den ersten Treffer
suche.addEventListener("input", filtern);
suche.addEventListener("keydown", (e) => {
  if (e.key !== "Enter") return;
  const erster = [...document.querySelectorAll(".knopf")].find(
    (k) => !k.hidden && !k.closest(".gruppe").hidden && !k.dataset.immer
  );
  if (erster) erster.click();
});

async function start() {
  const daten = await chrome.storage.local.get(SPEICHER_SCHLUESSEL);
  gemerkt = daten[SPEICHER_SCHLUESSEL] || [];

  GRUPPEN.forEach((gruppe) => {
    const { box, reihe } = gruppeBauen(gruppe);
    box.dataset.gruppe = gruppe.name;

    if (gruppe.name === MERK_GRUPPE) {
      merkReiheFuellen(reihe);
    } else {
      KACHELN.filter((k) => k.gruppe === gruppe.name).forEach((kachel) => {
        const k = knopfBauen(kachel);
        k.addEventListener("click", () => oeffnen(kachel.adresse));
        reihe.append(k);
      });
      if (!reihe.children.length) return; // leere Gruppe nicht zeigen
    }
    deck.append(box);
  });

  suche.focus();
}

start();
