# FileMp4
Convert any file into a video.

### WHY?!
Ich habe [Infinite-Storage-Glitch](https://github.com/DvorakDwarf/Infinite-Storage-Glitch) gefunden,
da es allerdings in Rust ist, wollte ich mal gucken, wie weit ich in Python damit komme und was man evtl. noch bearbeiten könnte.

Also meine Änderungen: 
- Farben statt Schwarz / weiß um 3 Byte in ein Pixel zu speichern (RGB (00-ff / 0 - 255))
- Größeres Bild, einfach um mehr Daten in ein Frame packen zu können.

Das eigentlich auch schon alles LOL.
Multi - Threading macht aktuell noch Probleme, daher ist es erstmal Single Thread.
Ich denke auch nicht, dass die Videos YouTube überleben, einfach wegen Komprimierung etc. aber das ist nicht so wichtig, war nur ein kleines Fun-Projekt, 
Macht damit, was ihr wollt.