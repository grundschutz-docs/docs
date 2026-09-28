---
title: "DEV – Entwicklung"
---

Die Praktik Entwicklung stellt sicher, dass Sicherheitsanforderungen bereits von Beginn an in die Planungs- und Entwicklungsphase von IT-Systemen und Anwendungen integriert werden. Auf diese Weise können potenzielle Schwachstellen frühzeitig erkannt und vermieden werden, wodurch die Sicherheit über den gesamten Lebenszyklus der IT-Systeme und Anwendungen hinweg gewährleistet ist. Entwicklung berücksichtigt die Software- und Systementwicklung, also die Erzeugung und Integration neuer IT-Komponenten in die IT-Infrastruktur der Institution. Durch die enge Zusammenarbeit mit anderen Praktiken wie IT-Betrieb, Asset Management und Konfiguration wird gewährleistet, dass die entwickelten IT-Komponenten nicht nur sicher entwickelt werden, sondern auch sicher betrieben, verwaltet und gepflegt werden können. Diese enge Verzahnung sorgt dafür, dass Sicherheitsanforderungen durchgängig und über alle Phasen hinweg eingehalten werden.

## DEV.1 Grundlagen

### DEV.1.1 – Verfahren und Regelungen

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18

> Entwicklung MUSS Verfahren und Regelungen zur Entwicklung von IT-Produkten verankern.

Für ein Verfahren zur Softwareentwicklung siehe BSI TR-03185. Entwickelt die Institution im Informationsverbund keine IT-Produkte, so sind diese und alle anderen Anforderungen der Praktik entbehrlich. Die bei der Festlegung des Verfahrens im Einzelnen zu berücksichtigenden Inhalte ergeben sich aus den Anforderungen dieser Praktik.

#### DEV.1.1.1 – Dokumentation

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.37, G 0.29, G 0.31

> Entwicklung MUSS die Verfahren und Regelungen dokumentieren.

Ohne eine Dokumentation könnte die Einhaltung der Verfahren und Regelungen von der Tagesform oder dem individuellen Wissen einzelner Mitarbeiter abhängen, was zu inkonsistenten Entscheidungen und Fehlern führen könnte; insbesondere beim Ausscheiden eines langjährigen Administrators könnte wertvolles prozessuales Wissen verloren gehen. Eine klare Dokumentation sichert die Verbindlichkeit und Wiederholbarkeit und dient als unverzichtbare Grundlage für die Einarbeitung neuer Kollegen, für die Durchführung von Audits und zur einheitlichen Anwendung der Regeln in der gesamten Institution. Die Dokumentation kann in einem eigenständigen Dokument als Richtlinie erfolgen, aber auch als Abschnitt in einem bereits bestehenden Dokument oder über die digital strukturiere Erfassung von Maßnahmen zur Umsetzung der Anforderungen, etwa über eine Software zum Management der Informationssicherheit. Sinnvoll ist es Ort und Struktur der Dokumentation an der jeweiligen Zielgruppe, d.h. den für das Management und die Umsetzung verantwortlichen Personen oder Rollen, auszurichten.

#### DEV.1.1.2 – Zuweisung der Aufgaben

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.31

> Entwicklung MUSS die mit den Verfahren und Regelungen verbundenen Aufgaben *[zuständigen Personen oder Rollen]* zuweisen.

Die Zuweisung von Aufgaben bezeichnet die eindeutige und verbindliche Übertragung von konkreten Tätigkeiten und Verantwortlichkeiten des Änderungsprozesses, wie etwa die Risikobewertung, die technische Umsetzung oder die finale Freigabe, an definierte Stellen in der Institution. Der Sinn dieser Vorschrift ist es, die Verantwortlichkeit ("Accountability") für jeden einzelnen Schritt im Prozess klarzustellen. Ohne eine solche Zuweisung könnten kritische Prüfungen unterbleiben, weil sich niemand explizit zuständig fühlt, was wiederum die Wahrscheinlichkeit fehlgeschlagener Änderungen erhöht. Eine klare Regelung kann sicherstellen, dass keine Aufgaben übersehen werden und jede Tätigkeit von einer dafür qualifizierten und befugten Stelle ausgeführt wird, was die Prozesssicherheit signifikant erhöht. Eine bewährte Methode zur Umsetzung ist die Erstellung einer RACI-Matrix (Responsible, Accountable, Consulted, Informed), die tabellarisch für jeden Prozessschritt darstellt, wer für die Durchführung verantwortlich ist, wer die Gesamtverantwortung trägt, wer zu konsultieren und wer zu informieren ist. Diese Zuständigkeiten können auch direkt in einem Workflow- oder Ticketsystem abgebildet werden, sodass Aufgaben, wie beispielsweise Genehmigungsschritte, automatisch an die richtige Gruppe oder Person weitergeleitet werden. Sinnvoll ist es die Zuweisung anhand von Rollen (z.B. "Anwendungsverantwortlicher", "Netzwerkadministrator", "Change Manager") vorzunehmen, statt an konkrete Personen. Dieser Ansatz stellt sicher, dass die Prozesse auch bei Personalwechseln stabil weiterlaufen, da die Zuständigkeit an die Funktion und nicht an das Individuum gebunden ist.

#### DEV.1.1.3 – Bekanntgabe

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18

> Entwicklung MUSS die zuständigen Personen oder Rollen über die Verfahren und Regelungen informieren.

Wenn die Zuständigen die etablierten Verfahren nicht kennen, besteht die Gefahr, dass diese – sei es aus Unwissenheit oder Bequemlichkeit – umgangen werden, was die Schutzwirkung des gesamten Managementsystems untergräbt. So könnte ein neuer Systemadministrator eine weitreichende Konfigurationsänderung vornehmen, ohne den vorgeschriebenen Genehmigungsprozess zu durchlaufen, was zu einem unbemerkten Sicherheitsrisiko führen könnte. Eine gezielte Information kann hingegen die Akzeptanz der Regelungen fördern und sicherstellen, dass alle Beteiligten ihre Rolle im Prozess verstehen und die Abläufe korrekt anwenden. Zur Umsetzung ist es sinnvoll die Dokumentation im Rahmen eines Onboarding-Prozesses bekanntzugeben und bei allen Änderungen eine automtatische Benachrichtigung aller zuständigen Personen oder Rollen anzustoßen.

### DEV.1.2 – Regelmäßige Überprüfung

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.29

> Entwicklung MUSS die Verfahren und Regelungen *[regelmäßig]* und anlassbezogen auf Aktualität überprüfen.

Eine geplante Überprüfung der etablierten Verfahren und Regelungen dient dazu festzustellen, ob diese noch wirksam, effizient und an die aktuellen Gegebenheiten angepasst sind. Eine anlassbezogene Überprüfung wird durch spezifische Ereignisse ausgelöst, wie etwa einen schwerwiegenden Sicherheitsvorfall, eine strategische Neuausrichtung der IT oder neue gesetzliche Anforderungen. Der Zweck dieser Anforderung ist es, die kontinuierliche Verbesserung und Anpassungsfähigkeit des Prozesses sicherzustellen, da veraltete Regelungen neuen technologischen Entwicklungen oder Bedrohungen nicht mehr gerecht werden könnten; ein vor Jahren für monolithische Anwendungen konzipierter Prozess ist beispielsweise für agile Entwicklungsmethoden oder Microservice-Architekturen ungeeignet. Die regelmäßige Überprüfung kann die Effektivität des Sicherheitsmanagements langfristig aufrechterhalten und die Resilienz der Institution stärken.

## DEV.2 Softwareentwicklung - Security by Design

### DEV.2.1 – Security by Design Architektur

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.28, G 0.46, G 0.18

> Entwicklung SOLLTE die Architektur nach dem Prinzip "Security by Design" verankern.

Unter "Security by Design" ist zu verstehen, dass Sicherheitsprinzipien und -mechanismen integrale Bestandteile der Architektur sind, anstatt nur nachträglich "angeflanscht" zu werden. Hierzu gehören Sicherheitsprinzipien wie Modularisierung, Verschlüsselung und Authentifizierung beim Entwurf der Architektur. Die Umsetzung kann durch Threat Modeling realisiert werden. Für Details siehe BSI TR-03185. Bei der Umsetzung von Security by Design empfiehlt sich auch ein Blick in die Praktik Konfiguration, spezifisch die Anforderungen zu Verschlüsselung, Authentifizierung, etc.

### DEV.2.2 – Dokumentation der (Software-)Architektur

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18

> Entwicklung für Anwendungen SOLLTE die Architektur dokumentieren.

Die Architektur bezeichnet im konkreten Kontext die strukturierte Beschreibung der grundlegenden Komponenten einer Software sowie deren Schnittstellen, Abhängigkeiten und das Datenmodell. Sie stellt dar, wie Module, Datenflüsse und externe Systeme ineinandergreifen, und bildet damit das Gerüst für Wartung, Weiterentwicklung und Sicherheitsbewertungen. Ohne dokumentierte Architektur könnte eine Institution nach Jahren vor der Situation stehen, dass nur einzelne Entwickler den Aufbau verstehen, was den Wissenstransfer erschwert und bei Personalwechseln erhebliche Risiken birgt. Eine unklare oder fehlende Dokumentation könnte zudem dazu führen, dass Abhängigkeiten von proprietären Technologien übersehen werden, wodurch sich ein Vendor Lock-in entwickelt, der die Institution langfristig bindet. Umgekehrt kann eine nachvollziehbare Architektur Dokumentation sicherstellen, dass Schwachstellenanalysen effizient durchgeführt werden, dass Sicherheitslücken frühzeitig erkannt werden und dass neue Entwickler schneller eingearbeitet werden können. Zur Umsetzung der Anforderung kann eine Institution standardisierte Diagrammtypen wie UML oder C4 einsetzen, um Abhängigkeiten und Schnittstellen verständlich abzubilden. Hilfreich kann es sein, die Architektur in mehreren Sichten zu dokumentieren, etwa eine logische Sicht (Funktionen und Module), eine technologische Sicht (Server, Container, Frameworks) und eine sicherheitsrelevante Sicht (z. B. Trust Boundaries). Die Dokumentation kann in Versionskontrollsystemen wie Git gepflegt werden, sodass Änderungen an Architekturentscheidungen nachvollziehbar bleiben. Ergänzend kann es praktikabel sein, automatisierte Werkzeuge einzusetzen, die Code-Strukturen analysieren und Diagramme generieren, wodurch Konsistenz zwischen Dokumentation und Implementierung unterstützt werden kann.

### DEV.2.3 – Ausführbarkeit mit minimalen Rechten

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.32, G 0.21

> Entwicklung für Anwendungen SOLLTE die fehlerfreie Ausführung mit den geringst möglichen Berechtigungen verankern.

Die Anwendung ermöglicht die Ausführung mit den geringst möglichen Berechtigungen, wenn sie nur die Berechtigungen benötigt, die für die gerade intendierte Funktionalität erforderlich sind (also z.B. auch ohne Kamerazugriff funktioniert, wenn Nutzende nur vorhandene Bilder betrachten möchten). Sind einzelne Berechtigungen nicht vorhanden, so funktioniert die Anwendung mit entsprechenden Einschränkungen weiterhin (Graceful Degradation).

### DEV.2.4 – Einschränkung Zugriffs auf Quellcode

**Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.22, G 0.46

> Entwicklung SOLLTE den schreibenden Zugriff auf Quellcode einschränken.

Eine Einschränkung des schreibenden Zugriffes auf den Quellcode auf die zur Aufgabenerfüllung erforderlichen Personen oder IT-Systeme hilft, unbefugte Änderungen am Quellcode zu verhindern. Nach dem Grundsatz der geringstmöglichen Berechtigung benötigen schreibenden Zugriff nur Personen wie Entwickler oder Maintainer, zu deren Aufgaben die Arbeit am Code gehört.

### DEV.2.5 – Einschränkung des Zugriffs auf Zugangsdaten

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.28, G 0.21, G 0.22, G 0.19

> Entwicklung für Anwendungen SOLLTE den lesenden und schreibenden Zugriff auf Zugangsdaten einschränken.

Von der Anwendung verwendete Zugangsdaten können z.B. API-Schlüssel oder Datenbankanmeldeinformationen sein. Statt diese im Quellcode zu hinterlegen ist es besser, sie in Umgebungsvariablen oder sogenannten Vaults zu speichern. Hierbei hilft es auch, solche Daten mit .gitignore-Regeln aus der Versionskontrolle auszuschließen.

### DEV.2.6 – Widerstandsfähigkeit gegen gängige Angriffsmuster

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.21, G 0.22, G 0.46

> Entwicklung für Anwendungen SOLLTE Schutzfunktionen gegen gängige Angriffsmuster installieren.

Gängige Angriffsmuster sind wiederkehrende Vorgehensweisen von Angreifenden, die in der Praxis häufig auftreten, z. B. SQL-Injection, Cross-Site-Scripting (XSS) oder Pufferüberläufe. Welche Angriffsmuster für die konkrete Anwendung gängig sind, hängt von Funktionalität und Architektur der Anwendung ab, z.B. Prompt Injection bei generativer KI. Die Vorschrift zielt darauf ab, dass Produkte bereits in der Entstehung so gestaltet werden, dass typische Schwachstellen systematisch erschwert werden. Ohne entsprechende Vorkehrungen könnte ein Angreifer etwa durch manipulierte Eingaben vertrauliche Daten auslesen oder unautorisiert Funktionen steuern. Werden Schutzfunktionen frühzeitig eingebaut, kann die Stabilität des Produkts erhöht, die Angriffsfläche reduziert und das Vertrauen der Nutzenden gestärkt werden. Zur Umsetzung können etablierte Programmierpraktiken wie das Verwenden sicherer Standardbibliotheken, das Einschränken von Nutzerrechten im Code oder das Einführen von Fallback-Mechanismen bei fehlerhaften Eingaben verwendet werden. Ergänzend kann die Institution Secure Coding Guidelines nutzen, die häufige Angriffsmuster adressieren und Entwickelnden praxisnahe Hilfen bieten.

#### DEV.2.6.1 – Eingabevalidierung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28

> Entwicklung für Anwendungen SOLLTE Eingabedaten auf eingeschleuste Befehle testen.

Bei der Eingabevalidierung (Input Validation) wird getestet, ob die Eingabedaten eingeschleuste Befehle enthalten, z.B. SQL-Injection, Kommandozeilenbefehle oder Prompt Injection bei generativer KI. Welche Eingaben betroffen sein könnten, kann durch eine Taint Analyse herausgefunden werden. Alternativ können auch alle Eingabedaten validiert werden (Server Side Validation).

#### DEV.2.6.2 – Ausgabekodierung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28

> Entwicklung für Anwendungen SOLLTE eine Ausgabekodierung ausführen.

Ausgabekodierung (Output Encoding) ist wichtig, da sie spezielle Zeichen neutralisiert und so Angriffe wie Cross-Site Scripting (XSS) oder HTML-Injektionen verhindert, die ansonsten Schadcode ausführen könnten. Empfehlenswert ist kontextabhängiges Encoding und Escaping, basierend auf standardisierten Frameworks wie OWASP ESAPI.

## DEV.3 Softwareentwicklung - Härtung

### DEV.3.1 – Replay-Angriffe

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.43

> Entwicklung für Anwendungen SOLLTE Replay-Angriffe blockieren.

Wenn die Anwendung Anfragen von anderen Anwendungen oder IT-Systemen entgegennimmt (z.B. per API), dann besteht die Gefahr, dass Angreifer eine vorherige Anfrage erneut verwenden um unbefugt Zugang zu erhalten. Maßnahmen können sein: (1) Identifikatoren, die nur einmal gültig sind (Nonce, Sequenznummern), (2) kryptographische Mechanismen wie MAC und Digitale Signaturen, Challenge-Response-Authentifizierung, OTP.

### DEV.3.2 – Routinen zur Fehlerbehandlung

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.28, G 0.21

> Entwicklung für Anwendungen SOLLTE spezifische und allgemeine Routinen zur Fehlerbehandlung ausführen.

Behandeln Sie Fehler (Exceptions) möglichst nahe an der Quelle (z.B. Buffer Overflows, fehlende Dateien) und sehen sie eine Routine vor, die unerwartete Fehler abfängt. Geben Sie passende Fehlermeldungen aus und protokollieren Sie Fehler.

### DEV.3.3 – Deaktivierung der Ausgabe schützenswerter Daten durch Fehlermeldungen

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.19

> Entwicklung für Anwendungen SOLLTE die Ausgabe schützenswerter Daten durch Fehlermeldungen deaktivieren.

Werden sensible Daten in Fehlermeldungen oder Log-Einträgen verwendet, kommt es leicht zur Offenlegung dieser Informationen gegenüber Unbefugten. Hierzu gehören auch Hinweise auf das Vorhandensein oder Nicht-Vorhandensein eines Nutzendenkontos.

### DEV.3.4 – Passwort-Hashing

**Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.28, G 0.19

> Entwicklung für Anwendungen SOLLTE das Hashing von Passwörtern, die zur Authentifizierung an der Anwendung verwendet werden vor der Verarbeitung oder Speicherung aktivieren.

Ziel ist der Schutz vor Angriffen, welche Passwörter beim Transport oder aus dem Speicher auslesen und sich hiermit anmelden. Dies kann durch Hash und Salt gemäß BSI TR-02102 vermieden werden.

## DEV.4 Softwareentwicklung - Code

### DEV.4.1 – Nutzerinformation bei kritischen Ereignissen

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.36, G 0.29

> Entwicklung für Anwendungen SOLLTE bei sicherheitskritischen Ereignissen die betroffenen Nutzenden informieren.

Z.B. bei Anmeldung von neuen Geräten, Zurücksetzen des Passwortes, ungewöhnlichen Standorten oder der Änderung von Stammdaten.

### DEV.4.2 – Einbindung externer Software

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.28, G 0.46, G 0.20

> Entwicklung für Anwendungen SOLLTE die Einbindung externer Softwareartefakte und -Schnittstellen aus unzuverlässigen oder unbekannten Quellen untersagen.

Externe Softwareartefakte sind in diesem Kontext nicht von der Institution entwickelte, in die eigene Anwendung eingebundene oder zur Laufzeit nachgeladene Bestandteile wie Bibliotheken, Frameworks, Container-Images, Plug-ins, Packages, Binärdateien, Skripte, Modelle, Templates oder Build-Abhängigkeiten (sog. Third-Party Components, Dependencies) verwendet. Externe Softwareschnittstellen sind fremde technische Übergabe- und Kommunikationspunkte, über die eine Anwendung Funktionen oder Daten anderer Systeme nutzt, etwa APIs, Webhooks, SDK-Schnittstellen, Datenfeeds, Authentifizierungsdienste oder Remote Services; geläufige englische Begriffe sind Third-Party APIs, External Interfaces, Webhooks, SDKs und Remote Services. Eine Quelle ist unzuverlässig, wenn zukünftig mit Verstößen gegen die Schutzziele Vertraulichkeit, Verfügbarkeit oder Integrität durch sie zu rechnen ist (d.h. eine Prognose der Vertrauenswürdigkeit). Dies ist insbesondere der Fall, wenn erhebliche Verstöße gegen die Schutzziele durch sie begangen worden sind oder Anzeichen dafür vorliegen, dass bei einer Verwendung mit solchen Verstößen zu rechnen ist. Unbekannte Quellen meint hier Quellen, deren Herkunft, Integrität, Pflegezustand, Verantwortlichkeit, Vertrauenswürdigkeit oder Sicherheitsniveau nicht belastbar nachvollziehbar ist, etwa anonyme Paket-Repositories, private Download-Links, unklare Git-Repositories, veraltete Mirror-Server, nicht verifizierte Container-Registries oder Schnittstellen ohne erkennbare Betreiber-, Sicherheits- und Änderungsinformationen.

### DEV.4.3 – Softwarebestandteile (SBOM)

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.28

> Entwicklung für Anwendungen SOLLTE die Bestandteile mit Hilfe einer Software Bill of Materials (SBOM) vor dem Release dokumentieren.

Details siehe BSI TR-03183-2. Anwendungen zur Modulverwaltung und Software Composition Analysis (SCA) können dabei unterstützen SBOMs als Teil eines CI/CD Prozesses automatisiert zu sammeln.

### DEV.4.4 – Integrität externer Software

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.22, G 0.46

> Entwicklung für Anwendungen SOLLTE die Integrität externer Softwareartefakte und -Schnittstellen vor dem Release testen.

Gemeint ist damit sowohl die technische Unversehrtheit (z. B. durch kryptografische Prüfungen wie Hash- oder Signaturvalidierung) als auch die inhaltliche Zuverlässigkeit (z. B. keine eingeschleusten Schadfunktionen oder versteckte Abhängigkeiten). Der Sinn und Zweck dieser Anforderung liegt darin, die Risiken durch unsichere oder manipulierte Fremdkomponenten zu reduzieren. So könnte ein Angreifer Schadcode in eine weit verbreitete Bibliothek einschleusen, die dann unbemerkt in der Anwendung landet, oder eine Abhängigkeit könnte im Hintergrund auf nicht mehr gepflegte Versionen verweisen. Eine wirksame Integritätsprüfung kann verhindern, dass fehlerhafte oder kompromittierte Bausteine in produktive Anwendungen gelangen und kann damit auch die Abhängigkeit von nicht vertrauenswürdigen Quellen abmildern. Zur Umsetzung können (1) Hashwerte oder digitale Signaturen von Bibliotheken mit den Referenzwerten der Hersteller verglichen werden, (2) der Bezug externer Pakete über offizielle, verifizierte Repositories, statt über inoffizielle Quellen stattfinden, und (3) in der Build-Pipeline eine automatisierte Integritätsprüfung eingerichtet sein, die verdächtige oder unvollständige Bibliotheken blockieret. Ergänzend kann eine institutionseigene Allowlist gepflegt werden, die geprüfte Versionen von Bibliotheken enthält, sodass Entwickler nicht unkontrolliert beliebige Abhängigkeiten einbinden. Ein praktischer Tipp kann sein, die Prüfmechanismen möglichst früh im Entwicklungsprozess zu automatisieren, um spätere manuelle Nacharbeiten oder Verzögerungen vor einem Release zu vermeiden.

### DEV.4.5 – Updates externer Software

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.28

> Entwicklung für Anwendungen SOLLTE externe Softwareartefakte auf Sicherheitsupdates vor dem Release testen.

Werden veraltete Softwareartefakte (z.B. Bibliotheken oder Container) in eine veröffentlichte Software eingebunden, so können diese Sicherheitslücken oder Fehler enthalten, die in den aktuellen Versionen bereits behoben sind. Prüfen Sie daher vor einer Freigabe der Software, ob eingebundene Software aktualisiert wurde.

### DEV.4.6 – Compileroptionen

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28

> Entwicklung für Anwendungen SOLLTE Compileroptionen für Sicherheitsfunktionen vor dem Release aktivieren.

Compileroptionen wie Stack Canaries, PIE, PIE, CFI können automatisch Schutzmechanismen in Programme einbauen. Bewährte Praxis ist es, diese Compileroptionen zu aktivieren, sofern es keine entgegenstehenden besonderen Gründe gibt, darauf im Einzelfall zu verzichten. Werden interpretierte Programmiersprachen verwendet, so ist die Anforderung analog auf die Interpreter-Optionen anzuwenden.

### DEV.4.7 – Deterministischer Binärcode

**Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.18, G 0.22, G 0.46

> Entwicklung für Anwendungen KANN eine reproduzierbare Vorgehensweise zur Erstellung eines bestimmten Binärcodes aus dem Quellcode dokumentieren.

Ein bestimmter Binärcode meint hier eine reproduzierbare Anwendung (Reproducible builds). Das bedeutet, dass jeder, der denselben Quellcode und dieselbe Build-Umgebung verwendet, bitweise identische Binärdateien erstellt, was die Integrität der Software gegen Manipulationen oder Malware sichert. Dies geschieht durch die genaue Beschreibung der Build-Umgebung und die Vermeidung von zufälligen Faktoren wie Zeitstempeln, die sich auf die erzeugten Artefakte auswirken könnten.

### DEV.4.8 – Default-Zugangsdaten

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.18, G 0.30

> Entwicklung für Anwendungen SOLLTE Default-Zugangsdaten vor dem Release dokumentieren.

Falls die Software Default-Zugangsdaten wie Passwörter oder Zertifikate enthält, so ist eine sichere Nutzung der Software nur möglich, wenn Nutzende hiervon Kenntnis erhalten um die Zugangsdaten ändern zu können. Sind keine Default-Zugangsdaten erforderlich, so ist die Anforderung entbehrlich.

### DEV.4.9 – Voreinstellungen nach dem Prinzip "Security by Default"

**Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.18, G 0.30

> Entwicklung für Anwendungen SOLLTE Voreinstellungen nach dem Prinzip "Security by Default" aktivieren.

Voreinstellungen sind die Parameter der Anwendung, mit denen diese im Auslieferungszustand (oder bei Cloud-Anwendungen beim Anlegen eines neuen Zugangskontos) ausgeführt wird. Welche Parameter hier konkret sicher sind ergibt sich aus der Praktik Konfiguration für die jeweilige Art von Zielobjekten.

### DEV.4.10 – Protokollierung von Codeänderungen

**Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.37, G 0.22

> Entwicklung für Anwendungen SOLLTE Änderungen am Quellcode einschließlich Zeitpunkt, Inhalt der Änderung, ändernder Person und der Begründung der Änderung protokollieren.

Im Kontext dieser Anforderung bezeichnet Quellcode den in einer Programmiersprache geschriebenen, von Menschen lesbaren Anteil einer Anwendung, während eine Änderung jede Anpassung, Ergänzung oder Entfernung dieses Codes umfasst. Unter Begründung ist die dokumentierte fachliche oder technische Motivation zu verstehen, die erläutert, warum eine Änderung notwendig war, beispielsweise zur Fehlerbehebung, Funktionserweiterung oder Verbesserung der Sicherheit. Der Zeitpunkt entspricht dabei einem präzisen Zeitstempel, der eine eindeutige zeitliche Nachvollziehbarkeit erlaubt, und die ändernde Person ist diejenige, die die Modifikation fachlich veranlasst oder technisch durchgeführt hat – nicht zwingend dieselbe Rolle wie ein Freigebender oder Reviewer. Die Protokollierung kann verhindern, dass unautorisierte oder fehlerhafte Anpassungen unentdeckt bleiben, und sie kann im Streitfall eine klare Nachvollziehbarkeit bieten. Ohne diese Nachweise könnte es zu unklaren Verantwortlichkeiten, erhöhtem Manipulationsrisiko oder schwer nachvollziehbaren Fehlfunktionen kommen. Eine Institution kann diese Anforderung durch Nutzung von Versionsverwaltungssystemen wie Git oder Subversion umsetzen, indem sie für jede Änderung standardisierte Commit-Meldungen mit Zeitstempel, Autor und Begründung erzwingt. Ergänzend kann ein Workflow etabliert werden, bei dem Änderungen erst nach einem Merge- oder Pull-Request mit dokumentierter Beschreibung in den Hauptzweig gelangen. Sinnvoll ist es zudem, einfache Vorlagen oder Textbausteine für Begründungen bereitzustellen, sodass Änderungen einheitlich und vollständig erklärt werden können. Für Transparenz kann zusätzlich ein automatisches Änderungsprotokoll generiert werden, das regelmäßig exportiert oder archiviert wird, um auch ohne Zugriff auf das Versionsverwaltungssystem auswertbar zu bleiben.

### DEV.4.11 – Test bei Änderungen am Quellcode

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.28, G 0.18

> Entwicklung für Anwendungen SOLLTE Änderungen am Quellcode im Einklang mit den Verfahren und Regelungen für Änderungen und Tests testen.

„Änderungen am Quellcode“ (engl. source code changes) bezeichnet im gegebenen Kontext sämtliche Modifikationen, die an den Programmbestandteilen einer Anwendung vorgenommen werden, also etwa neue Funktionen, Fehlerkorrekturen oder Anpassungen an Schnittstellen. Fehlerhafte oder ungetestete Anpassungen könnten etwa zu Sicherheitslücken, Datenverlust oder Instabilitäten im Betrieb führen, wohingegen eine strukturierte Prüfung verhindern kann, dass bekannte Schwachstellen erneut auftreten oder unbeabsichtigte Seiteneffekte entstehen. Solche Änderungen sind daher als Teil des Change Managements zu betrachten, dessen Anforderungen im Einzelnen in der Praktik Änderungen und Tests zu finden sind. Zur praktischen Umsetzung kann eine Institution jede Änderung automatisiert durch Static Application Security Testing (SAST) prüfen, wodurch potenzielle Schwachstellen direkt im Quellcode erkannt werden können. Ergänzend ist es sinnvoll Dynamic Application Security Testing (DAST) einzusetzen, um die lauffähige Anwendung in einer Testumgebung gegen typische Angriffe wie SQL-Injection oder Cross-Site-Scripting zu überprüfen. Sinnvolle Maßnahmen können dabei sein: (1) Aufbau einer Continuous-Integration-Pipeline, die automatisierte Unit-, Integrations- und Sicherheitstests einbindet und Ergebnisse konsolidiert darstellt, (2) Durchführung von manuellen explorativen Tests in einer isolierten Testumgebung, um auch unerwartete Nutzungsmuster zu prüfen, (3) Einsatz von Regressionstests, die sicherstellen können, dass neue Änderungen keine bestehenden Funktionen beeinträchtigen. Eine Institution kann damit die Qualitätssicherung stärken und gleichzeitig Angriffsflächen durch fehlerhafte Änderungen reduzieren.

## DEV.5 Softwareentwicklung - Updates

### DEV.5.1 – Verankerung des Zeitraums für Updates

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.28, G 0.18

> Entwicklung für Anwendungen SOLLTE die Bereitstellung von Sicherheitsupdates mindestens für *[einen bestimmten Zeitraum]* verankern.

Hierbei wird festgelegt, für welchen konkreten Zeitraum Sicherheitsaktualisierungen (Patches) für das Produkt mindestens bereitgestellt werden. Dazu gehört auch eine Definition von welchem Zeitpunkt aus der Zeitraum berechnet wird, z.B. Erstveröffentlichung des Produkts. Denken Sie dabei daran, ob ggf. Compliance-Verpflichtungen einzuhalten sind, z.B. § 475b Abs. 3 Nr. 2 BGB für Verbraucherverträge.

### DEV.5.2 – Information über Zeitraum für Updates

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.18, G 0.29

> Entwicklung für Anwendungen SOLLTE Auftraggeber über den festgelegten Zeitraum für Sicherheitsupdates informieren.

Stellen Sie den Empfängern der Software Informationen darüber bereit, wie lange Sicherheitsaktualisierungen gewährleistet werden und wie diese bezogen werden können.

### DEV.5.3 – Integritätsprüfung

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.20, G 0.22, G 0.46

> Entwicklung für Anwendungen SOLLTE Nutzende über Möglichkeiten zur Verifikation der Integrität von Installations-, Update- und Patchdateien informieren.

Dies kann z.B. durch die Veröffentlichung von Prüfsummen über einen authentifizierten Kanal wie eine Webseite mit X.509-Zertifikat erfolgen.

## DEV.6 Freigabe

### DEV.6.1 – Freigabe nach Änderungen und Tests

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.25, G 0.26

> Entwicklung SOLLTE die Freigabe zur Nutzung im Einklang mit den entsprechenden Verfahren und Regelungen für Änderungen und Tests autorisieren.

Eine Freigabe zur Nutzung (Release) meint hier die formelle und autorisierte Überführung einer entwickelten oder geänderten IT-Komponente (wie Software, Systemkonfiguration, Dienstleistung) von einer Test- oder Entwicklungsumgebung in eine Produktions- oder Betriebsumgebung, um den Endbenutzern zur Verfügung zu stehen. Die Vorschrift zielt darauf ab, sicherzustellen, dass nur getestete und abgestimmte Änderungen in den Betrieb gelangen. Ohne diese Autorisierung könnte ungetesteter Code oder eine nicht genehmigte Systemänderung zu schwerwiegenden Betriebsunterbrechungen, Datenverlust oder Sicherheitslücken führen. Eine formalisierte Freigabe kann die Integrität und Verfügbarkeit von Systemen schützen, indem sie die Einhaltung der etablierten Verfahren und Regelungen für Änderungen und Tests sicherstellt.

## DEV.7 Bereitstellung und Betrieb

### DEV.7.1 – Sichere Bereitstellung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.25, G 0.26

> Entwicklung SOLLTE die Bereitstellung im Einklang mit den entsprechenden Verfahren und Regelungen für Änderungen und Tests verankern.

Die Bereitstellung ist der Prozessschritt, durch den eine neu entwickelte oder geänderte Softwareversion, ein Dienst oder ein System in die Produktionsumgebung überführt und dort aktiv für die Endnutzer oder Geschäftsprozesse zugänglich gemacht wird. Die Anforderungen aus der Praktik Änderungen und Tests (also zum Change Management) betreffen auch die Bereitstellung. Eine geordnete Bereitstellung minimiert das Risiko, dass ungetestete oder nicht genehmigte Änderungen in Betrieb gehen, was sonst zu Dienstunterbrechungen, Datenverlust oder der Ausnutzung von Sicherheitslücken führen könnte.

### DEV.7.2 – Zertifikatsmonitoring

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.36, G 0.43

> Entwicklung für Anwendungen SOLLTE die Ausstellung neuer Zertifikate für die von der Anwendung verwendeten Domains überwachen.

Neue Zertifikate sind in diesem Kontext digitale Zertifikate, insbesondere TLS-/Serverzertifikate nach X.509, die zu einer von der Anwendung genutzten Domain oder Subdomain ausgestellt werden könnten und deren öffentliche Existenz regelmäßig über Certificate-Transparency-Protokolle, Zertifikatsregister oder vergleichbare Quellen erkennbar ist. Von der Anwendung verwendete Domains sind dabei die DNS-Namen, über die die Anwendung selbst, ihre Schnittstellen, Weiterleitungen, Mandantenbereiche oder technische Begleitdienste erreichbar sind, etwa Web-Frontends, API-Endpunkte, CDN- oder Load-Balancer-Namen; fachlich wird häufig von application domains, hostnames, FQDNs oder DNS names gesprochen. Die Vorschrift zielt darauf ab, ungewöhnliche oder unberechtigte Zertifikatsausstellungen frühzeitig erkennbar zu machen, weil eine solche Ausstellung auf Fehlkonfigurationen, kompromittierte DNS-Kontrolle, Missbrauch einer Validierungsmethode oder Vorbereitungen für Phishing- und Man-in-the-Middle-Szenarien hinweisen könnte. Eine entsprechende Beobachtung kann die Zeit bis zur Erkennung verkürzen und ermöglichen, betroffene Domains, Zertifizierungsstellen, DNS-Einträge oder Validierungswege gezielt zu prüfen, bevor Nutzende oder technische Clients einer täuschend echt wirkenden Gegenstelle vertrauen. Hierzu ist es sinnvoll Abfragen öffentlicher Certificate-Transparency-Logs für definierte FQDNs und Wildcards, Alarmierungen bei neuen Zertifikaten außerhalb erwarteter Aussteller oder Namensmuster, sowie regelmäßige Abgleiche einer gepflegten Domainliste mit neu beobachteten Zertifikatseinträgen zu verwenden.
