---
title: "DLS – Dienstleistersteuerung"
---

Die Praktik Dienstleistersteuerung regelt die kontinuierliche Überwachung und Steuerung externer Dienstleister, wie etwa Outsourcing-Partner oder Cloud-Anbieter. Sie stellt sicher, dass die erbrachten Leistungen den vereinbarten Sicherheitsanforderungen entsprechen und die Dienstleister ihre vertraglichen Verpflichtungen in Bezug auf die Informationssicherheit erfüllen. Im Gegensatz dazu befasst sich die Praktik Beschaffungsmanagement mit der Auswahl von Dienstleistern sowie der vertraglichen Absicherung, wobei die Integration von Informationssicherheitsanforderungen in den Beschaffungsprozess im Vordergrund steht. Während das Beschaffungsmanagement also die Grundlage für die Zusammenarbeit mit externen Dienstleistern schafft, übernimmt die Dienstleistersteuerung die fortlaufende Kontrolle und das Management dieser Beziehungen, um sicherzustellen, dass die vereinbarten Sicherheitsstandards auch langfristig eingehalten werden.

## DLS.1 Grundlagen

### DLS.1.1 – Verfahren und Regelungen

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18

> Dienstleistersteuerung für Dienstleistungen MUSS ein Verfahren zur Steuerung und geordneten Beendigung von Dienstleistungsverträgen verankern.

Hierzu gehört die Kontrolle der Einhaltung von Vereinbarungen zur Sicherheit mit Dienstleistern und (falls erforderlich) einen geeigneten Weg für die Beendigung von Verträgen vorzubereiten. Die bei der Festlegung des Verfahrens im Einzelnen zu berücksichtigenden Inhalte ergeben sich aus den Anforderungen dieser Praktik.

#### DLS.1.1.1 – Dokumentation

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.37

> Dienstleistersteuerung für Dienstleistungen MUSS die Verfahren und Regelungen dokumentieren.

Ohne eine Dokumentation könnte die Einhaltung der Verfahren und Regelungen von der Tagesform oder dem individuellen Wissen einzelner Mitarbeiter abhängen, was zu inkonsistenten Entscheidungen und Fehlern führen könnte; insbesondere beim Ausscheiden eines langjährigen Administrators könnte wertvolles prozessuales Wissen verloren gehen. Eine klare Dokumentation sichert die Verbindlichkeit und Wiederholbarkeit und dient als unverzichtbare Grundlage für die Einarbeitung neuer Kollegen, für die Durchführung von Audits und zur einheitlichen Anwendung der Regeln in der gesamten Institution. Die Dokumentation kann in einem eigenständigen Dokument als Richtlinie erfolgen, aber auch als Abschnitt in einem bereits bestehenden Dokument oder über die digital strukturiere Erfassung von Maßnahmen zur Umsetzung der Anforderungen, etwa über eine Software zum Management der Informationssicherheit. Sinnvoll ist es Ort und Struktur der Dokumentation an der jeweiligen Zielgruppe, d.h. den für das Management und die Umsetzung verantwortlichen Personen oder Rollen, auszurichten.

#### DLS.1.1.2 – Zuweisung der Aufgaben

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.31

> Dienstleistersteuerung für Dienstleistungen MUSS die mit den Verfahren und Regelungen verbundenen Aufgaben *[zuständigen Personen oder Rollen]* zuweisen.

Die Zuweisung von Aufgaben bezeichnet die eindeutige und verbindliche Übertragung von konkreten Tätigkeiten und Verantwortlichkeiten des Änderungsprozesses, wie etwa die Risikobewertung, die technische Umsetzung oder die finale Freigabe, an definierte Stellen in der Institution. Der Sinn dieser Vorschrift ist es, die Verantwortlichkeit ("Accountability") für jeden einzelnen Schritt im Prozess klarzustellen. Ohne eine solche Zuweisung könnten kritische Prüfungen unterbleiben, weil sich niemand explizit zuständig fühlt, was wiederum die Wahrscheinlichkeit fehlgeschlagener Änderungen erhöht. Eine klare Regelung kann sicherstellen, dass keine Aufgaben übersehen werden und jede Tätigkeit von einer dafür qualifizierten und befugten Stelle ausgeführt wird, was die Prozesssicherheit signifikant erhöht. Eine bewährte Methode zur Umsetzung ist die Erstellung einer RACI-Matrix (Responsible, Accountable, Consulted, Informed), die tabellarisch für jeden Prozessschritt darstellt, wer für die Durchführung verantwortlich ist, wer die Gesamtverantwortung trägt, wer zu konsultieren und wer zu informieren ist. Diese Zuständigkeiten können auch direkt in einem Workflow- oder Ticketsystem abgebildet werden, sodass Aufgaben, wie beispielsweise Genehmigungsschritte, automatisch an die richtige Gruppe oder Person weitergeleitet werden. Sinnvoll ist es die Zuweisung anhand von Rollen (z.B. "Anwendungsverantwortlicher", "Netzwerkadministrator", "Change Manager") vorzunehmen, statt an konkrete Personen. Dieser Ansatz stellt sicher, dass die Prozesse auch bei Personalwechseln stabil weiterlaufen, da die Zuständigkeit an die Funktion und nicht an das Individuum gebunden ist.

#### DLS.1.1.3 – Bekanntgabe

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.31

> Dienstleistersteuerung für Dienstleistungen MUSS die zuständigen Personen oder Rollen über die Verfahren und Regelungen informieren.

Wenn die Zuständigen die etablierten Verfahren nicht kennen, besteht die Gefahr, dass diese – sei es aus Unwissenheit oder Bequemlichkeit – umgangen werden, was die Schutzwirkung des gesamten Managementsystems untergräbt. So könnte ein neuer Systemadministrator eine weitreichende Konfigurationsänderung vornehmen, ohne den vorgeschriebenen Genehmigungsprozess zu durchlaufen, was zu einem unbemerkten Sicherheitsrisiko führen könnte. Eine gezielte Information kann hingegen die Akzeptanz der Regelungen fördern und sicherstellen, dass alle Beteiligten ihre Rolle im Prozess verstehen und die Abläufe korrekt anwenden. Zur Umsetzung ist es sinnvoll die Dokumentation im Rahmen eines Onboarding-Prozesses bekanntzugeben und bei allen Änderungen eine automtatische Benachrichtigung aller zuständigen Personen oder Rollen anzustoßen.

### DLS.1.2 – Regelmäßige Überprüfung

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18

> Dienstleistersteuerung für Dienstleistungen MUSS die Verfahren und Regelungen *[regelmäßig]* und anlassbezogen auf Aktualität überprüfen.

Eine geplante Überprüfung der etablierten Verfahren und Regelungen dient dazu festzustellen, ob diese noch wirksam, effizient und an die aktuellen Gegebenheiten angepasst sind. Eine anlassbezogene Überprüfung wird durch spezifische Ereignisse ausgelöst, wie etwa einen schwerwiegenden Sicherheitsvorfall, eine strategische Neuausrichtung der IT oder neue gesetzliche Anforderungen. Der Zweck dieser Anforderung ist es, die kontinuierliche Verbesserung und Anpassungsfähigkeit des Prozesses sicherzustellen, da veraltete Regelungen neuen technologischen Entwicklungen oder Bedrohungen nicht mehr gerecht werden könnten; ein vor Jahren für monolithische Anwendungen konzipierter Prozess ist beispielsweise für agile Entwicklungsmethoden oder Microservice-Architekturen ungeeignet. Die regelmäßige Überprüfung kann die Effektivität des Sicherheitsmanagements langfristig aufrechterhalten und die Resilienz der Institution stärken.

## DLS.2 Nutzung von digitalen Dienstleistungen

### DLS.2.1 – Mehr-Faktor-Authentifizierung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.14

> Dienstleistersteuerung für Dienstleistungen SOLLTE Mehr-Faktor-Authentifizierung bei Login in Online-Dienste aktivieren.

Online-Dienste wie die Verwaltung von TK-Rufnummern oder Cloud-Office-Anwendungen sind ein beliebtes Ziel für Angriffe durch Phishing oder Datenleaks. Sichern Sie diese Zugänge mit Mehr-Faktor-Authentifizierung (z.B. OTP) ab.

### DLS.2.2 – Transportverschlüsselung

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.18, G 0.14

> Dienstleistersteuerung für Daten SOLLTE den Transport bei der Übertragung zum Anbieter nach *[einem anerkannten Standard]* verschlüsseln.

„Transport“ bedeutet hier der technische Vorgang der Datenübertragung zwischen der Institution und dem Dienstleister, also etwa über das Internet oder dedizierte Leitungen. Der Sinn dieser Vorschrift liegt darin, die Vertraulichkeit und Integrität von Informationen zu schützen, wenn sie in fremde Infrastrukturen überführt werden. Ohne eine solche Maßnahme könnte ein Angreifer Daten während der Übertragung abfangen oder manipulieren, beispielsweise über „Man-in-the-Middle“-Angriffe oder durch Abhören unsicherer Netze. Da beschaffte Dienstleistungen typischerweise außerhalb der direkten Kontrolle der Institution liegen, gibt es hier eine eigene Vorgabe, um die besondere Risikosituation beim Übergang von interner zu externer Infrastruktur gezielt abzusichern. Eine Institution kann die Anforderung praktisch umsetzen, indem sie (1) den Einsatz von Protokollen wie TLS in allen Web- und API-basierten Schnittstellen zum Anbieter sicherstellt, (2) für administrative Zugänge oder besonders sensible Datenübertragungen zusätzlich VPN-Verbindungen nutzen kann, und (3) Zertifikatsprüfungen so konfiguriert, dass unsichere oder abgelaufene Zertifikate nicht akzeptiert werden.

### DLS.2.3 – Vollverschlüsselung

**Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.18, G 0.14

> Dienstleistersteuerung für Daten KANN diese, wenn der Anbieter deren Inhalt zur Vertragserbringung nicht kennen muss, für diesen nicht entschlüsselbar vor der Übertragung zum Dienstleister verschlüsseln.

Hierbei handelt es sich um eine Verschlüsselung at-rest, bei welcher der Dienstleister keinen Zugang zum Schlüssel erhält. Die Umsetzung kann z.B. auf Dateiebene oder durch Container erfolgen.

## DLS.3 Kontrolle von Dienstleistern

### DLS.3.1 – Einhaltung der Sicherheitsvorgaben

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.11, G 0.29, G 0.20

> Dienstleistersteuerung für Dienstleistungen SOLLTE die Einhaltung der Sicherheitsvorgaben durch den Dienstleister *[regelmäßig]* überprüfen.

Hierzu ist zu prüfen, ob Anzeichen vorliegen, dass der Dienstleister die im Vertrag geforderten Vorgaben nicht einhält und falls erforderlich Gegenmaßnahmen einzuleiten. Die Prüfung kann z.B. Zertifikate, regelmäßige Stichproben oder das Monitoring von Datenleaks vorsehen.

#### DLS.3.1.1 – Audit oder Zertifikat

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.29, G 0.11, G 0.20, G 0.18

> Dienstleistersteuerung für Outsourcing SOLLTE die Einhaltung der Sicherheitsvorgaben anhand eines *[Audits, Zertifikates oder vergleichbaren Sicherheitsnachweises]* *[regelmäßig]* überprüfen.

„Audit“ bezeichnet in diesem Zusammenhang eine systematische, unabhängige Überprüfung der vereinbarten Sicherheitsmaßnahmen durch fachkundige Dritte, beispielsweise in Form interner oder externer Prüfungen mit dokumentierten Ergebnissen. Ein „Zertifikat“ ist ein formaler Nachweis einer akkreditierten Prüfstelle, dass ein Dienstleister ein anerkanntes Sicherheitsframework eingehalten hat, wie etwa IT-Grundschutz oder ISO/IEC 27001. Ein „vergleichbarer Sicherheitsnachweis“ kann auch ein Prüfbericht, ein BSI C5-Testat oder eine Bestätigung unabhängiger Gutachter sein, sofern er inhaltlich nachvollziehbar darlegt, dass definierte Sicherheitsanforderungen wirksam umgesetzt wurden. Ohne Nachweise könnte ein Dienstleister vereinbarte Sicherheitsmaßnahmen vernachlässigen, was zu unbemerkten Datenabflüssen, unzureichendem Patch-Management oder Ausfällen durch mangelhafte Notfallvorsorge führen könnte. Durch nachvollziehbare Prüfungen kann dagegen erreicht werden, dass Sicherheitsstandards eingehalten werden, Schwachstellen frühzeitig sichtbar werden und ein belastbares Vertrauen in die Dienstleisterbeziehung entsteht.

### DLS.3.2 – Checkup

**Stufe:** `erhöht` · **Aufwand:** 4 · **Gefährdungen:** G 0.11, G 0.20

> Dienstleistersteuerung für Outsourcing KANN die risikoorientierte Entscheidung über Outsourcing auf Grundlage der Geschäftsprozessprofile auf Änderungen der Gefährdungslage oder Prozessinhalte *[regelmäßig]* überprüfen.

Die risikoorientierte Entscheidung über Outsourcing kann in diesem Kontext als wiederkehrende Bewertung der Abhängigkeiten und Gefahren verstanden werden, die durch externe Dienstleister in den Geschäftsprozessen einer Institution entstehen. Der Parameter regelmäßig kann je nach Kritikalität der ausgelagerten Prozesse sinnvoll mit Werten wie halbjährlich, jährlich oder nach definierten Ereignissen (z. B. Einführung neuer regulatorischer Vorgaben oder Sicherheitsvorfälle) ausgefüllt werden. Änderungen der Gefährdungslage beziehen sich auf die dynamische Entwicklung von Bedrohungen wie Cyberangriffe, Lieferkettenstörungen oder neue regulatorische Anforderungen, während Änderungen der Prozessinhalte vor allem die Anpassung oder Erweiterung der durch Dienstleister erbrachten Leistungen umfassen. Der Zweck dieser Vorschrift liegt darin, frühzeitig sicherzustellen, dass die bisherigen Risikoeinschätzungen und Dienstleistervereinbarungen weiterhin tragfähig sind und nicht durch externe Veränderungen entwertet werden. Ohne eine solche Überprüfung könnte beispielsweise ein Dienstleister aufgrund verschärfter Bedrohungen unzureichenden Schutz bieten oder durch eine stillschweigende Ausweitung von Leistungen in Bereiche gelangen, die ursprünglich nicht risikobewertet wurden. Eine regelmäßige Kontrolle kann dagegen dafür sorgen, dass Risiken durch Outsourcing transparent bleiben und rechtzeitig nachjustiert werden. Zur praktischen Umsetzung kann eine Institution beispielsweise (1) eine Checkliste führen, die bei jeder Neubewertung konkrete Aspekte wie Datenlokation, technische Sicherheitsmaßnahmen oder Zertifikatsgültigkeiten abfragt und (2) ein automatisiertes Monitoring nutzen, das öffentliche Sicherheitsnachweise wie Testate nach BSI C5 oder SOC-Reports erfasst und in die Bewertung einbindet. Auch die Nutzung von Incident-Datenbanken oder branchenspezifischen Threat-Feeds kann helfen, Gefährdungslagen aktuell einzuschätzen. Ein bewährter Tipp ist es, nicht nur formale Unterlagen zu prüfen, sondern auch technische Stichproben durchzuführen, etwa in Form von Konfigurationsprüfungen oder Penetrationstests, sofern dies durch den Dienstleister gestattet wird. Damit kann die Institution sicherstellen, dass die theoretische Risikoabwägung durch reale Prüfungen gestützt wird und sich an tatsächlichen Veränderungen orientiert.

### DLS.3.3 – Strategie-Check

**Stufe:** `erhöht` · **Aufwand:** 4 · **Gefährdungen:** G 0.11, G 0.20

> Dienstleistersteuerung für Outsourcing KANN die Strategie auf Vollständigkeit und Korrektheit in Bezug auf die betrachteten Geschäftsprozesse bei Änderungen der Geschäftsprozessprofile überprüfen.

Vollständigkeit bedeutet hier, dass die Gesamtheit der ausgelagerten Prozesse erfasst, beschrieben und in ihrer Abhängigkeit zu internen Prozessen berücksichtigt ist. Korrektheit meint, dass die Beschreibungen, Schnittstellen und Verantwortlichkeiten zwischen Institution und Dienstleister sachlich richtig, aktuell und belastbar dokumentiert sind. Zur Umsetzung kann eine Institution strukturierte Verfahren einführen, die bei Änderungen in den Prozessprofilen automatisch eine Prüfung des Outsourcing-Setups auslösen. Dies kann z. B. durch Abgleich der aktuellen Servicebeschreibungen mit Prozesslandkarten erfolgen, sodass fehlende oder doppelt definierte Zuständigkeiten sichtbar werden.

### DLS.3.4 – Anhörung

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.11, G 0.20

> Dienstleistersteuerung für Outsourcing SOLLTE den Dienstleister zu Sicherheitsmaßnahmen für betroffene Zielobjekte anhören.

Betroffen sind alle Zielobjekte, zu denen vom Dienstleister (Teil-)Leistungen erbracht werden. Für eine Anhörung ist es erforderlich, dass der Dienstleister über die geplanten Maßnahmen informiert ist und ausreichend Gelegenheit zur Stellungnahme erhält.

### DLS.3.5 – Blockierung unzuverlässiger Dienstleister

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.11, G 0.19, G 0.20

> Dienstleistersteuerung für Dienstleistungen SOLLTE unzuverlässige Dienstleister oder Subdienstleister blockieren.

Ein Dienstleister gilt als unzuverlässig, wenn zukünftig mit Verstößen gegen die Schutzziele Vertraulichkeit, Verfügbarkeit oder Integrität durch ihn zu rechnen ist (d.h. eine Prognose der Vertrauenswürdigkeit). Dies ist insbesondere dann der Fall, wenn erhebliche Verstöße gegen die Schutzziele bereits durch ihn begangen wurden oder Anzeichen dafür vorliegen, dass bei einer weiteren Verwendung mit solchen Verstößen zu rechnen ist. Beispielsweise kann dies eintreten, wenn die Verwendung des DNS-Servers eines wirtschaftlichen Konkurrenten diesem die schützenswerten Adressen von der Institution besuchter Internetseiten ausliefert oder eine Behörde Software mit Internetzugriff einsetzen möchte, die jedoch von einem Hersteller stammt, dessen Hauptsitz in einem öffentlich für politische Spionage bekannten Staat liegt. Dies kann durch eine Liste blockierter Vertragspartner umgesetzt werden. Eine Umsetzung für Subdienstleister kann z.B. durch die Benennung autorisierter Subdienstleister, oder die Weitergabe von Kriterien für Subdienstleister an den Dienstleister erfolgen.

### DLS.3.6 – Portabilität

**Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.11, G 0.20

> Dienstleistersteuerung für Outsourcing KANN die Portabilität des ausgelagerten Prozesses *[regelmäßig]* überprüfen.

Hierunter ist zu verstehen, dass regelmäßig ein Test durchgeführt wird, bei dem die Funktionsfähigkeit des ausgelagerten (Teil-) Prozesses in einer Umgebung, die nicht bei diesem Dienstleister liegt, überprüft wird. Ziel ist es sicherzustellen, dass der Prozess bei einem Ausfall des Dienstleisters an anderer Stelle zeitnah gestartet werden kann.

## DLS.4 Dekommissionierung von Dienstleistern

### DLS.4.1 – Dekomissionierung

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.18

> Dienstleistersteuerung für Dienstleistungen SOLLTE eine Vorgehensweise zur Dekommissionierung vor Vertragsende verankern.

Der Begriff Dekommissionierung bezeichnet hier das strukturierte und nachweisbare Vorgehen, wie eine Institution die Nutzung eines Dienstes oder die Zusammenarbeit mit einem Dienstleister kontrolliert beendet, ohne dass Informationssicherheit, Verfügbarkeit oder Nachvollziehbarkeit beeinträchtigt werden. Der Sinn dieser Vorgabe liegt darin, Risiken wie den unkontrollierten Verbleib sensibler Daten bei einem Dienstleister oder unerkannte Abhängigkeiten von dessen Infrastruktur zu vermeiden. Ohne ein definiertes Vorgehen könnte etwa ein Anbieter weiterhin Zugriff auf produktive Systeme behalten oder Kopien vertraulicher Daten in seiner Umgebung zurückhalten, was ein erhebliches Risiko darstellen könnte. Die praktische Umsetzung kann in mehreren abgestuften Maßnahmen bestehen: (1) Ein geplanter Abschalttermin kann genutzt werden, um Systeme, Schnittstellen und Berechtigungen kontrolliert zurückzubauen und anschließend durch ein Freigabeprotokoll zu bestätigen. (2) Ein Prozessleitfaden kann die frühzeitige Identifikation von zu dekommissionierenden Schnittstellen, Zugangsdaten und Subdienstleistern vorsehen, damit deren Abschaltung rechtzeitig koordiniert werden kann. (3) Eine Checkliste kann sicherstellen, dass auch weniger offensichtliche Abhängigkeiten – etwa hinterlegte API-Tokens, Support-Zugänge oder im Monitoring integrierte Endpunkte – im Abschlussprozess berücksichtigt werden. (4) Technisch kann die Nutzung von zentral verwalteten Zugriffskonten und Logging-Systemen die Überprüfung erleichtern, ob ein Dienstleister nach der Deaktivierung tatsächlich keinen Zugriff mehr hat. Auf diese Weise kann die Institution die Dienstleistersteuerung auch vorzeitig geordnet beenden, ohne dass Informationssicherheitsrisiken unkontrolliert fortbestehen.

#### DLS.4.1.1 – Unabhängigkeit

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18

> Dienstleistersteuerung für Outsourcing SOLLTE die Unabhängigkeit der Verarbeitung schützenswerter Informationen vor der Außerbetriebnahme testen.

„Unabhängigkeit der Verarbeitung“ meint hier die Fähigkeit, dass die Nutzung von Informationen in Geschäftsprozessen der Institution nicht von den Systemen, Verfahren oder Interessen des externen Dienstleisters abhängig ist, sodass ihre Integrität, Verfügbarkeit und Vertraulichkeit auch nach einer Außerbetriebnahme des Outsourcings gewährleistet bleibt. Die Vorschrift dient dem Zweck, die Risiken zu minimieren, die entstehen können, wenn ein Dienstleister seine Leistung einstellt, Verträge beendet werden oder ein abruptes Ende der Zusammenarbeit erfolgt. Ohne Vorkehrungen könnte dies dazu führen, dass kritische Daten unzugänglich bleiben, unkontrolliert gelöscht werden oder in Abhängigkeit von proprietären Formaten verloren gehen. Zur Umsetzung kann die Institution verschiedene Maßnahmen prüfen: (1) Ein systematischer Test, ob Daten in standardisierten, portablen Formaten exportierbar sind und in eigenen oder alternativen Systemen fehlerfrei weiterverarbeitet werden können. (2) Ein Probelauf, bei dem die Verbindung zum Dienstleister gezielt getrennt wird, um zu überprüfen, ob die Institution ihre Geschäftsprozesse auch ohne aktive Anbindung fortführen kann. (3) Ein kontrolliertes Abschalten einzelner vom Dienstleister erbrachter Dienste, um zu verifizieren, ob vorbereitete Ersatzprozesse oder interne Systeme die Funktion übernehmen. (4) Eine Teststellung für die Rückgabe von Datenbeständen am Ende der Vertragslaufzeit, bei der die Vollständigkeit, Konsistenz und Nutzbarkeit der gelieferten Daten geprüft wird. Mit solchen Maßnahmen kann die Institution sicherstellen, dass die Verarbeitung schützenswerter Informationen eigenständig aufrechterhalten werden kann.

#### DLS.4.1.2 – Berechtigungen deaktivieren

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.18, G 0.29

> Dienstleistersteuerung für Dienstleistungen SOLLTE für den Vertrag benötigte Berechtigungen bei Vertragsende unverzüglich deaktivieren.

Berechtigungen sind hier alle Zugangs-, Zutritts- und Zugriffsrechte, die von der Institution für Mitarbeitende, Organisationseinheiten oder Subunternehmer des Dienstleisters eingerichtet oder geändert wurden. Hierzu können diese Rechte gelöscht, deaktiviert oder reduziert werden, soweit sie nicht mehr (z.B. für andere Verträge) benötigt werden.
