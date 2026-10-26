# RKK — itsenäinen videotuotanto ja julkaisu ilman ChatGPT-keskustelun käsityötä

**26.10.2026 | Tilanne- ja arkkitehtuuripäätös (suunnitelma, ei käyttöönottoilmoitus).** Tämä dokumentti perustuu julkisen `glesima/kehaketut-feed`-repositorion tosiasialliseen sisältöön sekä Dropboxin ja Metricoolin olemassa oleviin RKK-yhteyksiin.

## Tiivistelmä

**Tänään jatkuvasti automaattista:** julkisen verkkosivun GitHub Actions -ajot (BoxerBase, uutiset, auditointi) sekä Dropbox File Request **vastaanotto**, jossa tallentaminen toimii ilman ChatGPT:tä.

**Tänään EI täysin automaattista:** uuden `/RKK/Uudet_videot`-MP4:n havaitseminen ja yhdistäminen luotettuun tapahtuma/ottelutunnisteeseen; monta MP4:tä yhdeksi koostavien Python-ohjelmien käynnistys; median vienti Metricooliin; ajoitetun julkaisun vahvistus/korjaus kolmessa kanavassa. Nämä on viime kierroksilla ajettu käsin ChatGPT-työkaluilla tai yksityisessä testiympäristössä. ChatGPT ei nyt toimi RKK:n taustapalvelimena eikä suljetun keskustelun ulkopuolella jatku automaattista kuvankäsittelyä.

**Tuleva tavoite:** `Dropbox file request -> yksityinen 24/7 käsittelijä -> luotettu ottelu-/oikeusrekisteri -> laadukas event-kooste -> 3 julkaisua -> URL-varmennus + ilmoitus vain virheistä`. Käyttäjän ensisijainen tavoite on **ei hyväksyntäklikkausta per video** ennakkovaltuutetulle standardimateriaalille. Poikkeuksia ei päästetä automaattisesti ulos.

## Nykyisen GitHub-repositorion tosiasiat

- `.github/workflows/update.yml` hoitaa sivuston aineistopäivitykset, `site-audit.yml` auditoinnin ja `pr-validation.yml` kooditestit. **Mitään jatkuvaa mediankäsittely-/julkaisutyönkulkua ei näissä ole.**
- `scripts/media/filming_intake.py`: *vain käyttäjän erikseen käynnistämä* yksityisen paikallisen kansion MP4-inventaario (koko, kesto, ääni, SHA-256, jo julkaistun boutin varoitukset). Ei Dropbox-authia tai daemonia.
- `scripts/media/suggest_clips.py`: offline-liikeanalyysin ehdokaslistaus; ei nyrkkeilysuorituksen tarkkaa merkityksen ymmärtämistä.
- `scripts/media/build_reel.py` ja `broadcast_style.py`: yhden videon editointi ja vakio-TV-tyyli.
- `scripts/media/event_recap.py`: 1–12 lähde-MP4:n yhdistäminen, varovainen auto-publish-eligibility ja kolmen kanavan JSON-outbox, **mutta ei verkon kautta tapahtuvaa julkaisua**. Vaatii itsenäiset, luotetut oikeudet/ottelutulokset/deduplikointilokin. `auto_publish_ready` ei yksin lähetä mitään.
- Dropbox `/RKK/Uudet_videot`, File Request `https://www.dropbox.com/request/vjppmba9qlotgd9arodn` on käytössä. Dropbox tallentaa vastaanotetut tiedostot, mutta tällä hetkellä ei laukaise mediaohjelmaa eikä sisällä itsenäisesti riittäviä ottelufaktoja.

## Suositeltu vaiheittainen arkkitehtuuri

### Vaihe A — ChatGPT pois videon käsittelyketjusta (ensisijainen)

- **Oma yksityinen käsittelykone:** valitaan käyttäjän aina päällä oleva Linux/Kubuntu-kone, jos se todella voi pysyä päällä ja Dropbox-synkronointi on luotettava. Vaihtoehto 24/7 pilvi-VPS/worker jos kone ei ole jatkuvasti käytettävissä. Älä rakenna jatkuvaa kriittistä ajoa kannettavalle, joka nukkuu.
- Oma scoped Dropbox OAuth -yhteys, `/files/list_folder` cursor + `/longpoll` (tai serverillä Dropbox webhook), synkkaa vain `/RKK/Uudet_videot`, ei koko henkilökohtaista Dropboxia. Käsittelijä käyttää pysyvää `systemd`-palvelua + uudelleenkäynnistystä + lokeja.
- Odota täysin valmistunutta latausta: stable size, Dropbox-revisio, ffprobe-ehjyyttä; tiedosto ja SHA-256 -> idempotentti tietokantajono (SQLite aluksi).
- Luo ja validoi `event_id + bout_id` **luotetusta tiedosta** (ei arvaamalla videon henkilöiden identiteettiä eikä tulkitsemalla tiedoston päivämäärää varmaksi otteluksi). Helppo tuleva lataussivu voi näyttää ottelijan nimen ja kilpailun valintoina; tarvittaessa kuvaajan tekstitieto menee HOLD-tilaan.
- Julkaisuluvat/alaikäisten oikeudet ovat yksityisessä varmennetussa rekisterissä, eivät avointen lähettäjien ilmoittamalla `approved`-kentällä. Näitä voidaan tarkistaa jo ennen videon saapumista.
- **Tapahtumapuskuri**: odota sovittuun määräaikaan tai ilmoitukseen `kaikki ottelut toimitettu`, muuten ensimmäisen tiedoston vastaanotto saattaisi julkaista koosteen ennen muita tiedostoja.
- Laatuvalinta: 1–3 tasapuolista katkelmaa per eri ottelu, kohtaus- ja liikelaadun pisteytys; jos laatu huono, videoiden rajaus puutteellinen, tai faktat ristiriidassa, HOLD. Älä merkitse pelkkää liikepistettä oikeaksi osumaksi.
- FFmpeg & Pillow tekevät 9:16 1080×1920 MP4:n, RKK-logo, nimet, vahvistetut tulokset, kansikuva ja tekstit; tarvittaessa paikallinen kielimalli tai erillinen API luonnollisempaan copyyn. ChatGPT Pro -tilaus **ei sellaisenaan aja** tätä jatkuvaa ohjelmaa eikä ole sama kuin mahdollinen erikseen laskutettava API.
- Pysyvä ledger `(event_id, content_version/hash, network)` ja tilakone: `RECEIVED -> VERIFIED -> WAIT_EVENT_COMPLETE -> EDITING -> QA -> READY -> SUBMITTING -> PUBLISHED_VERIFIED` tai `HOLD`/ `FAILED`.

### Vaihe B — julkaisemisen ensimmäinen halpa vaihtoehto: Make + Metricool MCP (testattava)

- Metricoolin **MCP toimii myös Free-tilillä** ja sen virallinen osoite on `https://ai.metricool.com/mcp`. Metricool itse dokumentoi **Make.com:n MCP OAuth -kytkennän**, jossa Make-skenaario kutsuu Metricoolin Planner-työkaluja.
- Tämä **ei ole sama asia** kuin maksullinen Metricool REST API: suora REST-API vaatii Advanced tai Custom.
- Ensimmäinen tekninen koe: prosessori tallentaa **hyväksytyn lopullisen MP4:n** ja `publication_handoff.json`-paketin erilliseen, luotettuun ready-kansioon / lyhytaikaiseen turvalliseen mediaosoitteeseen. Make havaitsee uuden valmiin paketin, käyttää OAuth-autentikoitua Metricool-MCP:tä ja luo FB Reel, IG Reel (`autoPublish=true`, `showReelOnFeed=true`) ja YT Short (`type=short`, `madeForKids` tiedon mukaisesti) **vain oikeaan RKK-brand-id:hen 7632678**.
- **Avoin kokeen ehto:** Make:n MCP/OAuth-yhteyden pysyvyys ilman ihmiskirjautumista, MP4:n sallittu suora media-URL/Dropbox-integraatio, mediatyypit, mahdolliset Make-kiintiöt/kulut sekä yhteyden täydet julkaisuoikeudet. Mikään näistä ei ole vielä tuotantotestattu; pelkkä linkin ja OAuthin olemassaolo ei todista 24/7-toimintaa. Samalle MP4:lle voi tarvittaessa avata rajatun, nopeasti vanhenevan **lopullisen julkaisumasterin** media-URL:n, ei koskaan raakavideon pysyvää julkista linkkiä.
- Free-kiintiö on **20 ajastettua/julkaistua postausta kuukaudessa** Metricoolin kuvauksen mukaisesti; yksi video kolmessa verkossa lasketaan kolmena julkaisuna. Kuluja seurataan; Make-skenaario ei välttämättä ole ilmainen suurilla käyttömäärillä.
- Testaa ensimmäiseksi yhden oman luvallisen *uuden* videon kolmen kanavan private/draft- tai rajatulla testijulkaisulla, joka ei toista jo julkaistua kilpailua. Älä automatisoi julkista linkkiä ilman kolmen kanavan näkyvyysvarmistusta.

### Vaihe C — vaihtoehto Metricool Advanced tai suorat some-alustojen API:t

- **Option 1:** Metricool Advanced/Custom antaa REST-API:n, jota oma Linux-palvelin/n8n/Make voi käyttää jatkuvaan automatisointiin. Lisäkuukausimaksu, ei osteta ennen tarpeen todentamista.
- **Option 2:** Facebook Page Reels sekä Instagram Business/Creator Reels Meta Graph API:lla ja YouTube Shorts YouTube Data API:lla; ei Metricool REST -tilausta. Kehittäminen ja OAuth-/App Review-/oikeusprosessit suurempia. IG:n Reel julkaistaan video-container + status + `media_publish`, Meta tarvitsee toimivan URL:n mediasta tai tuetun upload-reitin. YouTube-upload vaatii OAuthin ja mahdolliset projektin tarkistukset; syksyn 2026 YouTube-uploadin kiintiöjärjestelmä on muuttunut (älä käytä vanhaa 1600-kiintiöoletusta).
- Nämä ovat mahdollisia, eivät käyttöönotettuja. Ensin tee Make+MCP kokeilu, jotta nähdään tarvitseeko mitään maksullista ratkaisua.

### Vaihe D — julkaisun monitorointi ja poikkeuspolku

- Metricoolin `PUBLISHED/SENT` ei riitä varmistukseen: lokakuun 26.10. Instagramissa `autoPublish=OFF` teki vain puhelinilmoituksen eikä julkaissut Reel-videoita. Toteuta `publicUrl` + kanavasivun oikea näkyvyys tai alustakohtainen API-luku ennen `PUBLISHED_VERIFIED`-tilaa.
- Jos FB onnistuu, IG epäonnistuu ja YT onnistuu, **uusinta vain Instagramiin**; ei duplikaattia muihin.
- Vain ehdottomasti oikein varmennetuille, ennalta hyväksytyille lähteille *nollakosketus*; muu `HOLD` ja lyhyt ilmoitus mediavastaavalle. Ihmistarkistus varataan **poikkeuksille**, ei joka videolle.

## Käyttöönottojärjestys ilman arvausta

**P1.** Ota käyttäjän Linux-koneelle erillinen yksityinen `rkk-media-worker`-ympäristö ja testaa kerran uudella Dropbox-testitiedostolla: linkki -> synkronointi -> raportti ilman ChatGPT:tä.

**P2.** Lisää luotettu metadata + oikeusrekisteri + tapahtuman valmistumismerkki ja tee yksi virheetön automaattinen esikatselu oikeasta, ennestään julkaisemattomasta aineistosta.

**P3.** Toteuta Make-skenaario + Metricool MCP OAuth ja osoita oikealla luvallisella testillä, että media, tekstit, kanavat ja julkaisuvahvistus toimivat; tarkista kulut.

**P4.** Kytke automaattinen julkaisu vain vihreän polun aineistolle. Ensimmäisten useiden julkaisujen yhteydessä pidä aluksi myös varmistusilmoitus ja lokitus.

**P5.** Mittaa 24h/7vrk laatua, virheitä ja editoinnin käsityöaikaa. Paranna nyrkkeilyn semanttista kohtausvalintaa ennen kuin lähetät julkisesti epäedustavia poimintoja.

### Konkreettinen valmis/vielä puuttuu -määrittely

**Done:** Dropbox File Request vastaanotto, verkkosivun GH Actions, neljä paikallisesti ajettavaa media-analyysi/renderöintiohjelmaa, kaksi julkaistua pilottisisältöä kaikissa 3 kanavassa.

**Not done:** jatkuva Dropbox-listener, luotetun metadata-/oikeusrekisterin palvelin, tapahtumajono, full render -orkestrointi, automaattinen valmis-MP4:n mediahosting ja Metricool/Meta/YouTube julkaisusilta, verifiointi + retry + ilmoitukset.

## Lähdeviitteet

- Dropbox Developer API / detect changes: https://docs.dropboxapi.com/dropbox-api/docs/detecting-changes
- Dropbox webhook: https://docs.dropboxapi.com/dropbox-api/docs/webhooks
- Metricool MCP OAuth connection incl. Make: https://help.metricool.com/how-to-connect-metricools-mcp-eqp9h
- Metricool API vs MCP plan eligibility: https://help.metricool.com/plans-add-ons-and-api-access-explained-xux1u
- Metricool media URL restrictions: https://help.metricool.com/how-to-schedule-a-post-at-different-times-on-each-network-using-metricools-mcp-8tmhd
- Meta Instagram Official API collection (Meta): https://www.postman.com/meta/instagram/documentation/6yqw8pt/instagram-api
- Meta Facebook Reels Official API collection (Meta): https://www.postman.com/meta/facebook/documentation/r56bjfd/facebook-api
- YouTube Data API uploads: https://developers.google.com/youtube/data/reference/rest/v3/videos/insert
- GitHub Actions scheduled workflow caveats: https://docs.github.com/en/actions/how-tos/troubleshoot-workflows
- RKK current task: https://github.com/glesima/kehaketut-feed/issues/19
