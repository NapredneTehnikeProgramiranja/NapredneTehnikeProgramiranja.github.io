# Kako radi ova prezentacija?

Prezentacija je sastavljena kombinovanjem nekoliko tehnologija:
- GNU/Emacs
  [Org mode](http://orgmode.org/) +
  [Babel](http://orgmode.org/worg/org-contrib/babel/) --- kako bi svi
  materijali za učenje bili u
  formi
  [literate programming](https://en.wikipedia.org/wiki/Literate_programming) dokumenata,
  kako bi svako parče koda bilo izvršeno u kontekstu dokumenta pre
  eksportovanja u konačnu web stranicu.
- [Hakyll](https://jaspervdj.be/hakyll/) +
  [Stack](https://docs.haskellstack.org/en/stable/README/) --- kako bi
  se generisala statička web prezentacija samo iz onih delova koji
  treba da se nađu u prezentaciji.
- [GitHub pages](https://pages.github.com/) --- kako bi prezentacija
  bila javno dostupna.

## Tok rada

1. Preći na `develop` granu, sav razvoj se odvija tamo.
2. Unutar direktorijuma `org` napisati *org-mode* dokument koji želite
   da objavite (npr. *OCaml.org*) i popunite ga materijalom
   (koristite [Babel](http://orgmode.org/worg/org-contrib/babel/) kada
   je to moguće).
3. Eksportujte svoj dokument u HTML. U Emacs-u koristite
   `org-export-dispatch` funkciju i tamo odaberite `As HTML file`
   opciju.
4. Uradite standardnu proceduru Hakyll-a za generisanje prezentacije


    ``` shell
    $ stack build
    $ stack exec site build
    $ stack exec site watch
    ```

    I pogledajte svoju prezentaciju na [localhost:8000](http://localhost:8000).

    Sada Vam je ostalo samo da je objavite.
5. Objavljivanje prezentacije se radi tako što se **skoro** čitava
   `master` grana zameni **sadržajem** `_site` direktorijuma na
   `develop` grani:

   - dok ste još na `develop` grani kopirajte `_site` direktorijum u
     npr. `~/Desktop`.
   - pređite na `master` granu.
   - sa master grane obrišite sve osim: `CNAME`, `.git`, `.github`,
     `README.md`, `.gitignore`.
   - sadržaj `_site` direktorijuma koji ste stavili u npr. `~/Desktop`
     kopirajte na `master` granu.
   - push-ujte izmene na `master` granu na GitHub-u. Od ovog momenta
     Vaš materijaln je dostupan negde iza
     `http://naprednetehnikeprogramiranja.tk/org/`.
   - **vratite se na `develop` granu**.

   Skripta koja ovo automatizuje još ne postoji. Postojaće čim se za
   to nađe vremena.

   Komplikacija delimično
   potiče
   [odavde](https://help.github.com/articles/configuring-a-publishing-source-for-github-pages/).

### Pisanje objava == obaveštenja == postova

Objave se pišu u standardnom *markdown-u*.

1. Napišite svoju objavu po ugledu na neku iz `posts` direktorijuma.
2. Uradite korak 4. pa 5. od gore.

### Ostalo

- **index** stranica se piše direktno u `index.html`.
- **about** stranica se piše direktno u `about.rst`.
- **contact** stranica se piše direktno u `contact.markdown`.
- **statički resursi dostupni svuda** nalaze se u `resources`.
- **slike dostupne materijalima napravljenim org-om** nalaze se u `org/images`.

# Pronašli ste grešku?

Ako pronađete bilo kakvu grešku ili nedoslednost u ovim materijalima
(uključujući i sav povezan kod) molimo Vas da nam skrenete pažnju na
to kako bismo zajedno učinili ovaj kurs boljim.

Budite slobodni da otvorite [issue](https://github.com/NapredneTehnikeProgramiranja/NapredneTehnikeProgramiranja.github.io/issues).
