---
title: "KONF – Konfiguration"
description: "Die Praktik Konfiguration stellt sicher, dass IT-Komponenten – wie Anwendungen und IT-Systeme – gemäß den festgelegten Informationssicherheitsrichtlinien eingerichtet und kontinuierlich gepflegt werden, um Sicherheitslücken durch fehlerhafte oder unsichere Einstellungen zu vermeiden."
---

Die Praktik Konfiguration stellt sicher, dass IT-Komponenten – wie Anwendungen und IT-Systeme – gemäß den festgelegten Informationssicherheitsrichtlinien eingerichtet und kontinuierlich gepflegt werden, um Sicherheitslücken durch fehlerhafte oder unsichere Einstellungen zu vermeiden. Dies umfasst auch die nachvollziehbare Erstellung und Fortführung der Dokumentation.

## KONF.1 Grundlagen

### KONF.1.1 – Verfahren und Regelungen

**Pflicht:** MUSS · **Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18

> Konfiguration MUSS Verfahren und Regelungen zum Konfigurationsmanagement verankern.

Die Umsetzung kann in einem eigenen Prozess, oder integriert in andere Prozesse und Aufgaben erfolgen. Die bei der Festlegung des Verfahrens im Einzelnen zu berücksichtigenden Inhalte ergeben sich aus den Anforderungen dieser Praktik.

#### KONF.1.1.1 – Dokumentation

**Pflicht:** MUSS · **Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18

> Konfiguration MUSS die Verfahren und Regelungen dokumentieren.

Ohne eine Dokumentation könnte die Einhaltung der Verfahren und Regelungen von der Tagesform oder dem individuellen Wissen einzelner Mitarbeiter abhängen, was zu inkonsistenten Entscheidungen und Fehlern führen könnte; insbesondere beim Ausscheiden eines langjährigen Administrators könnte wertvolles prozessuales Wissen verloren gehen. Eine klare Dokumentation sichert die Verbindlichkeit und Wiederholbarkeit und dient als unverzichtbare Grundlage für die Einarbeitung neuer Kollegen, für die Durchführung von Audits und zur einheitlichen Anwendung der Regeln in der gesamten Institution. Die Dokumentation kann in einem eigenständigen Dokument als Richtlinie erfolgen, aber auch als Abschnitt in einem bereits bestehenden Dokument oder über die digital strukturiere Erfassung von Maßnahmen zur Umsetzung der Anforderungen, etwa über eine Software zum Management der Informationssicherheit. Sinnvoll ist es Ort und Struktur der Dokumentation an der jeweiligen Zielgruppe, d.h. den für das Management und die Umsetzung verantwortlichen Personen oder Rollen, auszurichten.

#### KONF.1.1.2 – Zuweisung der Aufgaben

**Pflicht:** MUSS · **Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18

> Konfiguration MUSS die mit den Verfahren und Regelungen verbundenen Aufgaben *[zuständigen Personen oder Rollen]* zuweisen.

Die Zuweisung von Aufgaben bezeichnet die eindeutige und verbindliche Übertragung von konkreten Tätigkeiten und Verantwortlichkeiten des Änderungsprozesses, wie etwa die Risikobewertung, die technische Umsetzung oder die finale Freigabe, an definierte Stellen in der Institution. Der Sinn dieser Vorschrift ist es, die Verantwortlichkeit ("Accountability") für jeden einzelnen Schritt im Prozess klarzustellen. Ohne eine solche Zuweisung könnten kritische Prüfungen unterbleiben, weil sich niemand explizit zuständig fühlt, was wiederum die Wahrscheinlichkeit fehlgeschlagener Änderungen erhöht. Eine klare Regelung kann sicherstellen, dass keine Aufgaben übersehen werden und jede Tätigkeit von einer dafür qualifizierten und befugten Stelle ausgeführt wird, was die Prozesssicherheit signifikant erhöht. Eine bewährte Methode zur Umsetzung ist die Erstellung einer RACI-Matrix (Responsible, Accountable, Consulted, Informed), die tabellarisch für jeden Prozessschritt darstellt, wer für die Durchführung verantwortlich ist, wer die Gesamtverantwortung trägt, wer zu konsultieren und wer zu informieren ist. Diese Zuständigkeiten können auch direkt in einem Workflow- oder Ticketsystem abgebildet werden, sodass Aufgaben, wie beispielsweise Genehmigungsschritte, automatisch an die richtige Gruppe oder Person weitergeleitet werden. Sinnvoll ist es die Zuweisung anhand von Rollen (z.B. "Anwendungsverantwortlicher", "Netzwerkadministrator", "Change Manager") vorzunehmen, statt an konkrete Personen. Dieser Ansatz stellt sicher, dass die Prozesse auch bei Personalwechseln stabil weiterlaufen, da die Zuständigkeit an die Funktion und nicht an das Individuum gebunden ist.

#### KONF.1.1.3 – Bekanntgabe

**Pflicht:** MUSS · **Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.31

> Konfiguration MUSS die zuständigen Personen oder Rollen über die Verfahren und Regelungen informieren.

Wenn die Zuständigen die etablierten Verfahren nicht kennen, besteht die Gefahr, dass diese – sei es aus Unwissenheit oder Bequemlichkeit – umgangen werden, was die Schutzwirkung des gesamten Managementsystems untergräbt. So könnte ein neuer Systemadministrator eine weitreichende Konfigurationsänderung vornehmen, ohne den vorgeschriebenen Genehmigungsprozess zu durchlaufen, was zu einem unbemerkten Sicherheitsrisiko führen könnte. Eine gezielte Information kann hingegen die Akzeptanz der Regelungen fördern und sicherstellen, dass alle Beteiligten ihre Rolle im Prozess verstehen und die Abläufe korrekt anwenden. Zur Umsetzung ist es sinnvoll die Dokumentation im Rahmen eines Onboarding-Prozesses bekanntzugeben und bei allen Änderungen eine automtatische Benachrichtigung aller zuständigen Personen oder Rollen anzustoßen.

### KONF.1.2 – Regelmäßige Überprüfung

**Pflicht:** MUSS · **Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.29

> Konfiguration MUSS die Verfahren und Regelungen *[regelmäßig]* und anlassbezogen auf Aktualität überprüfen.

Eine geplante der etablierten Verfahren und Regelungen dient dazu festzustellen, ob diese noch wirksam, effizient und an die aktuellen Gegebenheiten angepasst sind. Eine anlassbezogene Überprüfung wird durch spezifische Ereignisse ausgelöst, wie etwa einen schwerwiegenden Sicherheitsvorfall, eine strategische Neuausrichtung der IT oder neue gesetzliche Anforderungen. Der Zweck dieser Anforderung ist es, die kontinuierliche Verbesserung und Anpassungsfähigkeit des Prozesses sicherzustellen, da veraltete Regelungen neuen technologischen Entwicklungen oder Bedrohungen nicht mehr gerecht werden könnten; ein vor Jahren für monolithische Anwendungen konzipierter Prozess ist beispielsweise für agile Entwicklungsmethoden oder Microservice-Architekturen ungeeignet. Die regelmäßige Überprüfung kann die Effektivität des Sicherheitsmanagements langfristig aufrechterhalten und die Resilienz der Institution stärken.

### KONF.1.3 – Management von Werkzeugen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.20

> Konfiguration SOLLTE verwendete Konfigurationswerkzeuge einschließlich Verwendungszweck und Herkunft dokumentieren.

Der Begriff Konfigurationswerkzeuge bezeichnet in diesem Zusammenhang alle technischen Hilfsmittel, mit denen Systemeinstellungen erstellt, verändert oder verwaltet werden – beispielsweise Skriptsprachen, Automatisierungs-Frameworks, Versionsverwaltungswerkzeuge oder grafische Konfigurationsoberflächen. Unter Verwendungszweck wird verstanden, welche Funktion das jeweilige Werkzeug innerhalb des Betriebs erfüllt, etwa für automatisierte Serverbereitstellung, Netzwerkkonfiguration oder Datenbankparametersteuerung. Mit Herkunft ist die Herkunft des Werkzeugs gemeint, d. h. ob es sich um Eigenentwicklungen, quelloffene Software oder kommerzielle Produkte handelt und aus welchen Quellen diese bezogen werden. Die Dokumentation dieser Punkte kann Transparenz schaffen und Nachvollziehbarkeit erhöhen, wodurch Fehlkonfigurationen oder Manipulationen schneller erkannt werden können. Ohne klare Übersicht könnte unklar bleiben, mit welchen Mitteln kritische Systeme verändert wurden, was die Ursachenanalyse im Störungsfall erheblich erschweren könnte. Eine saubere Dokumentation kann verhindern, dass nicht vertrauenswürdige oder nicht mehr gepflegte Werkzeuge unbemerkt im Betrieb verbleiben und so potenzielle Angriffsvektoren entstehen. Für die Umsetzung kann die Institution eine strukturierte Werkzeugliste führen, in der pro Eintrag neben Name, Version und Hersteller auch Zweck und Beschaffungsquelle vermerkt werden. Diese Liste kann in einem Konfigurations- oder Inventarsystem gepflegt werden, sodass Aktualisierungen automatisiert oder zumindest standardisiert erfolgen können. Praktisch kann es helfen, jedes neue Werkzeug vor Einsatz über ein Freigabeverfahren einzutragen und zu kennzeichnen, ob es intern geprüft wurde. Eine einfache Möglichkeit besteht darin, bestehende Versionskontrollsysteme oder zentrale Wiki-Seiten zu nutzen, die alle relevanten Informationen versioniert und nachvollziehbar speichern können. Dies kann auch durch eine Markierung der administrativen Werkzeuge im Inventar der Anwendungen umgesetzt werden.

### KONF.1.4 – Einschränkung des Zugriffs auf Dokumentation

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.19, G 0.22, G 0.46

> Konfiguration SOLLTE den Zugriff auf dokumentierte Konfigurationen einschränken.

„Dokumentierte Konfigurationen“ sind hierbei festgehaltene Einstellungen von IT-Systemen, Anwendungen, Netzwerken oder Sicherheitskomponenten, die in schriftlicher oder elektronischer Form vorliegen und den Sollzustand einer IT-Umgebung definieren. Der Zweck der Vorschrift liegt darin, die Integrität und Vertraulichkeit solcher Konfigurationsinformationen zu schützen. Ein unkontrollierter Zugriff könnte beispielsweise dazu führen, dass ein Unbefugter Passworteinstellungen oder Firewall-Regeln manipuliert. Aus der Konfiguration von IT-Systemen könnte ein Angreifer zudem wichtige Informationen zu möglichen Schwachstellen ablesen (z.B. bei technisch notwendiger Verwendung schwacher Verschlüsselungsalgorithmen oder unsicherer Authentisierungsprotokolle wie NTLM). Ein strikter Zugriffsschutz (z.B. durch restriktive Berechtigungen oder Verschlüsselung) verhindert den unberechtigten Zugriff zu diesen sensiblen Informationen. Praktisch hilfreich kann auch sein, Konfigurationen verschlüsselt abzulegen und bei elektronischen Repositories sogenannte „Branch Protection“-Mechanismen einzusetzen, sodass Änderungen nur über geprüfte Freigabeprozesse übernommen werden können. Auf Papier vorliegende Konfigurationen kann die Institution in verschlossenen Schränken oder Archiven mit eingeschränktem Personenkreis verwahren.

### KONF.1.5 – Verschlüsselung von Konfigurationsgeheimnissen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.19

> Konfiguration SOLLTE Konfigurationsgeheimnisse verschlüsseln.

Konfigurationsgeheimnissen sind sensitive, nicht-öffentliche Daten, die von Systemen, Applikationen oder Diensten zur Laufzeit benötigt werden, um auf andere Ressourcen zuzugreifen oder ihre eigene Funktionalität sicherzustellen. Bekannte Beispiele sind Anmeldeinformationen wie Passwörter, Datenbank-Verbindungszeichenfolgen (Connection Strings), API-Schlüssel oder private Schlüssel von Zertifikaten; im Englischen wird hierfür übergreifend der Fachbegriff Secrets verwendet. Der Zweck dieser Vorschrift ist die Sicherstellung der Vertraulichkeit dieser hochsensiblen Informationen. Ungeschützt im Klartext hinterlegt, könnte ein Angreifer bei einem unautorisierten Zugriff auf Konfigurationsdateien, Quellcode-Verzeichnisse oder Backups diese Geheimnisse direkt auslesen und damit weitreichenden Zugriff auf angebundene Systeme oder Daten erlangen.

## KONF.2 Konfiguration von Systemen

### KONF.2.1 – Grundkonfiguration für Systeme

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18

> Konfiguration für IT-Systeme SOLLTE eine Grundkonfiguration dokumentieren.

Eine Grundkonfiguration (engl. baseline configuration) bezeichnet hier einen dokumentierten Ausgangszustand, der alle sicherheitsrelevanten Einstellungen, Dienste und Komponenten umfasst und als verbindlicher Referenzpunkt für den Betrieb und die Härtung dient. Sie stellt damit eine Art „Zielzustand“ dar, anhand dessen spätere Änderungen überprüft oder Abweichungen erkannt werden können. Ohne eine solche Referenz könnte es bei Installationen, Updates oder Wiederherstellungen zu unsicheren Abweichungen kommen, etwa wenn unnötige Dienste aktiv bleiben, Standardkonten nicht deaktiviert sind oder Kommunikationsschnittstellen unkontrolliert offenstehen; umgekehrt kann eine saubere Grundkonfiguration sicherstellen, dass Systeme konsistent, nachvollziehbar und auf Basis etablierter Sicherheitsanforderungen betrieben werden. Hierzu gehört z.B. die Konfiguration der Uhrensychronisation, von DNS und Verzeichnisdiensten, die Änderung von Default-Zugangsdaten oder der automatische Abruf benötigter Lizenzen. Die Umsetzung einer Grundkonfiguration kann durch verschiedene Maßnahmen unterstützt werden: (1) Es ist sinnvoll, Herstellerdokumentationen zu sichten und empfohlene Härtungseinstellungen (z. B. Deaktivierung unsicherer Protokolle) als Ausgangspunkt zu übernehmen. (2) Ergänzend können Empfehlungen des BSI oder Benchmarks wie die CIS Benchmarks herangezogen werden, um systematisch sicherheitskritische Parameter zu prüfen und einzupflegen. (3) Für komplexe Umgebungen kann ein Konfigurationsskript oder ein Automatisierungs-Tool (z. B. Ansible, Puppet, Chef) genutzt werden, um eine reproduzierbare Baseline einzuspielen und Abhängigkeiten der Komponenten konsistent zu berücksichtigen. Auf diese Weise kann die Institution sicherstellen, dass jede Installation oder Wiederherstellung eines Systems auf einer überprüfbaren und einheitlichen Basis erfolgt.

#### KONF.2.1.1 – Versionierung der Systemkonfiguration

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.45

> Konfiguration für IT-Systeme SOLLTE eine Versionierung vorheriger Konfigurationen verankern.

Die Versionierung bezeichnet hier die strukturierte Nachvollziehbarkeit von Änderungen an Konfigurationen, also das Speichern, Dokumentieren und bei Bedarf Wiederherstellen älterer Zustände eines IT-Systems. Sie unterscheidet sich von einem einfachen Backup dadurch, dass nicht nur eine Kopie vorliegt, sondern explizit eine fortlaufende Historie mit Vergleichen, Rücksetzpunkten (rollback points) und optional Kommentaren geführt wird. Der Zweck liegt darin, dass eine ungewollte oder fehlerhafte Anpassung an einer Konfiguration im Betrieb schnell erkannt und – wenn erforderlich – präzise auf einen definierten, funktionsfähigen Zustand zurückgesetzt werden kann. Ohne eine solche Versionierung könnte eine fehlerhafte Änderung unbemerkt bleiben oder nur schwer rückgängig gemacht werden. Praktisch umgesetzt kann dies z. B. durch den Einsatz von Konfigurationsmanagement-Tools erfolgen, die automatisch Änderungen versionieren und mit Prüfsummen sichern. Alternativ kann eine Institution auch Konfigurationsdateien regelmäßig in ein Versionsverwaltungssystem wie Git einspielen. Zusätzlich kann es hilfreich sein, Konfigurationsänderungen über standardisierte Änderungsprozesse einzupflegen, sodass jede Anpassung nachvollziehbar protokolliert wird. Eine weitere Möglichkeit kann die Einrichtung von Skripten sein, die Konfigurationsstände automatisch aus Geräten exportieren und revisionssicher ablegen. Zur Umsetzung können Anwendungen zur Geheimnisverwaltung, oft als Secrets-Manager oder Vault bezeichnet, eingesetzt werden. Solche Anwendungen speichern alle Geheimnisse zentral und hochverschlüsselt und stellen sie erst bei Bedarf zur Laufzeit über eine authentifizierte und gesicherte Schnittstelle (API) zur Verfügung. Eine weitere, weit verbreitete Praxis ist die Auslagerung von Secrets aus den Konfigurationsdateien in Umgebungsvariablen (Environment Variables) des ausführenden Systems, wodurch eine strikte Trennung von Code und Konfiguration erreicht wird. Alternativ kann auch die Konfigurationsdatei selbst oder zumindest die Abschnitte, die Geheimnisse enthalten, verschlüsselt werden, wobei dies erfordert, dass der zur Entschlüsselung notwendige Schlüssel seinerseits sicher an die Applikation übergeben wird.

### KONF.2.2 – Kryptographische Verfahren in IT-Systemen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.29

> Konfiguration für IT-Systeme SOLLTE kryptographische Verfahren nach *[anerkannten Standards]* im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement aktivieren.

Kryptographie wird für die Authentifizierung, Verschlüsselung und Integritätprüfung in Systemen verwendet, z.B. bei der Verschlüsselung von Speichermedien, bei der Anmeldung am System, Transportverschlüsselung von Systemupdates oder Integritätsprüfung von Systemfunktionen. Die Formulierung "im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement" bedeutet, dass die Funktionen so zu konfigurieren sind, wie in der Praktik Berechtigung (BER) festgelegt. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Kryptographie zu finden ist.

### KONF.2.3 – Änderung von Default-Zugangsdaten

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.30, G 0.23

> Konfiguration für IT-Systeme SOLLTE die Änderung von Default-Zugangsdaten ausführen.

"Default-Zugangsdaten" sind werkseitig voreingestellte Benutzername-Passwort-Kombinationen wie "root" oder "administrator", sowie vergleichbare Authentifizierungsmerkmale, die bei der Erstinbetriebnahme von IT-Systemen unverändert vorhanden sind. Diese Daten sind in der Regel öffentlich dokumentiert oder leicht im Internet auffindbar. Ihr Fortbestehen im Produktivbetrieb könnte ein erhebliches Risiko darstellen, da ein Angreifer mit minimalem Aufwand Zugriff auf Systeme erlangen könnte. Ein klassischer Vorfall könnte sein, dass ein öffentlich erreichbarer Router mit unveränderten Standardzugängen übernommen wird. Die Änderung kann demgegenüber sicherstellen, dass nur berechtigte Personen Zugriff erlangen, und kann damit unbefugte Manipulationen oder Datendiebstahl wirksam erschweren. Eine Institution kann die Anforderung umsetzen, indem bei der Inbetriebnahme jedes Systems ein Prozess etabliert wird, der die Standardzugangsdaten unmittelbar ersetzt. Dies kann beispielsweise (1) durch verpflichtende Initial-Setup-Routinen erfolgen, die eine Passwortänderung erzwingen, oder (2) durch zentrale Checklisten oder automatisierte Inventarisierung, die offene Standardzugänge identifizieren und schließen. Die Anforderung ist auch dann erfüllt, wenn diese Zugänge deaktiviert oder durch Zugänge mit von der Institution verwalteten Zugangsdaten ersetzt werden.

### KONF.2.4 – Deaktivierung nicht benötigter Systemfunktionen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.23, G 0.28

> Konfiguration für IT-Systeme SOLLTE nicht benötigte Systemfunktionen deaktivieren.

Die Deaktivierung von Funktionen, die für Betrieb oder aus Sicherheitssicht nicht benötigt werden, hilft, die Angriffsfläche und Fehlerkomplexität zu verringern, z.B. unnötige Identitäten, ggf. nicht benötigte Schnittstellen wie Bluetooth, nicht verwendete Netzprotokolle wie NTLMv1 Authentifizierung, schwache Verschlüsselungsalgorithmen wie TLS1.1, die Anzeige von Nachrichteninhalten auf dem Sperrbildschirm oder nicht benötigte System- oder Telemetriedienste. Relevant sind dabei sowohl Betriebssystem- als auch Firmwarefunktionen.

#### KONF.2.4.1 – Nicht benötigte Zertifikate

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.23, G 0.14

> Konfiguration für IT-Systeme SOLLTE nicht benötigte Zertifikate deaktivieren.

Hierbei ist insbesondere an die vom Betriebssystem als vertrauenswürdig eingestuften Zertifizierungsstellen zu denken, wenn sie nicht länger benötigt werden. Verfügt das IT-System über keine Zertifikate, so ist die Anforderung entbehrlich.

#### KONF.2.4.2 – Externe Cloud-Anbindungen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.19, G 0.23

> Konfiguration für IT-Systeme SOLLTE nicht benötigte Cloud-Anbindungen deaktivieren.

Eine Cloud-Anbindung ist eine technische Schnittstelle, über die ein IT-System Daten oder Dienste mit einer externen Cloud-Plattform austauscht. Dazu können sowohl direkte API-Integrationen wie die Anmeldung an Cloud-Verzeichnisdienste, aber auch automatische Synchronisationsmechanismen, Hintergrund-Updates über Cloud-Server oder agentenbasierte Remote-Management-Funktionen zählen. Nicht benötigte Anbindungen können dadurch identifiziert werden, dass sie weder für den produktiven Betrieb noch für Wartung, Support oder Sicherheitsfunktionen erforderlich sind. Der Sinn und Zweck dieser Regelung liegt darin, die Angriffsfläche zu reduzieren und unkontrollierte Datenflüsse zu vermeiden. Ein nicht genutzter, aber weiterhin aktiver Cloud-Connector könnte etwa unbemerkt sensible Metadaten an Drittdienste übertragen oder als Einfallstor für Schadsoftware missbraucht werden; die gezielte Deaktivierung kann dagegen unnötige Risiken eliminieren und die Übersichtlichkeit der Systemarchitektur erhöhen.

### KONF.2.5 – Überprüfung der Konfiguration

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.22, G 0.21, G 0.46, G 0.31

> Konfiguration für IT-Systeme SOLLTE die Übereinstimmung der tatsächlichen Konfiguration mit dem Referenzzustand *[regelmäßig]* überprüfen.

Referenzzustand („baseline configuration“) bezeichnet hier die dokumentierte und freigegebene Konfiguration eines IT-Systems, also die gewünschte und autorisierte Einstellung von Parametern, Diensten und Komponenten. Die tatsächliche Konfiguration ist die aktuelle technische Umsetzung dieser Einstellungen auf dem System selbst. Der Abgleich beider Zustände dient vor allem der Vermeidung von Configuration Drift – d.h. dass Systeme schleichend von der definierten Soll-Konfiguration abweichen. Dies könnte auftreten, wenn Änderungen nicht zentral dokumentiert oder automatisierte Installationen nicht einheitlich umgesetzt werden. Ohne diese Kontrolle könnte es zu unbemerkten Fehlkonfigurationen kommen, die Sicherheitslücken öffnen oder Betriebsstörungen verursachen. Durch regelmäßige Vergleiche kann eine Institution sicherstellen, dass Systeme konsistent, vertrauenswürdig und wartbar bleiben. Eine praktische Umsetzung kann auf verschiedenen Ebenen erfolgen. Technisch kann eine Institution (1) Konfigurations-Management-Werkzeuge einsetzen, die Referenzzustand-Definitionen mit Systemzuständen automatisch abgleichen, (2) Skripte oder Policies nutzen, die regelmäßig Konfigurationsdateien oder Systemeinstellungen auslesen und protokollieren, oder (3) Hash- oder Signaturverfahren anwenden, um Veränderungen an Konfigurationsdateien nachzuweisen. Prozessual kann es hilfreich sein, Änderungen zentral zu dokumentieren und automatische Reports über Abweichungen an Verantwortliche weiterzuleiten, damit diese reagieren können. Zusätzlich kann eine Institution Pilotprüfungen an Stichproben-Systemen durchführen, um die Wirksamkeit automatischer Abgleiche zu validieren. Durch diese Maßnahmen kann eine Institution eine belastbare Routine etablieren, die Configuration Drift reduziert und nicht nur technische Abweichungen sichtbar macht, sondern auch menschliche Fehler oder unautorisierte Eingriffe frühzeitig erkennen kann.

#### KONF.2.5.1 – Automatische Konfigurationsverwaltung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.31, G 0.23, G 0.21, G 0.22

> Konfiguration für IT-Systeme KANN die Überprüfung der Konfiguration durch *[einen automatisierten Mechanismus]* aktivieren.

Eine automatische Konfigurationsverwaltung ermöglicht eine einheitliche Konfiguration, z.B. für Passwortvorgaben, Verschlüsselung oder automatische Updates. Insbesondere bei der Verwaltung zahlreicher Endgeräte oder einer Bring Your Own Device Strategie (BYOD) bietet eine solche Verwaltung den einzig praktikablen Ansatz die Sicherheitsparameter der Geräte zu kontrollieren. Dies kann über selbst betriebenes zentrales Managementsystem (UEM oder MDM), Cloud-Dienste wie Intune oder Konfigurationsmanagement-Werkzeuge wie Ansible umgesetzt werden. Bei Abweichungen kann entweder ein automatisierter Mechanismus die erforderliche Konfiguration vornehmen, oder eine manuelle Entscheidung über die passende Behandlung erfolgen.

### KONF.2.6 – Automatische Konfigurationsverwaltung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.31, G 0.30, G 0.18

> Konfiguration für Endgeräte SOLLTE die Verwaltung durch ein Mobile Device Management (MDM) aktivieren.

Die Konfigurationsanforderungen für Mobile Device Management (MDM) sind im BSI-Mindeststandard für MDM umfassend beschrieben. Es ist empfehlenswert, diese Mindestanforderungen heranzuziehen. Ergänzend wird empfohlen, sicherheitsrelevante Kriterien bereits bei der Produktauswahl zu berücksichtigen, vertrauenswürdige Apps durch Reputationsdienste zu prüfen, kompromittierte Geräte (z. B. durch Jailbreak oder Root) automatisiert zu erkennen und Geofencing zur kontextbezogenen Richtliniendurchsetzung einzusetzen.

### KONF.2.7 – Souveräne Werkzeuge

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.11, G 0.18

> Konfiguration für IT-Systeme KANN Souveräne Werkzeuge installieren.

„Souveräne Werkzeuge“ sind Anwendungen, Systeme und physische Werkzeuge, die technisch, rechtlich und organisatorisch unabhängig von externen Herstellern, Cloud-Anbietern oder staatlicher Einflussnahme betrieben werden können. Das umfasst vor allem Lösungen, die lokal kontrollierbar und ohne zwingende Abhängigkeit zu externen Plattformen nutzbar sind. Der Sinn der Vorschrift liegt darin, die Handlungsfähigkeit und Sicherheit der Institution zu stärken: Ein rein cloudbasierter Konfigurationsdienst könnte durch einen plötzlichen Ausfall, eine staatlich erzwungene Sperrung oder durch nachträglich geänderte Lizenzbedingungen die Betriebsfähigkeit gefährden. Die Nutzung souveräner Werkzeuge kann dagegen die Verfügbarkeit kritischer Systeme erhöhen, die Datenhoheit bewahren und Manipulationsmöglichkeiten von Dritten minimieren. Souveräne Konfigurationssysteme machen unabhängig vor Ausfällen, Datenschutzverletzungen oder einseitigen Änderungen der Nutzungsbedingungen durch externe Dienstleister. Eine Institution kann diese Anforderung beispielsweise so umsetzen: (1) Es kann auf quelloffene Konfigurations-Frameworks zurückgegriffen werden, die lokal installiert und betrieben werden. (2) Virtualisierte oder containerisierte Varianten dieser Werkzeuge werden in der eigenen Infrastruktur betrieben, sodass keine unkontrollierten externen Abhängigkeiten entstehen. (3) Ergänzend kann ein internes Repository für Konfigurationsmodule eingerichtet werden, um eine vertrauenswürdige, geprüfte und nachvollziehbare Quellenbasis sicherzustellen.

### KONF.2.8 – Alternative Administrationszugänge

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.27, G 0.18

> Konfiguration für IT-Systeme KANN alternative Administrationszugänge installieren.

Das ist zum Beispiel von Bedeutung bei zentralen Systemen wie Firewalls und Router, bei deren Ausfall eine Fernwartung nicht mehr möglich ist. Hierzu können alternative Werkzeuge, sowie alternative Protokolle, Schnittstellen und Zugangskonten verwendet werden. Alternative Werkzeuge sind z.B. Kommandozeilenwerkzeuge, API-Schnittstellen oder die Konsole virtualisierter oder physischer Server, statt der Grafischen Benutzeroberfläche. Bei Cloud-Diensten kann dies z.B. durch Vorhalten von sowohl Browser-Zugang als auch CLI-Zugang geschehen. Alternative Zugangskonten sind z.B Break-Glass-Accounts, deren Zugangsdaten nur bei Notfällen aus einem Safe entnommen werden.

### KONF.2.9 – Abgesicherter und authentisierter Bootprozess

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.21, G 0.39

> Konfiguration für IT-Systeme KANN einen abgesicherten und authentisierten Bootprozess aktivieren.

Dies empfiehlt sich für eingebettete Systeme (Embedded Systems), indem z.B. der Bootloader die Integrität des Betriebssystems überprüft und es nur dann lädt, wenn es als korrekt eingestuft wurde. Ebenso empfiehlt es sich ein mehrstufiges Boot-Konzept mit kryptographisch sicherer Überprüfung der Einzelschritte zu realisieren, sichere Hardware-Vertrauensanker zu verwenden, bei ARM & UEFI-basierten Systemem jeweils (ARM) Secure Boot zu nutzen.

## KONF.3 Physischer Schutz

### KONF.3.1 – Kryptographischer Hardwarespeicher

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.19, G 0.21

> Konfiguration für IT-Systeme SOLLTE einen kryptographischen Hardwarespeicher aktivieren.

Ein kryptographischer Hardwarespeicher bezeichnet in diesem Kontext eine gesicherte, hardwarebasierte Komponente, die kryptographische Schlüssel oder andere besonders sensible Geheimnisse in einer isolierten und manipulationsgeschützten Umgebung verwahrt. Der Einsatz solcher Speicher kann das Risiko deutlich reduzieren, dass kryptographische Schlüssel bei einem Softwareangriff kompromittiert werden, und kann gleichzeitig die Integrität sicherheitskritischer Prozesse wie Verschlüsselung, Signatur oder Authentifizierung erhöhen. Als Standards können hierzu etwa eine Trusted Execution Environment (TEE), Secure Elements (SE) or Dedicated Security Components (DSC) infrage kommen. Vgl. ISO/IEC 11889 (TPM 2.0), ISO/IEC 19790 / FIPS 140-3 oder ETSI EN 303 645 (für IoT).

### KONF.3.2 – Speicherverschlüsselung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.19, G 0.14

> Konfiguration für IT-Systeme SOLLTE integrierte Festspeichermedien verschlüsseln.

Die Verschlüsselung von Datenträgern erschwert es Angreifern, Daten von verlorenen oder gestohlenen Geräten auszulesen. Die Verschlüsselung kann in Hard- oder Software (z.B. Windows BitLocker®, Apple FileVault®, Linux® dm-crypt) erfolgen. Für anerkannte kryptographische Algorithmen siehe BSI TR 02102.

### KONF.3.3 – SIM-PIN

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.30, G 0.16, G 0.17

> Konfiguration für IT-Systeme SOLLTE bei Mobilfunkanschluss eine SIM-PIN aktivieren.

Eine SIM-PIN ist eine persönliche Identifikationsnummer, die direkt auf der SIM-Karte gespeichert wird und beim Starten oder Einlegen der Karte abgefragt wird. Sie dient nicht der Benutzeranmeldung am Endgerät selbst, sondern schützt den Mobilfunkanschluss auf Netzebene. Ohne aktivierte SIM-PIN könnte ein Angreifer bei Verlust oder Diebstahl einer SIM-Karte unmittelbar den Mobilfunkanschluss verwenden, etwa für kostenpflichtige Anrufe oder zum Abfangen von SMS-TANs. Die Aktivierung einer SIM-PIN kann somit eine missbräuchliche Nutzung deutlich erschweren, indem ein zusätzliches Hindernis für den unbefugten Zugriff auf Mobilfunkdienste geschaffen wird. Gilt auch für stationäre Systeme mit SIM oder Systeme die eine eSIM verwenden, da eine PIN je nach Diensteanbieter SIM-Swapping vorbeugen kann. Falls das System keine SIM-Karte verwendet, ist die Anforderung entbehrlich.

### KONF.3.4 – Physischer Diebstahlschutz

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.16

> Konfiguration für Endgeräte KANN einen physischen Diebstahlschutz installieren.

Ein physischer Diebstahlschutz bezeichnet im vorliegenden Kontext sämtliche Vorrichtungen oder Maßnahmen, die ein Entwenden von Endgeräten wie Laptops, Tablets oder Arbeitsplatzrechnern erschweren. Hierzu gehören insbesondere physische Schlösser, die mithilfe eines Stahlkabels mit einer dafür vorgesehenen Öffnung am Endgerät verbunden werden können, sodass das Endgerät an einem festen Gegenstand fixiert bleibt. Der Sinn dieser Vorgabe liegt darin, das Risiko zu reduzieren, dass ein Gerät durch unbefugte Dritte entwendet und dadurch der Zugriff auf gespeicherte Informationen oder Zugangsdaten ermöglicht wird. Ein Vorfall könnte entstehen, wenn ein Angreifer ein ungesichertes Notebook während einer Konferenz oder in einem Büro mitnimmt und darüber unverschlüsselte Daten ausliest. Ein angemessen eingesetzter Diebstahlschutz kann die Gelegenheit zum Zugriff verringern, den Aufwand für einen Angreifer erhöhen und so die Wahrscheinlichkeit für den Verlust sensibler Informationen deutlich reduzieren. Zur praktischen Umsetzung kann eine Institution unterschiedliche Maßnahmen wählen. So kann ein Laptop-Kabelschloss genutzt werden, um mobile Geräte temporär an Arbeitsplätzen zu sichern, oder ein Schließfachschrank kann für Aufbewahrung außerhalb der Nutzungszeiten vorgesehen sein. Für stationäre Systeme kann eine feste Verschraubung mit dem Schreibtisch oder die Unterbringung in abschließbaren Möbeln erfolgen. Ergänzend kann eine Institution darauf achten, Geräte mit serienmäßig integrierten Vorrichtungen (z. B. Verriegelungsöffnungen für Kabelschlösser) zu beschaffen, um eine flexible Sicherung zu ermöglichen. Auch das Kennzeichnen von Geräten durch gravierte Inventarnummern oder gut sichtbare Eigentumsaufkleber kann eine zusätzliche Abschreckungswirkung entfalten.

### KONF.3.5 – Standortbestimmung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.16, G 0.17

> Konfiguration für IT-Systeme KANN eine Funktion zur Bestimmung des Standortes aus der Ferne *[durch einen automatisierten Mechanismus]* aktivieren.

Der Begriff automatisierter Mechanismus bezeichnet im gegebenen Kontext ein technisches Verfahren, das ohne manuelle Eingriffe die Standortbestimmung eines IT-Systems ermöglicht. Dies kann etwa durch GALILEO- oder GPS-Sensoren, durch WLAN- oder Mobilfunkortung, sowie durch Auswertung netzwerktechnischer Parameter erfolgen. Der Rückgriff auf die Standortbestimmung mittels Mobilfunksignal oder WLANs in der Nähe ist nur empfehlenswert, wenn das System die Satellitenbestimmung nicht unterstützt. Der Sinn dieser Vorschrift liegt darin, potenzielle Risiken durch unkontrollierte Standortänderungen oder verdeckte Verlagerungen von IT-Systemen zu reduzieren. Ein Vorfall könnte eintreten, wenn ein Server oder Endgerät unbemerkt aus einem gesicherten Bereich entfernt wird und dadurch sensible Daten oder Konfigurationen kompromittiert werden. Im positiven Fall kann die Standortbestimmung Transparenz über den Verbleib kritischer Systeme schaffen und so die Reaktionsfähigkeit bei Diebstahl oder Verlust erhöhen. Ein praktischer Ansatz kann sein, dass Systeme beim Start ihre Position automatisch protokollieren, sodass Abweichungen vom erwarteten Standort erkannt werden. Alternativ kann eine Softwarelösung eingesetzt werden, die Netzwerkverbindungen auf bestimmte Geozonen überprüft. Beachten Sie hierbei auch den Zusammenhang mit den Verfahren und Regelungen zum Informations- und Assetmanagement, sowie zur Detektion von Sicherheitsvorfällen, etwa dass Standortdaten regelmäßig in ein zentrales Monitoring-Tool eingespielt und mit erlaubten Standorten abgeglichen werden. Um technische Ressourcenauslastung und Datenschutz angemessen auszubalancieren ist es zweckmäßig dies nur für besonders schutzbedürftige Geräte vorzusehen und klar festzulegen, ob die Standortbestimmung kontinuierlich, ereignisbezogen oder stichprobenartig erfolgt.

### KONF.3.6 – Fernlöschung oder -sperre

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.16, G 0.17, G 0.30, G 0.19

> Konfiguration für Endgeräte KANN eine Funktion zur Fernlöschung oder -sperre aktivieren.

Eine automatische Fernlöschung meint hier die technische Möglichkeit, gespeicherte Daten eines Endgeräts über eine externe Steuerung dauerhaft zu entfernen, während eine Fernsperre das Gerät durch zentral initiierte Befehle unbenutzbar macht, ohne die Daten selbst zu löschen. Funktionen zur Fernlöschung (Remote Wiping) sind insbesondere relevant auf allen mobilen Endgeräten, damit bei Bedarf (z.B. wenn das Endgerät verloren geht oder gestohlen wird) alle Daten auf dem Gerät aus der Ferne gelöscht werden können. Ohne eine solche Funktion könnte ein verlorenes, vergessenes oder unzureichend zurückgesetztes Gerät Daten preisgeben oder unbefugt weiterverwendet werden. Für stationäre Endgeräte ist die Anforderung entbehrlich.

#### KONF.3.6.1 – Automatische Fernlöschung oder -sperre

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.16, G 0.30, G 0.19, G 0.17

> Konfiguration für Endgeräte KANN eine automatische Fernlöschung oder -sperre bei Inaktivität nach *[einer längeren Frist]* aktivieren.

Beide Mechanismen können bei längerer Inaktivität ausgelöst werden, also wenn ein Endgerät über einen bestimmten Zeitraum hinweg nicht mehr mit den Systemen der Institution in Kontakt steht oder nicht genutzt wird. Als angemessene Frist für eine solche Inaktivität können z. B. 30 Tage, 60 Tage oder 90 Tage definiert werden, abhängig vom Sicherheitsbedarf und der Einsatzumgebung. Dies kann verhindern, dass ungenutzte Geräte mit sensiblen Daten in Umlauf bleiben oder in falsche Hände geraten. Ein automatisches Entfernen oder Sperren kann hier das Risiko eines Datenabflusses erheblich reduzieren und gleichzeitig eine Kontrolle über den Gerätelebenszyklus sichern. Zur Umsetzung kann die Institution beispielsweise Mobile-Device-Management-Lösungen einsetzen, die nach Ablauf der gewählten Frist automatisiert Fernlöschung oder Fernsperre auslösen. Alternativ kann eine Endpoint-Security-Lösung integriert werden, die periodisch prüft, ob das Gerät eine Verbindung zum Netz herstellt, und bei Überschreiten des Schwellenwerts eine definierte Aktion anstößt. Auch ein Prozess, bei dem Inaktivität zunächst mit einer Warnmeldung angekündigt wird, bevor tatsächlich gesperrt oder gelöscht wird, kann die Benutzerfreundlichkeit erhöhen.

### KONF.3.7 – Einschränkung angeschlossener Peripherie

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.23, G 0.39, G 0.19

> Konfiguration für IT-Systeme SOLLTE angeschlossene Peripherie einschränken.

Peripherie bezeichnet angeschlossene Geräte, die über Schnittstellen wie USB, Bluetooth oder andere Ports mit dem IT-System kommunizieren. Gemeint sind sowohl physische Peripheriegeräte wie Drucker, USB-Sticks oder Netzanbindungen, als auch die Installation virtueller Peripherie z.B. virtuelle Druckertreiber. Einschränkung bedeutet hierbei, dass die Nutzung von Peripheriegeräten verhindert wird, die nicht von der Institution autorisiert wurden, abhängig vom Einsatzzweck des Systems. Der Sinn und Zweck dieser Regelung liegt darin, Angriffsflächen zu verringern und das Einschleusen oder Abfließen von Daten zu erschweren. So könnte ein unkontrollierter Anschluss externer USB-Sticks Schadsoftware einschleusen oder sensible Daten unbemerkt kopieren, während eine restriktive Konfiguration unautorisierte Datenabflüsse wirksam verhindern kann.

### KONF.3.8 – Einschränkung von Wechselmedien

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für IT-Systeme SOLLTE das automatische Einbinden von Wechselmedien einschränken.

Funktionen, die Wechselmedien automatisch einbinden und Inhalte darauf öffnen oder ausführen könnten zur unkontrollierter Verbreitung von Schadcode beitragen. Betrifft z.B. CD/DVD-Laufwerke, Bandlaufwerke oder USB-Sticks. Dies Kann umgesetzt werden, indem die Einbindung in das Betriebssystem durch spezielle Managementanwendungen blockiert wird oder auch durch systemeigene Sicherheitsfunktionen, z.B. indem alle Dateien auf Wechselmedien als nicht ausführbar markiert sind (Mount-Option „noexec“). Verfügt das IT-System über keine Anschlussmöglichkeit für Wechsellaufwerke, so ist die Anforderung entbehrlich.

## KONF.4 Vertrauenswürdige Basisdienste

### KONF.4.1 – Anbindung an Verzeichnisdienst

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.30

> Konfiguration für IT-Systeme SOLLTE die Anbindung an einen Verzeichnisdienst aktivieren.

Anbindung meint hier die Authentifizierung und Autorisierungsprüfung von Zugangskonten über einen Verzeichnisdient (häufig auch als Directory Service bezeichnet). Dies ermöglicht die zentrale Verwaltung von Identitäten und deren Berechtigungen. Dies bedeutet, dass Zugriffsrechte für alle angebundenen Systeme zentral verwaltet und bei Bedarf umgehend angepasst werden können, was die Einhaltung des Prinzips der geringsten Rechte (Principle of Least Privilege) unterstützt. Ein häufiger Ansatz zur technischen Umsetzung ist die Verwendung von Protokollen wie LDAP (Lightweight Directory Access Protocol) oder der Einsatz von Single Sign-On (SSO) Lösungen, die eine einmalige Authentifizierung des Nutzers für mehrere Systeme ermöglichen. Institutionen können dabei die Anbindung neuer Systeme durch Automatisierung im Rahmen des Provisioning-Prozesses sicherstellen, um menschliche Fehler zu reduzieren. Beispielsweise könnte ein Standard-Skript bei der Installation eines neuen Servers dessen automatische Anbindung an den Verzeichnisdient veranlassen. In Windows Betriebssystemen erfolgt die Konfiguration des Betriebssystem über entsprechende Gruppenrichtlinien (Group Policy Object) aus dem Active Directory.

#### KONF.4.1.1 – Weiterleitung von Anmeldeinformationen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.43, G 0.36

> Konfiguration für IT-Systeme SOLLTE die Weiterleitung mehrfach verwendbarer Anmeldeinformationen deaktivieren.

„Weiterleitung mehrfach verwendbarer Anmeldeinformationen“ (auch als Credential Forwarding oder Credential Delegation bezeichnet) meint Mechanismen, bei denen Anmeldeinformationen oder daraus abgeleitete Authentisierungsinformationen an ein weiteres System übertragen oder diesem zur weiteren Authentisierung zur Verfügung gestellt werden. Dadurch können auf dem Zielsystem Informationen oder Authentisierungsfähigkeiten verfügbar werden, die bei einer Kompromittierung für weitere Zugriffe missbraucht werden könnten. Die Einschränkung der Weiterleitung kann das Risiko reduzieren, dass Angreifende nach der Kompromittierung eines Systems Anmeldeinformationen oder daraus abgeleitete Authentisierungsinformationen für laterale Bewegungen verwenden. Insbesondere bei privilegierten Zugangskonten kann dadurch vermieden werden, dass wiederverwendbare Anmeldeinformationen auf weniger vertrauenswürdigen Systemen verfügbar werden. Für Remotezugriffe können Verfahren eingesetzt werden, bei denen die Anmeldeinformationen nicht an das Zielsystem übertragen werden. Beispiele unter Windows sind Remote Credential Guard oder Restricted Admin für Remotedesktopverbindungen. Bei SSH-Verbindungen kann auf die Weiterleitung des lokalen SSH-Authentisierungsagenten verzichtet werden. Wird Agent Forwarding nicht benötigt, kann dessen Verwendung client- und serverseitig eingeschränkt werden.

### KONF.4.2 – DNS-Anbindung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.22, G 0.43

> Konfiguration für IT-Systeme SOLLTE die vom System verwendeten DNS-Server autorisieren.

Autorisierte DNS-Server sind hier Resolving-Server, die von der Institution autorisiert wurden. Dies können entweder DNS-Server der Institution selbst oder externe DNS-Server zuverlässiger Anbieter sein.

#### KONF.4.2.1 – DNS-Verschlüsselung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.22, G 0.19, G 0.15

> Konfiguration für IT-Systeme SOLLTE DNS-Verbindungen durch *[einen anerkannten kryptographischen Algorithmus]* verschlüsseln.

DNS-Verschlüsselung, im Englischen oft als DNS over TLS (DoT) oder DNS over HTTPS (DoH) bezeichnet, ist ein Verfahren, bei dem Anfragen zur Namensauflösung im Internet kryptographisch geschützt werden, um deren Vertraulichkeit und Integrität sicherzustellen. Erfolgen diese Anfragen unverschlüsselt, könnte ein Angreifer im Netz die aufgerufenen Webseiten und Dienste eines Nutzers mitlesen und protokollieren. Schlimmer noch, ein Angreifer könnte die Antworten manipulieren, um den Nutzer unbemerkt auf gefälschte Webseiten umzuleiten, beispielsweise für Phishing-Angriffe. Die Aktivierung der DNS-Verschlüsselung kann einem solchen Ausspähen und Manipulieren der Namensauflösung effektiv entgegenwirken und stellt sicher, dass die Kommunikation zwischen dem Client und dem DNS-Server authentisch und nicht einsehbar ist. Nutzt das System kein DNS, so ist die Anforderung entbehrlich.

### KONF.4.3 – Authentifizierung von Fernwartungsfunktionen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.23, G 0.30

> Konfiguration für IT-Systeme SOLLTE Fernwartungsfunktionen im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement authentifizieren.

Unter Fernwartungsfunktionen versteht man technische Zugänge, die es ermöglichen, IT-Systeme aus der Ferne zu administrieren oder Fehler zu beheben, etwa über Protokolle wie RDP, SSH oder proprietäre Remote-Support-Lösungen. Fernwartungsfunktionen könnten für eine Institution erhebliche Risiken bergen, wenn ihre Nutzung nicht eindeutig authentifiziert wird. Ohne verlässliche Identitäts- und Berechtigungsprüfung könnte ein Unbefugter über eine Remote-Schnittstelle auf Systeme zugreifen, Konfigurationen manipulieren oder Schadsoftware einschleusen. Die Formulierung "im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement" bedeutet, dass die Authentifizierung so erfolgt, wie in der Praktik Berechtigung (BER) festgelegt. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Kryptographie zu finden ist.

### KONF.4.4 – Einschränkung von Fernwartungsfunktionen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.30, G 0.32

> Konfiguration für IT-Systeme SOLLTE Fernwartungsfunktionen im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement einschränken.

Fernwartungszugänge, etwa über RDP, SNMP oder Anwendungen zur Fernsteuerung des Systems erlauben typischerweise eine Vielzahl von Eingriffen in Systemkonfiguration und Datenverarbeitungen. Beispiele sind die Remote-Zwischenablage und die automatische Einbindung von Peripheriegeräten, Wechseldatenträgern und Netzlaufwerken. Unautorisierte Fernwartungszugänge könnten für Angriffe missbraucht werden. Die Formulierung "im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement" bedeutet, dass die Authentifizierung so erfolgt, wie in der Praktik Berechtigung (BER) festgelegt. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Kryptographie zu finden ist.

### KONF.4.5 – Zeitquellen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.22, G 0.43

> Konfiguration für IT-Systeme SOLLTE Zeitquellen autorisieren.

Eine einheitliche Zeitquelle für die Systemuhr (meist über NTP oder PTP) ist essenziell für die einheitliche Auswertung von Logdateien, sowie für moderne kryptographische Verfahren. Es empfiehlt sich zu definieren, welche NTP-Server von welchen NTP-Clients genutzt werden sollen und ob NTP-Server im Broadcast-Modus oder im Client-Server-Modus arbeiten. Letzteres (Client-Server) ist hierbei Best Practice. In bestimmten Fällen empfiehlt es sich außerdem, dass sich NTP-Server bei der Kommunikation gegenüber Clients authentisieren und demnach NTP-Clients nur authentifizierte NTP-Daten akzeptieren.

## KONF.5 Authentifizierung

### KONF.5.1 – Authentifizierung am System

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.18

> Konfiguration für IT-Systeme SOLLTE den Zugriff auf das System im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement authentifizieren.

Betrifft sowohl die lokale Anmeldung über eine Benutzeroberfläche als auch den Zugriff über Fernwartungsprotokolle oder -anwendungen wie RDP, SNMP, wenn diese vorhanden sind. Die Umsetzung erfolgt im einfachsten Fall durch einen Login, bzw. eine Bildschirmsperre für das IT-System. Biometrische Daten wie Fingerabdrücke können gefälscht werden und sind nicht so leicht zu ändern wie Passwörter. Setzen Sie Biometrie daher nicht als einzigen Authentifizierungsfaktor ein, sondern wenn, dann nur zur Ergänzung (Mehr-Faktor-Authentifizierung). Die Formulierung "im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement" bedeutet, dass die Authentifizierung so erfolgt, wie in der Praktik Berechtigung (BER) festgelegt. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Kryptographie zu finden ist. Die Anforderung ist entbehrlich, wenn das System keinen Zugriff auf schützenswerte Daten erlaubt, z.B. bei Nutzung als Kiosk.

#### KONF.5.1.1 – Authentifizierung an der Firmware

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.30, G 0.21

> Konfiguration für IT-Systeme SOLLTE den Zugriff auf die Firmware im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement authentifizieren.

Durch unautorisierte Änderungen an Einstellungen der Firmware (UEFI oder Embedded System) könnten Fehlerzustände entstehen oder Sicherheitsfunktionen wie TPM deaktiviert werden. Dies kann je nach Firmware durch lokale Zugangspasswörter oder zentrale Berechtigung umgesetzt werden. Hierbei sind insbesondere Einstellungen von Sicherheitsfunktionen oder der Netzanbindung relevant. Die Formulierung "im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement" bedeutet, dass die Authentifizierung so erfolgt, wie in der Praktik Berechtigung (BER) festgelegt. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Kryptographie zu finden ist.

#### KONF.5.1.2 – Pre-Boot-Authentifizierung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.30, G 0.19

> Konfiguration für Endgeräte KANN den Zugriff vor dem Start des Betriebssystems authentifizieren.

Diese Authentifizierung vor dem Start, oft als "Pre-Boot Authentication" (PBA) oder "Hardware-based Authentication" bezeichnet, verhindert, dass ein Gerät gestartet wird, bevor sich Nutzende mit Anmeldeinformationen, wie zum Beispiel einem Passwort oder einem biometrischen Merkmal, autorisiert haben. Ohne diese Authentifizierung könnte ein Angreifer versuchen, das Gerät direkt zu booten, die Festplatte zu kopieren oder zu manipulieren, um sensitive Daten zu extrahieren. Eine gängige Methode ist die Verwendung einer Festplattenverschlüsselung (Full Disk Encryption, FDE) mit einer Pre-Boot-Authentifizierung. Eine Institution könnte auch eine Mehr-Faktor-Authentifizierung (MFA) vor dem Start des Betriebssystems einsetzen, beispielsweise indem ein Hardware-Token oder ein biometrischer Scan zusätzlich zum Passwort erforderlich ist, was die Sicherheit weiter erhöht.

### KONF.5.2 – Keine Mehrfachanmeldung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.30, G 0.32

> Konfiguration für IT-Systeme SOLLTE die gleichzeitige Anmeldung mehrerer Zugangskonten deaktivieren.

Wenn Nutzende mit verschiedenen Identitäten simultan im System angemeldet sind, erhöht sich das Risiko von versehentlichen Datenvermischungen oder Falscheingaben deutlich. Dies kann besonders in sensiblen Bereichen wie im Finanzwesen oder Gesundheitswesen schwerwiegende Folgen haben, wo vertrauliche Kundendaten oder Patienteninformationen unbeabsichtigt zwischen verschiedenen Kontexten übertragen werden könnten. Bei Vorfällen wird so auch erschwert herauszufinden, von welchem Zugangskonto bestimmte Ereignisse stammen.

## KONF.6 Rollen und Berechtigungen

### KONF.6.1 – Minimal erforderliche Berechtigungen für Anwendungen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.32, G 0.30

> Konfiguration für IT-Systeme SOLLTE erforderliche Berechtigungen für Anwendungen einschränken.

Ziel ist es, Angriffsflächen zu minimieren und unerwünschte Seiteneffekte zu vermeiden. Durch restriktive Rechtevergabe pro App lässt sich das Risiko für Zugriffe auf sensible Bereiche stark senken. Gleichzeitig trägt dieses Prinzip dazu bei, eine klare Trennung zwischen den einzelnen Systemkomponenten zu bewahren und unkontrollierte Wechselwirkungen zu verhindern. Beispiele sind Lese- und Schreibrechte für Verzeichnisse, insbesondere für Systemverzeichnisse, Berechtigungen zum Zugriff auf Sensoren oder Peripheriegeräte, sowie der Netzzugriff. Um die Umsetzung zu erleichtern können Berechtigungsprofile erstellt werden, die je nach Anwendungsklasse (z. B. Office, Multimedia, Tools) eine Basislinie an Privilegien definieren. Diese Profile können in einer zentralen Verwaltungssoftware (z. B. über Gruppenrichtlinien oder ein Mobile‑Device‑Management) hinterlegt und automatisch auf neue Installationen angewendet werden. Vor der Freigabe einer Softwareinstallation kann ein Reviewprozess etabliert werden, bei dem anhand von Funktionsdokumentationen geprüft wird, welche minimalen Rechte erforderlich sind. Darüber hinaus kann der Einsatz von Sandboxing- oder Virtualisierungstechnologien unterstützen, indem Anwendungen in einer isolierten Umgebung mit genau festgelegten Schnittstellen betrieben werden können. Tools zur Rechteanalyse (etwa zur Ermittlung der tatsächlich genutzten APIs und Dateizugriffe) können helfen, überflüssige Freigaben im Nachgang weiter einzuschränken.

#### KONF.6.1.1 – Datenkapselung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.19, G 0.22

> Konfiguration für IT-Systeme KANN Datenkapselung aktivieren.

Bei der Datenkapselung, im Englischen als data encapsulation bekannt, handelt es sich um einen Schutzmechanismus, bei dem Daten logisch vor dem Zugriff des restlichen Systems verborgen werden. Hierdurch wird der direkte Zugriff unterbunden und ausschließlich über definierte, sichere Schnittstellen bereitgestellt. Zweck ist es, die Angriffsfläche auf sensible Daten zu verringern und deren Integrität sowie Vertraulichkeit zu wahren. Ohne eine solche Kapselung könnte beispielsweise eine Schadsoftware auf einem Server direkt auf Konfigurationsdateien oder im Arbeitsspeicher gehaltene Anmeldeinformationen anderer Anwendungen zugreifen und diese manipulieren oder ausleiten. Durch eine wirksame Datenkapselung kann die Institution sicherstellen, dass Zugriffe nur über vorab genehmigte und protokollierte Wege erfolgen, was eine unautorisierte Modifikation oder einen unbemerkten Abfluss von Daten erschwert. Technisch erfolgt dies zum Beispiel durch einen abgeschlossenen Speicherbereich auf einem mobilen Gerät für persönliche Informationen wie Kontakte oder Kalender (PIM-Container). Die Kapselung erfordert eine separate Authentisierung vor dem Zugriff auf die gekapstelten Daten und eine vom Betriebssystem unabhängige Daten- & Transportverschlüsselung innerhalb der Kapselung.

#### KONF.6.1.2 – Isolierung von Anwendungen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für IT-Systeme KANN die Isolierung von *[bestimmten Anwendungen]* aktivieren.

Die Isolation von Anwendungen (auch Application Sandboxing oder Application Confinement genannt) kann die Auswirkungen von Fehlfunktionen oder einer Kompromittierung auf andere Anwendungen und Systemressourcen begrenzen. Hierzu werden Zugriffe einer Anwendung auf beispielsweise Prozesse, Dateisystembereiche, Netzwerkressourcen oder Geräte auf die für ihren Betrieb vorgesehenen Ressourcen und Schnittstellen beschränkt. „Bestimmte Anwendungen“ bezeichnet die Anwendungen, für die aufgrund ihres Einsatzzwecks oder der damit verbundenen Risiken eine isolierte Ausführung vorgesehen ist. Die Isolation kann mit unterschiedlichen technischen Mechanismen umgesetzt werden. Hierzu zählen beispielsweise Betriebssystemfunktionen zur Zugriffsbeschränkung wie SELinux- oder AppArmor-Profile, containerbasierte Isolation oder die Ausführung in virtuellen Maschinen. Die verschiedenen Verfahren bieten unterschiedliche Isolationsstärken. Container teilen sich typischerweise den Kernel des Hostsystems, während virtuelle Maschinen zusätzlich über ein eigenes Gastbetriebssystem und einen eigenen Kernel gegenüber dem Hostsystem abgegrenzt sind.

#### KONF.6.1.3 – Isolierte Arbeitsumgebungen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.19, G 0.31

> Konfiguration für Endgeräte KANN die Isolation verschiedener Arbeitsumgebungen für verschiedene Verwendungen aktivieren.

Verschiedene Verwendungen sind z.B. die berufliche und private Nutzung, oder die Nutzung als IT-System mit erhöhtem Schutzbedarf und das Surfen im Internet. Arbeitsumgebungen sind getrennt, wenn die zu schützenden Daten ausschließlich in der geschützten Umgebung verbleiben. Beispielimplementierungen sind Apple® Configuration Profile oder Android™ Work Profile. Je nach Aufbau des Systems können hierzu z.B. Trennung auf Betriebssystemebene, netzbasierte Trennung, Virtualisierung oder Container eingesetzt werden.

### KONF.6.2 – Gemeinsam genutzte Verzeichnisse

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.19, G 0.30

> Konfiguration für Dateiserver SOLLTE die Zugriffsrechte gemeinsam verwendeter Verzeichnisse einschränken.

Relevant sind hierbei sowohl speziell eingerichtete Verzeichnisse für die gemeinsame Bearbeitung von Dateien als auch Verzeichnisse, die vom System für gemeinsame Dateien verwendet werden, z.B. /tmp. Unter Linux kann das Sticky-Bit verwendet werden, um den Zugriff auf die Dateien in diesem Verzeichnis einzuschränken, so dass nur noch der Eigentümer einer Datei (oder der Eigentümer des Verzeichnisses) diese Datei löschen oder umbenennen darf.

### KONF.6.3 – Kiosk-Modus

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.19, G 0.46

> Konfiguration für Endgeräte KANN das automatische Zurücksetzen auf einen definierten Zustand nach der Nutzung aktivieren.

Ein Kiosk‑Modus (auch als Gast-Zugang bezeichnet) kann dazu dienen, die Integrität und den definierten Ausgangszustand eines Systems dauerhaft sicherzustellen, indem nach jeder Sitzung oder in regelmäßigen Abständen ein vollständiger Rücksetzvorgang angestoßen wird. Damit soll verhindert werden, dass ungewollte Änderungen – etwa durch Malware, böswillige Manipulation oder versehentlich abgelegte Nutzerdaten – dauerhaft auf dem System verbleiben. Gleichzeitig kann so gewährleistet werden, dass jede neue Nutzer­session in einer standardisierten, getesteten Umgebung beginnt, was sowohl den Support‑Aufwand reduziert als auch Datenschutzaspekte stärkt, da keine personenbezogenen Daten auf dem Gerät zurückbleiben können. Typische Anwendungsfälle können öffentliche Terminals in Bibliotheken oder Behörden, digitale Informations­stelen in Museen und Einkaufszentren sowie Schulungs‑ oder Präsentationsrechner in Unternehmen sein. In solchen Szenarien kann das System beim Ausloggen oder nach einer festgelegten Zeit (z. B. nachts) automatisch auf ein sauberes Basis-Image zurückgesetzt werden. Denkbar ist auch ein Einsatz in Fabrikumgebungen, um Versuchs‑ und Prüfsysteme immer wieder in einen definierten Ausgangszustand zu bringen, oder in Testlaboren für Software, wo nach jedem Testlauf eine reine Umgebung erforderlich ist. Für die produktneutrale Umsetzung kann man beispielsweise mit Virtualisierungs­technologien arbeiten, die mittels Snapshot‑Rollback beim Neustart eine saubere VM‑Instanz bereitstellen. Alternativ kann ein Live‑Betriebssystem vollständig im Arbeitsspeicher laufen oder das Dateisystem über Overlay‑Techniken (z. B. OverlayFS, AUFS) nur virtuell überschrieben werden – alle Änderungen verwerfen sich beim Neustart automatisch. Auch der Einsatz von read‑only‑Partitionen kombiniert mit einem Schreibbereich in RAM kann eine einfache Lösung sein. Skript­basierte Cron‑Jobs oder Systemd‑Timer können den Rücksetz­prozess zu definierten Zeiten anstoßen. Externes Logging und Konfigurations­management (etwa über Ansible oder Puppet) kann dabei helfen, wichtige Ereignisse und Konfigurations­änderungen zu protokollieren, ohne den Kiosk‑Modus zu beeinträchtigen.

### KONF.6.4 – Privilegierte Systemfunktionen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.32, G 0.30

> Konfiguration für IT-Systeme SOLLTE privilegierte Funktionen einschränken.

Sind privilegierte Funktionen nicht eingeschränkt, so könnten Innentäter oder Angreifer über das Netz unbefugte Manipulationen vornehmen, Fehlkonfigurationen ausgelöst werden oder sich Schadcode automatisch einnisten. Privilegierte Funktionen können z.B. ein lokales Berechtigungsmanagement, die Installation von Anwendungen, der Schreibzugriff auf Systemverzeichnisse oder die Änderung der Systemkonfiguration sein.

#### KONF.6.4.1 – Rollenbasierte Privilegierung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.30, G 0.32

> Konfiguration für IT-Systeme KANN rollenbasiertes Berechtigungsmanagement aktivieren.

Rollenbasierte Administration schränkt die Berechtigungen administrativer Zugangskonten anhand von Rollen so ein, dass nur die jeweils erforderlichen Funktionen freigeschaltet sind. Dies kann z.B. mit Windows PowerShell Just Enough Administration (JEA) oder SELinux, AppArmor oder Sudoers umgesetzt werden.

### KONF.6.5 – Dynamische Zugriffskontrolle im System

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.32, G 0.30

> Konfiguration für IT-Systeme KANN dynamische Zugriffskontrolle im System aktivieren.

Eine dynamische Zugriffskontrolle (engl. Dynamic Access Control, DAC) bezeichnet ein Verfahren, bei dem Zugriffsentscheidungen nicht ausschließlich auf statischen Berechtigungen (z. B. Benutzerrollen oder ACLs) beruhen, sondern zusätzlich kontextabhängige Bedingungen wie Gerätezustand, Sensitivität der Daten, Standort, Zeitfenster oder Sicherheitsklassifikation auswerten. Dabei bleibt die Policy, also die zugrundeliegende Regelmenge zur Zugriffsbewertung, fest definiert und nachvollziehbar dokumentiert – lediglich die Entscheidung über den konkreten Zugriff erfolgt dynamisch anhand dieser Bedingungen. Ziel ist eine feinere Steuerung des Datenzugriffs auf Basis aktueller Risikosituationen, ohne dass Administratoren Berechtigungen manuell anpassen müssen. Solche Mechanismen können etwa verhindern, dass ein Benutzer sensible Daten von einem nicht verwalteten Endgerät ausliest, während er im internen Netz regulär Zugriff hätte. Da DAC komplex sein kann ist es zweckmäßig, auch auf Funktionen zur Auditierung und Protokollierung der DAC zu achten.

### KONF.6.6 – Getrennte Datenhaltung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.19, G 0.30

> Konfiguration für Anwendungen SOLLTE Zugriffe eines Zugangskontos auf Daten anderer Zugangskonten einschränken.

Dies kann je nach Anwendung z.B. durch eine in der Anwendung integrierte Rollen- und Rechteverwaltung, Zugriffsrechte auf Dateisystemebene oder durch die Verwendung unterschiedlicher Systeme oder Netze pro Zugang realisiert werden.

#### KONF.6.6.1 – Mandantenfähigkeit

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.19, G 0.22

> Konfiguration für Anwendungen SOLLTE wenn die Anwendung mehrere Mandaten bedient, für jeden Mandanten eine eigene Berechtigungskonfiguration aktivieren.

Der Ausdruck "mehrere Mandanten" (im Englischen auch multi-tenancy genannt) bezieht sich auf eine Softwarearchitektur, bei der eine einzige Instanz einer Anwendung gleichzeitig die Bedürfnisse mehrerer, voneinander unabhängiger Kundengruppen (Mandanten) bedient. Eine eigene Berechtigungskonfiguration bedeutet, dass jeder Mandant eine separate, von den anderen getrennte Sammlung von Zugriffsregeln und -rechten erhält. Dies dient dem Schutz vor Datenlecks, da ein Angreifer, der sich unrechtmäßig Zugang zu einem Mandanten verschafft, dadurch nicht automatisch die Berechtigungen für andere Mandanten übernimmt. Eine separate Konfiguration kann verhindern, dass ein Fehlverhalten oder eine Fehlkonfiguration bei einem Mandanten die Sicherheit aller anderen beeinträchtigt. Technische Möglichkeiten hierfür sind die Verwendung von mandantenspezifischen Datenbank-Schemata oder die logische Trennung von Daten innerhalb einer gemeinsamen Datenbank durch Mandanten-IDs. Darüber hinaus kann die Institution sicherstellen, dass die Authentifizierung und Autorisierung für jeden Mandanten streng getrennt sind, zum Beispiel durch die Nutzung unterschiedlicher API-Schlüssel oder Single-Sign-On-Konfigurationen pro Mandant.

### KONF.6.7 – Privilegierte Funktionen der Anwendung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.32, G 0.30

> Konfiguration für Anwendungen SOLLTE privilegierte Funktionen einschränken.

Sind privilegierte Funktionen nicht eingeschränkt, so könnten Innentäter oder Angreifer über das Netz unbefugte Manipulationen vornehmen, Fehlkonfigurationen ausgelöst werden oder sich Schadcode automatisch einnisten. Privilegierte Funktionen können z.B. ein Berechtigungsmanagement der Anwendung, der Zugriff auf Daten mehrerer Zugangskonten, das Hinzufügen oder Entfernen akzeptierter X.509-Zertifikate, ein Moderationsrecht oder die Änderung der Sicherheitskonfiguration der Anwendung sein.

### KONF.6.8 – Berechtigungen des Webserver-Prozesses

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.32, G 0.30

> Konfiguration für Webserver SOLLTE die Berechtigungen des Webserver-Prozesses einschränken.

Wird der laufende Prozess über das Web kompromittiert, so verhindert eine Einschränkung der Rechte eine weitere Ausbreitung des Angriffs. Relevant sind dabei Zugriffsrechte für Dateisystem und Systemfunktionen. Zweckmäßig ist es hierzu, die Berechtigungen so einzuschränken, dass der Serverdienst a) keinen Zugriff auf Dateien außerhalb des WWW-Wurzelverzeichnisses hat, b) Schreibzugriffe innerhalb des WWW‑Wurzelverzeichnisses nur in explizit autorisierten Unter­verzeichnissen hat, c) keine Programme oder Shell‑Befehle außerhalb der vorgesehenen Interpreter ausführen kann, d) keine privilegierten Berechtigungen besitzt. Unterverzeichnisse die Schreibrechte benötigen könnten sind etwa /uploads, /cache, /tmp.

### KONF.6.9 – Zugriff auf Code

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.19, G 0.22

> Konfiguration für Webserver SOLLTE den Zugriff auf Quelldateien einschränken.

Quelldateien sind in diesem Zusammenhang alle Dateien, die zur Funktionsweise einer Webanwendung benötigt werden, deren Auslieferung an den Browser von Nutzenden aber nicht erforderlich ist. Dazu gehören Programmier- oder Skriptcode, Konfigurationsdateien, Datenbankverbindungen und sensible Daten wie APIs oder Anmeldeinformationen. Das Verhindern des direkten Zugriffs auf diese Dateien dient der Prävention von Informationslecks und der Minderung des Risikos unautorisierter Offenlegung. Eine nicht restriktive Konfiguration könnte beispielsweise die Offenlegung von Code-Teilen, die Logik der Anwendung oder sogar hartkodierten Passwörtern ermöglichen, was zu einer weitreichenden Kompromittierung des Systems führen könnte. Die Umsetzung kann durch platzieren dieser Dateien außerhalb des WWW-Wurzelverzeichnisses erfolgen. Weiterhin kann der Zugriff auf bestimmte Dateitypen wie .php, .ini, .env oder .sql mittels Webserver-Regeln (z.B. in .htaccess für Apache oder location-Blöcke in Nginx) explizit verweigert werden, wodurch auch versehentlich im öffentlichen Verzeichnis abgelegte Quelldateien geschützt sind. Bei der Wahl eines Content-Management-Systems oder Frameworks kann eine sichere Standardkonfiguration die Umsetzung erleichtern. Zusätzlich können serverseitige Skripte so konfiguriert werden, dass sie nur aus vordefinierten, sicheren Verzeichnissen ausgeführt werden dürfen, was als Secure Execution Path bekannt ist.

### KONF.6.10 – Auflistung von Verzeichnisinhalten

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.19

> Konfiguration für Webserver SOLLTE die Auflistung von Verzeichnisinhalten einschränken.

Über das Auflisten von Verzeichnisinhalten erhalten Angreifer Einblick in die interne Struktur des Systems und potenziell sensibler Daten. Zur Umsetzung kann in der Konfiguration des Webservers (z.B. Apache, Nginx) die Directory-Listing-Funktion deaktiviert werden. Alternativ kann über Dateien wie .htaccess der Zugriff auf die notwendigen Verzeichnisse eingeschränkt werden.

### KONF.6.11 – Einschränkung von Uploads

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.39, G 0.40

> Konfiguration für Webserver SOLLTE Uploads einschränken.

Uploads sind Dateien, die von Nutzenden auf den Server übertragen werden. Diese könnten Schadprogramme enthalten oder den Speicher füllen. Sinnvolle Beschränkungen sind z.B. der Upload nur nach Anmeldung, eine maximale Dateigröße, erlaubte Dateitypen und deren Speicherorte.

### KONF.6.12 – Konferenzmoderation

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.19, G 0.30

> Konfiguration für VK-Anwendungen SOLLTE bei öffentlichen Konferenzschaltungen eine Konferenzmoderation aktivieren.

Bei Konferenzen kann es vorkommen, dass ungewollt Teilnehmende zu hören sind. Dies kann versehentlich geschehen oder im Rahmen eines Angriffes.

### KONF.6.13 – Dynamische Zugriffskontrolle in der Anwendung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.32, G 0.30

> Konfiguration für Anwendungen KANN dynamische Zugriffskontrolle in der Anwendung aktivieren.

Dynamische Zugriffskontrolle („dynamic access control“, DAC) bezeichnet hier eine Form der Autorisierungsprüfung innerhalb einer Anwendung, bei der die Entscheidung über den Zugriff nicht ausschließlich anhand statischer Rollen oder Benutzergruppen erfolgt, sondern zusätzlich kontextabhängige Bedingungen („contextual attributes“) berücksichtigt werden. Solche Bedingungen können beispielsweise der aktuelle Standort der Anmeldung, die Geräteklasse, der Zeitpunkt des Zugriffs oder die Sensitivität der angeforderten Daten sein. Die zugrunde liegende Zugriffsrichtlinie („policy“) bleibt dabei fest definiert – die Dynamik betrifft ausschließlich die Bewertung der in ihr vorgesehenen Parameter. Dadurch unterscheidet sich DAC auf Anwendungsebene von klassischen „role-based access control“ (RBAC)-Mechanismen, indem sie feinere, situative Entscheidungen erlaubt, ohne dass Berechtigungen für den Einzelfall manuell vergeben werden. Die Möglichkeit, eine dynamische Zugriffskontrolle in der Anwendung zu aktivieren, kann wesentlich dazu beitragen, unbefugte oder unangemessene Zugriffe zu verhindern, wenn sich Sicherheitsbedingungen ändern. Ohne solche Mechanismen könnte ein Benutzer etwa trotz eines kompromittierten Geräts oder außerhalb sicherer Netzbereiche weiterhin auf vertrauliche Daten zugreifen, was zu Datenabfluss oder Manipulation führen könnte. Die dynamische Kontrolle kann hingegen sicherstellen, dass Zugriffe nur gewährt werden, wenn aktuelle Kontextparameter mit den definierten Sicherheitsrichtlinien übereinstimmen, wodurch das Risiko situativer Angriffe deutlich reduziert werden kann. Beispiele sind Anwendungen (1) eine Policy-Engine wie XACML-kompatible Systeme zur regelbasierten Entscheidungsfindung verwenden, (2) Attributquellen wie Identity Provider oder Endpoint-Sicherheitslösungen zur Kontextbewertung einbinden oder (3) adaptive Autorisierungsmechanismen, etwa über Open Policy Agent.

### KONF.6.14 – Browser Sandboxing

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für Webbrowser SOLLTE Browser Sandboxing aktivieren.

Sandboxing bedeutet, dass jede Instanz und jeder Verarbeitungsprozess nur auf die eigenen Ressourcen zugreifen kann. Die Isolation kann durch eigene Threads oder eigene Prozesse realisiert sein.

### KONF.6.15 – Virtualisierte Browser-Umgebung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für Webbrowser KANN Virtualisierte Browser-Umgebung aktivieren.

Eine Browser-Umgebung ist virtualisiert, wenn der Code des Browser nicht im Betriebssystem des Clients, sondern in einem dediziert hierzu virtualisierten Betriebssystem ausgeführt wird, z.B. ReCoBS.

### KONF.6.16 – Datenaustausch in der Virtualisierung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.19, G 0.23

> Konfiguration für Virtualisierungslösungen KANN den Datenaustausch zwischen virtualisierten Client einschränken.

Der Datenaustausch zwischen virtualisierten Anwendungen umfasst jegliche direkte oder indirekte Kommunikationswege wie virtuelle Netzwerke, geteilte Speicherbereiche oder Copy-and-Paste-Funktionen über die Virtualisierungsplattform. Der Sinn dieser Anforderung liegt darin, unbeabsichtigte oder böswillige Datenübertragungen zwischen isolierten Anwendungen einzuschränken. Ohne diese Einschränkungen könnte Schadsoftware von einer kompromittierten VM unbemerkt auf eine andere übergreifen oder sensible Informationen könnten durch Fehlkonfigurationen ungewollt in eine fremde VM gelangen. Eine klare Abgrenzung kann hingegen sicherstellen, dass selbst bei Kompromittierung einer Anwendung deren Wirkungskreis begrenzt bleibt und Vertraulichkeit, Integrität sowie Stabilität anderer Anwendungen erhalten bleiben. Die praktische Umsetzung kann durch mehrere Maßnahmen erfolgen, die sich technisch wie prozessual ergänzen. So kann eine Institution (1) virtuelle Netzwerke segmentieren, sodass VMs nur über explizit eingerichtete Firewalls miteinander kommunizieren können, (2) gemeinsame Speicherbereiche oder Zwischenablagen deaktivieren, sofern diese nicht zwingend benötigt werden, und (3) die Nutzung von Schnittstellen wie USB-Passthrough oder Drag-and-Drop bewusst unterbinden oder nur für klar definierte Administrations-VMs freigeben. Darüber hinaus kann es sinnvoll sein, die Konfiguration regelmäßig mit Härtungsleitfäden abzugleichen. Ein pragmatischer Tipp ist es, beim Aufsetzen neuer VMs die Standardkonfigurationen bewusst restriktiv zu wählen und nur jene Austauschfunktionen schrittweise zu aktivieren, die für den Geschäftsbetrieb wirklich erforderlich sind.

## KONF.7 Schutz vor Schadcode

### KONF.7.1 – Echtzeitscanner

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für IT-Systeme SOLLTE eine automatische Prüfung auf Schadcode bei Installation oder Öffnung von Dateien aktivieren.

Schadcode kann sich sowohl auf lokalen Speichermedien, als auch auf Netzlaufwerken oder Wechseldatenträgern befinden. Für Netzlaufwerke kann die Anforderung auch umgesetzt werden, indem Dateien bei der Speicherung auf dem zentralen System auf Schadcode geprüft werden. Die Anwendung zur Schadcodeprüfung kann z.B. auch als EDR, XDR oder IDS bezeichnet werden. Moderne Systeme zur Erkennung von Schadcode verwenden eine Kombination aus Virensignaturen, Heuristiken, als auch Anomalieerkennung. Falls das System die Installation von Anwendungen nicht unterstützt, so ist dieser Teilschritt entbehrlich.

### KONF.7.2 – Regelmäßige Scans

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für IT-Systeme SOLLTE einen regelmäßigen Scan von Dateien auf dem System nach potenziellem Schadcode aktivieren.

Schadcode kann sich sowohl auf lokalen Speichermedien, als auch auf Netzlaufwerken oder Wechseldatenträgern befinden. Für Netzlaufwerke kann die Anforderung auch umgesetzt werden, indem Dateien bei der Speicherung auf dem zentralen System auf Schadcode geprüft werden. Die Anwendung zur Schadcodeprüfung kann z.B. auch als EDR, XDR oder IDS bezeichnet werden. Moderne Systeme zur Erkennung von Schadcode verwenden eine Kombination aus Virensignaturen, Heuristiken, als auch Anomalieerkennung. Falls das System die Installation von Anwendungen nicht unterstützt, so ist dieser Teilschritt entbehrlich.

### KONF.7.3 – Host-basierte Angriffserkennung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 3 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für IT-Systeme KANN Host-basierte Angriffserkennung aktivieren.

Host-basierte Angriffserkennung, im Englischen auch als Host-based Intrusion Detection (HID) oder Host-based Intrusion Prevention (HIP) bezeichnet, bezieht sich auf Mechanismen, die auf den einzelnen IT-Systemen, wie Servern oder Workstations, selbst operieren, um böswillige Aktivitäten zu erkennen und zu verhindern. Im Gegensatz zu netzwerkbasierten Systemen, die den Datenverkehr überwachen, fokussiert sich die Host-basierte Erkennung auf interne Systemereignisse, wie die Integrität von Dateisystemen, Änderungen an kritischen Konfigurationsdateien, oder die Erkennung von unbekannten Prozessen. Der Hauptzweck dieser Anforderung besteht darin, eine zusätzliche Sicherheitsebene zu schaffen, die direkt am Endpunkt (Host) agiert, was die Erkennung von Angriffen ermöglicht, die bereits die äußeren Schutzmechanismen überwunden haben könnten, beispielsweise wenn ein Angreifer eine bekannte Schwachstelle ausnutzt, um einen Prozess mit erhöhten Rechten auszuführen. Diese Maßnahmen können dabei helfen, interne Lateralbewegungen eines Angreifers zu erkennen und somit die Ausbreitung eines Vorfalls zu verlangsamen oder zu stoppen, bevor es zu einem größeren Schaden kommt.

### KONF.7.4 – Angriffserkennung anhand von Netzverkehr

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für IT-Systeme KANN Angriffserkennung anhand von Netzverkehr aktivieren.

Hierbei wird eine netzwerkbasierte Bedrohungsanalyse direkt auf dem IT-System durchgeführt. Dieser Ansatz, oft als Host-based Network Intrusion Detection System (H-NIDS) oder Endpoint Detection and Response (EDR) bezeichnet, ermöglicht eine tiefere Sicht in das Systemverhalten. Statt nur den Datenstrom am Perimeter zu überwachen, kann so die Institution verdächtige Aktivitäten wie das Scannen von Netzwerk-Ports, den Aufbau ungewöhnlicher Verbindungen zu Command-and-Control-Servern oder den Versuch der Datenexfiltration erkennen. Ohne diese Erkennung könnte sich ein Angreifer, der bereits in das Netzwerk eingedrungen ist, unentdeckt von System zu System bewegen oder sensible Daten unbemerkt nach außen senden. Die dezentrale Erkennung auf den Clients kann zudem dabei helfen, interne Lateral-Movement-Versuche zu identifizieren, da der Datenverkehr zwischen den Systemen überwacht wird, selbst wenn er das interne Netzwerk nicht verlässt. Um diese Anforderung umzusetzen, kann die Institution spezialisierte EDR- oder Endpoint-Security-Lösungen nutzen, die eine integrierte Funktion zur Netzwerküberwachung bieten. Es kann ebenfalls eine regelbasierte Erkennung über lokale Host-Firewalls oder Sicherheitsagenten aktiviert werden, die bestimmte Muster im Netzwerkverkehr blockieren oder protokollieren. Bei der Einführung solcher Maßnahmen ist es entscheidend, die Performance des Clients zu berücksichtigen. Daher kann die Konfiguration so optimiert werden, dass sie nur kritische Protokolle oder Ports überwacht, um die Systemressourcen zu schonen.

### KONF.7.5 – Alarmierung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.39, G 0.18

> Konfiguration für IT-Systeme SOLLTE eine Benachrichtigung bei potenziellem Schadcode aktivieren.

Durch die Aktivierung einer Benachrichtigung kann eine Institution schnell auf verdächtige Aktivitäten reagieren, noch bevor sich der Schadcode vollständig im System etablieren und erheblichen Schaden anrichten könnte. Eine Möglichkeit zur Umsetzung ist der Einsatz von Endpoint Detection and Response (EDR)-Lösungen, die in der Lage sind, Verhaltensanomalien in Echtzeit zu erkennen und sofortige Benachrichtigungen auszulösen. Eine effektive Umsetzung erfordert, dass die Benachrichtigungen sowohl an die Endnutzer als auch an die zuständigen IT-Sicherheitsteams gesendet werden, um eine umfassende und koordinierte Reaktion zu ermöglichen. Dabei können Automatisierungsregeln im Security Information and Event Management (SIEM) die Benachrichtigungen an die richtigen Personen eskalieren und so die Reaktionszeit verkürzen.

### KONF.7.6 – Automatische Updates

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.39, G 0.18

> Konfiguration für IT-Systeme SOLLTE Automatische Updates der Mechanismen zur Schadcodeerkennung aktivieren.

Da Schadprogramme und Angriffsmethoden ständig abgeändert werden um bekannte Erkennungsmuster zu umgehen, sind aktuelle Erkennungsfunktionen entscheidend um laufende Angriffe erkennen zu können, z.B. Signatur-Update oder Aktualisierungen der Lernfunktion zur Anomalieerkennung. Dies kann durch automatische Aktualisierungen der Signaturen und Mechanismen zur Angriffserkennung umgesetzt werden, z.B. als tagesaktueller Download von Viren-Signaturen. Die Anforderung kann auch durch einen schrittweisen Rollout der Erkennungsfunktionen umgesetzt werden, um einen Test in der Institution zu ermöglichen.

### KONF.7.7 – Regelmäßiger Funktionstest

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.39, G 0.18

> Konfiguration für IT-Systeme KANN die Funktionsfähigkeit des Schadcodeschutzes *[regelmäßig]* überprüfen.

Die Funktionsfähigkeit des Schadcodeschutzes beschreibt den operativen Zustand der eingesetzten Schutzmechanismen (engl. Malware Protection, oft auch Antivirus oder Endpoint Detection and Response, kurz EDR), der über die reine Installation der Software hinausgeht. Sie umfasst die korrekte Ausführung der Schutzdienste, die Aktualität der Erkennungssignaturen und Verhaltensregeln sowie die Fähigkeit, auf Bedrohungen aktiv zu reagieren und diese zu protokollieren. Eine regelmäßige Überprüfung dieser Funktionsfähigkeit kann die Institution vor unbemerkten Sicherheitslücken schützen. Ein deaktivierter oder fehlerhafter Schutzmechanismus könnte beispielsweise dazu führen, dass Ransomware unbemerkt Daten verschlüsselt oder ein Trojaner Anmeldeinformationen abgreift, obwohl eine Schutzsoftware installiert ist. Durch die proaktive Verifikation kann hingegen sichergestellt werden, dass diese wesentliche Verteidigungslinie durchgehend intakt ist und auf Angriffsversuche reagieren kann. Zur konkreten Umsetzung kann die Institution auf verschiedene, sich ergänzende Maßnahmen zurückgreifen. Eine zentrale Verwaltungskonsole der eingesetzten Schutzlösung kann genutzt werden, um den Status aller angebundenen Systeme automatisiert zu überwachen und Alarme auszulösen, wenn Systeme sich nicht mehr melden, veraltete Signaturen aufweisen oder Dienste beendet wurden. Ergänzend kann die tatsächliche Erkennungsleistung proaktiv durch den Einsatz einer standardisierten Testdatei wie dem EICAR-Teststring verifiziert werden; dieser kann automatisiert auf den Systemen platziert werden, um zu prüfen, ob der Schadcodeschutz wie erwartet anschlägt und eine Meldung generiert. Auf Systemen ohne zentrale Anbindung kann die Funktionsfähigkeit mittels Skripten überprüft werden, die lokal den Dienststatus und das Alter der Signaturdateien auslesen und in einer überwachten Logdatei dokumentieren.

### KONF.7.8 – Dual-Engine-Strategie

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.39, G 0.18

> Konfiguration für IT-Systeme KANN für die Erkennung von Schadcode unterschiedliche Scan-Engines aktivieren.

Hiermit ist gemeint, dass die Angriffserkennung mittels (zwei oder mehr) verschiedenen Scan-Engines durchgeführt wird, um die Erkennungswahrscheinlichkeit zu erhöhen. Hierdurch kann es zu Performanceeinbußen oder einer höheren Fehlerkennungquote kommen.

### KONF.7.9 – Einschränkung der Installation

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.39, G 0.20

> Konfiguration für IT-Systeme SOLLTE die Installation von Anwendungen einschränken.

Es empfiehlt sich z.B. die zu installierende Software nicht unkontrolliert in das Wurzeldateisystem des Betriebssystems zu installieren. Wenn die zu installierende Software aus dem Quellcode kompiliert werden soll, dann empfiehlt es sich diese nur unter einem unprivilegierten Konto zu entpacken, zu konfigurieren und zu übersetzen.

### KONF.7.10 – Einschränkung der Ausführung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.30, G 0.39

> Konfiguration für IT-Systeme SOLLTE die Ausführung nicht autorisierter Anwendungen einschränken.

Wenn Anwendungen an beliebigen Speicherorten installiert und ausgeführt werden, z.B. im Wurzeldateisystem des Betriebssystems oder an Speicherorten zusammen mit Daten der Nutzerumgebung, dann könnte dies zahlreiche Sicherheitsrisiken mit sich bringen. Unbefugte oder schadhafte Anwendungen könnten unbemerkt an unautorisierte Orte platziert werden, wo sie außerhalb etablierter Sicherheitskontrollen agieren und beispielsweise Privilege-Escalation-Angriffe durchführen können. Zudem wird das Risiko der Manipulation von Anwendungsdateien erhöht, da Angreifer gezielt nach nicht-geschützten Speicherorten suchen, um dort eigenen Code zu hinterlegen oder legitime Anwendungen zu modifizieren. Eine solche Situation kann zu "Living-off-the-Land"-Angriffen führen, bei denen Angreifer vorhandene legitime Programme missbrauchen, um Schadaktionen auszuführen, was die Erkennung erheblich erschwert. Die Beschränkung von Ausführungsspeicherorten (Execution Control) zielt darauf ab, die Angriffsfläche zu reduzieren und eine bessere Kontrolle über ausführbare Programme zu ermöglichen. Zur technischen Umsetzung dieser Anforderung kann eine Institution verschiedene Maßnahmen implementieren. Application Allowlisting kann eingesetzt werden, um nur vertrauenswürdige Anwendungen aus definierten Verzeichnissen auszuführen, beispielsweise mittels AppLocker unter Windows oder SELinux unter Linux-Systemen. Zusätzlich können Software Restriction Policies (SRPs) konfiguriert werden, um Ausführungsrechte auf bestimmte Verzeichnispfade zu begrenzen, wobei eine Trennung zwischen Systemverzeichnissen und Nutzerverzeichnissen empfehlenswert ist. Weitere wirksame Techniken umfassen die Implementierung von Code Signing, wodurch nur digital signierte Anwendungen ausgeführt werden können, sowie die Nutzung von Container-Technologien wie Docker, die eine isolierte Ausführungsumgebung bieten. Dabei kann auf das Inventar der Anwendungen als Grundlage zurückgegriffen werden.

### KONF.7.11 – Einschränkung von Softwarebibliotheken

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.30, G 0.39

> Konfiguration für IT-Systeme KANN die Ausführung nicht autorisierter Softwarebibliotheken einschränken.

Softwarebibliotheken sind wiederverwendbare Codesammlungen, die Entwicklern fertige Funktionalitäten bieten, ohne diese selbst programmieren zu müssen. Unautorisierte Bibliotheken stellen Sicherheitsrisiken dar, weil sie absichtlich eingeschleusten Schadcode enthalten könnten, der Daten ausspioniert oder Systeme kompromittiert. Sie durchlaufen seltener reguläre Sicherheitsüberprüfungen und könnten für Supply-Chain-Angriffe genutzt werden, bei denen harmlos erscheinender Code mit versteckten Schadfunktionen in Paketmanager eingeschleust wird. Zudem erhalten unautorisierte Bibliotheken häufig keine regelmäßigen Sicherheitsupdates, sodass bekannte Schwachstellen unbehoben bleiben. Mangelnde Dokumentation und unklare Abhängigkeiten von anderen ungeprüften Quellen erhöhen das Risiko zusätzlich. Beispiele sind Dateien der Typen .dll, .ocx, und .so. Die Umsetzung kann durch Sicherheitsfunktionen erfolgen, die nur das Laden autorisierter Bibliotheken in Systemprozessen erlaubt. Verfügt das IT-System über keine Möglichkeit zur Installation von Anwendungen, so ist die Anforderung entbehrlich.

### KONF.7.12 – Einschränkung von Skripten

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.30, G 0.39

> Konfiguration für IT-Systeme KANN die Ausführung nicht autorisierter Skripte einschränken.

Skripte könnten Schadcode enthalten oder zu Fehlerzuständen auf dem System führen. Die Auswirkungen schädlicher Skripte können eingeschränkt werden, indem nur bestimmte Systemfunktionen für Skripte erlaubt werden. Die Umsetzung ist mit Funktionen wie dem Windows PowerShell Constrained Language Mode oder Linux Secure Computing Mode möglich. Verfügt das System über keine Möglichkeit zur Ausführung von Skripten, so ist die Anforderung entbehrlich.

### KONF.7.13 – Einschränkung von Systemaufrufen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.30, G 0.39

> Konfiguration für IT-Systeme KANN Systemaufrufe pro Anwendung einschränken.

Ein Systemaufruf (engl. system call) ist dabei die Methode, mit der eine Anwendung Zugriff auf die Ressourcen des Betriebssystems anfordert, z.B. um eine Datei zu öffnen, in das Netzwerk zu kommunizieren oder einen neuen Prozess zu starten. Diese feingranulare Einschränkung wird in der Branche auch als Capability-based Security oder Seccomp (Secure Computing Mode) bezeichnet. Der Zweck dieser Vorschrift ist die gezielte Reduzierung der Angriffsfläche, indem selbst eine vertrauenswürdige, aber kompromittierte Anwendung daran gehindert wird, schädliche Aktionen auszuführen. Ein Angreifer könnte beispielsweise die Prozess-ID (PID) einer Anwendung kapern und versuchen, über deren Kontext privilegierte Systemaufrufe durchzuführen, um sich im Netzwerk auszubreiten oder sensible Daten zu löschen. Die Einschränkung dieser Aufrufe kann die Folgen eines erfolgreichen Angriffs erheblich mildern und so die Ausbreitung von Malware oder die Manipulation von Systemprozessen verhindern.

### KONF.7.14 – Code-Signierung im Betriebssystemkern

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.39, G 0.21

> Konfiguration für IT-Systeme SOLLTE die Signaturprüfung für nachladbaren Code im Kernelmodus aktivieren.

Nachladbarer Code im Kernelmodus verfügt typischerweise über weitreichende Berechtigungen und kann bei einer Kompromittierung erhebliche Auswirkungen auf das gesamte IT-System haben. Eine Signaturprüfung kann dazu beitragen, das Laden von nicht oder nicht vertrauenswürdig signiertem Code im Kernelmodus zu verhindern. Beispiele sind die erzwungene Signaturprüfung von Kernelmodulen unter Linux oder die Signaturprüfung von Kernelmodus-Treibern unter Windows. Die Schutzwirkung der Signaturprüfung hängt von den verwendeten Vertrauensankern ab. Hierbei kann insbesondere berücksichtigt werden, welche Signaturschlüssel beziehungsweise Herausgeber als vertrauenswürdig eingestuft werden. Eine gültige Signatur allein erlaubt keine Aussage über die Sicherheit oder Qualität des signierten Codes.

### KONF.7.15 – Lokale Firewall

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.23, G 0.18

> Konfiguration für IT-Systeme SOLLTE ein- und ausgehende Netzverbindungen einschränken.

Eine lokale Firewall ist eine Anwendung, welche nur die zum Betrieb und zur Wartung des IT-Systems notwendigen ein- und ausgehenden Verbindungen zulässt. Bringt das Betriebssystem diese Funktionalität bereits vom Werkszustand her mit, so ist die Anforderung ebenfalls erfüllt, wenn sie entsprechend konfiguriert ist. Zweckmäßig ist hierbei ein Allowlist-Ansatz, der die gewünschte Verbindung möglichst genau beschreibt (z.B. anhand Server-IP und Port).

### KONF.7.16 – Anti-Exploit

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.23

> Konfiguration für IT-Systeme SOLLTE Systemfunktionen zum Schutz des Systems vor der Ausnutzung bekannter Sicherheitslücken aktivieren.

Angreifer versuchen häufig, bekannte Sicherheitslücken oder offene Systemfunktionen zur Verbreitung oder Einnistung von Schadcode zu missbrauchen. Funktionen zum Schutz vor der Ausnutzung von Sicherheitslücken (Anti-Exploit) können helfen dies zu verhindern. Beispiele sind Data Execution Prevention (DEP), Defender Exploit Guard (WDEG) oder System Integrity Protection (SIP).

#### KONF.7.16.1 – Anti-Exploit für den Arbeitsspeicher

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.23

> Konfiguration für IT-Systeme SOLLTE den Schutz des Arbeitsspeichers vor der Ausnutzung bekannter Sicherheitslücken aktivieren.

Gelingt es Angreifern Code auf dem System auszuführen, so könnten sie versuchen, über den Arbeitsspeicher des Systems den Schadcode weiter zu verbreiten oder Zugriff auf Daten zu erlangen. Hierzu gehören Angriffe wie Buffer Overflows, Return-Oriented Programming, Heap Spraying, Use-After-Free, Memory Scraping oder Side-Channel-Angriffe wie Spectre und Meltdown. Schutzmaßnahmen hiergegen können durch Software oder durch Hardware umgesetzt sein. Softwarebasiert sind z.B. Address Space Layout Randomization (ASLR), Data Execution Prevention (DEP), Stack Canaries. Hardwarebasiert sind z.B. Trusted Execution Environments (TEE).

## KONF.8 Sicherheitsupdates

### KONF.8.1 – Automatische Überprüfung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.18, G 0.28

> Konfiguration für IT-Systeme SOLLTE das Vorliegen von Sicherheitsupdates überwachen.

Eine Überwachung von Sicherheitsupdates bedeutet, dass die IT-Systeme selbsttätig nach neuen Aktualisierungen suchen, die Schwachstellen in der Software beheben. Technisch können Systeme so konfiguriert werden, dass sie über zentrale Update-Server regelmäßig auf neue Patches prüfen. Es ist ratsam, einen automatisierten Prozess einzurichten, der bei Vorliegen von Updates diese automatisiert ausrollt oder eine Meldung an die zuständigen IT-Administratoren und ggf. die betroffenen Nutzer sendet. Diese Benachrichtigung kann über E-Mail, ein internes Ticketsystem oder ein Dashboard erfolgen. Ein guter Tipp ist die priorisierte Behandlung von Updates, bei der kritische Sicherheits-Patches vor Routine-Updates installiert werden.

#### KONF.8.1.1 – Automatische Sicherheitsupdates

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.18, G 0.28

> Konfiguration für IT-Systeme SOLLTE Sicherheitsupdates automatisch installieren.

Dies kann durch direkten Download vom Hersteller oder einen eigenen Verteilerserver umgesetzt werden, so lange dieser ebenfalls automatisch aktuell gehalten wird. Damit Sicherheitsupdates des Betriebssystems auch tatsächlich wirken und Fehlerzustände vermieden werden ist typischerweise ein Neustart erforderlich, damit die Betriebssystemfunktionen und damit verbundene Anwendungen aus dem installierten Update neu geladen und in einen definierten Zustand versetzt werden. Manche Systeme unterstützen alternativ auch Live-Patching des Betriebssystems im laufenden Betrieb.

### KONF.8.2 – Automatische Updates der Anwendung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.18, G 0.28

> Konfiguration für Anwendungen SOLLTE die automatische Installation von Sicherheitsupdates aktivieren.

Dies kann durch direkten Download vom Hersteller oder einen eigenen Verteilerserver umgesetzt werden, so lange dieser aktuell gehalten wird.

## KONF.9 Verfügbarkeit von Ressourcen

### KONF.9.1 – Speicherplatzbegrenzung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.27, G 0.40

> Konfiguration für IT-Systeme SOLLTE den Speicherplatz für die Nutzerumgebung einschränken.

Nutzerumgebung meint hier alle Anwendungen und Dienste, die auf dem System betrieben werden, aber keine Systemdienste sind. Alternativ empfiehlt es sich Mechanismen des verwendeten Datei- oder Betriebssystems zu nutzen, die Benutzende bei einem bestimmten Füllstand der Festplatte warnen oder nur noch Administrierenden Schreibrechte einräumen.

### KONF.9.2 – Begrenzung der Rechenleistung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.27, G 0.40

> Konfiguration für Hostsysteme KANN die zur Verfügung stehende Rechenleistung anhand von *[Schwellwerten]* einschränken.

Dies kann durch eine Beschränkung der Anzahl verwendeter Rechenkerne, der Rechenleistung pro Rechenkern oder durch eine indirekte Beschränkung (z.B. eine begrenzte Menge an Anfragen oder Eingabetoken in Anwendungen) umgesetzt werden.

### KONF.9.3 – Alternative Komponenten für kritische Funktionen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.18, G 0.25

> Konfiguration für IT-Systeme KANN alternative Komponenten für *[bestimmte kritische Funktionen]* installieren.

Beispiele sind redundante Stromnetzteile, Ethernet-Anschlüsse oder eine Mobilfunkanbindung als Ausfallsicherheit für die kabelgebundene Netzanbindung.

## KONF.10 Konfiguration von Anwendungen

### KONF.10.1 – Grundkonfiguration für Anwendungen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18

> Konfiguration für Anwendungen SOLLTE eine Grundkonfiguration dokumentieren.

Eine Grundkonfiguration (engl. baseline configuration) bezeichnet in diesem Kontext einen dokumentierten Ausgangszustand einer Anwendung, der sowohl funktionale Anforderungen als auch sicherheitsrelevante Einstellungen berücksichtigt. Sie umfasst unter anderem Parameter wie Benutzerrechte, Logging-Einstellungen, Schnittstellenaktivierungen oder Verschlüsselungsoptionen und bildet damit die Referenz, auf die spätere Anpassungen zurückgeführt oder überprüft werden können. Fehlt eine nachvollziehbare Grundkonfiguration, könnte es bei Updates, Migrationen oder im Incident-Fall zu schwer erkennbaren Abweichungen kommen, die unerwünschte Sicherheitslücken hinterlassen. Eine klare Dokumentation kann dagegen die Nachvollziehbarkeit erhöhen, unerwünschte Änderungen sichtbar machen und den sicheren Betrieb der Anwendung unterstützen. Zur praktischen Umsetzung kann die Institution eine dokumentierte Konfigurationsvorlage entwickeln, die sowohl Herstellerempfehlungen als auch anerkannte Empfehlungen des BSI oder aus Benchmarks wie die des Center for Internet Security (CIS) berücksichtigt. Die Sicherheit von Anwendungen ist in besonderem Maße kontextbezogen: So könnten z.B. über E-Mail oder Messenger hoch vertrauliche Daten ausgetauscht werden oder auch öffentliche Informationen. Daher ist hier eine Vertiefung der Risikoanalyse empfehlenswert, die sich an der Verwendung der Anwendungen in Geschäftsprozessen orientiert. Dabei besteht ein enger Bezug zu Compliance-Anforderungen, zum Beispiel an finanzielle Transaktionen oder den Datenschutz, je nachdem welche Datenverarbeitungen mit der Anwendung vorgenommen werden.

#### KONF.10.1.1 – Versionierung der Anwendungskonfiguration

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.18, G 0.45

> Konfiguration für Anwendungen SOLLTE eine Versionierung vorheriger Konfigurationen verankern.

Die Versionierung bezeichnet hier die strukturierte Nachvollziehbarkeit von Änderungen an Konfigurationen, also das Speichern, Dokumentieren und bei Bedarf Wiederherstellen älterer Zustände einer Anwendung. Sie unterscheidet sich von einem einfachen Backup dadurch, dass nicht nur eine Kopie vorliegt, sondern explizit eine fortlaufende Historie mit Vergleichen, Rücksetzpunkten (rollback points) und optional Kommentaren geführt wird. Der Zweck liegt darin, dass eine ungewollte oder fehlerhafte Anpassung an einer Anwendungskonfiguration im Betrieb schnell erkannt und – wenn erforderlich – präzise auf einen definierten, funktionsfähigen Zustand zurückgesetzt werden kann. Ohne diese Rückgriffsmöglichkeit könnte ein Konfigurationsfehler den gesamten Dienst außer Betrieb setzen, während eine Versionierung die Verfügbarkeit und Nachvollziehbarkeit stärken kann. Zur Umsetzung kann eine Institution technische Verfahren einsetzen, die eine automatische Ablage und Historisierung von Konfigurationsdateien unterstützen, beispielsweise durch (1) den Einsatz verteilter Versionskontrollsysteme wie Git oder Subversion (SVN) für textbasierte Konfigurationsdateien, (2) integrierte Konfigurationsarchivierung in gängigen Deployment- oder Container-Tools, oder (3) systemseitige Snapshot-Mechanismen, die gezielt für Konfigurationsverzeichnisse genutzt werden.

### KONF.10.2 – Kryptographische Verfahren in Anwendungen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.29

> Konfiguration für Anwendungen SOLLTE kryptographische Verfahren nach *[anerkannten Standards]* im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement aktivieren.

Kryptographie wird für die Authentifizierung, Verschlüsselung und Integritätprüfung in Anwendungen verwendet, z.B. bei der Anmeldung an der Anwendung oder digitalen Signierung von Nachrichten. Die Formulierung "im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement" bedeutet, dass die Authentifizierung so erfolgt, wie in der Praktik Berechtigung (BER) festgelegt. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Schlüsselmanagement zu finden ist. Anerkannte kryptographische Verfahren sind in der BSI TR-02102 zu finden.

### KONF.10.3 – Änderung von Default-Zugangsdaten

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.30, G 0.23

> Konfiguration für Anwendungen SOLLTE die Änderung von Default-Zugangsdaten ausführen.

Hiermit sind Default-Passwörter, als auch vertrauenswürdige Authentisierungs-Schlüssel oder Zertifikate fallen, die per Default zur Anmeldung akzeptiert werden, gemeint.

### KONF.10.4 – Deaktivierung nicht benötigter Anwendungsfunktionen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.23

> Konfiguration für Anwendungen SOLLTE nicht benötigte Anwendungsfunktionen deaktivieren.

Funktionen die für den Betrieb nicht benötigt werden stellen ein unnötiges Sicherheitsrisiko dar, da sie von Angreifern ausgenutzt werden oder durch Wechselwirkungen zu unvorhergesehenen Fehlern führen könnten. Hierzu gehören z.B. ungenutzte Cloud-Anbindungen, Module, Leistungsmerkmale oder Einstellungen. Installationspakete enthalten häufig eine Vielzahl von ausführbaren Dateien und Erweiterungen. Für den Betrieb nicht benötigte Anwendungskomponenten können Schwachstellen enthalten und sind ein unnötiges Sicherheitsrisiko.

### KONF.10.5 – Überprüfung der Konfiguration

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.31, G 0.23, G 0.21, G 0.22

> Konfiguration für Anwendungen SOLLTE die Übereinstimmung der tatsächlichen Konfiguration mit dem Referenzzustand *[regelmäßig]* überprüfen.

Referenzzustand („baseline configuration“) bezeichnet hier die dokumentierte und freigegebene Konfiguration der Anwendung, also die gewünschte und autorisierte Einstellung von Parametern, Diensten und Komponenten. Die tatsächliche Konfiguration ist die aktuelle technische Umsetzung dieser Einstellungen der Anwendung selbst. Der Abgleich beider Zustände dient vor allem der Vermeidung von Configuration Drift – d.h. dass Anwendungen schleichend von der definierten Grundkonfiguration abweichen. Dies könnte auftreten, wenn Änderungen nicht zentral dokumentiert oder automatisierte Installationen nicht einheitlich umgesetzt werden. Ohne diese Kontrolle könnte es zu unbemerkten Fehlkonfigurationen kommen, die Sicherheitslücken öffnen oder Betriebsstörungen verursachen. Durch regelmäßige Vergleiche kann eine Institution sicherstellen, dass Anwendungen konsistent, vertrauenswürdig und wartbar bleiben. Die Umsetzung kann technisch etwa mit Skripten erfolgen, die automatisiert Konfigurationsparameter auslesen und vergleichen. Auch der Einsatz von „Configuration Management“- oder „Compliance Scanning“-Werkzeugen kann unterstützen, indem sie Differenzen visualisieren und Reports erzeugen. Prozessual kann es hilfreich sein, Prüfintervalle nach Kritikalitätsklassen zu staffeln (z. B. sicherheitskritische Anwendungen wöchentlich, weniger kritische vierteljährlich) und Ergebnisse in Change-Management-Prozesse zurückzuführen.

#### KONF.10.5.1 – Automatisierte Überprüfung der Konfiguration

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.31, G 0.23, G 0.21, G 0.22

> Konfiguration für Anwendungen KANN die Überprüfung der Konfiguration durch *[einen automatisierten Mechanismus]* aktivieren.

Die automatische Auditierung der Systemkonfiguration ermöglicht eine kontinuierliche und effiziente Überprüfung, ob IT-Systeme sicher und regelkonform konfiguriert sind. Dabei wird die aktuelle Konfiguration automatisiert mit vordefinierten Soll-Vorgaben (etwa unternehmensinternen Richtlinien oder externen Benchmarks wie denen des Center for Internet Security (CIS)) abgeglichen. Dies ist besonders sinnvoll, da manuelle Prüfungen fehleranfällig, zeitaufwändig und in großen Infrastrukturen kaum durchführbar sind. Automatisierte Audits erhöhen die Transparenz, erkennen Abweichungen frühzeitig und erleichtern die Einhaltung von Compliance-Vorgaben. So wird die Angriffsfläche durch fehlerhafte oder unsichere Einstellungen erheblich reduziert.

## KONF.11 Vertrauensbeziehungen

### KONF.11.1 – Authentifizierung vor dem Zugriff

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.19, G 0.30

> Konfiguration für Anwendungen SOLLTE Zugriffe auf schützenswerte Daten im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement authentifizieren.

Ziel ist es, vertrauliche Daten vor dem Zugriff von Unbefugten zu schützen. Relevant sind hierbei sowohl Frontend-Zugänge wie Webportale, als auch Backend-Datenschnittstellen wie Datenbank-API. Dies kann durch eine anwendungsspezifische Authentifizierung, oder durch Nutzung eines zentralen Identity Providers (Single-Sign-On) erfüllt werden. Für die Authentifizierung kommen z.B. Passwörter, X.509-Zertifikate, OTP-Token in Frage. Zweckmäßig ist hierfür der Einsatz von Standardkomponenten wie OAuth 2.0 und die Verbindung mit einem zentralen Berechtigungsmanagement der Anwendung. Im Einklang mit den Anforderungen des Identitäts- und Berechtigungsmanagements bedeutet, dass für die Anwendung die Anforderungen aus der Praktik Identitäts- und Berechtigungsmanagement erfüllt sind, die dort festgelegt wurden. Hierzu gehört die Art der Authentifizierung (z.B. Passwort, Biometrie, Mehr-Faktor-Authentifizierung) ebenso wie die relevanten Parameter (Passwortkomplexität, etc.). Auf Daten die nicht vertraulich (z.B. öffentlich) sind kann auch ohne Authentifizierung Zugriff erlaubt sein. Die Formulierung "im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement" bedeutet, dass die Authentifizierung so erfolgt, wie in der Praktik Berechtigung (BER) festgelegt. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Kryptographie zu finden ist. Verarbeitet die Anwendung gar keine vertraulichen Daten, dann ist die Anforderung entbehrlich.

#### KONF.11.1.1 – Authentifizierung von geplanten Konversationen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.19, G 0.30

> Konfiguration für TK-Anwendungen SOLLTE den Zugriff auf geplante Konversationen im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement authentifizieren.

Viele TK-Anwendungen bieten geplante Konversationen, z.B. in virtuellen Meeting-Räumen oder über Telefonkonferenzen, die über eine Rufnummer erreichbar sind. Wird der Zugriff hierauf nicht authentifiziert, so könnten unbemerkt Unberechtigte teilnehmen und Informationen abhören oder auf Meta-Informationen wie Teilnehmer oder Uhrzeiten zugreifen. Der Schutz kann z.B. durch Passwörter/PINs oder über die Anmeldung per Zertifikat oder Single-Sign-On geschehen. Die Formulierung "im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement" bedeutet, dass die Authentifizierung so erfolgt, wie in der Praktik Berechtigung (BER) festgelegt. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Kryptographie zu finden ist.

#### KONF.11.1.2 – Authentifizierung von Netzverbindungen - clientseitig

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.43, G 0.36

> Konfiguration für Anwendungen SOLLTE die Gegenstelle vor dem Datenaustausch im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement authentifizieren.

Stellt eine Anwendung Anfragen über das Netz oder nimmt eine Anwendung Anfragen über das Netz entgegen, so gewährleistet eine gegenseitige Authentifizierung der Kommunikationspartner (mutual authentication), dass diese autorisiert ist Anfragen zu stellen oder zu beantworten. Eine gängige Lösung ist die Prüfung von X.509-Zertifikaten beim Verbindungaufbau mit TLS. Für die Umsetzung ist es nicht unbedingt erforderlich, dass sich die Gegenstelle bei jeder Anfrage/Abruf erneut authentifiziert, wenn bei der Authentifizierung eine sichere Verbindung per TLS aufgebaut wird. Mit Anfragen sind alle Zugriffe gemeint, sei es über eine Web-URL oder eigene API. Die Formulierung "im Einklang mit den zugehörigen Anforderungen zum Identitäts- und Berechtigungsmanagement" bedeutet, dass die Authentifizierung so erfolgt, wie in der Praktik Berechtigung (BER) festgelegt. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Kryptographie zu finden ist. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Kryptographie zu finden ist. Für lesende Zugriffe auf unkritische, öffentliche Daten ist die Authentifizierung der lesenden Anwendung entbehrlich.

### KONF.11.2 – Warteraum

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.19, G 0.30

> Konfiguration für VK-Anwendungen SOLLTE bei Konferenzschaltungen alle Teilnehmenden authentifizieren.

Dies kann z.B. Über eine explizite Gruppenmitgliedschaft von Zugangskonten, die Verteilung von Zugangsdaten per E-Mail oder virtuelle Warteräume erfüllt werden. Warteräume geben Konferenzmoderatoren die Möglichkeit, Teilnehmer vor Eintritt in einem virtuellen Warteraum persönlich zu authentifizieren.

### KONF.11.3 – Veröffentlichung von Domain-Infomationen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.19, G 0.14

> Konfiguration für DNS-Server SOLLTE die Veröffentlichung von Domain-Infomationen anhand von *[Kriterien]* einschränken.

Angreifer nutzen häufig DNS um das Netz zu erkunden (DNS-Reconnaissance). Veröffentlichen Sie Domain-Informationen nur, wenn diese zu einem Dienst gehören, der zur externen Nutzung gedacht ist. Nur intern benötigte DNS-Einträge dagegen bleiben intern. Kriterien können z.B. Domains oder Subdomain sein (intern.domain.com vs www.domain.com).

### KONF.11.4 – Erraten von Zugriffslinks

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.23, G 0.19

> Konfiguration für Webanwendungen SOLLTE das Durchprobieren von Zugriffslinks durch *[einen automatisierten Mechanismus]* blockieren.

Ermöglichen Links den Zugriff auf vertrauliche Daten ohne Authentifizierung, so könnten Angreifer versuchen diese zu finden, z.B. mit Durchprobieren von Meeting-Links oder Ressourcen-URLs. Mögliche Maßnahmen sind Nicht-Sequentielle IDs mit hoher Entropie, Rate Limiting von Anfragen oder CAPTCHA. Hierbei bietet sich eine Kombination von Maßnahmen an, die Anzahl erwarteter Zugriffe, Verfügbarkeits- und Usability-Kriterien ebenso beachtet wie das Risikoprofil der Anwendung. Bietet die Webanwendung keinerlei Zugriff auf schützenswerte Informationen ohne Authentifizierung, so ist die Anforderung entbehrlich.

### KONF.11.5 – Einschränkung unauthentifizierter Anschlüsse

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.23, G 0.30

> Konfiguration für TK-Anwendungen SOLLTE von unauthentifizierten Anschlüssen erreichbare Gegenstellen einschränken.

Als unauthentifizierte Anschlüsse (engl. unauthenticated connections) sind hier alle Endpunkte zu verstehen, die eine Kommunikation ohne Anmeldung ermöglichen. Dies umfasst beispielsweise Notfalltelefone in Aufzügen, öffentlich zugängliche Telefone oder auch Faxgeräte in ungesicherten Bereichen. Aber auch an Konferenzraum-Systeme für Videokonferenzen oder den anonymen Gast-Zugang zu Online-Meetings ist zu denken. Die Anforderung zielt darauf ab, den Missbrauch dieser Kommunikationskanäle zu unterbinden, deren Nutzung nicht eindeutig einem authentifizierten Benutzer zugeordnet werden kann. Ohne eine Einschränkung der erreichbaren Gegenstellen – also der kontaktierbaren externen Domänen, Meeting-IDs oder Benutzerkonten – könnte ein Angreifer vertrauliche interne Besprechungen ausspähen oder ein unautorisierter Gast könnte von einem Konferenzraum aus sensible Daten per Bildschirmübertragung an externe Dritte weitergeben. Ohne eine solche Einschränkung könnte ein unberechtigter Nutzer auf Kosten der Institution kostenpflichtige Mehrwertdienste oder teure Auslandsnummern anwählen und so erheblichen finanziellen Schaden verursachen. Ebenso könnte eine missbräuchliche Nutzung zur Belästigung Dritter oder zur Absetzung von böswilligen Notrufen erfolgen, was die Verfügbarkeit kritischer Ressourcen beeinträchtigen könnte.

### KONF.11.6 – Übersicht angemeldeter Verbindungen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.23, G 0.30

> Konfiguration für Anwendungen KANN eine Übersicht angemeldeter Verbindungen aktivieren.

Je nach Anwendung können dabei Informationen wie Gerätename, Betriebssystemtyp, Browser-Agent oder IP-Adresse angezeigt werden.

### KONF.11.7 – Einschränkung von Schnittstellen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.23, G 0.19

> Konfiguration für Anwendungen SOLLTE aktivierte Schnittstellen einschließlich denen zu anderen Anwendungen, Cloud-Funktionen oder Erweiterungen einschränken.

Die Einschränkung von Schnittstellen hilft, ungewollte oder böswillige Zugriffe auf Anwendungen und Daten zu verhindern. Durch das Festlegen klarer Regeln welche Systeme oder Anwendungen über welche Schnittstellen auf welche Daten zugreifen können wir das "Need to know" Prinzip in der Kommunikation umgesetzt. Ferner kann ein solcher Ansatz dazu beitragen, die Integrität und Vertraulichkeit von Informationen zu wahren, indem nur autorisierte Kommunikationspartner berechtigt werden, Daten zu lesen, zu schreiben oder Funktionalitäten aufzurufen. Beispiele sind die Synchronisierung von Lesezeichen und Historie im Browser, die Anbindung von Cloud-Funktionen, etwa eine serverless Image-Processing-API, für die ein entsprechendes Rollenkonzept noch nicht hinterlegt und von der Sicherheitsverantwortlichen geprüft wurde, oder die Installation einer Browsererweiterungen. Erweiterungen (Plugins, AddOns), die nicht von der Institution für die Verwendung autorisiert wurden, können zu ungewollten Datenabflüssen führen und Schadcode enthalten. Zur Umsetzung kann es hilfreich sein, standardisierte Formulare oder digitale Workflows zu etablieren, in denen die Notwendigkeit, der Umfang und die Verantwortlichen für jede neue Schnittstelle dokumentiert werden. Die Einschränkung kann auch durch Komponenten außerhalb der Anwendung erfolgen, zum Beispiel durch API-Gateways, die nur auf Whitelists registrierter Endpunkte reagieren, oder durch Einsatz von Zertifikaten und OAuth-Scopes. Um unautorisierte Erweiterungen technisch zu unterbinden kann die Deinstallation oder Deaktivierung der Erweiterungen, sowie das Setzen von Berechtigungen zur Installation nur für Administrierende umgesetzt werden.

#### KONF.11.7.1 – Einschränkung von Zonentransfers

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.30, G 0.19

> Konfiguration für DNS-Server SOLLTE Zonentransfers einschränken.

Zum Schutz vor DNS-Reconnaissance und DNS-Spoofing, da Zonendaten alle DNS-Einträger einer Domäne enthalten. Kann durch Einschränkung auf autorisierte IP-Adressen und TSIG umgesetzt werden.

#### KONF.11.7.2 – Einschränkung von TK-Verbindungen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.23, G 0.30

> Konfiguration für TK-Anwendungen SOLLTE unerwünschte TK-Verbindungen einschränken.

Kann durch Session Border Controller (SBC) oder Filterung innerhalb von Anwendungen umgesetzt werden. SBC filtern die Signalisierung und Mediastreams auf dem Kommunikationsweg, insbesondere beim Verbindungsaufbau mittels SIP, H.323 oder MGCP.

##### KONF.11.7.2.1 – Einschränkung der TK-Gegenstellen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.23, G 0.30

> Konfiguration für TK-Anwendungen SOLLTE Verbindungen mit externen Gegenstellen einschränken.

Telekommunikation mit externen Stellen ist essenziell für viele Geschäftsprozesse, aber auch beliebtes Ziel für Social Engineering und technische Angriffe. Kann z.B. durch eine Beschränkung auf europäische Rufnummernkreise oder den Ausschluss unerwünschter IP-Adressbereiche umgesetzt werden.

### KONF.11.8 – Verschlüsselung schützenswerter Daten (at-rest)

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.19, G 0.14

> Konfiguration für Anwendungen KANN schützenswerte Daten bei der Speicherung (at-rest) verschlüsseln.

Hierbei ist insbesondere an Zugangsdaten zu denken. Die Anforderung ist auch dann erfüllt, wenn Daten statt einer Verschlüsselung mit Hash und Salt versehen sind. Zur Umsetzung siehe BSI TR-02102.

## KONF.12 Kontrollierte Datenverarbeitung

### KONF.12.1 – Eingabevalidierung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.28, G 0.23

> Konfiguration für Anwendungen SOLLTE die Validierung von Eingabedaten durch *[einen automatisierten Mechanismus]* aktivieren.

Eingabevalidierung (engl. input validation) ist die technische und logische Überprüfung von Daten, die von Nutzenden, Schnittstellen oder externen Quellen an eine Anwendung übergeben werden. Ziel ist es, sicherzustellen, dass nur erwartete, syntaktisch und semantisch korrekte Eingaben verarbeitet werden – beispielsweise Zahlen in einem numerischen Feld, zulässige Dateiformate bei Uploads oder inhaltlich beschränkte Steuerzeichen in Formularen. Fehlende oder unzureichende Eingabevalidierung könnte es Angreifenden ermöglichen, schadhaften Code einzuschleusen (injection attacks wie SQL Injection oder Command Injection), Geschäftslogik zu manipulieren oder Systeme über Ressourcenmissbrauch lahmzulegen. Eine saubere Validierung kann dagegen die Angriffsfläche deutlich reduzieren und die Verlässlichkeit der Anwendung erhöhen. Dabei hängt die Ausgestaltung stark vom Einsatzzweck ab: Während etwa bei einer Textverarbeitung größere Freiheiten gewährt werden können, erfordern sensible Szenarien wie SQL-Injection bei Datenbankanfragen, die Abwehr von prompt injection bei Large Language Models (LLM) oder die Verarbeitung von Zahlungsdaten sehr strikte Prüfungen. Je nach Anwendung und Risikoprofil können Plausibilitätsprüfungen, die Beschränkung der Eingabedaten auf vordefinierte Werte, Verifikationen der Daten bei einer dritten Stelle (z.B. eines Zahlungsmittels beim Zahlungsanbieter), Regular Expression Entry Patterns, oder Data Escaping als Maßnahmen sinnvoll sein.

#### KONF.12.1.1 – Zertifikatsprüfung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.43

> Konfiguration für Webbrowser SOLLTE die automatische Validierung des Zertifikates einschließlich der vollständigen Zertifikatskette aktivieren.

Zertifikatsprüfung (Certificate Validation) ist eine Funktion, bei der ein Browser das digitale Zertifikat einer Webseite vor dem Verbindungsaufbau verifiziert. Dabei wird sichergestellt, dass das Zertifikat von einer vertrauenswürdigen Zertifizierungsstelle (CA - Certificate Authority) ausgestellt, gültig und nicht abgelaufen oder widerrufen ist. Dabei wird die vollständige Zertifikatskette, einschließlich des Root-Zertifikates verifiziert. Ist das Zertifikat ungültig, so wird der Aufruf der Seite blockiert. Die korrekte Implementierung dieses Prozesses kann die Vertraulichkeit und Integrität der übertragenen Daten gewährleisten und schützt vor Man-in-the-Middle-Angriffen, bei denen Angreifer versuchen, den Datenverkehr abzufangen. Zur Umsetzung dieser Anforderung können Institutionen die zentrale Konfiguration von Browsern über Gruppenrichtlinien (Group Policies) oder Mobile Device Management (MDM)-Lösungen vornehmen.

#### KONF.12.1.2 – Content Security Policy (CSP)

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.28, G 0.23

> Konfiguration für Webbrowser SOLLTE aufgerufene Inhalte anhand der von der Webseite bereitgestellten Content Security Policy einschränken.

Eine Content Security Policy (CSP) ist ein Sicherheitsmechanismus, der es einer Webseite erlaubt, dem Webbrowser mitzuteilen, von welchen Quellen er aktive Inhalte wie Skripte oder auch passive Inhalte wie Bilder laden darf. Durch diesen als Whitelist funktionierenden Ansatz kann die Institution die Angriffsfläche ihrer Webanwendungen erheblich reduzieren. Ohne eine wirksame CSP könnten Angreifer durch Cross-Site-Scripting-Angriffe (XSS) bösartige Skripte in eine Webseite einschleusen, die dann im Browser des Nutzers ausgeführt werden und beispielsweise sensible Daten auslesen oder Aktionen im Namen des Opfers durchführen könnten. Die Aktivierung einer CSP blockiert die Ausführung von nicht vertrauenswürdigen Skripten und das Laden unerwünschter Ressourcen und schützt somit die Integrität und Vertraulichkeit der Web-Sitzung.

#### KONF.12.1.3 – Same-Origin-Policy

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.19, G 0.28

> Konfiguration für Webbrowser SOLLTE aufgerufene Inhalte anhand der von der Webseite bereitgestellten Same-Origin-Policy einschränken.

Die Same-Origin-Policy, oft auch als SOP bekannt, ist ein fundamentaler Sicherheitsmechanismus im Webbrowser, der sicherstellt, dass von einer Quelle (Origin) geladene Skripte oder Dokumente nicht mit Ressourcen einer anderen Quelle interagieren können, wobei eine Quelle durch die Kombination aus Protokoll, Hostname und Port definiert wird. Sinn und Zweck dieser strikten Trennung ist der Schutz vor Datenabfluss und unbefugten Interaktionen zwischen unterschiedlichen Webanwendungen innerhalb derselben Browsersitzung. Ohne diese Isolierung könnte eine schadhafte Webseite beispielsweise vertrauliche Informationen aus einer parallel geöffneten legitimen Anwendung, wie einem Online-Banking-Portal oder internen Firmentool, auslesen und an einen Angreifer senden. Die konsequente Durchsetzung der Same-Origin-Policy durch den Browser kann solche Cross-Site-Scripting-Angriffe (XSS) effektiv unterbinden und somit die Vertraulichkeit und Integrität der vom Nutzer verarbeiteten Daten gewährleisten.

#### KONF.12.1.4 – Subresource Integrity-Prüfung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.22, G 0.46

> Konfiguration für Webbrowser SOLLTE aufgerufene Inhalte anhand der von der Webseite bereitgestellten Subresource Integrity-Prüfung einschränken.

Unter Subresource Integrity (SRI), zu Deutsch etwa „Integrität von Unterressourcen“, versteht man einen Sicherheitsmechanismus von Webbrowsern, der sicherstellt, dass die vom Browser geladenen Ressourcen, wie z.B. JavaScript-Dateien oder CSS-Stylesheets, die von einem Drittanbieter (etwa einem Content Delivery Network, CDN) stammen, nicht unerwünscht manipuliert wurden. Technisch geschieht dies dadurch, dass die Webseite beim Einbinden der Ressource einen kryptografischen Hashwert (oder Digest) der erwarteten Datei als Attribut (z.B. integrity="...") mitsendet. Der Webbrowser kann dann nach dem Herunterladen der Ressource diesen Hashwert neu berechnen und mit dem bereitgestellten Wert vergleichen. Dies ist notwendig, da die Institution zwar die eigene Webseite kontrolliert, aber nicht die Server Dritter, von denen oft Bibliotheken geladen werden. Der Sinn und Zweck dieser Vorschrift liegt darin, die Sicherheit der Endnutzer zu erhöhen und Risiken durch manipulierte externe Inhalte zu minimieren. Ohne diese Prüfung könnte eine kompromittierte Drittanbieter-Ressource bösen Code in die Webseite der Institution einschleusen, was zu Vorfällen wie Datendiebstahl oder der Installation von Malware auf den Geräten der Nutzer führen könnte.

#### KONF.12.1.5 – HTTP Strict Transport Security (HSTS)

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.15, G 0.43

> Konfiguration für Webbrowser SOLLTE aufgerufene Inhalte anhand der von der Webseite bereitgestellten HTTP Strict Transport Security (HSTS) Richtlinie einschränken.

Die HTTP Strict Transport Security (HSTS) ist ein Web-Sicherheitsmechanismus – definiert in IETF RFC 6797 – der Webbrowser zwingt, eine ausschließlich verschlüsselte Verbindung (HTTPS) mit einem Webserver zu nutzen, selbst wenn der Nutzer oder eine Anwendung versucht, über das unsichere HTTP zuzugreifen. Konkret beinhaltet die HSTS-Richtlinie (oder Policy) einen speziellen HTTP-Antwort-Header, den der Webserver an den Browser sendet, der die Dauer (max-age) festlegt, für die der Browser die Verbindung nur über HTTPS herstellen soll. Die restriktive Konfiguration von Webbrowsern in Bezug auf diese Richtlinie kann die Schutzwirkung erhöhen, da so das Risiko eines Man-in-the-Middle (MITM)-Angriffs, bei dem ein Angreifer eine unverschlüsselte Verbindung abfangen oder den Nutzer auf eine unsichere Seite umleiten könnte, deutlich reduziert wird. Eine solche Konfiguration kann die Institution vor dem ungewollten Downgrade-Angriff (Downgrade Attack) schützen, bei dem die Verbindung von HTTPS auf das unsichere HTTP erzwungen wird.

#### KONF.12.1.6 – JavaScript

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.39, G 0.28

> Konfiguration für Webbrowser KANN JavaScript einschränken.

Schadcode in JavaScript kann unbefugt auf sensible Daten zugreifen oder die angezeigte Webseite manipulieren. Da viele Webseiten JavaScript zur Ausführung benötigen, ist die Deaktivierung von JavaScript mit erheblichen funktionalen Einschränkungen verbunden. Ein möglicher Kompromiss ist, dass Administrierende oder Nutzende Ausnahmen für einzelne Seiten hinzufügen können.

#### KONF.12.1.7 – Filtern schädlicher Webinhalte

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.39, G 0.28

> Konfiguration für Webanwendungen SOLLTE eine Filterung schädlicher Webinhalte aktivieren.

Anfragen an Webanwendungen könnten dazu führen, dass diese sich anders verhalten als gewollt. Mögliche Folgen sind die unzulässige Preisgabe von Informationen, die Manipulation oder der Verlust von Daten sowie Betriebsstörungen. Typische Auslöser sind SQL Injection oder Cross-Site-Scripting. Solche potenziell schädlich wirkenden Inhalte können durch eine Web Application Firewall oder durch geeignete Eingabevalidierung in der Webanwendung gefiltert werden.

#### KONF.12.1.8 – Duplikate im Verzeichnisbaum

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.46

> Konfiguration für Verzeichnisdienste SOLLTE Duplikate im Verzeichnisbaum blockieren.

Da jedes Zugangskonto nur einmal benötigt wird können Duplikate von Attributen wie Name oder Organisationseinheit nur als Fehler oder Angriff vorkommen. In OpenLDAP kann dies beispielsweise durch Overlays realisiert werden. Dies gilt ausschließlich für Daten von Nutzenden.

#### KONF.12.1.9 – Journaling

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.46, G 0.45

> Konfiguration für Dateiserver SOLLTE Dateisystem-Journaling aktivieren.

Beim Journaling werden Änderungen an Dateien zunächst in einem speziellen Protokoll (Journal) aufgezeichnet, bevor sie tatsächlich geschrieben werden, um Datenintegrität und Konsistenz sicherzustellen. Auf einem Dateiserver ist dies besonders wichtig, da es das Risiko von Datenverlusten bei plötzlichen Abstürzen oder Stromausfällen minimiert und eine schnelle Wiederherstellung ermöglicht.

#### KONF.12.1.10 – HTTP-Response-Header

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.23

> Konfiguration für Webanwendungen SOLLTE HTTP-Response-Header aktivieren.

Hierzu können z.B. Content-Security-Policy (CSP), X-Frame-Options, X-XSS-Protection, Referrer-Policy, Permissions-Policy, HSTS und X-Content-Type-Optionen gehören.

#### KONF.12.1.11 – Aktive Dateiinhalte

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für Office-Anwendungen SOLLTE aktive Inhalte in Office-Dateien deaktivieren.

Aktive Inhalte (Makros) in Office-Dokumenten können Schadcode enthalten oder zu nicht nachvollziehbaren Datenfehlern führen. Viele Nutzende verwenden solche Funktionen jedoch für ihre Arbeit, so dass eine generelle Sperrung mit Einschränkungen verbunden ist. Autorisierte Ausnahmen bilden daher einen guten Kompromiss bei normalen Schutzbedarf. Dies kann durch den geschützten Modus (Protected View) umgesetzt werden. Werden bestimmte Makros dennoch häufig benötigt, so können Makros mit digitaler Signatur einer anerkannten Zertifizierungsstelle oder von vertrauenswürdigen Speicherorten zugelassen werden.

### KONF.12.2 – Verschlüsselungsstatus der aktuellen Verbindung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.15, G 0.43

> Konfiguration für Webbrowser SOLLTE eine Anzeige der Verschlüsselung der aktuellen Verbindung aktivieren.

Die Anzeige der Verschlüsselung der aktuellen Verbindung im Webbrowser, auch bekannt als Connection Encryption Indicator oder oft durch ein 🔒-Symbol dargestellt, ist ein essenzielles Merkmal für die Wahrnehmung der Vertrauenswürdigkeit einer Online-Kommunikation. Sie visualisiert, ob die Datenübertragung zwischen dem Browser des Benutzers und dem Webserver mittels eines kryptografischen Protokolls, typischerweise Transport Layer Security (TLS) (früher Secure Sockets Layer (SSL)), abgesichert ist. Diese Vorschrift zielt darauf ab, das Risiko des Abhörens von Daten durch Dritte (Eavesdropping) zu minimieren; denn ohne diese Anzeige könnte ein Benutzer unbemerkt sensible Informationen über eine ungesicherte Verbindung eingeben, was beispielsweise zur Kompromittierung von Anmeldedaten oder vertraulichen Geschäftsinformationen führen könnte.

### KONF.12.3 – Cookies

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.19, G 0.14

> Konfiguration für Webbrowser SOLLTE Cookies einschränken.

Cookies sind Dateien, in denen Webseiten Daten auf dem System speichern. Sie können Authentifizierungstoken und andere personenbezogene Daten enthalten und durch Angriffe wie Cross-Site-Scripting (XSS) oder Session Hijacking kompromittiert werden. Die Speicherung von Cookies per Default auszuschalten könnte jedoch zu Funktionseinschränkungen führen. Nutzende oder Administrierende können Ausnahmen für bestimmte Webseiten, z.B. im Intranet, hinzufügen.

### KONF.12.4 – Speicherung von Zugangsdaten

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.19, G 0.30

> Konfiguration für Webbrowser SOLLTE die Speicherung von Zugangsdaten *[in einem dedizierten Passwort-Manager mit Browser-Integration oder direkt im Browser durch ein Master-Passwort geschützt]* aktivieren.

Werden Zugangsdaten gespeichert, so könnten Angreifer diese auslesen und missbrauchen. Daher ist es wichtig, Vertraulichkeit und Integrität sensibler Anmeldedaten zu gewährleisten. Durch die Nutzung einer geprüften Browser‑Extension kann sichergestellt werden, dass Passwörter nur in einem verschlüsselten Vault abgelegt werden, der zentral verwaltet oder versioniert wird. Ein starkes Master‑Passwort kann als Schlüssel dienen, sodass selbst bei Verlust des Geräts oder unautorisiertem Zugriff auf die lokale Datenbank die Daten ohne Kenntnis dieses Passworts nicht lesbar sind. Wird die Funktion komplett deaktiviert, kann das Risiko unkontrollierter Speicherung oder unsicherer Autovervollständigung minimiert werden – der Anwender kann sich stattdessen etwa auf einen externen Manager oder eine Single‑Sign‑On‑Lösung verlassen. Konkret kann dies in der Praxis auf verschiedene Weisen aussehen: So kann eine Institution über Gruppenrichtlinien festlegen, dass nur eine offiziell freigegebene Extension (etwa einer Open‑Source‑Lösung oder eines kommerziellen Anbieters) installiert werden darf. Alternativ lassen sich browserinterne Passwort‑Speicher mit einem Master‑Passwort verschlüsseln – denkbar ist hier sowohl die Nutzung integrierter Funktionen von Browsern mit zuverlässiger Krypto‑Engine als auch externer Tools wie plattformübergreifende Passwort‑Manager, die eine Browser‑Anbindung per Plugin bieten. In Szenarien mit besonders hohen Sicherheitsanforderungen kann die Speicherung ganz deaktiviert werden, etwa indem das entsprechende Feature per Policy abgeschaltet wird und Nutzer gezielt mit einem eigenständigen, von der Institution kontrollierten Tool arbeiten. Für die Umsetzung bietet es sich an, zunächst eine klare Richtlinie zu formulieren, die alle Mitarbeitenden über die zugelassenen Speicherwege informiert und gleichzeitig erklärt, warum unautorisierte Methoden unerwünscht sein können. IT‑Administratoren können über zentrale Management‑Werkzeuge (GPOs, MDM‑Systeme) die Installation autorisierter Extensions automatisieren und unerwünschte Funktionen deaktivieren. Es kann hilfreich sein, standardisierte Vorlagen für sichere Master‑Passwörter zu kommunizieren und regelmäßige Schulungen anzubieten, in denen der Umgang mit dem Passwort‑Manager, das Prüfen der Passwortstärke und das Einspielen von Updates erklärt werden. Schließlich kann eine optionale Passwort‑Auditing‑Funktion im Manager eingesetzt werden, mit der Nutzer Schwachstellen in ihren Passwörtern erkennen und verbessern können – so bleibt die gesamte Passwortlandschaft im Unternehmen übersichtlich und sicher.

### KONF.12.5 – Auto-Vervollständigung von Daten

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.19, G 0.30

> Konfiguration für Webbrowser SOLLTE die Auto-Vervollständigung von Daten einschränken.

Webseiten können Eingaben auch auslesen, bevor diese abgesendet werden. Die Deaktivierung der Auto-Vervollständigung verhindert, dass der Browser diese Daten automatisch eingibt.

### KONF.12.6 – Browser-Historie

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.19, G 0.14

> Konfiguration für Webbrowser KANN die dauerhafte Browser-Historie deaktivieren.

Kann durch das Löschen der Historie beim Beenden oder durch Deaktivierung der Historie umgesetzt werden.

### KONF.12.7 – Erweiterte Attribute

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.30, G 0.22

> Konfiguration für Dateiserver SOLLTE erweiterte Attribute aktivieren.

Erweiterte Attribute ermöglichen die Speicherung von Metadaten zu Dateien zur Speicherung von Zugriffsrechten und Statusindikatoren. Kann unter Linux durch Samba mit Extended Attributes und unter Windows durch Nutzung des NTFS-Dateisystems umgesetzt werden.

### KONF.12.8 – Teilnahme per Default ohne Bild und Ton

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.19, G 0.14

> Konfiguration für VK-Anwendungen SOLLTE beim Beitritt zu Konferenzschaltungen Bild und Ton per Default deaktivieren.

Eine Konfiguration, bei der die Standardeinstellung (per default) für Bild und Ton deaktiviert ist, bedeutet, dass Nutzerinnen und Nutzer die Videokonferenz-Anwendungen (VK-Anwendungen) betreten, ohne dass ihre Kamera und ihr Mikrofon automatisch eingeschaltet sind. Diese Voreinstellung minimiert das Risiko, dass sensible oder private Informationen unbeabsichtigt geteilt werden. Einem Vorfall, bei dem vertrauliche Gespräche im Hintergrund unfreiwillig übertragen werden, könnte so effektiv vorgebeugt werden. Die Institution kann dadurch das Risiko unbeabsichtigter Datenexposition minimieren, indem die Kontrolle über die Aktivierung von Bild und Ton explizit bei den Nutzenden bleibt. Um diese Anforderung umzusetzen, kann die Institution die technischen Einstellungen in der Verwaltungs- oder Admin-Konsole der jeweiligen Anwendung anpassen, um die Standardwerte für alle Teilnehmenden zu ändern. Ebenfalls kann eine technische Richtlinie implementiert werden, die sicherstellt, dass die Applikation vor dem Start eines Meetings eine Checkliste anzeigt, die die Nutzenden explizit auffordert, Kamera und Mikrofon bewusst zu aktivieren.

### KONF.12.9 – Keine heimliche Aufzeichnung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.19, G 0.29

> Konfiguration für VK-Anwendungen SOLLTE heimliche Aufzeichnungen deaktivieren.

Heimliche Aufzeichnungen verletzen die Vertraulichkeit der Kommunikation. Eine Aufzeichnung von Wort und Bild ohne den Willen der Aufgezeichneten kann zudem eine Persönlichkeitsrechtsverletzung bis hin zur Straftat (§ 201 StGB) darstellen. Falls die Anwendung so konfiguriert ist, dass Bild und Ton aufgezeichnet werden könnten, ist es daher unabdingbar, dass alle Teilnehmenden von der Anwendung über die Aufzeichnung informiert werden - auch wenn sie eine Konfernzschaltung später betreten oder kurz nicht zugehört haben. Dies gilt auch für Aufzeichnungen, die KI-gestützt ausgewertet werden. Falls die Möglichkeit zur Aufzeichnung vollständig deaktiviert ist, so ist diese Anforderung ebenfalls erfüllt. Alternativ kann die Anforderung auch erfüllt werden, indem die Anwendung beim Start einer Aufnahme alle Teilnehmenden informiert, z.B. über die Anzeige eines zu bestätigenden Warnhinweises und eine Ansage.

### KONF.12.10 – Cookie-Attribute

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.19, G 0.43

> Konfiguration für Webanwendungen SOLLTE Cookie-Attribute aktivieren.

"Secure" erzwingt die verschlüsselte HTTPS-Übertragung, wodurch Man-in-the-middle-Angriffe verhindert werden. "SameSite" sorgt dafür, dass Cookies nur zurückgesendet werden, wenn die Anfrage von der ursprünglichen Seite stammt. Hierdurch werden Cross-Site-Request-Forgery-Angriffe erschwert. "HttpOnly" verbietet es Client-seitigen Skripten auf das Cookie zuzugreifen, wodurch Cross-Site Scripting (XSS) erschwert wird.

### KONF.12.11 – Anonyme oder Pseudonyme Kommunikation

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.19, G 0.14

> Konfiguration für TK-Anwendungen KANN die Übermittlung *[eines Pseudonyms oder gar keiner Anzeigekennung]* zur Gegenstelle aktivieren.

Wenn eine persönliche Identifikation von Kommunikationspartnern erforderlich ist, ist eine Verschleierung von Erreichbarkeiten sinnvoll. In der klassischen Telefonie kann hierfür die Rufnummerunterdrückung für ausgehende Anrufe (CLIR) oder eine Pseudonymisierung, z.B. durch Übermittlung der 0 statt der Nebenstelle, genutzt werden. Für die Verschleierung der Netzquelle können Proxy-Server oder Anonymisierungsgateways genutzt werden. Für weitere Details siehe "Kompendium für organisationsinterne Telekommunikationssysteme mit erhöhtem Schutzbedarf".

### KONF.12.12 – Verbindungsprotokoll

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.37, G 0.23

> Konfiguration für TK-Anwendungen SOLLTE ein für Nutzende verfügbares Verbindungsprotokoll protokollieren.

Ein solches Protokoll, oft auch als Call Detail Record (CDR) oder Connection Log bezeichnet, dokumentiert für Nutzende nachvollziehbar die Kommunikationsverbindungen, die sie über die Anwendung herstellen. Das Protokoll könnte dabei erfassen, wann eine Verbindung aufgebaut wurde, wie lange sie bestand, mit wem sie stattfand (z.B. die Rufnummer oder der Benutzername der Gegenstelle) und aus welcher Richtung (ein- oder ausgehend) sie kam. In der klassischen Telefonie ist dies die Auflistung der zuletzt ein- oder ausgehenden Anrufe. Eine solche Protokollierung kann als wichtige Maßnahme der Rechenschaftspflicht oder Accountability dienen. Durch die lückenlose Protokollierung der Aktivitäten der Nutzenden kann transparent nachvollzogen werden, welche Verbindungen zu welchem Zeitpunkt hergestellt wurden. Dies kann dabei helfen, ungewöhnliche oder nicht autorisierte Kommunikationsversuche zu erkennen und die Integrität der genutzten Systeme zu wahren. Ohne ein solches Protokoll könnte eine unberechtigte Nutzung oder ein Datenabfluss aus dem internen Netzwerk unentdeckt bleiben. Hierbei besteht ein enger Zusammenhang mit Compliance-Verpflichtungen zur Aufbewahrung und Löschung von Telekommunikationsdaten.

### KONF.12.13 – Sendebericht

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.37

> Konfiguration für Faxe SOLLTE einen Sendebericht protokollieren.

Ein Sendebericht ermöglicht es bei der Verwendung von Faxen nachzuweisen, dass das Fax tatsächlich an die Gegenstelle versendet wurde. Für einen rechtssicheren Nachweis ist es sinnvoll, wenn der Sendebericht außerdem weitere Angaben wie die versendete Seitenzahl, eine Vorschau der ersten Seite odes des gesamten Inhaltes, sowie den Status mit dem die Verbindung beendet wurde (z.B. OK) beinhaltet.

### KONF.12.14 – DNS-Falschinformationen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.43, G 0.22

> Konfiguration für DNS-Server SOLLTE DNS-Antworten, die falsche Domain-Informationen liefern, deaktivieren.

Falsch sind Domain-Informationen, wenn sie nicht der tatsächlichen Erreichbarkeit des Zieles entsprechen, sondern z.B. auf Werbeseiten umleiten. DNS-Server, die falsche Antworten liefern, können zu unerwarteten Fehlern in Anwendungen oder zum DNS-Hijacking führen. Sie sind an unerwarteten Websites, Zertifikatsfehlern oder mit DNS-Prüfsoftware zu erkennen. Gilt sowohl für die Konfiguration des eigenen Servers, als auch für die verwendeten DNS Upstream Server.

## KONF.13 Senden und Empfangen von Nachrichten

### KONF.13.1 – Filtern schädlicher Nachrichten

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für Interpersonelle Kommunikation SOLLTE eine Filterung schädlicher Nachrichteninhalte aktivieren.

Unter Filterung schädlicher Nachrichteninhalte versteht man Verfahren, die Inhalte automatisch prüfen und unerwünschte, gefährliche oder manipulative Bestandteile erkennen, blockieren oder kennzeichnen können. Der Sinn dieser Vorgabe liegt darin, potenziell gefährliche Inhalte wie Phishing-Versuche, schadhaften Code oder gezielte Desinformation frühzeitig abzufangen. Ohne eine solche Filterung könnte Schadsoftware über Anhänge eingeschleust werden oder Mitarbeitende könnten durch manipulierte Links zu vertraulichen Datenabgaben verleitet werden. Mit einer wirksamen Filterung kann die Angriffsfläche reduziert, das Vertrauen in die Kommunikationskanäle erhöht und die Produktivität geschützt werden. Zur Umsetzung kann eine Institution technische Maßnahmen kombinieren: (1) E-Mail-Gateways oder Chat-Schnittstellen können mit Inhaltsfiltern ausgestattet werden, die bekannte Malware-Signaturen, verdächtige Links oder gefährliche Dateitypen erkennen. (2) Ergänzend kann heuristische Analyse und maschinelles Lernen eingesetzt werden, um Muster verdächtiger Inhalte zu identifizieren, auch wenn diese noch nicht in Signaturdatenbanken enthalten sind. (3) Regeln zur Blockierung bestimmter Dateianhänge (z. B. ausführbare Dateien) können eingerichtet werden, während sichere Alternativen für den Austausch bereitgestellt werden. (4) Schließlich kann ein klarer Prozess vorgesehen werden, um falsch-positive Erkennungen manuell zu prüfen und legitime Kommunikation wieder freizugeben.

#### KONF.13.1.1 – SPAM-Filter

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.39, G 0.42

> Konfiguration für Interpersonelle Kommunikation SOLLTE die Zustellung unerwünschter Nachrichten blockieren.

Unter Zustellung unerwünschter Nachrichten ist das Blockieren oder Filtern von Spam, Phishing-Versuchen, Social-Engineering-Nachrichten oder belästigender Kommunikation zu verstehen. Diese Anforderung zielt darauf ab, die Integrität der Kommunikationskanäle zu wahren und das Risiko von Sicherheits- oder Vertrauensbrüchen zu reduzieren. Ohne geeignete Filtermechanismen könnte Schadsoftware per Anhang eingeschleust werden, sensible Informationen könnten durch täuschend echte Phishing-Nachrichten abgegriffen werden oder Mitarbeitende könnten durch gezielte Belästigungen in ihrer Arbeitsfähigkeit eingeschränkt werden. Zur Umsetzung kann eine Institution verschiedene Ansätze kombinieren: (1) Der Einsatz serverseitiger Filtermechanismen auf Mail-Gateways oder Collaboration-Plattformen kann zentral die meisten unerwünschten Nachrichten aussortieren. (2) Ergänzend können clientseitige Filterregeln aktiviert werden, die Benutzern zusätzliche Möglichkeiten zur Sortierung bieten, etwa über Whitelists und Blacklists. Praktisch kann es auch hilfreich sein, Quarantäneordner einzurichten, damit Anwender verdächtige Nachrichten selbständig einsehen und fälschlich blockierte Nachrichten zurückholen können.

#### KONF.13.1.2 – Interpretation aktiver Inhalte

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.39, G 0.23

> Konfiguration für Interpersonelle Kommunikation SOLLTE die automatische Interpretation aktiver Inhalte deaktivieren.

Unter aktiven Inhalten sind hier Elemente zu verstehen, die beim Empfang automatisch ausgeführt oder interpretiert werden könnten, wie z. B. eingebettete Skripte in E-Mails, dynamische Makros in Dokumenten oder der automatische Download von externen Bildern in Chat-Nachrichten. Hintergrund ist, dass eine empfangene Nachricht nicht nur reinen Text oder statische Informationen enthalten könnte, sondern zusätzliche versteckte Anweisungen, die beim Anzeigen sofort wirken. Ein typischer Vorfall könnte etwa sein, dass eine Mitarbeiterin eine HTML-E-Mail öffnet, die ein eingebettetes JavaScript enthält und dadurch unbemerkt Zugangsdaten abgegriffen werden. Durch Deaktivieren solcher Inhalte wird verhindert, dass Schadcode automatisch ausgeführt wird. Dies betrifft sowohl Inhalte in Freitext-Datenfeldern als auch an die Nachricht angehängte Dateien. Beispielsweise kann in Mail-Clients die Ausführung von Makros deaktiviert, die Darstellung externer Inhalte blockiert oder das Rendern von Skripten untersagt werden. Ebenso kann bei Messaging-Diensten die Anzeige von aktiven Inhalten durch Filter eingeschränkt werden, sodass nur reiner Text oder geprüfte Anhänge angezeigt werden. Ergänzend kann es hilfreich sein, benutzerseitige Tipps wie das standardmäßige Verwenden einer Nur-Text-Ansicht oder die klare Kennzeichnung von blockierten Inhalten zu etablieren. Institutionen können durch regelmäßige Konfigurationsprüfungen sicherstellen, dass Änderungen durch Updates oder neue Versionen die Deaktivierung nicht unbemerkt wieder aufheben.

### KONF.13.2 – Authentizität von Nachrichten

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.36, G 0.22

> Konfiguration für Interpersonelle Kommunikation SOLLTE eine automatische Verifikation der Authentizität von Nachrichten aktivieren.

Die Authentizität von Nachrichten bezeichnet in diesem Zusammenhang die nachweisbare Echtheit und Unverfälschtheit einer digitalen Mitteilung im Rahmen der interpersonellen Kommunikation, also die Sicherheit, dass eine Nachricht tatsächlich von der angegebenen Quelle stammt und auf dem Übertragungsweg nicht manipuliert wurde. Im Fachjargon wird hier häufig von Message Authenticity oder auch von Origin Authentication gesprochen, wobei beide Begriffe eng mit kryptographischen Verfahren wie Digital Signatures oder Message Authentication Codes (MACs) verbunden sind. Der Sinn dieser Anforderung liegt darin, sicherzustellen, dass Angreifer keine falschen Identitäten vortäuschen oder den Inhalt von Nachrichten unbemerkt verändern können. Andernfalls könnte etwa eine gefälschte Anweisung in einem Chat zu Fehlhandlungen führen oder ein manipuliertes Dokument im E-Mail-Verkehr falsche Entscheidungen auslösen. Eine automatische Verifikation kann hingegen das Vertrauen in die Integrität und Herkunft der Kommunikation gewährleisten. Zur Umsetzung kann eine Institution beispielsweise digitale Signaturen einsetzen, die durch etablierte Standards wie S/MIME oder OpenPGP realisiert werden können, sodass E-Mail-Programme die Echtheit automatisch überprüfen. Auch der Einsatz von Ende-zu-Ende-Verschlüsselung mit eingebauter Authentizitätsprüfung, etwa bei Protokollen wie Signal Protocol oder TLS mit Client-Zertifikaten, kann eine geeignete Maßnahme sein. Darüber hinaus kann die Integration einer zentralen Public Key Infrastructure (PKI) oder die Nutzung verteilter Vertrauensmodelle (z. B. Web of Trust) sicherstellen, dass Schlüsselpaare zuverlässig verwaltet werden und Anwender ohne manuelle Prüfungen von Zertifikaten auskommen.

#### KONF.13.2.1 – Verifikation der Sendeberechtigung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.43, G 0.36

> Konfiguration für E-Mail SOLLTE eine automatische Verifikation der Sendeberechtigung aktivieren.

Mit dem Sender Policy Framework (SPF) kann geprüft werden, ob der Sender zum Versand von E-Mails für diese Mailadresse berechtigt war. E-Mails ohne SPF-Header sind unzureichend authentifiziert, so dass sie leicht für Spoofing oder Phishing missbraucht werden können. Allerdings werden noch immer E-Mails ohne SPF verschickt, so dass eine Blockierung zu funktionalen Einschränkungen führen könnte. Kompromissmaßnahmen können z.B. die Markierung der E-Mail mit einem Warnhinweis , Allowlisting, Greylisting, Quarantäne oder eine Filterung durch Anomalieerkennung sein.

#### KONF.13.2.2 – Verifikation der Serversignatur

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.36, G 0.46

> Konfiguration für E-Mail SOLLTE die Serversignatur eingehender E-Mails automatisch authentifizieren.

Die DKIM-Signatur ist zu unterscheiden von einer PGP-Signatur, die in der Regel nicht automatisch vergeben wird. E-Mails ohne DKIM sind unzureichend authentifiziert, so dass sie leicht für Spoofing oder Phishing missbraucht werden können. Allerdings werden noch immer E-Mails ohne DKIM verschickt, so dass eine Blockierung zu funktionalen Einschränkungen führen könnte. Kompromissmaßnahmen können z.B. die Markierung der E-Mail mit einem Warnhinweis , Allowlisting, Greylisting, Quarantäne oder eine Filterung durch Anomalieerkennung sein. Die Formulierung "im Einklang mit den Festlegungen des Identitäts- und Berechtigungsmanagements" bedeutet, dass die Authentifizierung so erfolgt, wie in der Praktik IDM festgelegt. Hierzu gehört insbesondere die Verwendung aktueller kryptographischer Verfahren, wie sie im Thema Kryptographie zu finden ist.

### KONF.13.3 – Kryptographische Signatur des Mailservers

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.36, G 0.46

> Konfiguration für E-Mail SOLLTE die Kryptographische Signatur des Mailservers aktivieren.

Die kryptographischen Signatur des Mailservers ist ein digitaler Stempel des versendenden Mailservers selbst, mit dem die Authentizität des sendenden Mailservers belegt wird. Ein bekannter technischer Standard hierfür ist DomainKeys Identified Mail (DKIM). Diese Signatur wird durch den absendenden Mailserver (oder einen vorgeschalteten Dienst) unter Verwendung eines privaten kryptographischen Schlüssels erzeugt. Der Empfänger kann die Signatur mit einem öffentlich zugänglichen Schlüssel, der typischerweise im Domain Name System (DNS) der sendenden Domain hinterlegt ist, verifizieren. Diese Schutzmaßnahme kann die Glaubwürdigkeit der E-Mails erhöhen und trägt zur Prävention von Risiken bei, wie dem Spoofing des Absenders: Ein Angreifer könnte ohne eine solche Signatur die Identität der Institution vortäuschen, was zu Phishing-Vorfällen führen könnte.

### KONF.13.4 – Kryptographische Signatur durch Nutzende

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.36, G 0.37

> Konfiguration für E-Mail KANN die kryptographische Signatur durch Nutzende aktivieren.

Wird eine vom E-Mail vom Sendenden signiert, so können bei Empfang die Authentizität und Integrität der Nachricht verifiziert werden. Dies kann mit S/MIME oder PGP umgesetzt werden.

### KONF.13.5 – Publikation der Sendeberechtigung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.36, G 0.43

> Konfiguration für E-Mail SOLLTE die Publikation der eigenen Sendeberechtigung im DNS aktivieren.

Dies wird typischerweise über spezielle DNS-Einträge wie den Sender Policy Framework (SPF) realisiert. Damit kann eine Institution im DNS festlegen, welche Mail-Server berechtigt sind, E-Mails im Namen ihrer Domäne zu versenden. Ein entsprechender DNS-Eintrag, der sogenannte SPF-Record, ermöglicht es empfangenden Mail-Servern, die Absender-Adresse einer eingehenden E-Mail zu überprüfen. Dies kann die Schutzwirkung gegen gängige Risiken wie E-Mail-Spoofing verbessern, bei dem sich ein Angreifer als legitimer Absender ausgibt, um die Empfänger zu täuschen. Ohne eine solche Konfiguration könnte ein Angreifer beispielsweise E-Mails mit gefälschter Absenderadresse verschicken, die scheinbar von der Geschäftsleitung stammen, um einen Nutzer zur Herausgabe von sensiblen Informationen zu verleiten (Phishing). Durch die Aktivierung von SPF kann das Risiko verringert werden, dass solche bösartigen Nachrichten die Postfächer von Nutzern erreichen. Es ist wichtig, den Eintrag sorgfältig zu erstellen, um alle legitimen Absender abzudecken, einschließlich Diensten von Drittanbietern. Ein häufiger Fehler ist, dass nicht alle autorisierten Mail-Server korrekt gelistet sind, was dazu führen könnte, dass legitime E-Mails fälschlicherweise als Spam markiert werden.

#### KONF.13.5.1 – Strenge Senderpolicy

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.36, G 0.42

> Konfiguration für E-Mail SOLLTE eine strenge Senderpolicy aktivieren.

Ein strenger Senderpolicy-Eintrag, auch "hard fail" (-all) genannt, weist empfangende Mailserver an, E-Mails, die von nicht autorisierten Servern stammen, zurückzuweisen oder als Spam zu markieren. Dies kann das Risiko von Phishing-Angriffen erheblich reduzieren, bei denen Angreifer versuchen, sich als vertrauenswürdige Institutionen auszugeben. Eine solche Konfiguration kann auch Spoofing verhindern, bei dem die Absenderadresse gefälscht wird, was dazu führen könnte, dass Kunden oder Mitarbeiter betrügerischen Anweisungen folgen, die scheinbar von der Institution selbst stammen. Zur Umsetzung einer strengen Senderpolicy kann die Institution sicherstellen, dass sie einen SPF-Eintrag in ihren DNS-Einstellungen hinterlegt. Dieser Eintrag sollte alle autorisierten Server explizit auflisten und mit dem "-all" Mechanismus enden, um eine strikte Ablehnung nicht konformer E-Mails zu signalisieren.

### KONF.13.6 – Publikation der Serversignatur

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.36, G 0.46

> Konfiguration für E-Mail SOLLTE die Publikation der Serversignatur im DNS aktivieren.

Eine Serversignatur, auch bekannt als DKIM (DomainKeys Identified Mail), ist eine kryptografische Signatur, die der E-Mail-Dienst der Institution an jede ausgehende Nachricht anhängt. Sie stellt sicher, dass die E-Mail tatsächlich von der angegebenen Domain gesendet wurde und während der Übertragung nicht manipuliert wurde. Ohne diese Signatur könnte ein Angreifer E-Mails im Namen der Institution versenden (E-Mail-Spoofing), was zu Phishing-Angriffen, dem Diebstahl von Zugangsdaten oder der Verbreitung von Malware führen könnte. Das Aktivieren der Publikation im DNS bedeutet, den öffentlichen Teil dieses kryptografischen Schlüssels im Domain Name System (DNS) der Domain zu veröffentlichen. Empfangende E-Mail-Server können diesen öffentlichen Schlüssel verwenden, um die Signatur der E-Mail zu verifizieren und somit deren Echtheit zu bestätigen. Zur Umsetzung kann die Institution E-Mail-Server-Software so konfigurieren, dass sie DKIM-Signaturen automatisch zu ausgehenden Nachrichten hinzufügt. Dies kann oft durch die Installation und Konfiguration von speziellen DKIM-Filter-Plugins erreicht werden.

### KONF.13.7 – TLS-Reports

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.43, G 0.15

> Konfiguration für E-Mail KANN TLS-Reports *[regelmäßig]* überprüfen.

TLS-Reports, auch TLS-RPT (Transport Layer Security Reporting) genannt, sind Berichte, mit denen Betreiber von Mailservern einander Probleme beim E-Mail-Versand über TLS melden können. Sie können Informationen zu Verbindungsproblemen und möglichen Sicherheitsproblemen enthalten. Hierzu kann TLS-RPT (Transport Layer Security Reporting) genutzt werden.

### KONF.13.8 – DMARC-Reports

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.36, G 0.42

> Konfiguration für E-Mail KANN DMARC-Reports *[regelmäßig oder bei Eingang]* überprüfen.

Mit DMARC kann der Empfänger dem Sender automatische Berichte über den DMARC-Status empfangener E-Mails bereitstellen. Diese Berichte liefern Hinweise auf fehlgeschlagene Authentifizierungsprüfungen, Fehlkonfigurationen oder Missbrauchsversuche. Eine automatisierte Auswertung unterstützt dabei, Zustellprobleme frühzeitig zu erkennen und geeignete Korrekturmaßnahmen abzuleiten.

### KONF.13.9 – Publikation der DMARC-Richtlinie

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.36, G 0.42

> Konfiguration für E-Mail SOLLTE die Publikation der DMARC-Richtlinie aktivieren.

Eine DMARC-Richtlinie legt fest, welchen Umgang sie sich von Empfängern wünschen, die E-Mails von ihrer Domain nicht authentifizieren können. Die Information der Empfänger kann über einen DMARC-Eintrag im DNS erfolgen.

### KONF.13.10 – Authentifizierung der Server-Zertifikate über DNS

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.43, G 0.36

> Konfiguration für E-Mail SOLLTE die Authentifizierung der Server-Zertifikate über das DNS aktivieren.

Die Authentifizierung der Server-Zertifikate über das DNS (Domain Name System) kann die Sicherheit der E-Mail-Kommunikation erheblich steigern. Dabei werden Zertifikatsinformationen in DNS-Einträgen genutzt, um die Echtheit der TLS/SSL-Zertifikate eines E-Mail-Servers zu überprüfen und sicherzustellen, dass man tatsächlich mit dem beabsichtigten Kommunikationspartner spricht. Techniken wie DANE (DNS-based Authentication of Named Entities) oder CAA (Certificate Authority Authorization) nutzen spezifische DNS-Resource Records (wie TLSA oder CAA Records), um entweder die verwendeten Zertifikate oder die autorisierten Zertifizierungsstellen im DNS zu hinterlegen. Dies kann verhindern, dass ein Angreifer eine gefälschte Identität vortäuschen oder eine Man-in-the-Middle-Attacke durchführen könnte, indem er ein nicht autorisiertes oder kompromittiertes Zertifikat präsentiert. Ohne diese zusätzliche Überprüfung könnte ein Angreifer beispielsweise den E-Mail-Verkehr der Institution abfangen und mitlesen, während er sich als der legitime Server ausgibt. Die Aktivierung dieser DNS-basierten Überprüfung kann also die Vertraulichkeit und Integrität der übertragenen E-Mails schützen. Zur Umsetzung werden Informationen über eigene Serverzertifikate im DNS hinterlegt und die Prüfung eingehender E-Mails auf hinterlegte Einträge der sendenden Servers aktiviert.

### KONF.13.11 – MTA-STS

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.43, G 0.15

> Konfiguration für E-Mail SOLLTE MTA-STS aktivieren.

Die Mail Transfer Agent Strict Transport Security (MTA-STS) ist ein wichtiger Standard zur Erhöhung der Sicherheit im E-Mail-Verkehr, der die verschlüsselte Zustellung von Nachrichten durch die Erzwingung von Transport Layer Security (TLS) auf der Übertragungsebene gewährleistet. MTA-STS stellt dabei sicher, dass versendende Mail Transfer Agents (MTA) nur verschlüsselte Verbindungen zum Ziel-MTA aufbauen, wodurch Downgrade-Angriffe oder die Umleitung auf unsichere Kanäle wirksam unterbunden werden können. Der Zweck dieser Vorschrift liegt darin, die Vertraulichkeit und Integrität von E-Mail-Inhalten während der Übertragung zu schützen. Ohne MTA-STS könnte ein Angreifer die Kommunikation abfangen und den unverschlüsselten E-Mail-Verkehr mitlesen (Eavesdropping) oder die Nachricht manipulieren, bevor sie den Empfänger erreicht. Die Aktivierung kann das Risiko minimieren, dass E-Mails über unsichere oder unauthentifizierte Verbindungen übertragen werden, selbst wenn die Ziel-Institution TLS unterstützt, was einen robusten Schutz gegen gängige Man-in-the-Middle-Angriffe bietet. Obwohl DNS-Based Authentication of Named Entities (DANE) eine stärkere kryptografische Authentifizierung des TLS-Zertifikats des Ziel-MTA bietet, sollte MTA-STS zusätzlich aktiviert werden, da es eine alternative oder ergänzende Schutzschicht darstellt, falls DANE beim Kommunikationspartner noch nicht implementiert ist oder dessen DNS-Sicherheit (DNSSEC) nicht vertrauenswürdig ist.

## KONF.14 Verteilte Anwendungen

### KONF.14.1 – Verschlüsselung beim Transport

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.43, G 0.15

> Konfiguration für Anwendungen SOLLTE Kommunikation beim Transport über Netze nach *[einem anerkannten Standard]* verschlüsseln.

Werden Daten unverschlüsselt übertragen, so könnten sie abgehört oder unbemerkt manipuliert werden. Relevant sind hierbei alle von der Anwendung übertragenen Daten, inklusive Authentifizierung an der Benutzerschnittstelle oder API, Abruf von Daten, Server-Server-Replikation oder zur Datensicherung. Das betrifft sowohl Inhalts- als auch Metadaten. Die Umsetzung kann mit Algorithmen zur Transportverschlüsselung wie Transport Layer Security (TLS) oder Ende-zu-Ende-Verschlüsselung erfolgen. Für aktuelle Verschlüsselungsverfahren siehe BSI TR-02102. Die Konfiguration der Verschlüsselung kann sich daran orientieren, wie lange die transportieren Daten, z.B. Transaktionen, vertraulich zu behandeln sind. Eine Herausforderung hierbei sind Anwendungen, die über allgemeine Anbindungen mit anderen Institutionen kommunizieren, z.B. E-Mails oder Anrufe ins öffentliche Telefonnetz. Diese Anwendungen können nur ihren Teil der Verbindungsstrecke verschlüsseln, so dass der Rest der Strecke und damit die Verbindung an sich dennoch unverschlüsselt sein könnte. Überträgt die Anwendung keine schützenswerten Daten über das Netz, so ist die Anforderung entbehrlich.

#### KONF.14.1.1 – Obligatorische Verschlüsselung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.43, G 0.15

> Konfiguration für Anwendungen SOLLTE unverschlüsselte und anfällige Verbindungen über Netze deaktivieren.

Obligatorische Verschlüsselung bedeutet, dass die Anwendung ausschließlich nach dem Stand der Technik verschlüsselt kommuniziert. Unverschlüsselte oder mit bekannten Methoden angreifbare Verbindungsanfragen werden dagegen abgelehnt. Die Verwendung obligatorischer Verschlüsselung im Internet ist aktuell sehr uneinheitlich: Viele E-Mail-Server z.B. verschlüsseln im Auslieferungszustand nur opportunistisch - also nur wenn der Verbindungsaufbau so funktioniert. Das macht Verbindungen anfällig für Downgrade-Angriffe. Diese lassen sich verhindern, indem unverschlüsselte Verbindungen vollständig deaktiviert werden. Andererseits kann es dadurch auch zu Verbindungsproblemen mit Servern kommen, die überhaupt keine Verschlüsselung mit aktuellen Protokollen unterstützen. Für aktuelle Verschlüsselungsverfahren siehe BSI TR-02102.

#### KONF.14.1.2 – Ende-zu-Ende-Verschlüsselung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.19, G 0.15

> Konfiguration für Anwendungen KANN die Kommunikation Ende-zu-Ende über Netze verschlüsseln.

Eine Ende-zu-Ende-Verschlüsselung stellt sicher, dass auch Server auf dem Weg zwischen den Endpunkten die Kommunikation nicht auslesen können. Die Unterstützung von Ende-zu-Ende-Verschlüsselung unterscheidet sich zwischen verschiedenen Kommunikationsanwendungen noch immer erheblich: Viele E-Mail-Server verschlüsseln gar nicht oder nur bei Verwendung spezieller Erweiterungen so, während viele Messenger-Apps die Ende-zu-Ende-Verschlüsselung ohne Nutzerinteraktion automatisch erzwingen. Dies kann je nach Anwendung z.B. mittels OpenPGP, S/MIME oder Signal Protocol geschehen. Für aktuelle Verschlüsselungsverfahren siehe BSI TR-02102. Für weitere Details zur Telekommunikation siehe "Kompendium für organisationsinterne Telekommunikationssysteme mit erhöhtem Schutzbedarf".

### KONF.14.2 – Source Port Randomisierung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.43, G 0.22

> Konfiguration für DNS-Server SOLLTE Source Port Randomisierung aktivieren.

Die mehrfache Verwendung gleicher Source Ports erleichtert Angreifern das Erraten gültiger Antworten, z. B. bei DNS-Spoofing oder Cache-Poisoning-Angriffen. Sourceport-Randomisierung (IETFC RFC 5452) erhöht die Anzahl möglicher Kombinationen und erschwert derartige Angriffe.

### KONF.14.3 – Iterative Beantwortung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 1 · **Gefährdungen:** G 0.40, G 0.30

> Konfiguration für DNS-Server SOLLTE die iterative Beantwortung von DNS-Anfragen aus dem Internet aktivieren.

Bei iterativen Anfragen kommt die Antwort direkt vom autoritativen Server, statt auf zwischengespeicherte Antworten anderer DNS-Resolver zu vertrauen. Dies reduziert die Angriffsfläche für Cache Poisoning und erschwert DNS-Tunneling zur Datenexfiltration oder Command-and-Control-Kommunikation.

### KONF.14.4 – Caching

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.27, G 0.40

> Konfiguration für Anwendungen von Endgeräten KANN eine Zwischenspeicherung häufig verwendeter Daten aktivieren.

Caches sind lokale Zwischenspeicher, die Zugriffe beschleunigen oder bei Netzstörungen ersetzen können. Kann durch Caching-Funktionen auf dem Client, auf Servern in Außenstellen (z.B. Windows BranchCache, Squid Proxy Cache oder CacheFS) oder Caching auf WAN-Netzkomponenten umgesetzt werden.

### KONF.14.5 – Zeitüberschreitung von Netzverbindungen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.27, G 0.40

> Konfiguration für Anwendungen SOLLTE Netzverbindungen bei Zeitüberschreitung blockieren.

Dauerhaft aufrecht erhaltene, ungenutzte Verbindungen erhöhen die Gefahr unbefugter Zugriffe auf die Anwendung oder eines Überlaufens von Systemressourcen.

## KONF.15 Ressourcenauslastung

### KONF.15.1 – Begrenzung des Speicherplatzes

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.27, G 0.40

> Konfiguration für Anwendungen von Hostsystemen KANN in der Anwendung zur Verfügung stehenden Speicherplatz pro *[Zugangskonto oder Mandant]* anhand von *[Schwellwerten]* einschränken.

Dies ist besonders in Multi-Tenant-Architekturen relevant, wie sie häufig bei Cloud-Diensten oder SaaS-Anwendungen (Software as a Service) zum Einsatz kommen. Ein solcher maximaler Schwellwert (engl. threshold) könnte beispielsweise 5 GB oder 10 GB betragen und stellt die Obergrenze für den Speicherplatz dar, der einem einzelnen Konto oder Mandanten zugewiesen wird. Die Beschränkung des verfügbaren Speicherplatzes kann verhindern, dass ein einzelnes Konto oder ein Mandant die gesamten Ressourcen des Hostsystems belegt und so die Leistung für andere Nutzer negativ beeinflusst, was zu einer Denial-of-Service-Situation (DoS) führen könnte. Bei der Umsetzung ist es sinnvoll auch ein Benachrichtigungssystem zu etablieren, das Nutzer oder Administratoren informiert, wenn ein Schwellenwert kurz vor der Überschreitung steht. Zudem können automatisierte Prozesse zur Datenbereinigung (data lifecycle management) in Betracht gezogen werden, die ältere oder nicht mehr benötigte Dateien in solchen Fällen archivieren oder löschen, um den Speicherplatz effizient zu nutzen. Die Institution kann auch verschiedene Schwellenwerte für unterschiedliche Kontotypen oder Mandanten festlegen, basierend auf deren spezifischen Bedürfnissen.

### KONF.15.2 – Begrenzung der Rechenleistung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.27, G 0.40

> Konfiguration für Anwendungen von Hostsystemen KANN die Rechenleistung einschränken.

Kann durch eine Beschränkung der Anzahl verwendeter Rechenkerne, der Rechenleistung pro Rechenkern oder durch eine indirekte Beschränkung (z.B. eine begrenzte Menge an Anfragen oder Eingabetoken) umgesetzt werden. Beispielsweise kann in einem Verzeichnisdienst ein maximaler Schwellwert für die Zeit eingestellt werden, die eine Suchanfrage in Anspruch nehmen darf, um die Auslastung des Verzeichnisdienstes durch einzelne Anfragen nicht zu gefährden.

### KONF.15.3 – Denial of Service

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.27, G 0.40

> Konfiguration für Anwendungen von Hostsystemen KANN Schutzmaßnahmen gegen Denial of Service aktivieren.

Denial-of-Service-Angriffe zielen darauf ab, die Webanwendung für legitime Nutzende nicht mehr erreichbar zu machen. Webanwendungen im öffentlichen Interesse sind häufig Ziel derartiger Angriffe. Mechanismen wie Content Delivery Network und Load Balancer können die Lastfähigkeit der Anwendung erhöhen, während Filterfunktionen Angriffsmuster erkennen und aus den Anfragen herausfiltern können.

### KONF.15.4 – Überbuchung von virtualisierten Ressourcen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.27, G 0.40

> Konfiguration für Virtualisierungslösungen KANN die Überbuchung von virtualisierten Ressourcen deaktivieren.

Die Überbuchung (engl. overcommitment) beschreibt in Virtualisierungslösungen die Zuweisung von mehr virtuellen Ressourcen – etwa CPU-Kernen, Arbeitsspeicher oder Speicherplatz – an virtuelle Instanzen, als physisch tatsächlich vorhanden sind. Dies kann kurzfristig zu einer höheren Auslastung und Dichte von virtuellen Instanzen führen, birgt jedoch das Risiko, dass die zugrunde liegende Hardware unter Last nicht mehr alle angefragten Ressourcen bereitstellen kann. Der Zweck der Anforderung liegt darin, die Stabilität, Verfügbarkeit und Vorhersehbarkeit der virtualisierten Umgebung sicherzustellen. Ohne diese Begrenzung könnte es unter hoher Auslastung zu Leistungseinbrüchen, Systemabstürzen oder inkonsistenten Speicherzuständen kommen, während eine restriktive Konfiguration die Zuverlässigkeit und die Berechenbarkeit der Performance einer virtuellen Infrastruktur deutlich verbessern kann. Eine Institution kann die Umsetzung dieser Vorgabe durch verschiedene Maßnahmen erreichen: (1) In der Hypervisor-Konfiguration kann die Vergabe virtueller CPUs und Arbeitsspeicher exakt auf die physisch vorhandenen Ressourcen begrenzt werden. (2) Es kann sinnvoll sein, Profile oder Templates für virtuelle Maschinen zu nutzen, die konservative Standardwerte vorgeben, sodass die Gefahr unbeabsichtigter Überbuchung reduziert wird.
