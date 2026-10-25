# Kehä-Ketut – yhtenäisen premium-ulkoasun käyttöönotto

Tämä on Yhdistysavaimen ylläpitäjän asennusohje. GitHubin CSS ja sivupohjat ovat valmiita, mutta niillä **ei yksin vaihdeta Yhdistysavaimen sisältöä**.

## 1. Tarkista Yhdistysavaimen tilausversio

- Plus/Premium: vasemman työkalupalkin Koodieditori mahdollistaa sivuston head-osaan tyylilinkin.
- Start: käytä Ulkoasu → Tyylit koko sivuston väreihin, fonttiin, riviväliin, osioiden väliin ja painikkeiden muotoon. Erillisiin HTML-osiin voi lisätä oman CSS-linkin.
- Free: tämän kokoisen sivuston koko sivurakenne ei normaalisti vastaa Free-rajoituksia, mutta älä arvaa tilauksen versiota.

**Plus/Premium-koodieditoriin turvallinen, pieni linkki:**

<link rel="stylesheet" href="https://glesima.github.io/kehaketut-feed/rkk-premium-site.css?v=1">

Tämä linkki ei sisällä JavaScriptiä. Tallenna vasta, kun julkisen esikatselun etusivu, harjoittelusivu ja jäsenlomake näyttävät toimivilta. Muutokset voi palauttaa poistamalla linkin. Yhdistysavaimen koodieditoriin liittyy oma ylläpitäjäriski; älä liitä sinne suurta kokeilematonta JavaScript-pakettia.

**Kaikissa versioissa** suositellut Ulkoasu → Tyylit -lähtöasetukset:
- Seuran punainen #B91C2B
- Pääteksti grafiitti #171A1F
- Taustat valkoinen #FFFFFF ja vaalea #F3F5F7
- Painikkeissa maltillinen 8–12 px kulmanpyöristys, korteissa noin 16 px
- Riviväli noin 1.6; osioiden väli mieluummin 24–32 px kuin päällekkäiset 70 px tyhjät välit
- Pidä nykyinen tumma nyrkkeilykehän taustakuva/hero, jos se näkyy hyvältä myös mobiilissa.

## 2. Puuttuva tulokset → Ajankohtaista -väliviiva

GitHubin docs/news-embed.js sisältää CSS-muutoksen joka piirtää saman punakeskisen erottimen myös uutisosion **yläpuolelle**. Tämä on saman linjan alareunan ja muiden osioiden välisten erottimien kanssa. Muutoksen julkaisun jälkeen päivitä selain Ctrl+Shift+R ja tarkista myös mobiiliesikatselu. Älä lisää toiseksi erillistä HTML-viivaa samaan paikkaan.

## 3. Valmiiden sivupohjien käyttö

**Harjoittelu:** avaa /harjoittelu/ → muokkaa vanhaa harjoitusryhmätekstiosuutta → korvaa se tiedoston embed/YHDISTYSAVAIN_HARJOITTELU_PREMIUM.html sisällöllä. Älä lisää saman tekstin rinnalle, muuten sisällöstä tulee päällekkäinen.

**Seura:** korvaa Seura-yleissivun oma johdanto tiedoston embed/YHDISTYSAVAIN_SEURA_PREMIUM.html mukaisilla navigointikorteilla. Älä siirrä tai poista Hall of Famen, historiatekstien tai muistokirjoituksen alkuperäisiä sivuja.

**Liity mukaan:** lisää vain esittelyosion HTML tiedostosta embed/YHDISTYSAVAIN_LIITY_PREMIUM.html nykyisen natiivi-jäsenlomakkeen yläpuolelle. Älä korvaa natiivia jäsenlomaketta HTML-lomakkeella.

**Tuloksia-arkisto:** tiedosto embed/YHDISTYSAVAIN_TULOSARKISTO_PREMIUM.html luo vuosille 2002–2019 helppolukuisen ruudukon. Säilytä alkuperäiset 18 vuosisivua ja niiden historialliset tulokset.

Kaikissa pohjissa on sama GitHub CSS-linkki myös niitä Yhdistysavain-versioita varten, joilla ei ole Koodieditoria. Tämä mahdollistaa yhden GitHub-tiedoston keskitetyn CSS-ylläpidon.

## 4. Ennen muiden sivujen sisältöpäivitystä

Pyydä ryhmien vetäjiä vahvistamaan nykyiset hinnat, jäsenmaksut, SuomiSport-lisenssikäytäntö, harjoitusajat, yhteyshenkilöt sekä seuran vaatteiden tilaustapa. Nyrkkeilijäsivuilla Tomi vahvistaa aktiiviset ottelijat ja painoluokat. Kuvat alaikäisistä vain asianmukaisin luvin.

## 5. Hakukoneet ja alatunniste

Yhdistysavain → Sivun asetukset → Metatiedot: yksilöllinen otsikko, lyhyt kuvaus, tarvittaessa oma somekuva. Etusivulta tulee poistaa vanha 25.8.2026-kurssi ja väite ottelujen päivittymättömyydestä alkuperäisistä piilotetuista tekstiosioista, ei vain piilottaa niitä CSS:llä.

Yhdistysavain → Alatunniste: lisää Facebookin ja Instagramin oikeat linkit. Lisää YouTube ja TikTok vasta kun seuran tilit ja omistusoikeudet on varmistettu.

## 6. Testit ja paluu aiempaan

- Käy läpi etusivu, kolme harjoitteluryhmää, ilmoittautuminen/jäsenlomake, viisi kilpailijaprofiilia, yhteystiedot, uutiset ja yksi historian vuosilehti tietokoneella ja puhelimella.
- Jos global CSS vaikuttaa Yhdistysavaimen kirjautumis- tai muokkaustyökaluihin, poista Koodieditorin linkki välittömästi. Halutessasi käytä vain HTML-lohkokohtaisia .rkk-page-luokkia.
- Yhdistysavain säilyttää sivuhistoriaa, joten vanha sisältö voidaan palauttaa Sivun asetukset → Historia -kohdasta.
- GitHubin automaattinen sivuinventaario on vain **lukuoperaatio**; se ei koskaan muuta alkuperäisiä Yhdistysavaimen sivuja.

Ohje: https://ohjeet.yhdistysavain.fi/kotisivut/osiot/koodieditori/
