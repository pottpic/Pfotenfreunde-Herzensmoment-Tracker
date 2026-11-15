// ============================================================
// MONI, HIER TRÄGST DU DEINE SACHEN EIN
// Gilt für Angebotsseite, Aushang und Karten gleichzeitig.
// ============================================================
const KONFIG = {
  // Adresse der Angebotsseite (da führen die QR-Codes hin)
  seitenUrl: "https://pottpic.github.io/Pfotenfreunde-Herzensmoment-Tracker/angebot/",

  // true = gelber Entwurf-Hinweis oben. Auf false stellen, wenn alles stimmt.
  entwurf: true,

  // WhatsApp-Nummer mit Ländervorwahl, ohne + und ohne Leerzeichen, z. B. "4917612345678"
  whatsapp: "4917621681512",

  // Deine Mail-Adresse für Anfragen
  mail: "",

  // Instagram-Name ohne @
  instagram: "pottpic",

  // Wann mit Gutschein geshootet wird
  shootingAb: "ab Frühjahr 2027",

  // Kleiner Satz für Leute, die ihre Bilder noch vor Weihnachten wollen
  // (keine Termine, keine Platzzahl – Moni entscheidet pro Anfrage)
  dezemberHinweis: "Du willst deine Bilder noch vor Weihnachten? Schreib mir einfach, vormittags geht im Dezember noch was.",

  // Gutschein: wie lange gültig
  gutscheinGueltig: "bis 31.12.2027",

  // Preise: von Moni freigegeben am 15.11.2026
  angebote: [
    {
      id: "gutschein-klein",
      titel: "Gutschein „Kleines Glück“",
      fuer: "Das Geschenk für Hundemenschen – geshootet wird ab Frühjahr",
      preis: "99 €",
      zusatz: "Gutschein",
      punkte: [
        "30 Minuten Shooting, Termin frei wählbar",
        "5 bearbeitete Lieblingsbilder als Datei",
        "Schöner Gutschein zum Ausdrucken",
        "Einlösbar, wann's passt"
      ],
      highlight: true,
      badge: "Weihnachtsgeschenk 🎁"
    },
    {
      id: "gutschein-gross",
      titel: "Gutschein „Herzensmoment“",
      fuer: "Für die, die ihren Hund richtig feiern wollen",
      preis: "189 €",
      zusatz: "Gutschein",
      punkte: [
        "60 Minuten Shooting, Lieblingsort aussuchen",
        "12 bearbeitete Lieblingsbilder als Datei",
        "Schöner Gutschein zum Ausdrucken",
        "Gern auch mit Mensch mit drauf"
      ],
      highlight: false
    }
  ]
};
