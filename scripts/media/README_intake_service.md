# RKK: yksityisen videovastaanoton jatkuva paikallinen palvelu

**26.10.2026 – ohjelma toteutettu, ei asennettu Kubuntu-koneelle.**

Tämä on seuraava irtikytkentä ChatGPT-keskustelusta. Kun kuvaajien Dropbox-kansio synkronoidaan erikseen käyttäjän omaan yksityiseen kansioon, intake_service.py huomaa uusia MP4-tiedostoja pysyvällä 30 sekunnin skannausvälillä, odottaa niiden valmistumista, tarkistaa formaatin ja tuottaa pysyvät handoff JSON -raportit. Se käyttää SQLitea, joten uudelleenkäynnistys ei hukkaa tunnistettuja videoita.

## Valmiina ja puuttuu

- Valmis Dropbox File Request: https://www.dropbox.com/request/vjppmba9qlotgd9arodn -> /RKK/Uudet_videot.
- Tämä skripti ei itse autentikoi Dropboxiin eikä hae verkosta mitään. Kubuntun Dropbox-synkkaus tai rclone-vastaanotto on **vielä kytkemättä ja testaamatta**.
- Se ei muokkaa raakavideota, editoi, lähetä Metricooliin eikä julkaise mihinkään kanavaan. Tarkistukset tuottavat aina HOLD-tilaisen raportin.
- Lähde MP4 ei muutu. Symlinkit ohitetaan. Sama sisältö eri tiedostossa huomataan SHA-256:lla. Erillinen tiedostokohtainen JSON säilyttää kummankin lähteen tiedot.
- Yksityisen handoff-kansion ja tietokannan käyttöoikeudet rajataan omistajalle. Ei tunnisteta nyrkkeilijöitä kuvasta, eikä lähettäjän hyväksyntämerkin perusteella luoda julkaisulupaa.

## Testaa paikallisella Kubuntu-/Linux-koneella

Tarvitaan Python 3.10+, FFmpeg/ffprobe ja etukäteen toimivaksi vahvistettu paikallinen synkkakansio, johon tulee vain omaan Dropboxiin lähetettyjä alkuperäisiä MP4-tiedostoja.

    export RKK_REPO="$HOME/projects/kehaketut-feed"
    export RKK_INBOX="$HOME/.local/share/rkk/incoming"
    mkdir -p "$RKK_INBOX" "$HOME/.local/state/rkk" "$HOME/.local/share/rkk/handoff"
    chmod 700 "$RKK_INBOX" "$HOME/.local/state/rkk" "$HOME/.local/share/rkk"
    sudo apt install ffmpeg python3

Testi yksi ajo:

    python3 "$RKK_REPO/scripts/media/intake_service.py" \
      --folder "$RKK_INBOX" \
      --db "$HOME/.local/state/rkk/inbox.sqlite" \
      --outbox "$HOME/.local/share/rkk/handoff" \
      --once

Jatkuva työ:

    python3 "$RKK_REPO/scripts/media/intake_service.py" \
      --folder "$RKK_INBOX" \
      --db "$HOME/.local/state/rkk/inbox.sqlite" \
      --outbox "$HOME/.local/share/rkk/handoff" \
      --interval-seconds 30 --stable-seconds 90

Käsittely vaatii kaksi peräkkäistä havaintoa, vähintään 90 sekuntia muuttumatonta tiedostoa ja sen jälkeen onnistuneen ffprobe-tarkistuksen. Käytä tarvittaessa luotettuja assignment- ja published-ledger JSON-tiedostoja tiedostojen nimien, ottelujen ja aiempien julkaisujen yhdistämiseksi; merkkijono approved ei anna julkaisuoikeutta.

Kopioi deploy/rkk-media-intake.service.example käyttäjän systemd user -palveluksi ~/.config/systemd/user/rkk-media-intake.service ja korvaa todellisilla paikallisilla poluilla. Sen jälkeen:

    systemctl --user daemon-reload
    systemctl --user enable --now rkk-media-intake.service
    systemctl --user status rkk-media-intake.service
    journalctl --user -u rkk-media-intake.service -n 60 --no-pager

Ei pidä suorittaa ennen kuin synkkakansio ja työkalut ovat olemassa. Palvelua ei ole vielä asennettu tämän keskustelun aikana käyttäjän koneelle.

## Jatkokehityksen kriittiset puuttuvat osat

1. Oikea Dropbox-pääsyn kautta käynnistyvä synkkaus (esim. Dropbox Desktop tai oma OAuth/rclone-konfiguraatio). Jos rclonea käytetään, salaiset tokenit vain käyttäjän koneella, ei tässä julkisessa GitHubissa.
2. Yksityinen ottelu- ja oikeusrekisteri sekä tapahtuman valmiusikkuna -> turvallinen automaattinen event_recap.py renderöinti. Nykyinen data on vain HOLD-merkintöjä.
3. Lopullisten MP4:ien hallittu medialataus ja jatkuva Make + Metricool MCP tai vaihtoehtoinen virallinen alustan API -julkaisu. Erillinen julkisen Facebook, Instagram, YouTube URL:n varmistus ja kanavakohtainen deduplikointiloki.

## Harjoitusten peruutuksen tekninen huomio

Riihimäen kaupunki perui Kamppailukeskuksen harjoitusvuorot 27.–29.10.2026 korjaustöiden sisäilmaongelman vuoksi; tilanne arvioidaan 29.10.2026. Facebook-tiedote ajastettiin 26.10. klo 21.43, Metricool FB post-id 407067188 (Auto publish päällä). Tämän PR:n GitHub Pages -tiedote ja mahdollinen news-embed.js-banneri eivät ole Yhdistysavaimen natiivin /uutiset/-artikkelin julkaisu. Natiivi julkaisu vaatii Yhdistysavaimen oman hallinnan.
