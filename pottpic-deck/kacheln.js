// ============================================================
//  POTTPIC DECK – hier stehen alle Knöpfe
// ============================================================
//
//  Neuen Knopf dazu? Einfach eine Zeile kopieren, einfügen und ändern:
//    { name: "Name", adresse: "https://...", zeichen: "🐾", gruppe: "Täglich" },
//
//  Wichtig:
//   • Die Gruppe muss genauso heißen wie oben bei GRUPPEN.
//   • Jede Zeile endet mit einem Komma.
//   • Die Anführungszeichen "..." müssen bleiben.
//  Danach in Chrome unter chrome://extensions beim Deck auf ↻ klicken.
// ============================================================

// Die Gruppen – in dieser Reihenfolge erscheinen sie im Deck.
// "farbe" ist die Farbe der kleinen Quadrate in der Gruppe.
const GRUPPEN = [
  { name: "Täglich",         zeichen: "☀️", farbe: "#F2C94C" },
  { name: "Heute anschauen", zeichen: "👀", farbe: "#F2994A" },
  { name: "Communities",     zeichen: "🐾", farbe: "#27AE60" },
  { name: "Postfächer",      zeichen: "📬", farbe: "#2F80ED" },
  { name: "Webseiten",       zeichen: "🌐", farbe: "#2DC5C5" },
  { name: "Social Media",    zeichen: "📱", farbe: "#EB5757" },
  { name: "Werkzeuge",       zeichen: "🧰", farbe: "#9B51E0" },
];

// Die festen Knöpfe – eine Zeile pro Knopf.
const KACHELN = [
  { name: "Trello",              adresse: "https://trello.com",                                         zeichen: "📋", gruppe: "Täglich" },
  { name: "Metricool",           adresse: "https://app.metricool.com",                                  zeichen: "📅", gruppe: "Täglich" },
  { name: "Claude",              adresse: "https://claude.ai",                                          zeichen: "✨", gruppe: "Täglich" },
  { name: "Google Kalender",     adresse: "https://calendar.google.com",                                zeichen: "🗓️", gruppe: "Täglich" },

  { name: "Pfotenfreunde",       adresse: "https://www.skool.com/pfotenfreunde-7944",                   zeichen: "🐶", gruppe: "Communities" },
  { name: "Anpfiff Fußball",     adresse: "https://www.skool.com/anpfiff-die-fuball-community-2517",    zeichen: "⚽", gruppe: "Communities" },
  { name: "Campingliebe",        adresse: "https://www.skool.com/campingliebe-1254",                    zeichen: "⛺", gruppe: "Communities" },

  { name: "Gmail",               adresse: "https://mail.google.com",                                    zeichen: "✉️", gruppe: "Postfächer" },
  { name: "CleverReach",         adresse: "https://www.cleverreach.com/de/login/",                      zeichen: "📨", gruppe: "Postfächer" },

  { name: "Pottpic",             adresse: "https://www.pottpic.de",                                     zeichen: "📸", gruppe: "Webseiten" },
  { name: "Schnauzenbande",    adresse: "https://www.hsv-dortmund-derne.de/",                       zeichen: "🦴", gruppe: "Webseiten" },
  { name: "GitHub Werkstatt",    adresse: "https://github.com/pottpic/Pfotenfreunde-Herzensmoment-Tracker", zeichen: "🛠️", gruppe: "Webseiten" },

  { name: "Instagram",           adresse: "https://www.instagram.com",                                  zeichen: "📷", gruppe: "Social Media" },
  { name: "Facebook",            adresse: "https://www.facebook.com",                                   zeichen: "👍", gruppe: "Social Media" },
  { name: "TikTok",              adresse: "https://www.tiktok.com",                                     zeichen: "🎵", gruppe: "Social Media" },
  { name: "Meta Suite",          adresse: "https://business.facebook.com",                              zeichen: "💼", gruppe: "Social Media" },

  { name: "Canva",               adresse: "https://www.canva.com",                                      zeichen: "🎨", gruppe: "Werkzeuge" },
  { name: "Magnific",            adresse: "https://www.magnific.ai",                                    zeichen: "🪄", gruppe: "Werkzeuge" },
  { name: "Google Drive",        adresse: "https://drive.google.com",                                   zeichen: "🗂️", gruppe: "Werkzeuge" },
  { name: "Plaud",               adresse: "https://web.plaud.ai",                                       zeichen: "🎙️", gruppe: "Werkzeuge" },
];
