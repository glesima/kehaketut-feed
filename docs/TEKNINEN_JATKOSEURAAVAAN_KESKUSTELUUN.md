# Seuraavan keskustelun tekninen jatko

Kilpailu-uutisoinnin täydennys: [uutispolitiikka](KILPAILU_UUTISOINTI_ILMAN_TURHAA_TOISTOA_2026-10-25.md) – kilpailukortti riittää tavallisista ilmoittautumisista ja tuloksista; vain merkittävistä kilpailuista erillinen hyväksyttävä ennakko/kooste, yksi per vaihe. Sovelluslogiikka scripts/editorial_news_triggers.py ja config/editorial_news_policy.json, ei vielä tausta-ajossa. 

Tilanne 25.10.2026: Kehä-Kettujen sivuston ulkoasu ja rajattu automaattinen BoxerBase-tietosyöte, 3 uutista, Juicer-instagram ja Metricoolin kautta päivittyvä Facebook-korttivirta ovat käytössä / otettu käyttöön. Nykyinen Github repo https://github.com/glesima/kehaketut-feed.

**Userin viimeisin prioriteetti:** kun uusi ottelu on käyty ja virallinen tulos julkaistu BoxerBasessa, tuloksen tulee ilmestyä automaattisesti etusivulle. Ei käsin seurattavien kilpailu-URLien lisäämistä, ei etusivun HTML-muokkausta joka ottelusta. Suunnitelma: [AUTOMAATTISET_OTTELUT_2026-10-25.md](AUTOMAATTISET_OTTELUT_2026-10-25.md).

Tämän jälkeen muut puutteet: BoxerBase-duplikaatit (Tomi), ottelijasivujen vanhat tekstiluvut, aktiivisten kilpailujen seuranta + dashboard, uutisnoston toiminta, FB- ja IG-osioiden yhtenäisyys, virhe-/vanhentuneisuusvalvonta, tuleva hyväksytty somejulkaisuluonnos. BoxRec poistettu pyynnöstä.

Ei toteuteta uusia GitHub Actions -tiheämpiä hakuja ilman BoxerBasen sallittavuuden tarkistusta ja havainnoitavaa tuloksen validointia. Säilytä viimeisin toimiva data virheissä, älä yhdistele saman nimisiä ottelijoita ilman ID-varmennusta. Uusia somejulkaisuja ei lähetetä itsenäisesti.
