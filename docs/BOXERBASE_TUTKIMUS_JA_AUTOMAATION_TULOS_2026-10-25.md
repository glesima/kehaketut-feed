# BoxerBase-tutkimus ja ilmoittautumisautomaation tuotantotesti – 25.10.2026

## Tiivistelmä

**Osa-alue otettu käyttöön:** Kehä-Kettujen etusivun tietosyöte löytää nyt BoxerBasen julkisella hakutoiminnolla kilpailuilmoittautumisia, jotka eivät näy palvelimelta saadun osallistujataulukon ensimmäisellä 20 rivillä. Ensimmäinen vahvistettu tuleva julkinen osuma on kaksi seuran ilmoittautunutta Nuorten SM-kilpailuissa, **Ilo Grönroos ja Kosmo Grönroos**. Tämä ei merkitse vahvistettua otteluparia tai kilpailutulosta.

## Mitä selvitettiin todellisesti?

1. BoxerBasen `/participants`-sivu on SvelteKit-selainsovellus.
2. Nuorten SM-kilpailun `/e/zdyYMbmXqIuV/participants` sivu ilmoittaa **157** osallistujaa, mutta alkuperäinen julkinen HTML sisältää vain **20** rivin taulukon (21 tr otsikkorivi mukaan lukien). Käytettävissä on sivunvaihto (1–8) ja hakukenttä. Pelkkä requests/BeautifulSoup ohittaa myöhemmillä sivuilla olevat ottelijat.
3. Julkisen **hakukentän** kautta etsimällä `Riihimäen` headless Chrome/Seleniumilla saatiin **kaksi tulosriviä** myös alkuperäisen 20 rivin ulkopuolelta. Sovelluksen normaalia julkista käyttöliittymää käytettiin ilman tunnuksia, eikä mitään suljettua API:a, henkilön syntymäaikoja tai maksutietoja luettu talteen.
4. `scripts/event_discovery.py` päivitettiin tunnistamaan tapahtumataulukon osallistujalinkki ja seuramerkintä, vaikka taulukossa on valinnainen ensimmäinen status-/toimintosarake.
5. `scripts/update_registrations_browser.py` käyttää käyttäjälle näkyvää julkista hakua vain tuleville/sopivan lähellä oleville julkisille kilpailuille, tarkistaa seuran tunnetun ottelijalistan ja tallentaa varmistetut julkiset osallistumiset kenttään `registrations`.
6. `scripts/update.py` ei enää pyyhi laajemman selaintarkistuksen julkisia ilmoittautumishavaintoja, jos ensimmäisellä 20 rivin palvelinsivulla ei näy seuramme nimiä.
7. Github Actionsin `.github/workflows/update.yml` ajaa BoxerBase-lähteet, uutiset sekä julkisten ilmoittautumisten selainhaun, julkaisee GitHub Pagesin datan ja näyttää ilmoittautuneet eri tilassa kuin `scheduled` ja `result_published`. Pääajastus neljä kertaa vuorokaudessa.
8. GitHubin läpäistyt testit: **21 testin sarja** ennen Selenium-vaiheen lisäämistä. Uudessa integraatioajossa nämä testit ja julkaisu onnistuivat.
9. Tuotantotieto `docs/data.json` päivittyi **2026-10-25 14:07:50 UTC**: `registrations` sisältää kaksi Nuorten SM 6.–8.11.2026 osallistujaa, **Ilo Grönroos** ja **Kosmo Grönroos**, seura **Riihimäen Kehä-Ketut ry**. `matches` sisältää edelleen kahdeksan aiemmin vahvistettua tulosta. Käyttöliittymä saa tiedot tämän JSONin kautta Yhdistysavaimen HTML-osioon; etusivua ei tarvitse käsin muuttaa.
10. Julkaisuajon evidenssi: https://github.com/glesima/kehaketut-feed/actions/runs/40200653158 . Datasta voidaan varmistaa rekisteröinnit: https://github.com/glesima/kehaketut-feed/blob/main/docs/data.json

## Oikea seura ja duplikaatit

- **Oikea virallinen seura:** Riihimäen Kehä-Ketut ry, `1Le8shnOwPIW`.
- **Väärä duplikaatti:** RIIHIMÄEN KEHÄ-KETUT, `mZjkT0LW248X`. Osa aiemmista otteluista, kuten Hämeenlinnan 24.10.2026, on merkitty väärälle seuraprofiilille. Nämä tunnetut historialliset tapahtumat tarkistetaan rajattuina poikkeuksina.
- Gleb Simanovin oikea tunniste `U2N_OOYxyFui`; siinä on myös Eemeli Platonenkon ottelu 27.9.2026. Josiaksen oikea seuran profiili `rLyNGj8sCoF7`, vanha rinnakkaisprofiili `vfT3Q-X7B3Tf`; kunnes BoxerBase yhdistetään, kattavampi tilasto näytetään erikseen rajatulla alias-säännöllä.
- Suomen Nyrkkeilyliitto vahvisti 13.10.2026, että väärään seuraan päätyneitä ilmoittautumisia on ja pääkäyttäjä korjaa niitä oikeisiin profiileihin. **Älä poista vanhoja profiileja ennen tulosten ja ilmoittautumisten siirron varmistamista.** https://www.nyrkkeilyliitto.com/uutiset/suomen-mestaruuskilpailujen-ilmoitt/

## Kolme eri lähdetietojen tilaa

- `registered`: nimi näkyy julkisessa osallistujalistassa. Ei lupaa ottelua.
- `scheduled`: julkinen ottelupari/timeslot julkaistu. Voi muuttua kilpailupäivänä. Kellonaikaarviota ei esitetä varmana.
- `result_published`: virallinen voitto/tappio/päätös julkaistu. Vain tällaiset menevät tuloskorteiksi.
- Jos osallistujaa **ei näy**, se voi johtua piilotetuista tiedoista, keskeneräisestä ilmoittautumisesta, hakunäkymän rajoista tai siitä, ettei ilmoittautumista ole. Älä päättele poisjääntiä ilman lähdettä.
- Viralliset näkyvyystiedot: https://fin.boxerbase.com/docs/event/visibility-and-publishing .

## Rajat ja vielä tekemättä

1. **Sivuhaun saatavuus:** Selenium-käyttöliittymä on julkinen mutta sitä voidaan muuttaa ilman ennakkoilmoitusta. Järjestäjä voi myös piilottaa julkiset osallistujat. Julkisen tiedon säännöllisen automaattisen käytön lupa/käyttöehdot ja suositeltu päivitysrytmi pyydetään BoxerBaselta.
2. **Virallinen luku-API/export/webhook:** dokumentoitua julkista rajapintaa ei löytynyt. Suositeltavin pitkäaikainen ratkaisu on pyytää BoxerBaselta luettavat tapahtumat, kaikki julkisesti julkaistut ilmoittautumiset sivutuksesta riippumatta, julkaistut otteluparit, tulokset, tunnisteet ja `updated_at`-muutosajat.
3. **Kaikki kilpailut:** uusi tapahtumahaku käyttää Suomen julkista tapahtumaluetteloa, mutta ei takaa kaikkien eri seurajärjestäjien tapahtumien täydellistä kattavuutta eikä ilmoittautumisia, jotka eivät ole julkisia.
4. **Kilpailupäivän tiheämpi seuranta:** toistaiseksi 4 päivitystä vrk, ei vielä 20–30 minuutin tapahtumaseurantaa. Tiheämpi sykli vasta luvallisen ja tehokkaan lähdereitin jälkeen.
5. **Otteluaikariskit:** ottelulistan arvioitu aika voi heittää tuntikausia; siksi etusivu linkittää lähteeseen eikä lupaa kellonaikaa.
6. **Tuplat ja korjatut tulokset:** ylläpidä `event_id`, `bout_id` ja `boxer_id` -avaimia; tuleva tuloskorjaus muuttaa olemassa olevaa tulosta eikä tee uutta ottelua. Nuorten tiedoista ei koskaan viedä syntymäaikoja tai maksutilaa julkiseen syötteeseen.
7. **Valmentajan lähdekorjaus:** Tomi/liiton pääkäyttäjä yhdistää duplikaattiseurat ja säilyttää tulos- ja ilmoittautumishistorian. Vaikutus syötteeseen tarkistetaan jälkeenpäin.
8. **Yhdistysavain:** uutinen julkaistaan edelleen `Uutiset → Lisää uutinen` -toiminnolla. Automaatio näyttää otsakortit mutta ei kirjoita automaattisesti natiiveja artikkeleita.
9. **Somet:** tulokset eivät vielä automaattisesti tee hyväksyttäviä Metricool-julkaisuja; seuraava vaihe vastaa tähän.

## Käyttöehtojen varmistuspyyntö BoxerBaselle

Pyydä virallisesta BoxerBase-tuesta / Suomen Nyrkkeilyliiton pääkäyttäjältä:
- Read-only dokumentoitu API, export, RSS tai webhook julkaistuihin tapahtumiin, osallistujalistaan, ottelulistaan ja virallisiin tuloksiin.
- Sivutuksen sekä tapahtumien ja nyrkkeilijöiden ID-tunnisteiden sekä julkaisun/muutoksen tilojen kuvaus.
- Sallitut kutsutiheydet ja avoimen kilpailudatan käyttölupa seuran verkkosivujen ajantasaisille kilpailu- ja tuloskorteille.
- Duplikaattiseuran `mZjkT0LW248X` ja urheilijoiden yhdistäminen oikeaan `1Le8shnOwPIW` seuraprofiiliin. Varmista, että vanhat ottelut ja ilmoittautumiset säilyvät.

## Johtopäätös

Julkisen hakukentän avulla tehty selainsidonnainen seuranta on todistetusti parempi kuin alkuperäinen vain ensimmäistä 20 osallistujaa lukevan Pythonin versio. Se on nyt käytössä, mutta pitkällä aikavälillä virallinen luku-API/raportti olisi vähähuoltoisempi ja oikeampi ratkaisu. Muut tietoturvarajoitukset ja toimituksellinen hyväksyntä pysyvät ennallaan.
