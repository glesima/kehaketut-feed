## 11.11.2026 – Ilon mestaruushaastatteluvideo kaikille neljälle kanavalle
Seuran vastuuhenkilö hyväksyi V7-videon ja valtuutti välittömän Facebook-, Instagram-, YouTube- ja kotisivujulkaisun. Video 101,134 s, 720×1280, H.264/AAC, tekstitykset kovakoodattu; mestaruus täsmennetään kaikissa teksteissä muodossa **B-junioreiden yli 80 kg sarjan Suomen mestari**. Sosiaalisen median julkaisut ovat jatkoa jo 9.11. julkaistulle Ilon mestaruusuutiselle, eivät ottelutulosten uudelleenjulkaisuja. Metricoolin Kehä-Ketut-brändi 7632678 vahvisti Facebook-reelin, Instagram-reelin ja YouTube Shortsin automaattisen julkaisun klo 22.05 Europe/Helsinki 11.11.2026; PUBLISHED-tila ja julkiset postaus-URL:t tarkistetaan erikseen ennen kuin onnistuminen vahvistetaan.

Julkisen GitHub Pagesin aiempi kuvallinen mestaruusartikkeli `docs/tiedotteet/ilo-gronroos-suomen-mestariksi-2026-11-09.html` sai uuden mestaruushaastattelun videoelementin. Video toistetaan jo Metricoolin yleisessä mediakirjastossa saatavilla olevasta, HTTPS 200 -tarkistetusta MP4-kopiosta (`static.metricool.com/planner/202611/7632678-file-9567687806549624587.mp4`); ei Dropboxin yksityisestä linkistä eikä uudesta natiivista CMS-uutisesta. Lisäksi uutisarkiston korttiteksti kertoo videosta, mutta vanha uutisotsikko ja uutinen säilyvät. Etusivun ja arkiston vanhoja linkkejä ei muutettu.

## 9.11.2026 – Facebook- ja Instagram-syötteiden PUBLISHED-fallback

Ylläpitäjä havaitsi yli neljän tunnin jälkeen, ettei 9.11. klo 17 julkaistua Ilon SM-kultaa näy verkkosivun somekorteissa. Molemmat Metricool-julkaisujen tekniset tietueet vahvistavat `PUBLISHED`-tilan ja julkiset osoitteet, mutta Instagramin ja Facebookin Analytics-haku ei vielä palauta niitä. Olemassa olevia `docs/facebook.json` ja `docs/instagram.json` -syötteitä täydennettiin täsmälleen yhdellä jo julkaistulla postauksella per kanava brändi-/tilivarmennuksen jälkeen; vanhat viimeisimmät julkaisut säilytettiin ja 6 merkinnän yläraja pidettiin. Instagramin julkinen julkaisu on `https://www.instagram.com/p/DfhnknqFVBF/` ja Facebookin `https://facebook.com/1570416605115618/posts/1587214296769182`. Kummankaan kanavan uutta viestiä ei luotu.

Instagramin esikatseluosoite tuli Metricoolin jo julkaistun postauksen mediatiedoista ja voidaan kopioida turvallisesti omaan `assets/instagram/DfhnknqFVBF.jpg`-polkuun vain tarkalla mediahostin/kuvatyypin tarkistuksella. Kirjautumista, yksityisiä Dropbox-linkkejä tai muita tilejä ei käytetä. Automaatioiden tuleva analytiikkaviive pitää käsitellä ilman syötteen palautumista vanhaan tai vahvistetun julkaisun katoamista.

## Uutisarkisto yhdistää GitHubin ja Yhdistysavaimen — 9.11.2026

Ylläpitäjä osoitti kuvakaappauksella, että etusivun ”Kaikki uutiset” -linkki vei edelleen Yhdistysavaimen `/uutiset/`-arkistoon, josta Ilon hyväksyttyä GitHub Pages -SM-kultauutista ei löytynyt. Tämä oli käyttäjälle näkyvä virhe, koska 9.11. oli jo hyväksytty GitHub Pages uutisten ensisijaiseksi julkaisupinnaksi.

Ratkaisuna tehdään **oma tyylikäs julkinen uutisarkisto** `docs/uutiset/index.html`. Tietolähteet: toimituksellisesti julkaistut GitHub Pages -artikkelit `docs/news-owned.js` ja alkuperäisestä Yhdistysavain-arkistosta kerätyt uutiskortit `docs/news-archive.json`. Jälkimmäistä voi täydentää vain jo julkisella CMS-sisällöllä; alkuperäistä arkistoa ei poisteta. Vanhat alkuperäiset CMS-linkit säilyvät. Ilon uutinen löytyy uudesta arkistosta ensimmäisenä ja artikkelin lopusta on paluulinkki arkistoon. Mukana on myös linkki alkuperäiseen vanhaan uutisarkistoon, koska kaikkia vanhoja sivuja ei välttämättä ole vielä inventoitu.

Etusivun ”Kaikki uutiset” sekä news-loader-virhetilan linkki osoittavat nyt omaan uutisarkistoon. Etusivun kolme uutiskorttia yhdistävät julkisesti hyväksytyt omat uutiset ja CMS:n julkiset uutiset päivämäärän mukaan; uuden oman uutisen julkaisu vaatii toimituksellisen hyväksynnän ja lisäyksen `news-owned.js`-rekisteriin. Ilon väliaikainen 30.11.2026 vanhentumislogiikka on poistettu: uutinen pysyy arkistossa ja etusivun kolmen tuoreimman joukossa niin kauan kuin sen päivämäärä oikeuttaa, ei erillisellä kampanja-ajastuksella.

## Uusi päätös 9.11.2026 — omat näyttävät verkkouutiset ensisijaisiksi

Seuran vastuuhenkilö hyväksyi Ilon SM-kultauutisen nykyisen GitHub Pages -ulkoasun ja totesi, ettei `glesima.github.io/kehaketut-feed/...` -osoite haittaa. Hän pitää Yhdistysavaimen omia uutisartikkeleita ulkoasultaan heikompina ja haluaa käyttää nykyisen kaltaista näyttävää, seuran brändin mukaista kuvallista GitHub Pages -artikkelipohjaa **ensisijaisesti aina kun voidaan**. Tämä päätös **korvaa vanhan ohjeen**, jonka mukaan Yhdistysavain oli uutisten ensisijainen julkaisupaikka. Yhdistysavainta voi käyttää tarvittaessa poikkeuksena esimerkiksi natiivitoiminnon tai erityisen yhteensopivuustarpeen vuoksi; sitä ei tarvitse käyttää vain oman domainin osoitteen saamiseksi.

Hyväksytty visuaalinen esimerkki: `docs/tiedotteet/ilo-gronroos-suomen-mestariksi-2026-11-09.html`. Seuran uutiset tehdään lähtökohtaisesti erillisiksi pysyviksi julkisiksi HTML-artikkeleiksi: laadukas typografia, brändi-ilme, hyvä mobiilinäkymä, julkaisupäivä, kuvien saavutettavuustekstit, mielekkäät kuvatekstit, kuvan käyttöoikeudet ja varmennetut faktat. Julkaisun jälkeen etusivulla tulee näkyä oikea linkki tähän artikkeliin. Älä julkaise kuvallista uutista ennen julkaisulupien ja sisältöjen vahvistamista; vanhat uutiset säilytetään.

**Nykyinen tekninen rajoitus:** etusivun `docs/news-embed.js` hakee yhä Yhdistysavaimen julkisia uutisia ja lisää Ilon jutun erillisellä väliaikaisella nostolla, joka päättyy 30.11.2026. Tämä yksittäinen erikoisnosto ei ole vielä yleiskäyttöinen GitHub-uutisarkisto eikä tuota automaattista nostoa seuraavalle GitHubissa julkaistulle jutulle. Seuraavan kehitysvaiheen tavoite: tehdä toimituksellisesti hallittu GitHub Pagesin uutisindeksi/arkisto ja etusivulle tästä ensisijaisesti ammentava, deduplikoiva kolmen kortin uutisnäkymä, säilyttäen nykyiset CMS-uutiset/historiat ja turvallinen virhevara. Osoitteen mahdollinen siirtäminen seuran alidomainiin on myöhemmin harkittava lisäparannus, **ei julkaisemisen edellytys**.

## Ilon SM-kultauutinen — 9.11.2026
Seuran vastuuhenkilö vahvisti 9.11.2026 Ilon kuvien ja SM-kultauutisen julkaisuluvat. Kaksi yksityisestä Dropboxista Metricooliin jo hyväksytysti kopioitua JPEG-kuvaa liitettiin Facebookin ja Instagramin luonnoksiin; molemmat siirrettiin automaattiseen julkaisuun 9.11.2026 klo 17.00 Europe/Helsinki (kanavan lopullinen PUBLISHED-tila tarkistetaan erikseen).

Yhdistysavaimen natiiviin uutisarkistoon ei ole tässä yhteydessä kirjoitusyhteyttä. Julkinen kuvallinen SM-uutinen on siksi toteutettu GitHub Pages -sivulle `docs/tiedotteet/ilo-gronroos-suomen-mestariksi-2026-11-09.html`; nykyisen etusivun uutisupotuksen ensimmäinen kortti nostaa jutun näkyviin 30.11.2026 saakka. Native CMS -uutisen ilmestyessä nosto korvautuu sillä (ei duplikaattia), eikä alkuperäistä CMS-arkistoa, news.jsonia tai sen syöttöä muuteta. Kolmen uutiskortin katto säilyy eikä erillistä banneria luoda.

Kuvat ladattiin julkaisuun Metricoolin media-osoitteista, ei Dropboxin yksityisistä linkeistä. Oman pysyvän kuva-assetin käyttöönotto jää jatkoasiaksi, mikäli CDN-linkki ei ole pysyvästi käytettävissä.

## Kempeleen Nuorten SM 2026 -otteluhistorian täydennys — 9.11.2026

Julkisista virallisista BoxerBase-tuloksista varmennettu lauantain 7.11.2026 puuttunut otteluhistoria: Ilo Grönroos voitti B-juniorien 80+ kg finaalissa Kevin-Kristjan Veskuksen 5–0 (ottelu `nrAXlpdEXsze`) ja voitti siten Suomen mestaruuden. Kosmo Grönroos hävisi B-juniorien 70 kg välierässä Otto Elias Mieloselle 0–5 (ottelu `T8SUpZo9ejpR`). Ilon aiempi perjantain 6.11. välierävoitto Oscar Lindemanista 4–1 säilytettiin ennallaan.

Molemmat julkisesti varmistetut ottelut lisättiin rajattuna historiallisena täydennyksenä nykyiseen `docs/data.json`-syötteeseen, säilyttäen lähde-URL, ottelun id, oikea kilpailupäivä, kulmat ja tuomaripisteet. Ottelutietoja ei keksitty eikä nyrkkeilijöiden palveluntarjoajan ilmoittamia kokonaisvoitto-/ottelumääriä summattu. `scripts/update.py` säilyttää aiemmat ottelumerkinnät URL-avaimella ja deduplikoi uuden provider-osuman saman tapahtuma-/ottelutunnisteen perusteella, joten täydentävä tietue säilyy myöhemmissä hauissa. Pitkän aikavälin kattava ottelulistojen aikajaksopoiminta on edelleen erillinen puute.

Viralliset lähteet: https://fin.boxerbase.com/fi/e/zdyYMbmXqIuV/m/nrAXlpdEXsze ja https://fin.boxerbase.com/fi/e/zdyYMbmXqIuV/matches?t=Xa-OpJf1h8oK. Julkisia Facebook-/Instagram-/Yhdistysavain-tiedotteita ei tämän lähdekorjauksen yhteydessä tehty.

## Codexin havaintojen korjaukset — 9.11.2026

GitHub PR #27:n Codex-katselmus havaitsi, että BoxerBase-ottelusivun otsikon puuttuessa varmistetun nyrkkeilijän linkkiteksti voi sisältää nimen perässä seuran nimen; aiempi täsmänimitarkistus saattoi pudottaa ottelun pois. Fallback-tunnistus hyväksyy nyt **vain täsmällisesti tunnetun seuran päätteen**, ja otsikon normaalit tarkistukset sekä erillinen osallistujan seuravarmennus säilyvät tiukkoina. Testit kattavat myös samannäköisen väärän seuran ja eri urheilijan torjunnan.

GitHub PR #29:n Codex-katselmus havaitsi, että tilastoristiriidan vuoksi nollatuiksi piilotetut voitot ja tappiot voidaan tulkita virheellisesti 0–0-saldoksi, jos otteluita on kirjattu nolla. Sekä lista- että profiilinäkymä estävät nyt nollaesityksen, kun `stats_quality=provider_counts_conflict`. Tavallinen tyhjä nollaprofiili säilyy yhtenäisenä. Python- ja JS-regressiotestit lisätty.

Erillinen lähdetietotarkistus: Kempeleen nuorten SM-turnauksen julkisella finaalisivulla Ilo Grönroos voitti Kevin-Kristjan Veskuksen 5–0 B-juniorien 80+ -sarjan finaalissa lauantaina 7.11.2026. Hän voitti myös Oscar Lindemanin välierässä 4–1. Nykyisestä syötteestä puuttuu finaali, joten historiallisten otteluiden poiminnan kattavuus vaatii erillistä jatkokorjausta. Tätä ei ole merkitty automaattisesti ratkaistuksi. Lähde: https://fin.boxerbase.com/fi/e/zdyYMbmXqIuV/m/nrAXlpdEXsze (julkinen ottelutulos), https://fin.boxerbase.com/fi/e/zdyYMbmXqIuV/g/MJpLlyyBZpSF (kilpailukaavio).

## Tulevien kilpailujen tiivistys — 9.11.2026
Ylläpitäjän toive: seuran etusivu ei saa näyttää kuuden yleisen tulevan kilpailun pitkää listaa ilman yhtään Kehä-Kettujen osallistujaa. Kilpailusivu näyttää nyt yhteensä **enintään kolme** seurakohtaista tulevaa tapahtumaa: julkisesti vahvistettuja tulevia ottelupareja tai seuran nykyisiä, tunnistettuihin ottelijoihin sidottuja julkisia ilmoittautumisia. Pelkässä yleisessä BoxerBase-tapahtumakalenterissa olevia kilpailuja ei nosteta sivulle. Samassa tapahtumassa olevat ilmoittautumiset yhdistetään yhdeksi kortiksi. Otteluparin tapahtumaa ei näytetä toistamiseen ilmoittautumiskorttina.

Vanhoja 'previously_observed'-havaintoja ei väitetä ajantasaisiksi ilmoittautumisiksi. Lähdeprofiilien ja kilpailujen taustahaku säilyy muuttumattomana; tietojen puuttuminen julkisesta syötteestä ei tarkoita ilmoittautumisen perumista. Jos seuraosallistumisista ei ole julkaistua vahvistusta, tuleva osio sisältää vain lyhyen neutraalin tekstin. Tämä on näkyvyysmuutos, ei ottelija-/tulostietojen muokkaus.

## Julkisen sivun selkokieli ja ilmoittautumisten näkyvyys — 8.11.2026
Ylläpitäjän palaute: BoxerBase on vain tietolähde, ei seuran oman kilpailusivun pääviesti. Näytetään siksi esimerkiksi ”6 ottelua”, ”2 voittoa” ja ”Tulevat kilpailut”. Lähde mainitaan korkeintaan pienenä tarkistusviitteenä. Aiempi ”BoxerBase-ottelua” poistettiin otsikkokorteista ja profiilitilastoista. Mahdollisesti puutteelliseen otteluhistoriaan ei lisätä keksittyjä voittoja tai tappioita.

Yleiseen kilpailukalenteriin lisättiin kunkin tapahtuman alle **vain jo erikseen julkisesti varmennetut** Kehä-Kettujen ilmoittautuneet, jos niitä on. Tapahtuman olemassaolo ei todista seuran osallistumista; ilman varmennusta teksti on ”Osallistumistiedot täydentyvät.” Tämä ei korvaa erillistä seuran vahvistamiin ilmoittautumisiin perustuvaa tietolähdettä. BoxerBasen kirjautunut ylläpitäjä voi nähdä tulevia kilpailuja, joiden osallistujat eivät ole vielä tavallisen kävijän julkisessa tietonäkymässä. Niiden henkilökohtaisia ilmoittautumistietoja ei haeta yksityisiä näkymiä kiertämällä eikä keksitä; ensin tarvitaan seuran tarkka nimikohtainen varmennus ja julkaisemisen peruste.

Muutoksia ei tehty muualle kuin GitHub Pages -näkymiin, niiden regressiotesteihin ja tähän tilannekirjaukseen. Yhdistysavaimen live-renderöinnin riippumaton toteaminen on vielä erillinen työ.

## Tulevat kilpailut ilman ylläpitäjän kirjautumista — 8.11.2026
BoxerBasen tapahtumahaku palauttaa julkisten tapahtumien listan `discovered_events`, mutta aiempi kilpailu-widget näytti tulevaisuuden osalta vain varmistetut otteluparit ja julkisilta osallistujasivuilta havainnoidut seurailmoittautumiset. Jos kumpaakaan ei ollut, yleinen kilpailukalenteri jäi kokonaan näyttämättä.

Widget näyttää nyt erikseen enintään kuusi tulevaa julkista BoxerBase-tapahtumaa, merkittynä **yleiseksi kilpailukalenteriksi**. Niitä ei esitetä Kehä-Kettujen otteluina tai ilmoittautumisina, ellei erillistä julkista näyttöä ole. Vain BoxerBase-domainin suorat tapahtuma-URL:t hyväksytään, vanhentuneet ja päällekkäiset tapahtumat suodatetaan. Kirjautuneen ylläpitäjän BoxerBase-näkymät voivat sisältää tietoa, jota julkinen lähde ei anna; ne eivät ole sama asia kuin julkisesti todennettu ilmoittautuminen.

Muutos koskee vain GitHub Pagesin `widget.html`-näkymää ja sen testejä, ei Yhdistysavaimen CMS:n staattisia tekstejä. Jälkimmäisen live-selaintodennus ja mahdolliset sisältömuutokset ovat erillisiä työvaiheita.

## Kilpailijakorttien tarkistus 8.11.2026
Ylläpitäjän kuvakaappaus oli otettu **ennen** BoxerBase-siirron voimaantuloa. Sitä ei saa käyttää uuden julkaisun virhetodisteena. Uusi julkinen tietosyöte sisältää 9 säilyneen seuran profiilia, uudet tunnisteet ja aiempien profiili-ID:iden vastaavuudet.

Ottelijakorteissa kerrotaan täsmällisesti BoxerBaseen kirjattu ottelumäärä (ei väitetä uran täydelliseksi ottelumääräksi). Kun profiilissa on 0 kirjattua ottelua eikä erillistä voitto-/tappioerittelyä, näytetään kortin yhtenäisyyden vuoksi 0 voittoa ja 0 tappiota **vain julkisen BoxerBase-tietolähteen osalta**, muuttamatta varsinaista lähdedataa. Ristiriitaisia tilastoja ei muuteta nolliksi eikä vanhojen profiilien eri lukuja summata. Julkisen lähteen mahdollista puutteellista urahistoriaa ei täytetä arvioilla.

## BoxerBase-korjaus vahvistettu 8.11.2026
Virallinen lähdeseura on `RIIHIMÄEN KEHÄ-KETUT` (`mZjkT0LW248X`), entinen `1Le8shnOwPIW` on palveluntarjoajan yhdistämä. PR #27 yhdistetty commitilla `b9c992ab3725af3fa8ca4a96e638f0fb048fd534`, kaikki tarkistukset läpäisty ja Pages-ajo `42524909199` onnistui. Julkaistavasta `docs/data.json`-syötteestä luettiin vahvistetusti 9 uutta BoxerBase-ottelijatunnistetta, 9 historiallista ottelumerkintää ja vanhat profiilitunnisteet uuteen rosteriin yhdistävä vastaavuustaulukko. Lähdettä ei enää lueta poistetulta seuratunnisteelta.

PR #28 suojasi neljän profiilin ristiriitaisia voitto-/tappioerittelyjä. Lähteessä nämä ylittivät ilmoitetun ottelumäärän, joten erittely piilotetaan eikä lukua korjata arvauksella. Uusi tietohaku `2026-11-08T21:29:36Z` vahvisti kaikki 9 ottelijaa ja 9 ottelumerkintää; Pages-ajo `42525447525` onnistui. Verkkosivun Yhdistysavain-ympäristön erillistä selaintarkistusta ei tässä yhteydessä onnistuttu suorittamaan. Kotisivun ylimääräistä sisältöä tai historiallisia uutisia ei muutettu.

## Lisätarkistus 8.11.2026 — BoxerBasen ristiriitaiset tilastot
Yhdistetyn seuran yhdeksän ottelijan uudet ID:t ja vanhojen profiilien vastaavuudet on luettu vahvistetusta julkaisuajosta. Neljässä profiilissa lähteen ilmoittamat voitot+tappiot ylittävät kokonaisottelumäärän. Näissä tapauksissa voitto-/tappioerittelyä ei näytetä arvauksena, mutta itse ottelija, hänen uusi tunnisteensa, ottelumääränsä ja vahvistetut tuloskortit jäävät näkyviin. Lähteen erittelyn tarkistusta ei ole merkitty ratkaistuksi.

## BoxerBase-lähdemuutos 8.11.2026
Virallisen yhdistetyn seuran tunniste on mZjkT0LW248X. Lähdemigraation koodi vaihtaa rosterin, säilyttää vanhat viralliset ottelut ja liittää aiemmat profiilit uuteen listaan vain täsmällisesti varmennetuilla nimillä. Se ei laske vanhojen duplikaattien ottelutilastoja yhteen. Lähdehaun ja Pages-käyttöönoton tulos tarkistetaan erikseen. Katso docs/BOXERBASE_MERGE_2026-11-08.md.

# Nykytila ja tunnetut rajat

Päivitetty 2.11.2026. Tämä tiedosto on nykytilan aloituspiste. Päivätyt suunnitelmat kuvaavat myös aiempia työvaiheita, eivät automaattisesti tämänhetkistä käyttöönottoa.

## Somepalstojen korkeudet korjattu — social v4, 2.11.2026

Ylläpitäjä vahvisti Juicerin korvaavan näkymän näkyvän, mutta kuvakaappauksessa Facebook-palsta jäi Instagramia pidemmäksi ja sen alaosassa oli ylimääräistä tyhjää. V4 korjaa rakenteen, ei vain venytä Instagramia saman tyhjän tilan mittaiseksi.

- Etusivun `docs/social-embed.js` lukee nyt myös Facebookin suoraan nykyisestä `facebook.json`-syötteestä. Erillinen Facebook-iframe, sen 530 px:n oletuskorkeus ja korkeuden viestikuuntelija poistettiin vain tästä someosiosta. Vanha `facebook.html` säilyy erillisenä yhteensopivuussivuna.
- Molemmissa sama otsikko–kolmen kortin lista–alalinkki/lähdetieto-rakenne. Desktopissa palstat ja vastaavat korttirivit asettuvat yhtä korkeiksi sisällön mukaan. Mobiilissa palstat ovat allekkain ilman pakotettua yhtäläistä korkeutta. Myös Facebookissa on Katso lisää -linkki.
- Nykyiset somejulkaisut, syötteiden tiedot, kuva-assetit ja ajastettujen ylläpitotehtävien asetukset säilyvät. Ei uusia somejulkaisuja, maksuja, Juicer-riippuvuutta tai muutoksia uutisiin/BoxerBase-upotuksiin/media-vastaanottimeen.
- `node --check` sekä 24 paikallista Chromium-skenaariota läpäisty. Leveydet 1600/1200/900/768/701/700/390/320 px. Mitatut tasakorkuiset desktop-palstat ja korttirivit, sama alalinkkien taso, normaali alareunapadding, ei kasvua toistuvissa leveysmuutoksissa. Testattu myös molempien kanavien erilliset virheet, turvattomat URL:t, duplikaatit, HTML-tekstin turvallinen näyttö, rikkoutunut kuva, eri julkaisumäärät ja suurempi teksti.
- Testit käyttävät synteettisiä tietoja ja pikkukuvia. Tämä ei ole riippumaton live-Yhdistysavain-selaintesti. Ajettava testi on `qa/check_social_layout.py`, erillinen vapaaehtoinen kehitystesti (Playwright/Chromium), ei uusi tuotantoriippuvuus.
- Koodicommit `057099de4d5ec95c5f4020d0e2cd01abca13b35e`. Testatun ja GitHubista takaisin luetun JS:n Git-blob SHA sama: `737d8dcfa514cb6eb0a3f34a1097991655d18bd3`. Pages-ajon tunniste `41531038511`; ajon lopullinen tila tarkistetaan GitHubista erikseen.
- Ajantasainen rakenne ja muuttumaton tietosopimus: `docs/INSTAGRAM_NOSTOT_2026-11-02.md`.

## Instagram: Juicer korvattu omalla tiiviillä nostolla 2.11.2026

Ensimmäisessä toteutuksessa `docs/social-embed.js` v3 korvasi Juicer-syötteen kolmella pienellä Instagram-kortilla. Kortissa on kuva, julkaisupäivä, lyhyt otsikko/ote ja linkki alkuperäiseen julkaisuun. Ei Juicer-scriptiä, mainosta, automaattisesti ladattavaa videosoitinta, loputonta syötettä tai sisäistä vieritystä. V3:n Facebook-kehys korvattiin yllä kuvatussa v4:ssä suorilla korteilla; Facebookin nykyinen päivitystehtävä säilyy. Mobiilissa palstat ovat allekkain.

- Alkuperäinen koodicommit `577727772aeb01f09dd8f5a24cf0f5e587c5e4f6`. Pages-ajo `41527594857` valmistui success-tilaan; testit, kuvavälimuisti ja Deploy Pages onnistuivat.
- Ensimmäinen syöte haettiin live-Metricool-yhteydestä oikean brändin 7632678 / @kehaketut tarkistuksen jälkeen. Reels-haku palautti kolme julkaistua videota; saman aikavälin tavallisten postausten haku oli tyhjä. Ei luonnoksia tai uusia somejulkaisuja.
- `docs/instagram.json` on erillinen some-nostojen tietolähde. Vanhat `docs/data.json`-Instagram-kentät tai Juicer eivät ohjaa tätä näkymää.
- GitHub Actions tallensi kaikki kolme oikeaa JPEG-esikatselua polkuun `docs/assets/instagram/`: DfCDNnGgVUU.jpg (2721 tavua), De9SHpJCSff.jpg (40466 tavua), De9QLdAkr_o.jpg (52979 tavua). Repon jälkiluku vahvisti tiedostot. Selaimet eivät ole riippuvaisia Instagramin väliaikaisten kuvalinkkien voimassaolosta.
- Ajastettu Instagram-ylläpito on luotu ja käytössä: neljä tarkistusta päivässä, vain tämän brändin jo julkiset Reels- ja Feed-julkaisut, kirjoituskohde vain `docs/instagram.json`. Tämä on ChatGPT:n ajastettua Metricool/GitHub-ylläpitoa, ei käyttäjän Kubuntun itsenäinen somepalvelu. Ensimmäinen listan täyttö tehtiin tässä työvaiheessa; tulevan ajastetun kierroksen suorittamista ei vielä väitetä testatuksi. Uuden julkaisun näkyminen riippuu Metricoolin tiedon saatavuudesta, tarkistuskierroksesta ja Pages-julkaisusta, ei reaaliaikaisesta push-ilmoituksesta.
- Erillinen `cache_instagram_thumbnails.py` kopioi sallituilta Meta-CDN-isänniltä enintään 3 MiB JPEG-kuvat atomisesti. Vanhat onnistuneet kuvat säilyvät virheessä; selain näyttää neutraalin linkkikortin puuttuvalle kuvalle. Korttilinkit/tekstit toimivat ilman kuvaa.
- V3:ssa paikallisesti 12 uutta yksikkötestiä ja 10 Chromium-skenaariota läpäisty: 1200/768/390/320 px, ei vaakaylivuotoa, duplikaattisuoja, rikkoutuva kuva/syöte, väärä brändi, turvattoman URL:n hylkäys ja tekstin turvallinen näyttö. Testatun JS:n Git-blob SHA täsmäsi julkaistuun lähteeseen.
- V3-layout-testi käytti synteettisiä pikkukuvia ja Facebookin staattista testisisältöä. Se ei ollut riippumaton lopullisen kehaketut.fi/Yhdistysavain-näkymän live-selaintarkistus. Julkisen sivun tuore renderöity näkymä ei ollut työympäristössä saatavilla. V4 poistaa tämän palstan iframe-riippuvuuden kokonaan.
- Ohje ja ylläpitosopimus: `docs/INSTAGRAM_NOSTOT_2026-11-02.md`. Juicer-tilausta ei ostettu tai peruttu. Historiallisia tiedotteita, somejulkaisuja, Facebook-syötettä, vastaanotinta tai media-automaatiota ei muutettu.

## Etusivun ylimääräinen tiedotenosto poistettu 2.11.2026

Ylläpitäjän pyynnöstä `docs/news-loader.js`:stä poistettiin harjoitusten jatkumista koskevan erillisen etusivuilmoituksen luontifunktio ja sen kutsu. Uutisten lataus, virhetilanteen uutisarkistolinkki ja duplikaattisuoja säilyvät. Tiedotesivuja, uutisarkistoa ja Facebook-julkaisua ei poistettu tai muokattu.

- Koodimuutos: `e245788abf10ee812a58fbef62b8d45337799ce2`.
- JavaScriptin syntaksitarkistus ja kahdeksan paikallista simuloidun DOM:n testiä läpäisty. Testit eivät ole oikean selaimen näyttötesti.
- Muutos käynnisti Pages-ajon `41520292153`; myöhempi työkalutarkistus vahvisti sen success-tilan. Tämä ei yksin ole selaimen näyttötesti.
- Alun perin 6.11. päättyväksi tarkoitettu lisänosto on poistettu koodista ennen määräaikaa. Alla oleva 30.10. julkaisutieto säilyy historiatietona.

## Harjoitukset jatkuvat 30.10.2026

Seuran vahvistuksen perusteella Kamppailukeskuksen harjoitukset jatkuvat perjantaina 30.10.2026 klo 17.00 alkaen normaalin harjoitusaikataulun mukaisesti. Peruutus 27.–29.10. on päättynyt. Korjausten valmistumisesta tai sisäilman mittaustuloksista ei esitetä erillisiä väitteitä.

- Facebook-tiedote julkaistu 30.10.2026 klo 01.40 Europe/Helsinki. Metricoolin jälkitarkistus palautti PUBLISHED-tilan, alustan postitunnisteen ja julkisen osoitteen: https://facebook.com/1570416605115618/posts/1575746574582621 . Ei uusintajulkaisua.
- Julkinen tiedotesivu: `docs/tiedotteet/harjoitukset-jatkuvat-2026-10-30.html`.
- Etusivun `news-loader.js` lisäsi alun perin erillisen jatkumisilmoituksen uutisosion yläpuolelle 30.10.–5.11.2026. Nosto poistettiin yllä kuvatusti 2.11.2026. Uutisten suora Yhdistysavain-haku säilyy ennallaan. Alkuperäisen julkaisun paikallisen JavaScript-tarkistuksen yhdeksän skenaariota läpäisivät aikarajojen, duplikaattisuojan, puuttuvan kohde-elementin, DOM-valmiuden ja virhevaran testit.
- Aiempi GitHub Pagesin peruutustiedote säilyy kokonaisena ja sen alkuun lisättiin päivätty päivitys sekä linkki jatkotiedotteeseen. Vanha määräaikainen peruutusbanneri on jo vanhentunut 30.10. klo 00.00.
- Sisältöcommit `5ecf465e4a892f998ae9ae4282de5c2bd0c3b6e6`; Pages-ajon `40975026700` Deploy Pages -vaihe palautti success. Tämä ei ole riippumaton selaimen näyttötesti Yhdistysavaimen etusivusta.
- Yhdistysavaimen omaan `/uutiset/`-arkistoon ei tällä työvaiheella luotu tai muokattu artikkelia. Etusivun tiedotenosto ja erillinen julkinen tiedotesivu ovat eri julkaisupinta kuin uutisarkisto.

## Vahvistettu ja lähteen laatu

- Verkkosivun uutisnäkymän suora haku, päivämääräkorjaus, mukautuva otsikkokoko ja `news-loader.js` ovat päähaarassa. Ylläpitäjä vahvisti lataajaosoitteen vaihdon. Historiallinen onnistunut Pages-ajo: `40395207746`. Tämä merkintä ei väitä uutta selainmittausta jokaisella laitteella.
- Kolme kilpailuvideokokonaisuutta on julkaistu Facebookiin, Instagramiin ja YouTubeen: yksittäinen Hämeenlinnan ottelu, saman tapahtuman kahden ottelun yhteiskooste sekä 70 sekunnin Tampere-kooste. Viimeinen julkaistiin 28.10.2026. Julkaisuista palautuivat kanavakohtaiset tunnisteet ja julkiset osoitteet; tämä ei tarkoita jatkuvaa itsenäistä julkaisupalvelua.
- Tampere-koosteen V1:ssä raportoitiin toisto-ongelma. Ylläpitäjä vahvisti V2:n toimivan muuttamatta omia soitinasetuksiaan. Korjattua vientiprofiilia käytetään lähtökohtana; havainto ei yksin todista tietyn soittimen tai ajurin virhettä.
- Materiaalien vastaanottolinkki on testattu. Yksityinen vastaanotin v0.2.4 on nyt asennettu ylläpitäjän omalle koneelle. Ylläpitäjän toimittama tilaraportti vahvisti 27.10. aktiivisen ja automaattisesti käynnistyvän käyttäjäpalvelun, kymmenen vastaanottokierrosta, nolla peräkkäistä virhettä sekä onnistuneen Dropbox-lukukierroksen.
- Vastaanotin on tarkoituksella **receive-only**: se lataa ja tarkistaa aineiston, mutta ei renderöi tai julkaise. Koneen ja käyttäjäpalvelun käytettävyys on edellytys; ympärivuorokautista saatavuutta ei ole todistettu.
- Paikallinen v0.2.5-ottelutietolomake on toimitettu ylläpitäjälle. Sen käyttöönottoa tai ensimmäistä tallennusta käyttäjän koneella ei ole vielä vahvistettu. Paikallinen ylläpitolomake ei ole kuvaajille jaettava verkkopalvelu.

## Ei vielä tuotantokäytössä kokonaisuutena

- Ulkoisille kuvaajille tarkoitettu tapahtuma-, ottelija- ja materiaalityyppivalinnan yhdistävä lähetyspalvelu. Paikallinen pilotti ja julkinen käyttöön otettu palvelu ovat eri asioita.
- Uploaderin tietojen automaattinen yhdistäminen luotettuun ottelutietoon ja erilliseen julkaisuoikeusrekisteriin.
- Jatkuva tapahtumakohtainen keräys, odotusikkuna, myöhäisen materiaalin toimituksellinen valinta ja tuotantorenderöinti.
- Uudelleenpakattujen ja leikattujen kopioiden luotettava tunnistus. SHA-256 tunnistaa täsmälleen samat tavut, ei saman tallenteen eri pakkauksia tai eri kameroita.
- Jatkuva renderöinti–somejulkaisu-palvelu ja osittain onnistuneen kolmen kanavan julkaisun palautuminen.
- Kiireellisten uutisten itsenäinen Facebook-jakeluyhteys.

## Julkaisun ja oikeuksien todentaminen

`Sent` tai `PUBLISHED` ilman alustan tunnistetta ei yksin todista julkista näkyvyyttä. Instagramin aiemmassa pilotissa Auto publish OFF tarkoitti mobiili-ilmoitusta. Jatkossa varmistetaan automaattijulkaisun asetus ja kanavakohtainen lopputulos. Epäonnistunut kanava käsitellään erikseen; onnistuneisiin ei tehdä sokkona kaksoisjulkaisua.

Lähettäjän ilmoitus kuvausluvasta on aineiston lähdetieto, ei oikeus myöntää seuran julkaisulupia. Normaali ennalta valtuutettu aineisto on tulevan automaation tavoite; epäselvät tiedot ja luvat ohjataan poikkeuskäsittelyyn. Kiireellisen uutisen toimituksellinen julkaisu on erillinen työnkulku.

## Jatkettavuus ja julkinen sisältöraja

Katso [CONTEXT_HANDOFF.md](CONTEXT_HANDOFF.md) ja [PUBLIC_SCOPE.md](PUBLIC_SCOPE.md). Tämän julkisen repositorion tulee kuvata seuran näkyvät palvelut ja neutraali käyttöönottotila. Yksityinen mediajärjestelmän koodi, ylläpitotiedot, kuvaajien tiedot, valtuutukset ja projektikeskustelun sisäiset päätökset säilytetään erikseen. Historiatiedostojen julkisuustarkastus on edelleen erillinen tehtävä; historiaa tai toimivia vastaanottolinkkejä ei poisteta automaattisesti.

Sivuston some-nostojen ylläpito on erotettu yllä videoiden tuotanto- ja julkaisuketjusta. Vastaanotinta tai somekanavien asetuksia ei muutettu. Vanhojen käsittelyraporttien mitätöinti, tilapäisten virheiden palautuminen ja uudet koko mediaketjun testit ovat yhä tuotantokäyttöönoton tarkistuskohtia.
