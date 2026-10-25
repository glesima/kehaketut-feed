# Kehä-Ketut – erillinen turvallinen sisältökanava (suunnitelma 25.10.2026)

## Pääperiaate: vastaanotto ei koskaan tarkoita julkaisua

**ÄLÄ käytä yhdistyksen virallista seurasähköpostia** sisältöautomaation saapuvana laatikkona. Siellä voi olla henkilökohtaisia, hallinnollisia ja luottamuksellisia viestejä. Käytetään vain uutta, tarkoitukseen luotua postilaatikkoa. Osoitetta ei ole vielä luotu eikä yhdistetty; tätä dokumenttia ei pidä tulkita toimivaksi automaatioksi.

### Vaihe 1 – vastaanotto

Hallituksen jäsen / valmentaja lähettää uuteen osoitteeseen viestin ja halutut liitteet, esimerkiksi:
- `[UUTINEN] Harjoitusryhmän kuulumiset`
- `[KILPAILU] Ilmoittautumiset`
- `[KUVA] Harjoitusten kuvat`
- `[VIDEO] Ottelun raakavideo`

Isot MP4-videot ohjataan mieluummin yksityiseen seuran hyväksymään Dropbox/Google Drive -vastaanottoon; ei julkiseen GitHub-repositorioon eikä pitkäaikaisiin avoimiin postiliitteisiin.

### Vaihe 2 – luonnos

Viestistä luodaan uusi ID, tila `DRAFT_PENDING_REVIEW`, ja sille:
- otsikko sekä lyhyt, asiallinen suomenkielinen uutinen,
- alkuperäiset tiedot ja lähteet,
- kuvat ja käyttöoikeusvahvistus (jos mukana kuvia),
- sosiaalisen median ehdotukset,
- kysymys epäselvistä nimi-/päivämäärätiedoista.

Vastaus lähetetään vain oikealle lähettäjälle. Palaute voi sisältää linkin luonnoksen hyväksyntänäkymään; älä käytä pelkkää sähköpostin otsikossa olevaa vapaasti kopioitavaa hyväksyntäavainsanaa.

### Vaihe 3 – hyväksyntä

Julkaisu edellyttää todettua, seuran valtuuttaman hyväksyjän tunnistetta, nimenomaista hyväksyntää ja oikeita kuvalupia. Tilat:
`RECEIVED -> DRAFT_PENDING_REVIEW -> NEEDS_CHANGES -> APPROVED -> QUEUED -> PUBLISHED`.
Kaikille julkaisuversioille kirjataan ID, sisältötiiviste, hyväksyjä, aikaleima, lähde ja kohdekanavat. Jos luonnosta muutetaan hyväksynnän jälkeen, hyväksyntä raukeaa ja se pitää hyväksyä uudelleen.

### Vaihe 4 – julkaisu

1. **Yhdistysavain:** nykyinen natiivi Uutiset → Lisää uutinen ei tarjoa varmistettua sähköpostin kautta toimivaa kirjoitus-API:a. Ensimmäinen julkaisutapa = hyväksytty luonnos kopioidaan Yhdistysavaimeen. Tämän jälkeen nykyinen GH-uutiskorttiautomaatio nostaa uutisen etusivulle.
2. **Myöhempi täysin automaattinen etusivu:** GitHub Pagesin erillinen hyväksyttyjen uutisten tietovarasto ja HTML-lista, jota näytetään Yhdistysavaimen sisällä. **Se ei itsessään lisää uutisia Yhdistysavaimen omaan uutisarkistoon**. Hallituksen on hyväksyttävä, että julkisen uutisarkiston pääasiallinen järjestelmä vaihtuu.
3. **Facebook/Instagram:** hyväksytty luonnos valmistellaan vain Metricoolin Riihimäen Kehä-Ketut -brändissä ID 7632678. Facebook ID 160875127258478 ja Instagram @kehaketut. Ei vahingossa henkilökohtaisia tai yrityksen tilejä.
4. **YouTube:** olemassa olevan oikean seurakanavan linkki ja ylläpitäjän käyttöoikeudet on varmistettava. Youtuben videoita ei julkaista ilman kanavan tarkistusta.

### Turva ja toiminnallinen rajaus

- Ei salaisuuksia, kirjautumistietoja, raakavideoita tai jäsentietoja julkiseen GitHubiin.
- Kuka tahansa voi jättää ehdotuksen erilliseen sisältöpostilaatikkoon, mutta julkaiseminen ja hyväksyntä edellyttävät erikseen todennettua valtuutusta; ei automaattista käsittelyä virallisen seurasähköpostin muista viesteistä.
- Kuka tahansa voi ehdottaa tekstiä, mutta ei hyväksyä julkaisemista ilman erillisiä oikeuksia.
- Alaikäisten kuvien julkaisu vain seuran käytäntöjen ja vaadittujen lupien mukaisesti.
- AI ei saa keksiä kilpailuihin osallistujia, ottelupareja, voittoja, aikatauluja tai valmentajan lausuntoja.
- Ilmoittautuminen, vahvistettu ottelu ja ottelutulos käsitellään erillisinä tiloina.
- Julkaisun epäonnistuminen ei saa johtaa toiseen tai väärään tilille tehtyyn automaattiseen julkaisuun.

### Käyttöönottoon tarvitaan yksi henkilökohtainen käyttäjätoimi

Uuden erillisen sähköpostitilin luominen / yhteyden valtuuttaminen, nimetty hyväksyjä sekä tarvittaessa Dropboxin yksityisen lähetyskansion vahvistus. Näitä ei ole tehty.


## Tarkennettu toteutusmalli 25.10.2026

### Uuden postilaatikon nimi

**Ensisijainen ehdotus:** `kehaketut.sisalto@gmail.com` (saatavuus tarkistettava perustettaessa). **Varanimi:** `kehaketut.aineisto@gmail.com`. Jos seuran `kehaketut.fi`-domainin sähköpostit voi järjestää turvallisesti, oma osoite kuten `sisalto@kehaketut.fi` olisi myöhemmin luonteva, mutta senkin tulee käyttää **erillistä** vastaanottolaatikkoa. Yhdistyksen viralliseen postiin ei aseteta automaattista edelleensiirtoa.

### Roolit, reititys ja kolme hyväksyjää

| Rooli | Lähettää materiaalia | Saa luonnoksen | Saa hyväksyä |
| --- | --- | --- | --- |
| Ulkopuolinen | Kyllä | Vastaanottokuittaus (vain turvalliseksi todetuille viesteille) | Ei |
| Hallituksen jäsen ilman hyväksyntäoikeutta | Kyllä | Oma luonnos näkyvissä, myös hyväksyjäkolmikko saa tarkastuspyynnön | Ei |
| Gleb, Pepe tai Erika (kukin omalla valtuutetulla Google-tilillä) | Kyllä | Omalta lähetykseltä oma luonnos; ulkopuolisen aineistosta kaikki kolme | **Yksi kolmesta riittää** |

Henkilökohtaisia sähköpostiosoitteita ei ole vielä vahvistettu. Hyväksyntäroolia ei anneta automaattisesti hallituksen sähköpostidomainin tai pelkän From-osoitteen perusteella. Jos tunnettu lähettäjä ei reagoi, sovittu muistutus/escalointi muihin hyväksyjiin. Sisällön hyväksyminen tai hylkääminen tehdään palvelimella atomisesti; kaksi samanaikaista napsautusta ei saa aiheuttaa kahta julkaisua.

### Sähköpostihuijaukset ja vahva hyväksyntä

1. Gmailin `Authentication-Results`, SPF/DKIM/DMARC ja `From`-osoitteen yhdenmukaisuus auttavat erottamaan väärennetyt viestit. Viestit, joiden identiteetti ei täsmää, laitetaan karanteeniin, eikä niihin lähetetä automaattista vastausta. **Näillä ei koskaan myönnetä hyväksyntäoikeutta**.
2. Ehdotettu approval-frontend: yksityinen backend (esim. Google Cloud Run / Functions, Firebase Authentication ja Firestore/Cloud Storage tai vastaava), henkilökohtainen Google OIDC -kirjautuminen ja palvelimella sallittujen `sub`-tunnisteiden lista. `iss`, `aud`, `exp`, `email_verified` ja `sub` tarkistetaan, ei vain näkyvää sähköpostinimeä.
3. Hyväksyntään henkilökohtainen **WebAuthn/passkey** ja tarvittaessa uudelleentunnistus; vaihtoehtona yksilöllinen TOTP (Authenticator-sovellus, vaihtuva kertakoodi) varamenetelmänä. **Ei yhteistä pysyvää kuusinumeroista koodia eikä pelkkää vastausta "HYVÄKSY".** Passkey on tietojenkalastelua vastaan suojaavampi kuin käsin syötettävä OTP.
4. Sähköpostissa oleva linkki avaa vain tietyn luonnoksen. **Linkki yksin ei hyväksy tai julkaise**. Palvelin varmistaa hyväksyjän oikeuden, sisällön version ja hyväksyttävät kohdekanavat joka toiminnossa.
5. `draft_id` + `version` + `SHA-256 content digest` + `reviewer_sub` + `approved_at` + `approved_channels` tallennetaan audit-lokiin. Sisällön tai median muutos mitätöi aiemman hyväksynnän.
6. Vain kolme hyväksyjää voivat suorittaa `approve` / `reject` / `block` -toimintoja; CSRF/istunto-/kertakäyttöisyystarkistukset sekä rajattu kutsumäärä tarvitaan. Hylkääminen ja osoitteen estäminen eivät saa vaarantaa laillista lähettäjää pelkän spoofattavan osoitteen perusteella.
7. Haittaliitteet ja prompt injection käsitellään ei-luotettuna materiaalina: MIME + magic bytes -tarkistukset, malware scan, kokorajat, tyypillisten linkkihuijausten varoitukset, HTML-sanitointi, yksityinen alkuperäismedia ja alaikäisten kuvalupien merkinnät. Estetystä materiaalista säilytetään vain sovitun retention mukainen auditointi, ei julkista materiaalia.

### Hyväksyjäkohtaiset näkyvyydet

**Tunnettu hyväksyjä lähettää** -> luonnos palautuu hänelle -> hän kirjautuu omalla Google-tilillään/passkeyllä -> hyväksyy yhden nimenomaisen version -> vasta silloin julkaisu etenee.

**Tavallinen hallituksen jäsen lähettää** -> luonnos palautuu hänelle esikatseluna, mutta hyväksyntäpyyntö toimitetaan Glebille, Pepelle ja Erikalle.

**Ulkopuolinen lähettää** -> ilmoitus ja skannattu turvallinen luonnosesikatselu toimitetaan kolmelle hyväksyjälle; lähettäjä ei saa hyväksyntälinkkiä eikä henkilötietoja. Vain yhden kolmesta tarvitsee hyväksyä. Spam → hylkää, karanteeni ja tarpeen mukaan sovellustason esto.

### Julkaisemisen raja

Natiivin Yhdistysavain `Uutiset → Lisää uutinen`-rajapinnan kirjoitustukea ei ole todennettu: ensimmäinen versio tuottaa **hyväksytyn luonnoksen**, jonka ylläpitäjä kopioi Yhdistysavaimeen. Vaihtoehtoinen oma GH-syöte voisi näyttää hyväksytyn uutisen etusivulla automaattisesti, mutta se **ei automaattisesti lisää** uutista Yhdistysavaimen omaan Uutiset-arkistoon. Julkaisupolku valitaan ennen tuotantoon viemistä.

### Asennuksen päätökset odottavat

- Käyttäjä perustaa erillisen postilaatikon ja antaa sille tarvittavat Gmail-integraation oikeudet.
- Gleb, Pepe, Erika: vahvistetaan kunkin todellinen Google-tili ja otetaan passkey käyttöön.
- Valitaan yksityinen backend, medialähetykset ja varastointipaikka; kustannukset ja EU-tietosuojavaatimukset tarkistetaan.
- Näitä ei ole vielä perustettu eikä ensimmäistäkään hyväksyntää suoritettu.

Taustalähteet:
- https://support.google.com/mail/answer/81126 (Google SPF/DKIM/DMARC)
- https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ (NIST phishing-resistant authentication/WebAuthn)
