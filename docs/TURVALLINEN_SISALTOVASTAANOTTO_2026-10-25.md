# Kehä-Ketut – erillinen turvallinen sisältökanava (suunnitelma 25.10.2026)

## Pääperiaate: vastaanotto ei koskaan tarkoita julkaisua

**ÄLÄ käytä yhdistyksen virallista seurasähköpostia** sisältöautomaation saapuvana laatikkona. Siellä voi olla henkilökohtaisia, hallinnollisia ja luottamuksellisia viestejä. Käytetään vain uutta, tarkoitukseen luotua postilaatikkoa. Sisältöosoite **kehaketut.aineisto@gmail.com** on luotu ja sen Gmail-yhteys on 25.10.2026 vahvistettu. Gmailiin on perustettu käsittelytunnisteet. Luonnoksen automaattinen teko, vahva hyväksyntä ja julkaisuputki eivät ole vielä käytössä.

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

Erillinen sisältö-Gmail ja sen yhteys on vahvistettu. Kolmen hyväksyjän yksilöllinen kirjautuminen sekä yksityinen backend ja tarvittaessa videokansion vahvistus ovat vielä tekemättä.


## Tarkennettu toteutusmalli 25.10.2026

### Uuden postilaatikon nimi

**Käyttöön otettu erillinen vastaanottoposti:** `kehaketut.aineisto@gmail.com`. Jos seuran `kehaketut.fi`-domainin sähköpostit voi järjestää turvallisesti, oma osoite kuten `sisalto@kehaketut.fi` olisi myöhemmin luonteva, mutta senkin tulee käyttää **erillistä** vastaanottolaatikkoa. Yhdistyksen viralliseen postiin ei aseteta automaattista edelleensiirtoa.

### Roolit, reititys ja kolme hyväksyjää

| Rooli | Lähettää materiaalia | Saa luonnoksen | Saa hyväksyä |
| --- | --- | --- | --- |
| Ulkopuolinen | Kyllä | Vastaanottokuittaus (vain turvalliseksi todetuille viesteille) | Ei |
| Hallituksen jäsen ilman hyväksyntäoikeutta | Kyllä | Oma luonnos näkyvissä, myös hyväksyjäkolmikko saa tarkastuspyynnön | Ei |
| Gleb, Pepe tai Erika (kukin erikseen todennetulla käyttäjätunnuksella / passkeyllä) | Kyllä | Omasta lähetyksestä lähettäjälle; ulkopuolisista ehdotuksista ilmoitus Glebille ja yhteiseen seurapostilaatikkoon | **Yksi kolmesta riittää** |

Pepe ja Erika käyttävät samaa seuran virallista postilaatikkoa `riihimaenkehaketut@gmail.com`; se soveltuu yhteiseksi ilmoitusosoitteeksi mutta ei erota hyväksyjien henkilöllisyyksiä. Hyväksyntäroolia ei anneta automaattisesti pelkän From-osoitteen tai yhteisen postilaatikon perusteella. Jos tunnettu lähettäjä ei reagoi, sovittu muistutus/escalointi muihin hyväksyjiin. Sisällön hyväksyminen tai hylkääminen tehdään palvelimella atomisesti; kaksi samanaikaista napsautusta ei saa aiheuttaa kahta julkaisua.

### Sähköpostihuijaukset ja vahva hyväksyntä

1. Gmailin `Authentication-Results`, SPF/DKIM/DMARC ja `From`-osoitteen yhdenmukaisuus auttavat erottamaan väärennetyt viestit. Viestit, joiden identiteetti ei täsmää, laitetaan karanteeniin, eikä niihin lähetetä automaattista vastausta. **Näillä ei koskaan myönnetä hyväksyntäoikeutta**.
2. Ehdotettu approval-frontend: yksityinen backend (esim. Google Cloud Run / Functions, Firebase Authentication ja Firestore/Cloud Storage tai vastaava), henkilökohtainen Google OIDC -kirjautuminen ja palvelimella sallittujen `sub`-tunnisteiden lista. `iss`, `aud`, `exp`, `email_verified` ja `sub` tarkistetaan, ei vain näkyvää sähköpostinimeä.
3. Hyväksyntään henkilökohtainen **WebAuthn/passkey** ja tarvittaessa uudelleentunnistus; vaihtoehtona yksilöllinen TOTP (Authenticator-sovellus, vaihtuva kertakoodi) varamenetelmänä. **Ei yhteistä pysyvää kuusinumeroista koodia eikä pelkkää vastausta "HYVÄKSY".** Passkey on tietojenkalastelua vastaan suojaavampi kuin käsin syötettävä OTP.
4. Sähköpostissa oleva linkki avaa vain tietyn luonnoksen. **Linkki yksin ei hyväksy tai julkaise**. Palvelin varmistaa hyväksyjän oikeuden, sisällön version ja hyväksyttävät kohdekanavat joka toiminnossa.
5. `draft_id` + `version` + `SHA-256 content digest` + `reviewer_sub` + `approved_at` + `approved_channels` tallennetaan audit-lokiin. Sisällön tai median muutos mitätöi aiemman hyväksynnän.
6. Vain kolme hyväksyjää voivat suorittaa `approve` / `reject` / `block` -toimintoja; CSRF/istunto-/kertakäyttöisyystarkistukset sekä rajattu kutsumäärä tarvitaan. Hylkääminen ja osoitteen estäminen eivät saa vaarantaa laillista lähettäjää pelkän spoofattavan osoitteen perusteella.
7. Haittaliitteet ja prompt injection käsitellään ei-luotettuna materiaalina: MIME + magic bytes -tarkistukset, malware scan, kokorajat, tyypillisten linkkihuijausten varoitukset, HTML-sanitointi, yksityinen alkuperäismedia ja alaikäisten kuvalupien merkinnät. Estetystä materiaalista säilytetään vain sovitun retention mukainen auditointi, ei julkista materiaalia.

### Hyväksyjäkohtaiset näkyvyydet

**Tunnettu hyväksyjä lähettää** -> luonnos palautuu lähetysosoitteeseen -> hyväksyminen tapahtuu omalla erillisellä tilillä/passkeyllä (ei yhteisen seurapostin tunnuksella) -> yksi nimenomainen luonnosversio etenee.

**Tavallinen hallituksen jäsen lähettää** -> luonnos palautuu hänelle esikatseluna, mutta hyväksyntäilmoitus lähtee Glebille ja seuran yhteiseen viralliseen postilaatikkoon, jota Pepe ja Erika seuraavat.

**Ulkopuolinen lähettää** -> turvallinen luonnosesikatselu ilmoitetaan Glebille ja yhteiseen seurapostilaatikkoon; lähettäjä ei saa hyväksyntälinkkiä eikä henkilökohtaisia tietoja. Vain yhden kolmesta tarvitsee hyväksyä. Spam → hylkää, karanteeni ja tarpeen mukaan sovellustason esto.

### Julkaisemisen raja

Natiivin Yhdistysavain `Uutiset → Lisää uutinen`-rajapinnan kirjoitustukea ei ole todennettu: ensimmäinen versio tuottaa **hyväksytyn luonnoksen**, jonka ylläpitäjä kopioi Yhdistysavaimeen. Vaihtoehtoinen oma GH-syöte voisi näyttää hyväksytyn uutisen etusivulla automaattisesti, mutta se **ei automaattisesti lisää** uutista Yhdistysavaimen omaan Uutiset-arkistoon. Julkaisupolku valitaan ennen tuotantoon viemistä.

### Asennuksen päätökset odottavat

- **Tehty:** kehaketut.aineisto@gmail.com luotu ja yhdistetty Gmail-integraatioon; kuusi käsittelytunnistetta luotu.
- **Kesken:** Glebille, Pepelle ja Erikalle rekisteröidään yksilölliset hyväksyjäidentiteetit joko henkilökohtaisilla Google-tileillä tai erillisinä käyttäjätunnuksina ja passkey-todentimina. Yhteisen seurapostin kirjautuminen ei yksilöi hyväksyjää.
- Valitaan yksityinen backend, medialähetykset ja varastointipaikka; kustannukset ja EU-tietosuojavaatimukset tarkistetaan.
- Julkaisun automaatiobackendiä tai varsinaista hyväksyntätoimintoa ei ole vielä otettu käyttöön; yhtäkään sisältöä ei ole julkaistu tämän prosessin kautta.

Taustalähteet:
- https://support.google.com/mail/answer/81126 (Google SPF/DKIM/DMARC)
- https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ (NIST phishing-resistant authentication/WebAuthn)

## Tarkennus: yhteinen seuraposti ja kaksi erillistä hyväksyjää (25.10.2026)

- **Aineiston sisääntulo**: `kehaketut.aineisto@gmail.com` (erillinen yhdistetty Gmail-tili).
- **Yhteinen ilmoitusosoite Pepelle ja Erikalle**: `riihimaenkehaketut@gmail.com` (verkkosivun julkinen seuraposti). Tästä laatikosta EI lueta kaikkia seuran viestejä sisältöautomaatiolle, eikä sen saapuvaa postia oteta syötteeksi.
- **Glebin ilmoitusosoite**: hänen oma todennettu Gmail-tilinsä. Ilmoituksia lähetetään tarvittaessa kahteen postilaatikkoon, mutta `approval_actor_id` on aina yksilöllinen Gleb/Pepe/Erika.
- Jos Pepe tai Erika lähettää materiaalia seuran yhteisestä laatikosta, luonnosvastauksen saa kyseinen yhteinen laatikko. Järjestelmä **ei** saa päätellä, kumpi lähetti sen; hyväksyjä kirjautuu erikseen omalla käyttäjätunnuksellaan.
- **Suositeltu toteutus**: pieni suojattu hyväksyntäsivu. Jokaiselle hyväksyjälle oma identiteetti. Yksinkertaisin on henkilökohtainen Google OAuth -tili + passkey/MFA. Jos Pepe tai Erika ei halua käyttää henkilökohtaista Google-osoitetta, voidaan tehdä erillinen sovelluksen käyttäjätunnus ja rekisteröidä yksilöllinen WebAuthn-passkey henkilökohtaiselle laitteelle. Pelkkä yhteisen Gmail-tilin OAuth-kirjautuminen ei riitä.
- Sähköpostin linkki avaa vain esikatselun. Palvelin vaatii kirjautuneen hyväksyjän, oikean roolin ja tarkalleen saman `draft_id + version + content_digest`-sisällön, ennen kuin hyväksyntä tallennetaan. Muutokset edellyttävät uutta hyväksyntää.
- Kolmen hyväksyjän oikeudet ovat samat, **yhden hyväksyntä riittää**, hylkääminen siirtää karanteeniin, estoa ei tehdä pelkän helposti väärennettävän `From`-osoitteen perusteella. Muut jo tehdyt hyväksynnät mitätöityvät jos julkaisun sisältö muuttuu.
- Luonnoksen palautus lähettäjälle on vain toimitus- ja tarkistusprosessi; sillä ei anneta julkaisuvaltuutta. Yksilöllinen audit-loki säilyttää tiedon siitä kuka hyväksyi ja milloin.
