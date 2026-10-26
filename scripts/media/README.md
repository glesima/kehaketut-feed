# Kehä-Ketut: raakavideosta tarkastettavaan Reels/Shorts-koosteeseen

Tämä yksittäisen videon testattu, toistettava **paikallinen pilotointityökalu** leikkaa ennakkoon ihmisen valitsemat jaksot ja luo samasta lähdemateriaalista videon, kansikuvan sekä renderöinnin metatiedot. Se käyttää aidosti seuran logoa ja tuttuja puna–valko–grafiitti-värejä.

## Rajaukset

- **Ei julkaise tai ajasta** mitään Facebookiin, Instagramiin, YouTubeen, Metricooliin eikä Yhdistysavaimeen.
- Ei tee teknisesti luotettavaa **automaattista osumien/otteluvoittojen tulkintaa**: tärkeät 4–8 klippiä hyväksyy valmentaja. `clips` ilmoitetaan JSON-manifestissa ja ne voivat olla eri pituisia.
- Ei generoi tekaistuja ottelutilanteita eikä muuta todellista lopputulosta.
- Säilyttää alkuperäisen raakavideon koskemattomana. Älä kopioi yksityisiä raakavideoita, hyväksymättömiä juniorikuvia tai käyttöoikeudellisia alkuperäislogoja julkiseen GitHubiin. Hae seuran hyväksytty logo omaan yksityiseen työtilaan.

## Vaaditaan

Python 3.10+, Pillow, ffmpeg ja ffprobe. Linuxissa asenna tarvittaessa `sudo apt install ffmpeg fonts-noto-core` ja `python3 -m pip install Pillow` virtuaaliympäristöön. Ilmaisilla paikallisilla työkaluilla ei synny uusia videopalvelujen tilausmaksuja.

## Ajo

```bash
python3 scripts/media/build_reel.py \
  --source "/polku/ottelu.mp4" \
  --logo "/polku/Keha-Ketut-logo-header-HD.png" \
  --manifest "scripts/media/example_manifest_hameenlinna_20261024.json" \
  --output-dir "/polku/yksityiseen/valmistuvat"
```

Varmista, että kyseisen videon ja sen julkaisemiseen tarvittavat oikeudet ovat kunnossa ennen käyttöä. Jos haluat ensin katsoa pelkän kansikuvan ja tarkistaa manifestin ilman MP4:n renderöintiä, lisää `--dry-run`.

## Manifestaation perustiedot

`date`, `place`, `red`, `blue`, `division`, `result` kirjoitetaan tarkistetusta lähteestä. `clips` sisältää `start`, `duration` (sekuntia) ja `crop_x` (vasemman reunan vaakarajaus pikseleinä alkuperäisestä). Mukana on yksi aiemman oikean otteluvideon 8 leikkeen referenssimanifesti: **ei ole automaattisesti pätevä muulle videotiedostolle**.

Renderöinnin jälkeen käytä näitä toimituksellisina luonnoksina:

- `*_draft.mp4` — pystyvideo, 1080 × 1920 H.264/AAC.
- `kansikuva.jpg` — pystykansikuva.
- `render_metadata.json` — klippien aikaleimat, syötteen tarkistetut faktat ja muistutus hyväksyntätilasta.
- `ffmpeg.log` — ongelmatilanteiden tekninen loki.
- `instagram_luonnos.txt`, `facebook_luonnos.txt`, `youtube_luonnos.txt`, `somejulkaisut_luonnos.md` — turvalliset luonnokset **vain manifestin annetuista faktoista**. Lopulliset ihmiselle kirjoitetut tekstit voivat olla luontevammat.
- `private_segments/` — tekniset leikevälit ja välimontaasi, **sisältävät yksityistä kuvamateriaalia**. Säilytä vain yksityisessä kansiossa.

**Ennen Metricooliin viemistä**: tarkista että rajaus on hyvä myös mobiililla; näytetyt nimet, kisat ja tulokset pitävät paikkansa; kuvien ja äänien oikeudet ovat kunnossa; ja yksi valtuutettu henkilö hyväksyy lopullisen videon + kanavakohtaiset tekstiversiot. Musiikkia ei tässä lisätä. Facebookin erillinen RSS-autolista ei kuulu tähän videotyönkulkuun.

Tulevat vaiheet: yksityinen lähetyskansio, aikaleimoja ehdottava analyysimoduuli, hyväksyntäsivu, tekoälyn alustakohtaiset tekstit ja vasta sen jälkeen valvottu Metricool-ajastus.

## Tarkistetut testit 26.10.2026

Työkalun manifestin hyväksyntätestit 6/6 läpi sekä koko kuuden minuutin raakavideosta renderöity 32 s esimerkkikooste omassa yksityisessä testiympäristössä (myös MP4-dekoodaus tarkistettu). Työkalun renderöinti on kaksivaiheinen: ensin lähdemateriaalin aikaleimalliset leikkeet yksitellen nopeasti rajattuna, sitten valmis 9:16-kuva, tulos- ja logoelementit. Tämä vähentää pitkän videon moninkertaista dekoodausta.

Alkuperäinen henkilökohtainen video tai logo eivät ole tämän repositoryn mukana. Käytä niitä vain luvallisissa paikallisissa kansioissa.
## Shorts- ja Reels-käyttöliittymän peittämät alueet (26.10.2026)

Ensimmäisessä Hämeenlinna-videopilotissa huomattiin Metricoolin YouTube Shorts -esikatselussa, että **YouTuben oma videon otsikko sekä painikkeet peittävät videon alalaidan nimet ja muun grafiikan**. Tämä ei ole videon tekninen virhe eikä johdu YouTube-otsikkokentän täyttämisestä väärin. Videon omat tekstit ja alustojen päälle piirtämä käyttöliittymä tulee suunnitella erikseen.

Korjattu V4-videopohja:
- sijoittaa seuran oikean logon, kilpailun otsikon, molempien ottelijoiden nimet ja päivämäärän **yläosaan** ennen varsinaista ottelumateriaalia;
- näyttää todennetun ottelun tuloksen **vasta viimeisen seitsemän sekunnin aikana** kuvan yläreunalla, ei sosiaalisen median otsikon alla;
- jättää **alimmat noin 28 % koko pystykuvasta ilman tärkeää tekstiä**. Alustojen oma otsikko, nimi, seuraamispainikkeet ja kommentti-/tykkäystoiminnot saavat peittää tätä koristetaustaa;
- pitää viimeisten sekuntien lopputunnuksen keskialueella.

Koska Instagramin, Facebookin ja YouTuben päälle piirtämät käyttöliittymät vaihtuvat laitteen, sovellusversion ja katsojan mukaan, tämä parantaa näkyvyyttä muttei takaa, etteikö jokin reunakohdan koriste peittyisi. Testaa esikatselu eri kanavissa myös puhelimella.

**YouTube-asetuksista** vain otsikko ja `Made for kids / not made for kids` -luokitus ovat tämän työnkulun varsinaisia pakollisia syötteitä; teksti-, tyyppi- ja näkyvyysasetukset arvioidaan tilanteen mukaan. Soittolista, tunnisteet ja Sports-kategoria eivät ole pakollisia. Testiin `Private` ja Metricoolissa `Save as draft`, **ei Schedule/Publish** ilman erillistä hyväksyntää. Tavallinen leikkaaminen/rajaukset/tekstigrafiikat eivät yksinään tarkoita YouTuben vaatimusten mukaista realistisesti AI:lla generoituja tai merkittävästi muokattuja tapahtumia.


## Automaattiset liikemäärän perusteella ehdotetut leikkeet (26.10.2026)

`scripts/media/suggest_clips.py` on **erillinen, paikallinen esivalintatyökalu**. Se käy raakavideon läpi käyttäen ffmpegillä tuotettuja pieniä harmaasävyruutuja, mittaa liikkeen määrää rajatulla kuva-alueella ja tekee toimituksellisen ehdokaslistan. Mitään ei ladata verkkoon eikä julkaista.

```bash
python3 scripts/media/suggest_clips.py \
  --source "/yksityinen/ottelu.mp4" \
  --output "/yksityinen/ehdotetut_leikkeet.json" \
  --count 10 --clip-seconds 4 --min-gap 12
```

- Ehdotukset ovat aikaleimoja ja numeerisia **aktiivisuuspisteitä**, eivät vahvistettuja lyöntejä tai voittoja. Samanlaisia pisteitä voi saada tuomarin liike, kameran heiluminen tai nopeat askeleet.
- Tulosteessa `crop_x` on tarkoituksella `null`: valmentaja/editori rajaa ottelijat ja tarkistaa kohdat ennen niiden siirtämistä `build_reel.py`-manifestiin.
- Ehdotusjärjestelmä **ei kirjoita valmista manifestia**, muuta hyväksyttyä videota eikä tee julkaisuja. Valmentaja hyväksyy sekä relevanttiuden että käyttöoikeudet.
- 26.10.2026 paikallinen koe yhdellä 6:06 minuuttia kestävällä aidolla ottelutallenteella: 10 neljän sekunnin ehdokasta muodostui; kahdeksan yksikkötestiä meni läpi. Kyse on kevyestä liikkeen mittauksesta **ei tekoälyn semanttisesta videoymmärryksestä**.
- Rajaus `--roi x,y,w,h` säädetään tarvittaessa, jos kehä sijaitsee eri osassa ruutua. Tuki enintään 60 minuutin videotiedostolle per ajo, jotta resurssit pysyvät rajattuina.

**Tuleva kehitys:** 1) leike-ehdotusten ihmisarvioinnin käyttöliittymä, 2) ottelijoiden seuranta rajausta varten, 3) hyväksyttävän julkaisupaketin automaattinen luonti ja 4) Metricoolin hyväksyttyyn julkaisuun siirto. Kunkin vaiheen testit ja ihmisen hyväksyntä ennen automaation laajentamista.


## Valinnainen TV-tyylinen visuaalinen pohja (`--style broadcast`)

Hämeenlinnan 24.10.2026 **V5 Broadcast Style** oli aiemmin erillinen kertaluontoinen vertailuvideo. Nyt samanlaisen laadukkaan visuaalisen pohjan voi tuottaa **muistakin omista luvallisista otteluvideoista** ilman käsin kovakoodattuja ottelijan nimiä ja ilman ulkoista videoeditointipalvelua:

```bash
python3 scripts/media/build_reel.py \
  --source "/yksityinen/ottelu.mp4" \
  --logo "/yksityinen/Keha-Ketut-logo-header-HD.png" \
  --manifest "/yksityinen/ottelun_hyvaksytyt_klipit.json" \
  --output-dir "/yksityinen/broadcast_kooste/" \
  --style broadcast
```

- **Oletus on edelleen `--style standard`**, joten vanha toimiva työnkulku ei muutu päivityksessä.
- Tyylipohja käyttää oikeaa seuramerkkiä, aitoa videon ruutua kevyesti sumennettuna taustana, tapahtuman paikkakuntaa ja päivää, molempien ottelijoiden nimiä, punaisen/sinisen kulman tunnusväriä, todennettu tulos -palkkia ja lopputunnusta.
- YouTuben/Instagramin käyttöliittymälle jätetään videon alaosaan turvallinen tila, eikä tärkeää tekstiä aseteta sinne.
- Lopputekstit ja kilpailutiedot otetaan **vain ihmisen tarkistamasta manifestista**; ennen julkaisua tarkistetaan myös, että ottelijoiden nimet mahtuvat grafiikkaan ja kuvan pystyrajaus toimii.
- Grafiikat eivät lisää tekoälyllä keksittyä ottelutilannetta, uutta musiikkia tai voittoa; alkuperäinen kehä-ääni säilyy.
- `--dry-run --style broadcast` luo grafiikat ja kannen ilman varsinaista MP4-renderöintiä.
- 26.10.2026: paikallinen 6 s MP4-koerenderöinti läpäisi teknisen dekoodauksen; graafisten assettien unit-testi testaa 1080×1920-koon sekä tulos- ja lopputunnuksen sijoittelun. Pitkien videoiden laatu riippuu edelleen lähdemateriaalista.

Tämä on **ulkoasutyyli**, ei lupa julkaista. Lopullisen videon sekä Facebook/Instagram/YouTube-julkaisujen hyväksyntä on yhä erillinen ihmisen tehtävä.
