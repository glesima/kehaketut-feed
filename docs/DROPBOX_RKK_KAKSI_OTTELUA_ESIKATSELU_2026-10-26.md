> **TARKENNUS 26.10.2026 – Instagramin puuttuneen julkaisun syy tunnistettu:** Käyttäjä vahvisti, että Instagram Reel -julkaisun **Auto publish oli OFF**. Metricoolin virallisen ohjeen mukaan tämä käynnistää manuaalisen julkaisun ilmoituksella; tila `Sent` tarkoittaa vain ilmoituksen lähettämistä, ei Instagramissa julkaistua videota. Käyttäjä ei tehnyt erillistä mobiilijulkaisua, joten Reeliä ei näy profiilissa. Aiempi `PUBLISHED`-merkintä Metricool-liitännässä ei tässä tapauksessa ollut luotettava todiste Instagramissa näkyvästä postauksesta. **Älä diagnosoi tätä Meta-poistoksi tai tee tukeen eskalointia oletuksena.**
>
> **Korjauspolku:** Metricool Calendar → alkuperäinen Instagram-postaus → **Duplicate** → jätä kanavaksi **vain Instagram** (FB ja YouTube julkaistu jo) → **Auto publish ON** → tuleva aika → ajoita/julkaise. Jos alkuperäinen notifikaatio on käytettävissä, vaihtoehto on suorittaa julkaisu puhelimella. Kun manuaalinen notifikaatio on jo lähetetty, Metricoolin ohjeen mukaan alkuperäistä postausta ei enää voi vaihtaa automaattiseksi: tarvitaan duplikaatti. Aina julkaisun jälkeen varmista oikea Instagram Reel -URL/näkyvyys ennen kuin kirjataan `PUBLIC_VERIFIED` tai yritetään retry. Tulevien automaatioiden on pakotettava IG Reel `autoPublish=true` ja tarkistettava erikseen alkuperäisen kanavan näkyvyys.
>
> Lähde: https://help.metricool.com/why-does-my-post-appear-as-sent-in-metricool-and-not-auto-published-467xf ja https://help.metricool.com/why-cant-i-enable-auto-publishing-66gg0 .

## Päivitys 26.10.2026 – videot tunnistettu käyttäjän vahvistuksella

Aiempi yllä kuvattu HOLD *videon ja ottelun vastaavuuden* osalta on nyt ratkaistu. **Älä enää pyydä käyttäjää nimeämään näitä kahta tiedostoa uudelleen.**

| Vahvistettu käyttäjän tiedosto | Seuran ottelija | BoxerBase | Kulma | Virallinen tulos |
|---|---|---|---|---|
| `VID-20261026-WA0004.mp4` (6:14) | **Simo Pöyry** | ottelu #16, miehet 85 kg | sininen | Lauri Mäenpää (punainen) voitti 3–2 |
| `VID-20261024-WA0006.mp4` (8:05) | **Kosmo Grönroos** | ottelu #33, B-juniorit 70 kg | punainen | Khaled Samkanai (sininen) voitti 5–0 |

Kilpailun virallinen otteluluettelo: https://www.boxerbase.com/e/d6jfSSe5nRpe/matches .

**Uusi nimetty esikatselu tuotettu:** 39,302 s H.264/AAC MP4 1080×1920, alkuperäinen RKK-logo, Simo ensin ja Kosmo toisena kilpailun kronologian mukaisesti, molemmista neljä todellista 4 sekunnin videoleikettä, ottelijat/vastustajat/luokat/oikeat tulokset ja yksityisen tarkistuksen merkinnät. MP4-dekoodaus onnistui ja käyttäjän yksityinen julkaisupaketti ZIP testattu. 3 valmista eri kanavien tekstiluonnosta. **Glebin jo julkaistua henkilökohtaista otteluvideota EI käytetty.** MP4/kuvat/lähteet eivät ole tässä julkisessa GitHub-repositoriossa.

**Muut jäljellä olevat estot:** kuvaajan ja kilpailunjärjestäjän julkaisuehdot sekä Kosmon juniorimateriaalin asianmukainen julkaisu-/huoltajalupa. Videon identiteettiä ei ole tunnistettu kasvoista; lähde on käyttäjän nimenomainen tiedostovastaavuus.

### Instagram-poikkeama erikseen

26.10. noin tunti ensimmäisen julkaisun jälkeen käyttäjän oma Instagram-profiilin kuvakaappaus osoitti vain yhden aiemman julkaisun, ei uutta Reeliä. Metricool-merkintä `Published` klo 12.30 (post ID `406452136`) jäi ilman `publicUrl`-arvoa, ja Reels-analytiikan haku oli vielä tyhjä. **Älä väitä tätä näytöllä näkyväksi onnistuneeksi Instagram-julkaisuksi äläkä tee uutta kopiojulkaisua ilman tarkistusta.** Metricoolin ohje: https://help.metricool.com/why-a-post-appears-as-published-but-is-not-visible-on-the-social-network-cnxh3 . Tarkista seuran Instagramin Reels, Arkisto/Äskettäin poistetut, tilin tila, sekä Metricoolin tuen saama Meta-vastaus. YouTube- ja Facebook-julkaisut löytyvät omista julkisista osoitteistaan.

# Kehä-Ketut / Dropboxin kaksi otteluvideota – 26.10.2026

## Päätös
Glebin henkilökohtainen ottelu on jo julkaistu kolmen kanavan kautta, eikä sitä tule toistaa seuraavassa kilpailupäivän koosteessa. Seuran tavoite on yksi kooste muista saman kilpailun otteluista, mahdollisimman automaattisella tuotanto-/julkaisupolulla.

## Dropboxin /RKK-kansio
- A: 8 min 5,5 s / 848×476 H.264, **ei ääniraitaa**.
- B: 6 min 14,4 s / 848×478 H.264 + AAC.
- Alkuperäisiä tiedostoja ei muutettu. Ei raakavideoita, julkisia latauslinkkejä eikä yksityisten tiedostojen tunnisteita GitHubiin.
- Kumpaakaan MP4:ää ei vielä varmasti liitetty juuri oikeaan ottelunumeroon, joten niitä ei ole nimetty eikä kuvien henkilöitä tunnistettu automaattisesti.

## Valmis erillinen yksityinen esikatselu
- 39,302 s, 1080×1920, H.264/AAC, koko videon dekoodaus läpi.
- Oikea Kehä-Kettujen kettulogo, tapahtuma Hämeenlinna 24.10.2026, kaksi nimetöntä otteluosiota sekä kahdeksan neljän sekunnin aitoa ottelukohtaa.
- Klipit valittu liikeheuristiikan ehdotusten pohjalta ja niiden erottamiskyky tarkistettu ruuduilta; ei väitetä tunnistetuiksi osumiksi tai paremmuudeksi.
- Yksi lähde ei sisällä ääntä, joten esikatselussa on hiljainen itse sävelletty rytmitausta; toisessa lähteessä mukana alkuperäinen kehä-ääni.
- ESITARKASTELU / EI JULKAISUUN -merkinnät näkyvät grafiikassa. Tuloksia ei ole valheellisesti sidottu tiedostoihin.
- Video ja alkuperäislogo vain ChatGPT-keskustelun yksityisinä tiedostoina.

## Viralliset kilpailutiedot (EI videoihin automaattisesti yhdistetty)
BoxerBase 24.10.2026: https://www.boxerbase.com/e/d6jfSSe5nRpe/matches
- Ottelu 16: Lauri Mäenpää (punainen), Simo Pöyry (sininen), Mäenpää voitti 3–2, miesten 85 kg.
- Ottelu 33: Kosmo Grönroos (punainen), Khaled Samkanai (sininen), Samkanai voitti 5–0, B-juniorit 70 kg.
- Glebin ottelu 19 jo erikseen julkaistu. Vanha rinnakkainen RKK-seuramerkintä on BoxerBasessa huomioitava.

## HOLD ennen julkista yhteisjulkaisua
1. Käyttäjän/kuvaajan tiedostokohtainen tieto siitä, kumpi /RKK-kansion video on Simon ja kumpi Kosmon ottelu (tai onko mukana muita).
2. Todennettava kuvauksen ja julkaisemisen lupa, mukaan lukien mahdollisen alaikäisen ottelijan huoltajan/edustajan suostumus ja soveltuvat kilpailujärjestäjän rajoitukset.
3. Kun ottelut voidaan vahvistaa, tuota nimet, sarja ja täsmällinen tulos omille otteluosiolle ja kolme kanavatekstiä.
4. Älä julkaise automaattisesti, jos vastaavuus/oikeudet/kanavan tila ovat epäselviä. Tulevan zero-touch-järjestelmän ennakkovaltuutettu vihreä polku voi silti toimia ilman klikkausta.

## Instagramin aiempi julkaisu
Metricoolin brändi 7632678 raportoi Glebin IG Reelin PUBLISHED klo 12.30. Ei julkista URL:ia liitännän vastauksessa, IG:n tämänpäiväinen analytiikkahaku tyhjä. Ei tehdä automaattisesti kaksoisjulkaisua: tarkista Instagram @kehaketut:n Reels-välilehti ja julkaisutiedot myöhemmin.

Tekninen toteutus ja tuleva automaatio: PR #18 sekä GitHub Issue #19.