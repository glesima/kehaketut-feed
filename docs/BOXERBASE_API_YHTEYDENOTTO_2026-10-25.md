# BoxerBase API / virallinen tietoyhteys – selvitys 25.10.2026

## Lähtötilanne
Riihimäen Kehä-Ketut ry:n oikea julkinen seuraprofiili: https://boxerbase.com/o/1Le8shnOwPIW/boxers . Rinnakkainen suuraakkosilla nimetty profiili: https://boxerbase.com/o/mZjkT0LW248X/boxers . Osalla urheilijoista on kaksoisprofiileja ja eri otteluhistoriat.

Hämeenlinnan 24.10.2026 kilpailussa oli 190 ilmoittautunutta, mutta kaikki eivät saaneet ottelua. BoxerBasen julkisen osallistujalistan HTML-esitys voi näyttää vain osan osallistujista. Ilmoittautuminen, vahvistettu ottelu ja julkaistu tulos ovat eri käsitteitä.

## Yhteydenotossa kysyttävää
- Tarjoaako BoxerBase seuralle luvallisen API:n, webhookin, syötteen tai dokumentoidun sivutetun lukuoikeuden julkaistuihin tapahtumiin, ilmoittautumisiin, ottelulistoihin, tuloksiin ja tilastoihin?
- Onko lukuoikeus maksullinen, mikä on suositeltu päivitystiheys ja saako luvan myös 190 osallistujan listan täydelliseen hakemiseen silloin, kun osallistujat on tarkoitettu julkisiksi?
- Miten erotetaan ilmoittautuminen, otteluparin julkaisu, tuomaripäätös ja myöhemmin korjattu tulos?
- Onko käytössä pysyvät organization/boxer/event/bout -ID:t sekä rajapinnan versiointi?
- Miten oikea Riihimäen Kehä-Ketut ry ja rinnakkaisprofiili yhdistetään ilman otteluhistorian menetystä? Voiko tuki tai Suomen Nyrkkeilyliiton pääkäyttäjä auttaa?
- Saako seura näyttää omalla sivullaan luvallisesti julkaistuja tietoja, ja kuinka käyttöoikeus rajataan vain julkisiin kenttiin? Ei syntymäaikoja tai muita tarpeettomia tietoja.

## Nykyinen toteutus
GitHub Actionsissa käytetään rajattua julkisten BoxerBase-sivujen hakua. Se noudattaa robots.txt:tä, tunnistaa vain näkyvän tiedon ja säilyttää vanhan kelvollisen aineiston, jos haku epäonnistuu. Julkisessa osallistujalistassa näkymätön ottelija ei tarkoita puuttuvaa ilmoittautumista.

## Tavoite
Erottaa etusivulla: ilmoittautuneet → vahvistetut ottelut (ei epävarmaa kellonaika-arviota) → julkaistut lopputulokset. Tietojen pitäisi päivittyä ilman käsin syötettävää kilpailua; samaa ottelua ei saa laskea kahdesti.

## Lisähuomio
Uusi kehaketut.aineisto@gmail.com on perustettu sisältöaineistolle. Sitä ei vielä ole yhdistetty automaatioon, eikä se anna sähköpostin lähettäjälle julkaisuoikeutta. Erillinen hyväksyntä tehdään oikean valtuutetun Google-kirjautumisen avulla.

Tämä on suunnitteluasiakirja; se ei väitä API:n olevan tarjolla tai yhteydenottopyyntöä lähetetyksi.
