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
  whatsapp: "",

  // Deine Mail-Adresse für Anfragen
  mail: "",

  // Instagram-Name ohne @
  instagram: "pottpic",

  // Mini-Shootings im Dezember (VORSCHLAG – Moni entscheidet)
  miniTermine: "Sa 05.12. und So 06.12.2026",
  miniOrt: "draußen im Dortmunder Norden – genauer Treffpunkt kommt mit der Buchung",
  miniPlaetze: 16,          // wie viele Slots es insgesamt gibt
  miniBuchenBis: "Di 01.12.",
  galerieBis: "Fr 18.12.",  // bis wann die Bilder da sind

  // Gutschein: wie lange gültig
  gutscheinGueltig: "bis 31.12.2027",

  // Preise (VORSCHLAG vom Team, Schätzung – Moni entscheidet)
  angebote: [
    {
      id: "mini",
      titel: "Mini-Shooting im Dezember",
      fuer: "Für dich und deinen Hund – noch vor Weihnachten",
      preis: "99 €",
      zusatz: "einmalig",
      punkte: [
        "20 Minuten draußen, ganz entspannt",
        "5 bearbeitete Lieblingsbilder als Datei",
        "Online-Galerie zum Aussuchen",
        "Weitere Bilder je 25 €",
        "Bilder rechtzeitig vor Heiligabend da"
      ],
      highlight: true,
      badge: "Nur im Dezember"
    },
    {
      id: "gutschein-klein",
      titel: "Gutschein „Kleines Glück“",
      fuer: "Zum Verschenken – geshootet wird 2027",
      preis: "99 €",
      zusatz: "Gutschein",
      punkte: [
        "30 Minuten Shooting, Termin frei wählbar",
        "5 bearbeitete Lieblingsbilder als Datei",
        "Schöner Gutschein zum Ausdrucken",
        "Einlösbar, wann's passt"
      ],
      highlight: false
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
