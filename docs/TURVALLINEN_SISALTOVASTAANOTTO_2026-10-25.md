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
- Vain nimetyt lähettäjät voivat jättää ehdotuksia julkaisuun; ei automaattista käsittelyä virallisen seurasähköpostin muista viesteistä.
- Kuka tahansa voi ehdottaa tekstiä, mutta ei hyväksyä julkaisemista ilman erillisiä oikeuksia.
- Alaikäisten kuvien julkaisu vain seuran käytäntöjen ja vaadittujen lupien mukaisesti.
- AI ei saa keksiä kilpailuihin osallistujia, ottelupareja, voittoja, aikatauluja tai valmentajan lausuntoja.
- Ilmoittautuminen, vahvistettu ottelu ja ottelutulos käsitellään erillisinä tiloina.
- Julkaisun epäonnistuminen ei saa johtaa toiseen tai väärään tilille tehtyyn automaattiseen julkaisuun.

### Käyttöönottoon tarvitaan yksi henkilökohtainen käyttäjätoimi

Uuden erillisen sähköpostitilin luominen / yhteyden valtuuttaminen, nimetty hyväksyjä sekä tarvittaessa Dropboxin yksityisen lähetyskansion vahvistus. Näitä ei ole tehty.
