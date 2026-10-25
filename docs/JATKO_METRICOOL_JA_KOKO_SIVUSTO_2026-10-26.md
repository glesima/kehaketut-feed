# Kehä-Ketut – jatko 26.10.2026: Metricool ja turvallinen koko sivuston uudistus

Tämä muistio jatkaa 24.–26.10.2026 käytyä Kehä-Kettujen sivusto- ja somekeskustelua. **Tila: suunnitelma + vahvistetut havainnot, ei kaikkien sivujen käyttöönottoilmoitus.** Tallenna seuraavat päätökset ja testitulokset jatkossakin GitHubiin, jotta työ ei katoa keskustelujen välillä.

## Käyttäjän sitovat tavoitteet

- **Koko kehaketut.fi**, ei vain etusivu, samaan laadukkaaseen puna-valko-grafiitti-ilmeeseen. Käytetään nykyistä brändiä: #B91C2B, #171A1F, #FFFFFF.
- **Historiallinen sisältö säilytetään kokonaisuudessaan**: vanhat kilpailutulokset, 2002–2019 vuosittaiset tulokset, seuran historiikki, muistokirjoitukset, mitalistit, Hall of Fame, ottelijaprofiilien vanhat kilpailukertomukset, uutiset, alkuperäiset linkit ja kuvat. Älä pyyhi, korvaa virheellisellä BoxerBase-lukumäärällä tai katkaise vanhoja URL-osoitteita.
- **Ei kallista Yhdistysavain-päivitystä pelkän ulkoasun takia.** Tarkista oikea tilausversio ennen koodieditorista puhumista. Suunnitelma toimii myös niin, että Yhdistysavaimen Ulkoasu > Tyylit koskee natiiviosia ja jokainen oma HTML-osio käyttää yhtä GitHub Pagesin CSS-tiedostoa.
- Somekanavat nyt **Facebook, Instagram ja YouTube**. **TikTok myöhemmin**, ei nyt työtä sen käyttöönottoon eikä ostovaatimuksia.
- Mitään RSS:stä, AI-uutisluonnoksesta tai BoxerBase-tapahtumasta ei julkaista automaattisesti ilman nimettyä ihmistarkistusta ja asianmukaista julkaisupäätöstä.

## Todennettu nykytila (26.10.2026)

- Repositorion `main` sisältää yhdistetyn PR #12:n: `docs/rkk-premium-site.css`, 4 Yhdistysavain-premium-HTML-pohjaa, uutisosioiden erotinlisäyksen `docs/news-embed.js`:ään ja viikoittaisen julkisen sivustoauditin.
- Viimeisin julkaistu sivustoinventaario `docs/SIVUSTON_AUTOMAATTINEN_AUDITTI.md`: **59 julkista sivua, 0 latausvirhettä** (vain rajattu tekninen auditointi, ei täydellinen toimituksellinen sisällöntarkistus). Sivut: etusivu 1, harjoittelu 10, historialliset tulokset 19, kilpailijat 6, liittyminen 1, seura ja historia 11, uutiset 10, yhteystiedot 1.
- GitHubin CSS- ja erotinkorjaus **ei osoita Yhdistysavain-sivujen lopullista visuaalista asennusta**. Eritoten puuttuva tulokset → Ajankohtaista -viiva tulee vielä tarkistaa todellisessa desktop- ja mobiilinäkymässä. Ei toista erillistä erotinta päälle.
- Metricoolin oikean yhdistetyn brändin tunniste on `7632678`, Facebook-sivu `160875127258478`, Instagram `kehaketut`. Metricoolin **26.10.2026 liitäntävastaus sisältää myös YouTube-yhteyden**; seuran kanavan identiteettiä, omistajuutta ja käyttöoikeuksia **ei ole vielä itsenäisesti vahvistettu**. Vanhemmat dokumentit väittävät YouTuben puuttuvan: vahvista ensin, älä perusta uutta kanavaa automaattisesti.
- Metricoolin ajastetut julkaisut tarkistettiin 24.10.–30.11.2026: palautui **0 ajastettua postausta**. Tämä ei tarkoita, ettei Autolist-jonossa voisi olla disabled-sisältöä. Käyttäjän RSS-dialogin esikatselu näytti 3 löytöä, mutta tallennuspainikkeen painamista ei ole vahvistettu.
- Julkiseen `news-rss.xml`-syötteeseen tehdään vain toimituksellisia Yhdistysavain-uutisia. Ottelutulosten `rss.xml` pidetään erillisenä, ettei jokaisesta ilmoittautumisesta synny somepostausta.

## Metricool: välittömät käyttöliittymäohjeet

1. RSS-dialogi: `Max characters=250`, `Prefix`/ `Suffix` tyhjät, `Add 3 previous posts=OFF`, `Include new post disabled=ON`, `Add new posts at beginning=ON`, sitten **Save**.
2. Autolist: nimi `RKK | Seurauutiset | Facebook`; kanavaksi vain Facebook; **Repeat=OFF**; käytä sopivaa julkaisuikkunaa, käyttäjän kuvassa oleva klo 23.10 ei ole oletusarvoisesti paras. Tallennus koko autolistille erikseen.
3. Vahvista seuraavan uutisen saapuminen pois päältä olevaksi jonokohteeksi. **Disabled ei ole tekninen monihenkilöinen hyväksyntäjärjestelmä**; ennen aktivointia tarkista uutisen otsikko, kuva, päivämäärä, kilpailutulos, kohderyhmä ja oikea Facebook-kanava.
4. Instagramille julkaistaan luvallista kuvaa tai videota, YouTubeen vain hyväksyttyä oikeaa videota (esim. Shorts). RSS-linkin ja logon kopioiminen YouTubeen ei ole videosisältöä.
5. TikTok siirretään myöhempään vaiheeseen.

## 59 sivun uudistus – konservatiivinen käyttöönottopolku

### A. Ennen ensimmäistäkään sivun korvaamista

- Inventoi tarkat URL:t ja sisällöt sivukohtaisesti; kirjaa alkuperäisen näkyvä teksti, luettelot/taulukot, lähdelinkit, videolinkit, kuvat ja alt-tekstit. Merkitse historiallinen aineisto **säilytettäväksi muuttumattomana**; korjaa vain selvät kirjoitusvirheet ja varmennettu ajantasainen tieto.
- Yhdistysavaimen **Sivuston arkistointi** antaa kuvien ja tiedostojen ZIP:n, *ei luotettavaa koko sivutekstien varmuuskopiota*. Ota lisäksi yksityinen täydellinen sivukohtainen sisältötalteenotto (HTML/teksti/PDF tarpeen mukaan), sekä säilytä lähteiden sivu-URL:t. Älä tallenna yksityistä tai käyttöoikeudellisesti epäselvää aineistoa julkiseen GitHubiin.
- Yhdistysavaimen **Sivun asetukset > Historia** on määräaikainen: Start 7 vrk, Plus 6 kk, Premium 18 kk, Free ei käytössä. Versiohistoria ei ole pysyvä pitkäaikaisarkisto.
- Tarkista sivuraja ja käytössä oleva versio; **piilottaminen ei ole sama kuin poistaminen, eikä ole vahvistettu että piilotettu sivu vapauttaisi tilausrajan sivupaikan**.

### B. Pilotointi ja julkaisusääntö

- Valitse pilottisivuksi **Harjoittelu** tai **Seura**. Yhdistysavaimessa `Sivuston rakenne > [sivu] > ratas > Kopioi sivu` luo julkaisemattoman rinnakkaiskopion, **jos tilin sivuraja sallii**. Kopioi yksi sivu kerrallaan: alisivuja ei siirretä automaattisesti.
- Tee uusi versio yhteisellä CSS:llä (`docs/rkk-premium-site.css`), käytä `embed/YHDISTYSAVAIN_HARJOITTELU_PREMIUM.html` tai `embed/YHDISTYSAVAIN_SEURA_PREMIUM.html` vain asianomaisella sivulla ja välttäen päällekkäisen tekstin.
- Vertaa alkuperäiseen, hyväksytä sisältö ja testaa puhelimella. Suosi uuden hyväksytyn HTML-rakenteen käyttöönottoa **vanhalla URL-osoitteella**, jotta linkit, hakukoneet ja seuran historian saavutettavuus säilyvät.
- Jos erillinen uusi URL on perusteltu, merkitse siirto, lisää toimiva sisäinen linkitys ja tarvittaessa Yhdistysavaimen uudelleenohjaus. **Älä muuta alkuperäistä historian sivua ei-julkaistuksi vain sivurajan kiertämiseksi.** `Julkaistu (ei valikossa)` pitää sivun käytettävissä suoralla URL:lla, mutta se ei ole korvike näkyvälle historia-arkistolle.
- Jos sivuraja ei salli rinnakkaiskopiota, valmistele rakenne ja HTML GitHubissa, ota varmuuskopio alkuperäisestä ja vaihda sisältö vasta tarkistuksen jälkeen **nykyiseen sivuun**. Älä poista sivua vapauttaaksesi tilaa.

### C. Sivuryhmien toteutusjärjestys

1. Etusivu: tarkista CSS-erotin, mobiilikorkeudet, mahdollinen vanha virheellinen väite tulosten automaatiosta, ei turhaa HTML-kopiointia.
2. Harjoittelu (10): yhteiset ryhmäkortit, henkilökohtaiset ryhmäsivut, 3 hinta-/lisenssisivua, 3 aikataulusivua. **Ajan- ja hinnantarkistus valmentajilta ensin**; vanha 2018-lisenssikuvaus ei ole ajantasaisuuden todiste.
3. Seura ja historia (11) sekä Tuloksia-arkisto (19): uusi navikortisto, ajanjanallinen, helppolukuinen arkisto, alkuperäinen sisältö ja vuosien 2002–2019 jokainen tulos säilyvät; pitkä historiikki ei saa lyhentyä otsikkokortiksi.
4. Kilpailijat (6): luettelo + 5 profiilia, alkuperäiset saavutukset ja videot säilyvät; BoxerBase-ottelumääriä ei väitetä koko uraksi; valmentajan hyväksymä ajantasainen tieto.
5. Liity mukaan (1): uusi johdanto, **säilytä Yhdistysavaimen natiivi jäsenlomake**, testaa.
6. Yhteystiedot (1): korjaa `Rihimäki` > `Riihimäki` osoitteen varmistuksen jälkeen; vahvista vastuuhenkilöt ja jäsenasioiden viestikanava.
7. Uutiset (10): yksi visuaalinen tyyli uutisarkistossa; historia pysyy, vanhoja tapahtumia ei levitetä uutena sosiaaliseen mediaan.

### D. Hyväksymisehdot ja dokumentointi

- Jokaisella 59 sivulla on status: `INVENTOITU -> TALTIOITU -> UUDISTETTU_LUONNOS -> HYVAKSYTTY -> JULKAISTU -> TESTATTU`. Dokumentoi ennen/jälkeen-kuvakaappaukset, vanhan ja uuden URL:n suhde, sisällön säilymisen tarkistus ja mahdollinen palautus.
- CSS:n muutokset GitHubiin sovittuna erillisenä commitina; sisältöjen muutoksista URL-kohtainen muutosloki. Käytä nykyistä PR/issue-työnkulkua, ei historian uudelleenkirjoitusta.
- Ei väitettä 59 sivun valmistumisesta ennen kuin 59 on tarkistettu, näkyvät tarvittavat sisällöt säilyvät ja mobiili/desktop sekä liittymislomake toimivat.
- Olemassa olevat koodit ja muutokset: `docs/PREMIUM_SIVUSTO_ASENNUS_2026-10-26.md`, `docs/SIVUSTON_KOKONAISAUDITTI_2026-10-26.md`, `docs/SIVUSTON_AUTOMAATTINEN_AUDITTI.md`, `embed/`-kansion 4 HTML-pohjaa.

## Todennuslähteitä

- https://ohjeet.yhdistysavain.fi/kotisivut/sivut/sivun-asetukset/ (kopio, julkaisematon, julkaistu-ei-valikossa)
- https://ohjeet.yhdistysavain.fi/kotisivut/sivut/sivun-asetukset/historia/ (versioiden säilytys)
- https://ohjeet.yhdistysavain.fi/kotisivut/arkistointi/ (arkisto-ZIP:n rajaus)
- https://ohjeet.yhdistysavain.fi/kotisivut/sivun-uudelleenohjaus/
- https://help.metricool.com/how-to-link-an-rss-feed-to-an-autolist-ank6m

## Metricoolin todettu jatkotilanne – 26.10.2026 klo noin 01.01 Suomen aikaa (käyttäjän kuvakaappaukset)

- RSS-linkitys ja koko autolista on **tallennettu onnistuneesti**. Autolistien luettelossa on `RKK | Seurauutiset | Facebook`, kanavana Facebook, kytkin **Enabled: Yes**, sisältöä **0 postausta**, ja Next time -kenttä on tyhjä.
- RSS-esikatselussa oli 3 aiempaa uutista. Asetukset kuvassa: `Max characters: 250`, `Prefix` ja `Suffix` tyhjinä, `Add 3 previous posts: OFF`, `Include new post disabled: ON`, `Add new posts at the beginning: OFF`; itse autolistan `Repeat: OFF`. Tyhjää jonoa **ei tulkita viaksi**, koska aiempien uutisten tuonti on estetty. `Add new posts at the beginning` on valinnainen järjestyskysymys; OFF lisää uudet jonon loppuun, ei estä RSS:ää.
- Ajastusnäkymässä aika oli **11:10 PM (23.10)** ja viikonpäivistä ei näkynyt valittua päivää. **Varmista viikonpäivien valinta** ja siirrä ajankohta ehdotuksena tiistaille ja torstaille klo **18.00 Europe/Helsinki**. Tämä on kokeiltava lähtöaika, ei todistetusti paras. `Next time` voi olla tyhjä myös siksi, ettei jonossa ole aktiivisia postauksia; pelkästä tästä ei saa päätellä ajastusvikaa.
- RSS-toiminto vastaanottaa vain **uudet, tämän liittämisen jälkeen ilmestyvät** artikkelit. Ne saapuvat **disabled**-tilassa ja vaativat käsin aktivoinnin ennen julkaisemista (Metricoolin dokumentaatio). Ensimmäistä uutta artikkelia käytetään testinä, ei julkaista tahattomasti vanhoja artikkeleita.
- **Käyttäjä vahvisti nimenomaisesti 26.10.2026, että Metricoolin YouTube-kanava on oikea Kehä-Kettujen kanava.** Vanhojen dokumenttien epäily yhteyden oikeellisuudesta on tältä osin vanhentunut; julkaisujen tekninen toimivuus ja kanavakohtaiset formaatit tarkistetaan erikseen. Ei uuden kanavan perustamista. TikTok myöhemmin.
- Facebook-linkkiesikatselu kuvassa näytti seuran logon. Metricoolin RSS-ohjeen mukaan Facebook luo linkkiesikatselun julkaisuhetkellä ja käyttää artikkelin `og:image`-tietoa, jos sellainen on. Tulevaisuudessa harkitse uutiskohtaisia luvallisia kuvia ja omaa OG-kuvaa, jotta jokainen uutinen ei ole pelkkä seuralogo. Ei automaattista kuva-/videojulkaisua ilman ihmisen hyväksyntää.

Lähde: https://help.metricool.com/how-to-link-an-rss-feed-to-an-autolist-ank6m ; https://help.metricool.com/schedule-content-from-an-autolist-fxehk .
