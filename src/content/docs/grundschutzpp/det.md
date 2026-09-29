---
title: "DET – Detektion"
description: "Die Praktik Detektion sorgt dafür, dass sicherheitsrelevante Ereignisse rechtzeitig erkannt werden."
---

Die Praktik Detektion sorgt dafür, dass sicherheitsrelevante Ereignisse rechtzeitig erkannt werden. Zu diesem Zweck werden geeignete organisatorische, personelle und technische Maßnahmen im Vorfeld geplant, implementiert und regelmäßig geübt. Damit die Detektion erfolgreich ist, muss umfassend protokolliert werden. Das Zusammenspiel zwischen den Praktiken Protokollierung und Detektion ist für die erfolgreiche Erkennung sicherheitsrelevanter Ereignisse unerlässlich. Die Praktik Detektion regelt jedoch nicht den Umgang mit sicherheitsrelevanten Ereignissen nach deren Erkennung. Dies ist Aufgabe der Praktik Sicherheitsvorfallsbehandlung.

## DET.1 Grundlagen

### DET.1.1 – Verfahren und Regelungen

**Pflicht:** MUSS · **Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.29

**Vorgänger:** [DER.1.A1-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [DER.1.A1-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [IND.1.A10-UA.6](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion MUSS Verfahren und Regelungen zur Detektion von Sicherheitsvorfällen verankern.

Durch die steigende Menge und Komplexität von Datenverarbeitungen sind Sicherheitsvorfälle auch bei bester Prävention zu erwarten. Ein Verfahren zur Detektion stellt sicher, dass Sicherheitsvorfälle zeitnah entdeckt werden können. Hierzu gehört, wie aktiv und passiv Sicherheitsvorfälle erkannt werden, sowie wer bei der Erkennung dabei wofür zuständig ist. Die Umsetzung kann in einem eigenen Prozess, oder integriert in andere Prozesse und Aufgaben erfolgen. Die bei der Festlegung des Verfahrens im Einzelnen zu berücksichtigenden Inhalte ergeben sich aus den Anforderungen dieser Praktik.

#### DET.1.1.1 – Dokumentation

**Pflicht:** MUSS · **Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.37

> Detektion MUSS die Verfahren und Regelungen dokumentieren.

Ohne eine Dokumentation könnte die Einhaltung der Verfahren und Regelungen von der Tagesform oder dem individuellen Wissen einzelner Mitarbeiter abhängen, was zu inkonsistenten Entscheidungen und Fehlern führen könnte; insbesondere beim Ausscheiden eines langjährigen Administrators könnte wertvolles prozessuales Wissen verloren gehen. Eine klare Dokumentation sichert die Verbindlichkeit und Wiederholbarkeit und dient als unverzichtbare Grundlage für die Einarbeitung neuer Kollegen, für die Durchführung von Audits und zur einheitlichen Anwendung der Regeln in der gesamten Institution. Die Dokumentation kann in einem eigenständigen Dokument als Richtlinie erfolgen, aber auch als Abschnitt in einem bereits bestehenden Dokument oder über die digital strukturiere Erfassung von Maßnahmen zur Umsetzung der Anforderungen, etwa über eine Software zum Management der Informationssicherheit. Sinnvoll ist es Ort und Struktur der Dokumentation an der jeweiligen Zielgruppe, d.h. den für das Management und die Umsetzung verantwortlichen Personen oder Rollen, auszurichten.

#### DET.1.1.2 – Zuweisung der Aufgaben

**Pflicht:** MUSS · **Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18

> Detektion MUSS die mit den Verfahren und Regelungen verbundenen Aufgaben *[zuständigen Personen oder Rollen]* zuweisen.

Die Zuweisung von Aufgaben bezeichnet die eindeutige und verbindliche Übertragung von konkreten Tätigkeiten und Verantwortlichkeiten des Änderungsprozesses, wie etwa die Risikobewertung, die technische Umsetzung oder die finale Freigabe, an definierte Stellen in der Institution. Der Sinn dieser Vorschrift ist es, die Verantwortlichkeit ("Accountability") für jeden einzelnen Schritt im Prozess klarzustellen. Ohne eine solche Zuweisung könnten kritische Prüfungen unterbleiben, weil sich niemand explizit zuständig fühlt, was wiederum die Wahrscheinlichkeit fehlgeschlagener Änderungen erhöht. Eine klare Regelung kann sicherstellen, dass keine Aufgaben übersehen werden und jede Tätigkeit von einer dafür qualifizierten und befugten Stelle ausgeführt wird, was die Prozesssicherheit signifikant erhöht. Eine bewährte Methode zur Umsetzung ist die Erstellung einer RACI-Matrix (Responsible, Accountable, Consulted, Informed), die tabellarisch für jeden Prozessschritt darstellt, wer für die Durchführung verantwortlich ist, wer die Gesamtverantwortung trägt, wer zu konsultieren und wer zu informieren ist. Diese Zuständigkeiten können auch direkt in einem Workflow- oder Ticketsystem abgebildet werden, sodass Aufgaben, wie beispielsweise Genehmigungsschritte, automatisch an die richtige Gruppe oder Person weitergeleitet werden. Sinnvoll ist es, die Zuweisung anhand von Rollen (z. B. "Anwendungsverantwortlicher", "Netzwerkadministrator", "Change Manager") vorzunehmen, statt an konkrete Personen. Dieser Ansatz stellt sicher, dass die Prozesse auch bei Personalwechseln stabil weiterlaufen, da die Zuständigkeit an die Funktion und nicht an das Individuum gebunden ist.

#### DET.1.1.3 – Bekanntgabe

**Pflicht:** MUSS · **Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.31

**Vorgänger:** [DER.1.A1-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.4.3.A1-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_4_3_Eingebettete_Systeme_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion MUSS die zuständigen Personen oder Rollen über die Verfahren und Regelungen informieren.

Wenn die Zuständigen die etablierten Verfahren nicht kennen, besteht die Gefahr, dass diese – sei es aus Unwissenheit oder Bequemlichkeit – umgangen werden, was die Schutzwirkung des gesamten Managementsystems untergräbt. So könnte ein neuer Systemadministrator eine weitreichende Konfigurationsänderung vornehmen, ohne den vorgeschriebenen Genehmigungsprozess zu durchlaufen, was zu einem unbemerkten Sicherheitsrisiko führen könnte. Eine gezielte Information kann hingegen die Akzeptanz der Regelungen fördern und sicherstellen, dass alle Beteiligten ihre Rolle im Prozess verstehen und die Abläufe korrekt anwenden. Zur Umsetzung ist es sinnvoll die Dokumentation im Rahmen eines Onboarding-Prozesses bekanntzugeben und bei allen Änderungen eine automtatische Benachrichtigung aller zuständigen Personen oder Rollen anzustoßen.

### DET.1.2 – Regelmäßige Überprüfung

**Pflicht:** MUSS · **Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.27, G 0.29

**Vorgänger:** [DER.1.A1-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to)

> Detektion MUSS die Verfahren und Regelungen *[regelmäßig]* und anlassbezogen auf Aktualität überprüfen.

Eine geplante Überprüfung der etablierten Verfahren und Regelungen dient dazu festzustellen, ob diese noch wirksam, effizient und an die aktuellen Gegebenheiten angepasst sind. Eine anlassbezogene Überprüfung wird durch spezifische Ereignisse ausgelöst, wie etwa einen schwerwiegenden Sicherheitsvorfall, eine strategische Neuausrichtung der IT oder neue gesetzliche Anforderungen. Der Zweck dieser Anforderung ist es, die kontinuierliche Verbesserung und Anpassungsfähigkeit des Prozesses sicherzustellen, da veraltete Regelungen neuen technologischen Entwicklungen oder Bedrohungen nicht mehr gerecht werden könnten; ein vor Jahren für monolithische Anwendungen konzipierter Prozess ist beispielsweise für agile Entwicklungsmethoden oder Microservice-Architekturen ungeeignet. Die regelmäßige Überprüfung kann die Effektivität des Sicherheitsmanagements langfristig aufrechterhalten und die Resilienz der Institution stärken.

## DET.2 Meldung von Ereignissen

### DET.2.1 – Meldeverfahren

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.18, G 0.29, G 0.20, G 0.47

**Vorgänger:** [DER.1.A3-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [DER.2.1.A9-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [DER.2.1.A9-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [IND.1.A10-UA.6](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion SOLLTE ein Meldeverfahren verankern.

Ein Meldeverfahren bezeichnet in diesem Kontext einen nachvollziehbaren und definierten Ablauf zur Erfassung, Weiterleitung und Bearbeitung erkannter sicherheitsrelevanter Ereignisse oder Auffälligkeiten („Incident Reporting“ oder „Security Event Reporting“). Dazu gehört, welche Ereignisse als meldepflichtig gelten, über welche Kommunikationswege Meldungen erfolgen können, welche Stellen dabei informiert werden und innerhalb welcher Zeiträume eine Bearbeitung stattfindet. Die Anforderung zielt darauf ab, dass erkannte Sicherheitsereignisse nicht unbeachtet bleiben oder nur informell kommuniziert werden. Ohne ein geregeltes Vorgehen könnte ein Vorfall verspätet bearbeitet werden, wichtige Informationen könnten verloren gehen oder Warnhinweise könnten nicht die zuständigen Stellen erreichen. Ein etabliertes Meldeverfahren kann hingegen eine schnelle Reaktion, eine konsistente Bewertung von Ereignissen und eine koordinierte Behandlung erkannter Auffälligkeiten unterstützen. Die konkrete Ausgestaltung kann sich dabei an Größe, Struktur und Schutzbedarf der Institution orientieren. Geeignet sind etwa zentrale Meldestellen, Ticketsysteme, standardisierte Meldeformulare und abgestufte Eskalationsprozesse.

#### DET.2.1.1 – Sofortmaßnahmen Nutzender

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.39, G 0.41, G 0.47, G 0.25

**Vorgänger:** [IND.1.A10-UA.6](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion SOLLTE Regelungen für Sofortmaßnahmen durch Nutzende verankern.

Beispiele für Sofortmaßnahmen sind der sofortige Stopp weiterer Tätigkeiten an betroffenen Systemen, die Dokumentation von Beobachtungen oder zu meldende Informationen (W-Fragen). Hierfür kann die IT-Notfallkarte „Verhalten bei IT-Notfällen“ des BSI genutzt werden.

#### DET.2.1.2 – Meldeformulare

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.39, G 0.41, G 0.47

**Vorgänger:** [APP.3.2.A20-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [DER.2.1.A20-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion SOLLTE Meldeformulare für Vorfallsmeldungen installieren.

Die Angabe des Meldezeitpunktes oder der Name des Meldenden, kann auch durch ein Formular automatisch ausgefüllt werden.

#### DET.2.1.3 – Rückmeldungen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.29, G 0.18, G 0.33, G 0.47

**Vorgänger:** [DER.2.1.A9-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion SOLLTE ein Verfahren für Rückmeldungen verankern.

Rückmeldungen an Personen, die potenzielle Vorfälle gemeldet haben, sind hilfreich, da sie zum besseren Verständnis beitragen, worauf bei künftigen Meldungen zu achten ist und wie die Meldenden zur Bearbeitung des Vorfalls beitragen können. Ohne Rückmeldung könnte Unsicherheit entstehen, ob ein Vorfall überhaupt aufgenommen oder ernst genommen wurde, was zu Frustration oder einer sinkenden Bereitschaft zur Meldung künftiger Ereignisse führen könnte. Eine zeitnahe und angemessene Rückmeldung kann dagegen die Nutzenden in ihrem sicherheitsbewussten Verhalten bestärken, die Relevanz ihrer Meldung verdeutlichen und Missverständnisse vermeiden. So kann beispielsweise eine Rückmeldung nach einem gemeldeten Phishing-Versuch klarstellen, ob es sich um einen bekannten Angriff handelte oder ob zusätzliche Maßnahmen wie das Zurücksetzen eines Passworts empfohlen werden. Ebenso kann eine Rückmeldung nach einem gemeldeten Systemausfall erläutern, ob dieser sicherheitsrelevant war oder eine rein technische Störung vorlag. Ein Rückmeldeverfahren kann in diesem Kontext als ein strukturierter Ablauf definiert werden, über den die meldende Person nach Eingang ihrer Meldung eine Information über den Status, die Relevanz und – falls sinnvoll – empfohlene Folgeschritte erhält. Ein automatisiertes Ticketsystem kann beispielsweise sofortige Eingangsbestätigungen generieren und Statusänderungen kommunizieren. Ebenso kann eine abgestufte Rückmeldepflicht sinnvoll sein, bei der kritische Vorfälle eine priorisierte persönliche Rückmeldung durch Fachpersonal erhalten, während unkritische Meldungen standardisierte Mitteilungen bekommen. Technische Hilfsmittel wie Mail-Vorlagen, interne Chatbots oder Self-Service-Portale können die Effizienz erhöhen

### DET.2.2 – Security Operations Center

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 4 · **Gefährdungen:** G 0.29, G 0.18, G 0.33, G 0.20

**Vorgänger:** [DER.2.1.A20-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [DER.2.1.A20-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [DER.2.1.A21-UA.6](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [DER.2.1.A21-UA.8](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [DER.2.1.A21-UA.9](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion KANN die Erkennung, Beurteilung und initiale Behandlung von Vorfällen *[dediziertem Personal]* zuweisen.

Ein Security Operations Center (SOC) ist eine organisatorische Einheit, deren dedizierte Aufgabe die Überwachung von sicherheitskritischen Ereignissen, sowie die Reaktion auf Sicherheitsvorfälle ist. Für die Definition eines sicherheitskritischen Ereignisses, siehe Glossar (Namensräume des Grundschutz++). Aufgrund der Komplexität und besonderen Bedeutung der Aufgabe leisten Spezialisten für Detektion und Reaktion auf Sicherheitsvorfälle einen wichtigen Beitrag zur effektiven Informationssicherheit einer Institution. Werden diese Aufgaben von speziell hierfür geschultem Personal übernommen und nicht „nebenbei“ von Betriebspersonal, so werden Zielkonflikte zwischen Informationssicherheit und reibungslosem Betrieb vermieden und die Qualität der Sicherheitsbeurteilungen steigt. Kann durch ein selbst betriebenes SOC oder einen Dienstleister realisiert werden.

### DET.2.3 – Ständiger Bereitschaftsdienst

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.27, G 0.23, G 0.41, G 0.47

**Vorgänger:** [DER.1.A6-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [DER.2.1.A20-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion KANN einen ständigen Bereitschaftsdienst verankern.

Dies erfordert, dass 24/7 eine Person bereitgehalten wird, welche bei sicherheitsrelevanter Alarmierung umgehend die Behebung des Vorfalls aufnimmt. Welche Ereignisse kritisch sind, ist dabei von der Kritikalität der betroffenen Systeme oder Anwendungen abhängig. Für die Definition eines sicherheitskritischen Ereignisses, siehe Glossar (Namensräume des Grundschutz++).

## DET.3 Protokollierung

### DET.3.1 – Protokollierung sicherheitsrelevanter Ereignisse

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.37, G 0.32, G 0.29

**Vorgänger:** [DER.1.A5-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [IND.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [IND.1.A10-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [IND.1.A10-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [INF.13.A21-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [INF.13.A21-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equal-to) · [NET.1.2.A26-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [NET.1.2.A7-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [NET.3.4.A16-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_4_Network_Access_Control_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.5.A3-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.4.4.A18-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_4_4_Allgemeines_IoT_Geraet_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion für Anwendungen SOLLTE Sicherheitsrelevante Ereignisse mindestens für *[eine bestimmte Frist]* protokollieren.

Für die Definition eines Sicherheitsrelevanten Ereignisses, siehe Glossar (Namensräume des Grundschutz++). Relevant sind hierbei insbesondere die Protokollierung auf zentralen Diensten und Servern. Dazu gehören auch vorhandene Cloud-Anwendungen oder -Dienste. Hier besteht ein enger Bezug zur Praktik Änderungen und Tests.

#### DET.3.1.1 – Authentifizierungen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.37, G 0.27, G 0.23

**Vorgänger:** [APP.3.2.A4-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [NET.1.2.A7-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für IT-Systeme SOLLTE Authentifizierungen bei Erfolg und Fehlschlag protokollieren.

Relevant sind dabei z.B. die lokale Anmeldung, Anmeldung und Zugriffe auf Schnittstellen des Systems über das Netz, oder auch die physische Authentifizierung an einem Zutrittskontrollsystem.

#### DET.3.1.2 – Ausgeführte Kommandozeilenbefehle

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.31, G 0.32, G 0.30

**Vorgänger:** [SYS.1.2.3.A7-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_2_3_Windows_Server_Edition_2023.pdf?__blob=publicationFile&v=5#download=1) (subset-of) · [SYS.2.2.3.A22-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_2_3_Clients_unter_Windows_Edition_2023.pdf?__blob=publicationFile&v=5#download=1) (subset-of) · [SYS.2.3.A1-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_3_Clients_unter_Linux_und_Unix_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion für IT-Systeme SOLLTE ausgeführte Kommandozeilenbefehle protokollieren.

Angreifer nutzen Kommandozeilenfunktionen wie Bash oder Windows PowerShell, um mit Bordmitteln schädliche Befehle auszuführen. Hier sind vor allem Living-off-the-Land-Binaries (LOLBins) und Nutzlasten (Malware Payloads) zu nennen.

#### DET.3.1.3 – Anbindung von Peripheriegeräten

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.37, G 0.18, G 0.23

**Vorgänger:** [IND.1.A10-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [OPS.1.1.5.A3-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [OPS.1.1.5.A6-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.1.9.A13-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_9_Terminalserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion für IT-Systeme SOLLTE das Anschließen von Peripheriegeräten protokollieren.

Das Protokollieren der Anbindung von Peripheriegeräten kann helfen, Manipulationsversuche an IT-Systemen frühzeitig zu erkennen und nachzuvollziehen. Ohne ein solches Protokoll könnte beispielsweise ein unbefugtes Speichermedium angeschlossen und vertrauliche Daten unbemerkt entwendet werden, oder es könnte Schadsoftware über ein USB-Gerät eingeschleust werden. Auch manipulierte Eingabegeräte könnten genutzt werden, um Tastatureingaben auszulesen oder unbemerkt Befehle einzuschleusen. Unter Peripheriegeräten sind in diesem Kontext externe Komponenten (aus Hardware oder virtuell) zu verstehen, die ein IT-System erweitern oder mit diesem verbunden werden – etwa USB-Sticks, externe Festplatten, Smartphones im Lade- oder Datenmodus, Drucker oder auch spezialisierte Geräte wie Diagnose- oder Messinstrumente. Zur praktischen Umsetzung kann eine Institution beispielsweise auf Betriebssystemfunktionen zurückgreifen, die Geräteanschlüsse im System-Log erfassen, oder ergänzende Endpoint-Management-Lösungen einsetzen, die eine zentralisierte Protokollierung erlauben.

#### DET.3.1.4 – Systemfehler

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.37, G 0.23, G 0.26, G 0.18

**Vorgänger:** [APP.3.2.A4-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [APP.3.3.A14-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_3_Fileserver_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [NET.1.2.A26-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [NET.3.1.A7-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_1_Router_und_Switches_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [OPS.1.1.7.A15-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_7_Systemmanagement_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (superset-of) · [SYS.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für IT-Systeme SOLLTE Fehlermeldungen des Systems protokollieren.

Die Protokollierung von Fehlermeldungen kann eine wesentliche Grundlage für die Früherkennung von Sicherheits- und Stabilitätsproblemen in IT-Systemen bilden. Ohne ein systematisches Logging könnte ein kritischer Hardwaredefekt, eine beschädigte Systemdatei oder ein fehlgeschlagener Sicherheits-Update-Prozess unentdeckt bleiben und dadurch die Integrität oder Verfügbarkeit von IT-Systemen gefährden. Ebenso könnte ein Angreifer, der wiederholt unautorisierte Befehle ausführt oder Dienste fehlerhaft anspricht, unbemerkt bleiben, wenn die resultierenden Fehlermeldungen nicht nachvollzogen werden. Auf technischer Ebene kann es zweckmäßig sein, das native Logging des Betriebssysteme zu aktivieren und so zu konfigurieren, dass Fehlermeldungen konsistent erfasst werden – beispielsweise über Syslog-Dienste oder Windows-Event-Logs. Eine zentrale Log-Sammlung kann helfen, auch bei verteilten Systemen eine einheitliche Auswertung vorzunehmen.

#### DET.3.1.5 – Störungen der Netzerreichbarkeit

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 3 · **Gefährdungen:** G 0.37, G 0.23, G 0.29

**Vorgänger:** [NET.1.2.A26-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [NET.1.2.A7-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [NET.3.1.A7-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_1_Router_und_Switches_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [OPS.1.1.5.A3-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [SYS.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für IT-Systeme KANN Störungen der Netzerreichbarkeit protokollieren.

Eine Störung der Netzerreichbarkeit kann ein Indiz für Überlastungen, Fehler oder Angriffe im Netz sein. Wann eine Störung vorliegt, kann anhand von Schwellwerten, z.B. durch das Ausbleiben eines regelmäßigen Heartbeat-Paketes, getestet werden.

#### DET.3.1.6 – Systemspezifische Ereignisse

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.37, G 0.23, G 0.29

**Vorgänger:** [DER.1.A15-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [OPS.1.1.5.A11-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [SYS.1.9.A13-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_9_Terminalserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion für IT-Systeme KANN *[bestimmte systemspezifische Ereignisse]* protokollieren.

Bestimmte systemspezifische Ereignisse meint hier, dass von der Instiution konkret festgehalten wurde, welche für das System relevanten Ereignisse im Einzelnen protokolliert werden. Beispiele sind Aktionen mit spezifisch konfigurierten privilegierten Berechtigungen, Prozessaktivitäten des Betriebssystems, wie das Starten eines Systemprozesses, Dateierzeugung oder das Laden eines Treibers, die Modifikation von Systemkonfigurationsdateien oder die Installation oder Deinstallation von Systemdiensten und Anwendungen, sowie das Herunterfahren oder Neustarten des Systems. Die Festlegung, welche dieser oder weiterer systemspezifischer Ereignisse protokolliert werden, obliegt der Institution und hängt von der jeweiligen Systemumgebung und dem Schutzbedarf ab.

#### DET.3.1.7 – Was, Wann, Wo

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 5 · **Gefährdungen:** G 0.37, G 0.18

**Vorgänger:** [INF.13.A21-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [NET.3.2.A9-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_2_Firewall_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [OPS.1.1.5.A1-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für Anwendungen SOLLTE zu jedem sicherheitsrelevanten Ereignis mindestens Zeitpunkt, die Quelle und das Zielobjekt protokollieren.

Für die Definition eines Sicherheitsrelevanten Ereignisses, siehe Glossar (Namensräume des Grundschutz++). Damit einem Ereignis zuverlässig ein bestimmter Zeitpunkt zugewiesen werden kann, ist eine einheitliche Zeitquelle für die Systemuhr (meist über NTP oder PTP) als Voraussetzung erforderlich. Bei der Protokollierung der Herkunft oder Quelle (z.B. Gerätenamen, IP-Adresse) besteht ein enger Zusammenhang zu Compliance-Anforderungen, etwa zum Datenschutz.

#### DET.3.1.8 – Privilegierte Ereignisse

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.37, G 0.23, G 0.29

**Vorgänger:** [IND.1.A15-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [SYS.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.1.9.A13-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_9_Terminalserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [SYS.2.5.A16-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_5_Client_Virtualisierung_Edition_2023.pdf?__blob=publicationFile&v=2#download=1) (intersects-with) · [SYS.4.3.A3-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_4_3_Eingebettete_Systeme_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion für Anwendungen SOLLTE privilegierte Ereignisse einschließlich der Aktivierung, Deaktivierung oder Blockierung privilegierter Funktionen protokollieren.

Privilegierte Ereignisse sind Vorgänge, bei denen besonders weitreichende Rechte genutzt werden – beispielsweise die Vergabe oder Entziehung von Administratorrechten, das Deaktivieren von Virenscannern oder Änderungen an Firewallregeln. Gerade solche Eingriffe könnten einen erheblichen Einfluss auf die Verfügbarkeit und Integrität von Daten haben. Ohne eine gezielte Aufzeichnung könnten sicherheitsrelevante Änderungen unentdeckt bleiben – etwa, wenn ein Angreifer unbefugt einen privilegierten Account übernimmt und Spuren verwischt, oder wenn ein interner Benutzer kritische Funktionen deaktiviert, wodurch Schutzmaßnahmen umgangen werden.

#### DET.3.1.9 – Fehler der Anwendung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.37, G 0.23, G 0.32

**Vorgänger:** [APP.3.2.A4-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [CON.10.A13-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/03_CON_Konzepte_und_Vorgehensweisen/CON_10_Entwicklung_von_Webanwendungen_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [DER.1.A5-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [NET.1.2.A7-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion für Anwendungen SOLLTE Fehlermeldungen der Anwendung protokollieren.

Fehlermeldungen können wichtige Hinweise auf technisches Versagen oder menschliches Fehlverhalten liefern. Insbesondere, wenn Fehlermeldungen neuartig sind, oder gehäuft auftreten, können sie Indiz für Probleme sein, die behandlungsbedürftig sind. Denken Sie insbesondere auch an Fehlermeldungen in automatisierten Prozessen, da diese möglicherweise sonst nicht zur Kenntnisnahme gelangen.

#### DET.3.1.10 – Nutzungsstatistik

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 4 · **Gefährdungen:** G 0.37, G 0.23, G 0.29, G 0.27

**Vorgänger:** [APP.3.2.A4-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [APP.3.6.A15-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_6_DNS_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [DER.1.A13-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.5.A11-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für Anwendungen KANN eine Nutzungsstatistik protokollieren.

Bei der statistischen Protokollierung werden z.B. Anzahl oder Durchschnittswerte gespeichert, nicht jedoch die genaue Herkunft oder der Zeitstempel bestimmter Ereignisse. Nutzungsstatistiken wahren die Privatsphäre der einzelnen Nutzenden, ermöglichen jedoch eine Erkennung von Fehlern oder Anomalien in der Nutzung. Beispiele sind die Anzahl von Anfragen für eine bestimmte Ressource (etwa Webserver-URL oder DNS-Name), Anzahl der Anfragen einer bestimmten Anfrageart, Geräte- oder Anwendungskategorien (etwa pro Browseragent oder Betriebssystemversion), Anzahl bestimmter Antworttypen (z.B. Webserver-Fehlercodes), sowie Zugriffsversuche. Hierdurch können Betriebsprobleme wie Caching Fehler oder DoS-Angriffe erkannt werden.

#### DET.3.1.11 – Anwendungsspezifische Ereignisse

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 4 · **Gefährdungen:** G 0.37, G 0.23, G 0.32, G 0.46

**Vorgänger:** [OPS.1.1.2.A18-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_2_Ordnungsgemaesse_IT_Administration_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.5.A1-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [OPS.1.1.5.A11-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für Anwendungen KANN *[bestimmte anwendungsspezifische Ereignisse]* protokollieren.

Die Festlegung, welche spezifischen Ereignisse protokolliert werden, obliegt der Institution und hängt von der jeweiligen Systemumgebung und dem Schutzbedarf ab. Beispiele sind Änderungen an Zugangskonten im Verzeichnisdienst, Telekommunikationsverbindungen, ein Verstoß gegen eine konfigurierte Policy, unautorisierter Zugriff, API-Aufrufe zwischen verschiedenen Anwendungskomponenten, Transaktionen in einem Finanzsystem oder einer E-Commerce-Anwendung, Konfigurationsänderungen oder ein Absturz der Anwendung. Die Protokollierung dieser Ereignisse kann helfen, die Behandlung durch das Betriebspersonal anzustoßen oder Indizien für Ermittler zu sichern.

#### DET.3.1.12 – Datenverarbeitungen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.37

**Vorgänger:** [APP.3.2.A4-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [IND.1.A10-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [INF.13.A21-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [NET.4.1.A5-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_4_1_TK_Anlagen_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (superset-of) · [OPS.1.1.5.A11-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für Daten KANN die Verarbeitung von Daten protokollieren.

Bei Daten mit hohem Schutzbedarf kann es sinnvoll sein, bestimmte Verarbeitungen (z.B. Zugriffe, Veränderungen, Löschung, Datenexporte) zu protokollieren. Änderungen können mit Versionsverwaltungssystemen automatisch protokolliert werden. Beispiele sind Zugriffe auf Dateifreigaben, Webportale oder Datenbank-Abfragen durch eine Anwendung, der Export von Verbindungsdaten auf dem TK-Server, oder der Versand von Nachrichten mit bestimmten Schlüsselnwörtern.

### DET.3.2 – Integration von Cloud-Diensten

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.14, G 0.23, G 0.18

**Vorgänger:** [APP.1.4.A8-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_1_4_Mobile_Anwendungen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [APP.5.4.A4-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_5_4_Unified_Communications_und_Collaboration_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [DER.2.2.A9-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_2_Vorsorge_fuer_die_IT_Forensik_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [OPS.1.1.5.A9-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für Cloud-Dienste KANN Ereignisse in der Cloud im Audit Log der Institution protokollieren.

Daten in Cloud-Diensten könnten von Angreifern über das Internet angegriffen werden, ohne dass Ereignisse im internen Netz hierauf Rückschlüsse geben. Dies könnte zum Beispiel durch Phishing geschehen, wodurch ein OAuth Token für den Cloud-Zugang missbraucht wird. Die Integration der Logs des Cloud-Dienstleisters in die institutionseigene Protokollierung kann hier helfen, z.B. bei Authentifizierung oder Berechtigungsänderungen, sowie bei Zugriff oder Veränderung von Daten. Insbesondere die Integration des Loggings mit einer bedingten Zugriffsrichtlinie kann hier helfen, z.B. indem Zugriffe von ungewöhnlichen IP-Adressen oder Browser Agents auf Angriffe hinweisen können. Die Integration von Cloud-Protokollen in ein internes Logging birgt oft erhebliche Herausforderungen, darunter die Bewältigung des enormen Volumens und der Vielfalt an Datenformaten, was durch selektive Protokollierung, Datennormalisierung und -anreicherung angegangen werden kann. Die Absicherung der Datenpipeline gegen Man-in-the-Middle-Angriffe kann durch die Einhaltung der technischen Anforderungen an die beteiligten IT-Systeme und Anwendungen bewältigt werden, z.B. Verschlüsselung und Authentifizierung. Da Cloud-Anbieter oftzusätzliche Gebühren für den Datentransfer (Egress-Kosten) verlangen bietet es sich an, die Protokolle vor der Übertragung zu filtern, um die Kosten für die Verbesserung der Sicherheit gering zu halten.

### DET.3.3 – Filterung nicht benötigter Inhalte

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.37, G 0.26, G 0.18, G 0.46

**Vorgänger:** [APP.3.3.A14-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_3_Fileserver_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [OPS.1.2.2.A8-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_2_2_Archivierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion KANN die Protokollierung nicht benötigter Inhalte anhand von *[Kriterien]* einschränken.

Je nach Anwendung und Konfigurationeinstellungen könnten Protokolle auch Daten enthalten, die dort nicht benötigt werden, z.B. um die Vertraulichkeit der Daten zu wahren oder aufgrund von Compliance-Anforderungen. Dem kommt eine noch höhere Bedeutung zu, wenn die Protokolle zwischen Institutionen ausgetauscht, oder bei Cloud-Dienstleistern gespeichert oder analysiert werden. Maßnahmen können z.B. Anonymisierung von IP-Adressen oder anderen personenbezogenen Daten oder Geschäftsgeheimnissen, sowie enge Löschfristen sein. Für Verkehrsdaten kann der BfDI Leitfaden Speicherung Verkehrsdaten als Grundlage genutzt werden. Soweit möglich, ist es sinnvoll, die Filterung minimalinvasiv zu gestalten, d.h. nur diejenigen Daten auszufiltern, deren Speicherung nicht rechtlich oder tatsächlich möglich ist, die restlichen Angaben zum Ergebnis jedoch zu protokollieren.

### DET.3.4 – Speicherkapazität

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.37, G 0.32, G 0.46

**Vorgänger:** [IND.1.A15-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [NET.1.2.A35-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [OPS.1.1.2.A28-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_2_Ordnungsgemaesse_IT_Administration_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.5.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.5.A5-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [OPS.1.1.5.A9-UA.6](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [SYS.4.5.A11-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_4_5_Wechseldatentraeger_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [SYS.4.5.A11-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_4_5_Wechseldatentraeger_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion SOLLTE den für die Protokollierung zur Verfügung stehenden Speicherplatz *[bei Erreichen eines bestimmten Schwellwertes oder regelmäßig]* überprüfen.

Diese Vorschrift zielt darauf ab, die Verfügbarkeit der Protokolldaten sicherzustellen. Das ist essenziell, da eine unterbrochene oder lückenhafte Aufzeichnung die Früherkennung von Angriffen unmöglich machen könnte, was dazu führen könnte, dass kritische forensische Beweise für eine Untersuchung fehlen. Die Umsetzung dieser Anforderung kann auf verschiedene Arten erfolgen. Es könnte ein Skript oder ein automatisierter Dienst eingesetzt werden, der den Füllstand des Speicherplatzes in regelmäßigen Abständen, zum Beispiel alle 15 Minuten oder einmal pro Stunde, prüft. Alternativ kann eine Überprüfung bei einem definierten Schwellenwert durchgeführt werden, etwa wenn 80 % oder 90 % des zugewiesenen Speicherplatzes belegt sind. Zur Behebung könnte bei Kapazitätsengpässen eine automatische Archivierung älterer Protokolldaten auf einem separaten, kostengünstigeren Speicher gestartet werden, um den primären Speicher zu entlasten. Es kann aber auch eine Rotationsstrategie für Log-Dateien konfiguriert werden, die bei Erreichen einer bestimmten Größe oder eines Alters die ältesten Dateien löscht oder archiviert.

### DET.3.5 – Revisionssicherheit

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.18, G 0.37

**Vorgänger:** [DER.2.2.A14-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_2_Vorsorge_fuer_die_IT_Forensik_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [DER.2.2.A5-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_2_Vorsorge_fuer_die_IT_Forensik_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [NET.1.2.A35-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion SOLLTE Änderungen am Audit Log revisionssicher dokumentieren.

Wenn die Protokollaufzeichnung unzureichend vor Veränderung geschützt ist, könnten Innentäter diese manipulieren oder löschen, um nicht erkannt oder belangt zu werden. Hierzu gehört auch, dass Administrierende die Protokolldaten zu ihren eigenen Tätigkeiten manipulieren oder löschen könnten. Die Integrität kann durch die Erstellung und getrennte Aufbewahrung von kryptografischen Hashes oder ein Versionskontrollsystem sichergestellt werden. Um sicherzustellen, dass nur autorisierte Personen die Protokolle verändern können, können z.B. Verschlüsselung und getrennte Aufbewahrung des Schlüssels, einmalig beschreibare Datenträger, oder ein Protokollierungsserver/SIEM mit stark eingeschränkten Zugriffsrechten eingesetzt werden. Auch die Aufzeichnung in einer öffentlichen Transparenzdatei ist möglich, wenn die Protokolle keine vertraulichen Daten enthalten.

### DET.3.6 – Unbestreitbarkeit

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 3 · **Gefährdungen:** G 0.37, G 0.23, G 0.32, G 0.46

> Detektion für Daten KANN Nachweise für den Zusammenhang *[bestimter Ereignisse]* mit *[einer bestimmten Person oder Rolle]* dokumentieren.

Für Handlungen, die eine besondere Bedeutung für die rechtliche Compliance oder die korrekte Verarbeitung von Daten in kritischen Geschäftsprozessen haben, kann es sinnvoll sein, eine zweifelsfreie Zuordnung des Ereignisses zu einer Person zu gewährleisten. Beispiele können das Senden von Nachrichten als Geschäftsleitung, die Überweisung hoher Beträge auf Konten im Ausland oder der Zugang einer Nachricht mit großer rechtlicher Bedeutung sein. Für einen zweifelsfreien Nachweis reicht die einfache Zuordnung zu einem Zugangskonto oft nicht aus, da das Konto auch von anderen missbraucht worden sein könnte. Zum Nachweis können verschiedene Maßnahmen eingesetzt werden: Digitale Signaturen auf Basis asymmetrischer Kryptographie können die Urheberschaft von Dokumenten verifizieren, während Zeitstempel von vertrauenswürdigen Zeitservern die chronologische Integrität sicherstellen. Eine dezentrale Speicherung der Logs auf verschiedenen Systemen erschwert Manipulationsversuche; ergänzend erhöht die Implementierung einer Blockchain-Technologie mit verketteten Hashwerten die Fälschungssicherheit erheblich. Hardwarebasierte Sicherheitsmodule (HSMs) können kryptografische Schlüssel vor unbefugtem Zugriff schützen.

## DET.4 Überwachung von Aktivitäten

### DET.4.1 – Überwachung der Protokollierung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.32, G 0.37, G 0.27

**Vorgänger:** [APP.4.2.A32-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_4_2_SAP_ERP_System_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [DER.1.A14-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [DER.1.A6-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [IND.1.A10-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [OPS.1.1.5.A3-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_5_Protokollierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion SOLLTE die Funktionsfähigkeit der Protokollierung überwachen.

Zu den Kriterien kann beispielsweise die Aktivierung oder Deaktkvierung des Loggings auf Systemen, sowie die Datenmenge eingehender Logs in einem bestimmten Zeitraum gehören.

### DET.4.2 – Automatische Angriffserkennung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 5 · **Gefährdungen:** G 0.39, G 0.23, G 0.32

**Vorgänger:** [DER.1.A17-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [DER.1.A17-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [SYS.1.1.A27-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [SYS.1.9.A19-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_9_Terminalserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.2.5.A17-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_5_Client_Virtualisierung_Edition_2023.pdf?__blob=publicationFile&v=2#download=1) (superset-of) · [SYS.4.4.A17-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_4_4_Allgemeines_IoT_Geraet_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion für IT-Systeme SOLLTE diese auf Anzeichen für Angriffe durch *[einen automatisierten Mechanismus]* überwachen.

Wenn professionelle Tätergruppen Zugriff auf Systeme und Daten erhalten, nutzen sie diese zunehmend schneller für ihre Zwecke aus, z.B. um Daten abfließen zu lassen oder Ransomware zu verteilen. Zur Umsetzung können sowohl netz- als auch hostbasierte Erkennungssysteme (NIDS und HIDS) verwendet werden. Für die Detektion bei IT-Systemen ohne Installationsmöglichkeit wie Appliances, IoT-Geräte oder OT-Systeme kann ein kombinierter Ansatz aus Netzwerk- und Loganalyse sinnvoll sein. Angriffe können signaturbasiert, sowie durch Verhaltensanalyse und Anomalien erkannt werden. Die Anforderung kann auch mit bereits vorhandenen oder im System integrierten Angriffserkennungsmechanismen erfüllt werden. Zweckmäßig ist es Schwellwerte und Kategorien (Info, Warnung, Alarm) so festzulegen, dass Probleme frühzeitig erkannt werden können, aber beim Betriebspersonal keine Alarmmüdigkeit (alert fatigue) aufkommt. Hierzu ist es hilfreich die Ergebnisse regelmäßig auszuwerten und wenn nötig Korrekturmaßnahmen zu ergreifen.

### DET.4.3 – Überwachung der Angriffserkennung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.39, G 0.32, G 0.28

**Vorgänger:** [NET.3.2.A23-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_2_Firewall_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of)

> Detektion SOLLTE die Funktionsfähigkeit der automatisierten Angriffserkennung überwachen.

Hierzu gehört insbesondere die Aktivierung oder Deaktivierung der Angriffserkennung, oder das Stoppen zugehöriger Dienste.

### DET.4.4 – Änderungen an Sicherheitsrichtlinien

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.39, G 0.32, G 0.28

**Vorgänger:** [APP.4.2.A30-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_4_2_SAP_ERP_System_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [NET.3.2.A23-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_2_Firewall_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [NET.3.4.A12-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_4_Network_Access_Control_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [SYS.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion SOLLTE Änderungen an Sicherheitsrichtlinien einschließlich deren Aktivierung oder Deaktivierung überwachen.

Wird die Aktivität von automatisierten Sicherheitswerkzeugen nicht überwacht, so könnten Angreifer diese Schutzmechanismen unbemerkt deaktivieren und die Person so in falscher Sicherheit wiegen. Zudem installieren Angreifer gerne permanente Hintertüren über neue Konten oder Gruppenwechsel. Automatisierte Sicherheitsrichtlinien sind z.B. Ausnahmelisten von Antivirus- oder EDR, über den Verzeichnisdienst hinzugefügte Gruppenzugehörigkeiten zu sicherheitsrelevanten Gruppen (z.B. Admin), NAC oder Firewallregeln.

### DET.4.5 – Unerwünschte Datenabflüsse

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.37, G 0.19

**Vorgänger:** [NET.1.1.A35-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_1_Netzarchitektur_und_design_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [SYS.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion KANN unerwünschte Datenabflüsse überwachen.

Unerwünschte Datenabflüsse beziehen sich hier auf jede unautorisierte Übertragung sensibler Informationen aus internen IT-Systemen oder Anwendungen nach außen (engl. data leakage oder data exfiltration). Darunter fallen sowohl absichtliche als auch unbeabsichtigte Transfers, etwa über Endgeräte, Netzwerkkanäle oder Cloud-Schnittstellen, wobei Data Loss Prevention (DLP) als Sammelbegriff für technische und organisatorische Maßnahmen dient, die solche Abflüsse erkennen oder verhindern können. Die Überwachung kann gewährleisten, dass vertrauliche Inhalte nicht unbemerkt der Kontrolle entzogen werden. Herkunft und Ziel solcher Abflüsse können zusätzlich Indikatoren für kompromittierte Zugangskonten oder Fehlkonfigurationen liefern. Der Zweck der Vorschrift liegt darin, potenzielle Datenabflüsse frühzeitig sichtbar zu machen, sodass aufkommende Risiken wie der Verlust von personenbezogenen Datensätzen oder vertraulichen Forschungsunterlagen erkannt werden können; andernfalls könnte ein Angreifer persistente Kommunikationskanäle nutzen, um über längere Zeit unbemerkt Daten abzuziehen. Eine wirksame Überwachung kann dabei Anomalien identifizieren, die auf Missbrauch, Malware-Aktivität oder Fehlbedienungen hindeuten, und kann die Integrität sowie Vertraulichkeit schützenswerter Informationen erhöhen. Mögliche Varianten der Umsetzung können auf datei- und inhaltsbasierter DLP-Analyse, Netzwerk-DLP über definierte inspection points, Monitoring von Cloud-Workloads mittels API-gestützter DLP-Funktionen oder Endpoint-DLP basierend auf Richtlinien für Kopieren, Drucken oder Übertragungen über Wechselmedien beruhen.

### DET.4.6 – Anomale Nutzung der Anwendung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 3 · **Gefährdungen:** G 0.32, G 0.28, G 0.23

**Vorgänger:** [APP.4.3.A20-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_4_3_Relationale_Datenbanksysteme_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [CON.10.A6-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/03_CON_Konzepte_und_Vorgehensweisen/CON_10_Entwicklung_von_Webanwendungen_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [OPS.1.1.7.A25-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_7_Systemmanagement_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [SYS.1.6.A24-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_6_Containerisierung_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [SYS.2.5.A17-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_5_Client_Virtualisierung_Edition_2023.pdf?__blob=publicationFile&v=2#download=1) (equivalent-to)

> Detektion für Anwendungen KANN die Nutzung der Anwendung auf Anomalien überwachen.

Beispiele sind massenhafte Downloads von Dateiservern oder Cloud-Diensten, Datenbankabfragen die eine ungewöhnlich hohe Menge von Daten oder Einträgen, die unerreichbar sein sollen, zurückliefern, oder automatische E-Mail-Weiterleitungen an externe Domains.

#### DET.4.6.1 – Verhaltensanalyse von Zugangskonten

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.32, G 0.39, G 0.37

**Vorgänger:** [OPS.1.1.7.A25-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_7_Systemmanagement_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [SYS.2.1.A45-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_1_Allgemeiner_Client_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für Verzeichnisdienste KANN das Verhalten von Zugangskonten überwachen.

User and Entity Behaviour Analytics (UEBA) nutzt moderne Verfahren einschließlich KI, um Anomalien im Verhalten von Zugangskonten oder Systemen zu erkennen, z.B. Anmeldungen zu ungewöhnlichen Zeiten, von ungewöhnlichen Orten, durch Verwendung veralteter Authentifzierungsverfahren wie NTLMv1 oder die Ausführung ungewöhnlicher Anwendungen. Ungewöhnliches Verhalten kann Anzeichen für netzbasierte Angriffe oder Innentäter sein. Allerdings gilt es hierbei auch rechtliche Vorgaben zum Datenschutz und betriebliche Mitbestimmungsrechte zu beachten. Ein sinnvoller Maßstab für die Ausgestaltung von Umfang und Detailltiefe der Überwachung können die Geschäfts- und Sicherheitsziele sein. Sinnvoll ist es hierbei begleitende Maßnahmen zur Compliance einzuführen, beispielsweise das manuelle Analysen nur unter bestimmten Voraussetzungen oder Beteiligungen vorgenommen werden.

### DET.4.7 – Auslaufen von Domains

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.25, G 0.26, G 0.27

**Vorgänger:** [APP.3.6.A7-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_6_DNS_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [APP.3.6.A8-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_6_DNS_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für Webserver KANN das Auslaufen von Domains überwachen.

Wenn Registrierungsfristen und Verlängerungszeiträume nicht im Blick behalten werden, könnte eine Domain aus Versehen verfallen und damit einhergehend Erreichbarkeits­probleme, Vertrauensverluste oder gar Sicherheits­lücken entstehen. Als Beispiele können Domains dienen, die für Web­auftritte, E‑Mail-Systeme oder API-Endpunkte genutzt werden. Ebenso kann es sich um Subdomains handeln, die für interne Tools, Test­umgebungen oder automatisierte Monitoring­dienste registriert sind. Auch Domains, die nur der Weiterleitung auf Haupt­präsenzen dienen oder die für Zertifikats­ver­waltung (z. B. ACME-Challenges) verwendet werden, können unter diese Überwachung fallen. Jede dieser Anwendungsfälle kann potenziell betroffen sein, wenn die Registrierung unbemerkt abläuft. Hilfreich ist hierfür ein zentrales Inventar aller genutzten Domains in dem Registrierungs­daten (Ablaufdatum, Registrar, Kontakt­email) erfasst werden. Automatisierte Scripts oder Aufgaben­tickets können eingerichtet werden, die in festgelegten Abständen (z. B. 60, 30 und 7 Tage vor Ablauf) eine Benachrichtigung auslösen. Auch Monitoring-Plattformen mit DNS-Plugins können verwendet werden, um Fristen zu prüfen und Erinnerungen zu generieren. Zusätzlich kann eine Prozess­beschreibung definiert werden, in der Verantwortlichkeiten und Eskalations­wege bei nahendem Domain­ablauf festgehalten sind, um schnelle Entscheidungen und Verlängerungen zu ermöglichen.

### DET.4.8 – Ausstellung neuer HTTPS-Zertifikate

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.15

> Detektion für Webserver KANN die rechtzeitige Ausstellung neuer HTTPS-Zertifikate für Hostsysteme, die im Internet erreichbar sind, überwachen.

„Rechtzeitige Ausstellung neuer HTTPS-Zertifikate“ meint hier, dass überwacht wird, ob vor Ablauf eines bestehenden TLS-/HTTPS-Zertifikats ein neues, gültiges und zur jeweiligen Webserver-Identität passendes Zertifikat aktiviert wird (certificate expiry monitoring, certificate renewal). „HTTPS-Zertifikate“ sind hier X.509-Zertifikate für TLS-gesicherte Webverbindungen, die insbesondere Servernamen, Gültigkeitszeitraum, ausstellende Zertifizierungsstelle und kryptografische Bindung an einen Schlüssel enthalten. „Server, die im Internet erreichbar sind“ bezeichnet Webserver mit öffentlich erreichbarer Adresse oder öffentlich auflösbarem Namen, etwa Webportale, APIs, Kundenportale oder Administrationsoberflächen, sofern sie aus dem Internet angesprochen werden können. Die Vorschrift zielt darauf ab, ablaufende oder nicht rechtzeitig erneuerte Zertifikate frühzeitig sichtbar zu machen: Ein versäumter Austausch könnte zu Browserwarnungen, Dienstunterbrechungen, fehlgeschlagenen API-Verbindungen, Vertrauensverlust bei Nutzenden oder improvisierten Notfallmaßnahmen führen. Eine entsprechende Detektion kann die Verfügbarkeit und Vertrauenswürdigkeit öffentlich erreichbarer Webdienste unterstützen und kann zugleich Hinweise auf Fehlkonfigurationen, unvollständige Automatisierung oder unerwartete Änderungen im Zertifikatsbestand liefern. Hierbei ist es sinnvoll nicht nur die Restlaufzeit mit Schwellwerten zu überwachen, sondern auch die tatsächliche Bereitstellung des neuen Zertifikates. Dazu können ein Monitoring der Zertifikatsdaten direkt am Webendpunkt, sowie Auswertungen aus Load-Balancern oder Reverse-Proxys gehören.

### DET.4.9 – Manipulations-Checkup

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.23, G 0.39, G 0.32, G 0.41

**Vorgänger:** [CON.1.A20-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/03_CON_Konzepte_und_Vorgehensweisen/CON_1_Kryptokonzept_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [IND.1.A17-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [SYS.1.1.A27-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [SYS.4.3.A16-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_4_3_Eingebettete_Systeme_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion für IT-Systeme KANN das System auf Manipulationsversuche *[regelmäßig]* überprüfen.

Falls Systeme einem erhöhten Manipulationsrisiko ausgesetzt sind (z.B. wegen öffentlicher Aufstellung), die Vertraulichkeit oder Integrität des Systems oder damit verbundener Daten oder Netze jedoch nicht vernachlässigenswert ist, so ist eine regelmäßige Überprüfung auf Manipulationen empfehlenswert. Hierfür können Gerätesiegel verwendet werden. Maßnahmen bei Feststellung einer Manipulation können z.B. das Zurücksetzen auf den Werkszustand oder die Aussonderung sein.

### DET.4.10 – Host-basierte Köder

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.21, G 0.23, G 0.40, G 0.32

**Vorgänger:** [SYS.1.1.A27-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion für IT-Systeme KANN Host-basierte Köder installieren.

Köder sind Anwendungen, Dateien oder Datensätze auf dem IT-System, welche die Aufmerksamkeit von Angreifern auf sich ziehen, um diese zu entdecken, nachzuverfolgen oder von echten Zielen abzulenken. Sie werden auch als Canaries oder Tripwire bezeichnet. Beispielsweise kann das Sicherheitsteam eine gefälschte, aber verlockende Datei (z. B. „IBAN-Kontodaten.xlsx“) im System platzieren und eine Überwachung einrichten, die sie benachrichtigt, wenn die Datei berührt wird - da legitime Benutzer nicht darauf zugreifen können, signalisiert jede Interaktion potenziell unbefugte Aktivitäten. Ein weiteres Beispiel ist eine Datei „unattended.xml“, da sie für Angreifer nützliche Anmeldedaten für automatische Installationen enthalten könnte. Indem Sie eine gefälschte Version mit harmlosen Daten erstellen und den Zugriff auf die Datei oder Anmeldeversuche mit diesen Zugangsdaten überwachen, erhalten Sie eine frühzeitige Warnung, wenn jemand Ihr System auf der Suche nach einfachen Möglichkeiten zur Erlangung von Administratorrechten durchforstet, so dass Sie reagieren können, bevor es zu einem schwerwiegenderen Verstoß kommt. Allerdings kann es hierbei zu falsch-positiv Vorfallsmeldungen kommen, insbesondere wenn die Köder dort platziert werden wo sie für legitime Nutzende leicht zugänglich sind.

### DET.4.11 – Anomalien in Netzen und am Perimeter

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 5 · **Gefährdungen:** G 0.23, G 0.39, G 0.32

**Vorgänger:** [DER.1.A9-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [DER.1.A9-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [NET.2.1.A13-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_2_1_WLAN_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [NET.3.1.A15-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_1_Router_und_Switches_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [SYS.2.5.A17-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_5_Client_Virtualisierung_Edition_2023.pdf?__blob=publicationFile&v=2#download=1) (subset-of)

> Detektion für Netze SOLLTE den Netzwerkverkehr auf Anomalien überwachen.

Beispiele sind ausgehende Netzverbindungen zu als bösartig bekannten oder gänzlich unbekannten DNS-Domains oder IP-Adressen, Anzeichen für DNS-Tunneling (ungewöhnlich lange Subdomains oder Spitzenwerte für TXT-Mengen), ungewöhnlich hohes Datenvolumen zu Cloud-Speicherlösungen, sowie unautorisierte Portscans oder Brute Force Angriffe auf Fernwartungsschnittstellen wie RDP oder SSH sein. Hierdurch können Verbindungen zu Angreiferservern (C2 Beacons), die Ausbreitung von Angriffen über das Netz, oder Datenabflüsse erkannt werden.

#### DET.4.11.1 – Authentifizierungsversuche an externen Schnittstellen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.23, G 0.32

**Vorgänger:** [NET.1.2.A7-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [NET.3.2.A2-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_2_Firewall_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (superset-of) · [NET.3.3.A5-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_3_VPN_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für Externe Netzanschlüsse KANN Authentifizierungsversuche auf unauthorisierte Verbindungen *[regelmäßig]* überprüfen.

Ohne solche Überprüfungen könnte ein Angreifer unbemerkt wiederholt Zugangsdaten erraten (Brute-Force- oder Wörterbuchangriffe) oder unautorisierte Geräte an Schnittstellen wie VPN-Gateways, Firewalls oder externen Modems anbinden. Auch ein unbemerktes Einschleusen von Schadsoftware über offene Remote-Desktop- oder SSH-Verbindungen könnte langfristig unentdeckt bleiben. Eine kontinuierliche Auswertung von Anmeldeversuchen kann dagegen Auffälligkeiten wie ungewöhnlich viele Fehlversuche, Anmeldungen aus geografisch atypischen Regionen oder Verbindungsaufbau außerhalb üblicher Betriebszeiten aufzeigen und so eine wirksame Schutzwirkung entfalten. Als Frist können Intervalle wie "täglich", "wöchentlich" oder "in Echtzeit" je nach Kritikalität des Anschlusses angemessen sein. Verbindungen sind hier unautorisiert, wenn Anzeichen vorliegen, dass sie von unautorisierten Personen oder von unautorisierten Systemen stammen. Die Überprüfung kann manuell oder durch automatische Analyse von Logdateien erfolgen. Empfehlenswert ist eine kontinuierliche Überwachung. Dabei kann z.B. nach ungewöhnlichen vielen fehlgeschlagenen Anmeldungen, veralteten Berechtigungen, Einwahlen von Adminaccounts, ungewöhnlichen Einwahlorten/IP-Adressbereichen/User Agents oder Uhrzeiten gesucht werden. Als Reaktion kommen z.B. Sperren betroffener Adressbereiche, die Abschaltung angegriffener Schnittstellen oder stärkere Authentifizierungsmechanismen wie Mehr-Faktor-Authentifizierung in Betracht.

#### DET.4.11.2 – Netzwerk-Honeypots

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.23, G 0.39

**Vorgänger:** [DER.1.A9-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion für Netze KANN Netzwerk-Honeypots installieren.

Honeypots sind Systeme, die das Verhalten eines Betriebsservers simulieren, um bei netzbasierten Angriffen Informationen über den Angriff zu erhalten. Geeignet sind z.B. vermeintliche Rechnungsbearbeitungssysteme oder Datenbank-Server. Alarmierungsereignisse können hier z.B. Login-Versuche oder unerwartete API-Abfragen sein. Allerdings kann es hierbei zu falsch-positiv Vorfallsmeldungen kommen, insbesondere wenn die Honeypots dort platziert werden, wo sie für legitime Nutzende leicht zugänglich sind, oder wenn legitime Netzwerkscans bereits eine Alarmierung auslösen. Daher ist es sinnvoll, die konkreten Einsatzgegebenheiten in einer Risikoanalyse zu betrachten und den möglichen Detektionsmehrwert mit den potenziellen Risiken solcher falsch-positiv Meldungen abzuwägen.

#### DET.4.11.3 – Netzverkehrsfluss

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.23, G 0.39, G 0.37

**Vorgänger:** [DER.1.A9-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [NET.3.2.A9-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_2_Firewall_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with)

> Detektion für Netze KANN auf kritische Netzverkehrsflüsse anhand von *[Kriterien]* überwachen.

Ein Netzverkehrsfluss ist eine Aufzeichnung von Verkehrsdaten einer Netzwerkverbindung (wie Quell-/Ziel-IP, Ports, Protokoll, übertragene Datenmenge und Zeitdauer). Die Aufzeichnung des gesamten Verkehrs (Packet Capture) des vollständigen Inhalts aller Datenpakete ist hierzu nicht erforderlich, sodass die zu untersuchende Datenmenge überschaubar bleibt. Allerdings sind hier Compliance-Anforderungen zur Datenspeicherung relevant. Für datenschutzrechtliche Fragen zu Verkehrsdaten kann der BfDI Leitfaden Speicherung Verkehrsdaten als Grundlage genutzt werden. Beispiele für Kriterien sind die Aufzeichnung an wichtigen Netzgrenzen (DMS-Internet), in kritischen Netzen, zwischen Serversystemen oder bei Leistungsproblemen.

### DET.4.12 – Monitoring der Netzverfügbarkeit

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.23, G 0.25, G 0.26, G 0.27

**Vorgänger:** [NET.1.2.A25-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [NET.1.2.A26-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [OPS.1.1.1.A9-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (superset-of)

> Detektion für Netze SOLLTE die Verfügbarkeit des Netzes anhand von *[Schwellwerten]* überwachen.

Die Verfügbarkeit von Netzen, insbesondere des Internetanschlusses, sowie im Kern- und Verteilernetz, ist von zentraler Bedeutung für die Verfügbarkeit von IT-Infrastrukturen. Ein Monitoring ermöglicht es dem Betriebspersonal, bei Netzproblemen reagieren zu können, bevor Beschwerden von Nutzenden aufkommen. Kann durch Hello-Packete von Netzkomponenten oder die Erreichbarkeit von Diensten über das Netz umgesetzt werden.

#### DET.4.12.1 – Auslastung des Netzes

**Pflicht:** SOLLTE · **Stufe:** `erhöht` · **Aufwand:** 4 · **Gefährdungen:** G 0.25, G 0.26, G 0.27, G 0.18

**Vorgänger:** [NET.1.2.A25-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [NET.1.2.A25-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_1_2_Netzmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion für Netze SOLLTE die Auslastung des Netzes anhand von *[Schwellwerten]* überwachen.

Die Überwachung der Netzauslastung ermöglicht eine schnelle Reaktion bei Verfügbarkeitsproblemen. Wichtige Indikatoren sind Auslastung der verfügbaren Bandbreite, Netzlatenz und Packverluste. Unerwartet hoher Datenverkehr kann auch ein Indiz für einen unautorisierten Zugriff auf große Datenmengen sein. Zur Umsetzung ist es zweckmäßig zunächst Normwerte zu ermitteln (Baselining).

### DET.4.13 – Verfügbarkeit des Hostsystems

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.25, G 0.27, G 0.18, G 0.23

**Vorgänger:** [APP.3.2.A18-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [APP.4.2.A9-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_4_2_SAP_ERP_System_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [OPS.1.1.7.A15-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_7_Systemmanagement_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [SYS.1.1.A23-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [SYS.1.5.A17-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_5_Virtualisierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [SYS.1.9.A14-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_9_Terminalserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion für Hostsysteme SOLLTE die Netzerreichbarkeit anhand von *[Schwellwerten]* überwachen.

Schwellwerte (engl. thresholds) sind hier Grenzwerte, die als Maßstab für die normale oder erwartete Netzerreichbarkeit des Hostsystems dienen. Diese Schwellwerte könnten beispielsweise eine bestimmte Anzahl an Fehlversuchen zur Erreichbarkeit in einem definierten Zeitfenster oder eine überdurchschnittlich hohe Anzahl an Verbindungsanfragen sein, die auf ungewöhnliche Netzwerkaktivität hindeuten. Ein Server könnte beispielsweise aufgrund eines Denial-of-Service-Angriffs (DoS) nicht mehr erreichbar sein, wodurch Dienste für Nutzende ausfallen. Ebenso könnte eine unerwartete Nichterreichbarkeit auf einen Hardwaredefekt, einen Konfigurationsfehler oder einen internen Angriff hindeuten, bei dem der Server vom Netz getrennt wurde, um Spuren zu verwischen. Die Überwachung anhand von Schwellwerten kann der Institution dabei helfen, solche Vorfälle frühzeitig zu erkennen und zu reagieren, bevor sie größeren Schaden anrichten. Die Überwachung kann über ein internes Monitoring-System umgesetzt werden, das kontinuierlich die Erreichbarkeit der Server mittels sogenannter Health-Checks oder Probes prüft. Dabei kann beispielsweise ein automatisches Ping-Verfahren eingesetzt werden, das in regelmäßigen Abständen die Antwortzeit des Servers misst. Die festgelegten Schwellwerte könnten zum Beispiel die maximal erlaubte Anzahl an aufeinanderfolgenden fehlgeschlagenen Ping-Antworten oder die durchschnittliche Antwortzeit sein.

### DET.4.14 – Verfügbarkeit der Anwendung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.25, G 0.27, G 0.18, G 0.23

**Vorgänger:** [APP.3.2.A18-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [APP.4.2.A9-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_4_2_SAP_ERP_System_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [APP.5.4.A11-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_5_4_Unified_Communications_und_Collaboration_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [OPS.1.1.7.A15-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_7_Systemmanagement_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (superset-of) · [SYS.1.1.A23-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [SYS.1.9.A14-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_9_Terminalserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion für Anwendungen SOLLTE die Netzerreichbarkeit anhand von *[Schwellwerten]* überwachen.

Dabei wird die Erreichbarkeit des Dienstes der Anwendung selbst, z.B. auf den bereitstellenden Servern, nicht nur die Erreichbarkeit des Systems überwacht.

### DET.4.15 – Ressourcenauslastung von Hostsystemen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.25, G 0.27, G 0.18

**Vorgänger:** [APP.3.6.A7-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_6_DNS_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.7.A15-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_7_Systemmanagement_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (superset-of) · [OPS.1.2.2.A12-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_2_2_Archivierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [SYS.1.5.A17-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_5_Virtualisierung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [SYS.1.7.A16-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_7_IBM_Z_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [SYS.1.9.A14-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_9_Terminalserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [SYS.2.5.A15-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_5_Client_Virtualisierung_Edition_2023.pdf?__blob=publicationFile&v=2#download=1) (subset-of) · [SYS.2.6.A10-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_6_Virtual_Desktop_Infrastructure_Edition_2023.pdf?__blob=publicationFile&v=2#download=1) (subset-of)

> Detektion für Hostsysteme SOLLTE die Ressourcenauslastung anhand von *[Schwellwerten]* überwachen.

Hierzu zählt z.B. die Auslastung der CPU, des Arbeitsspeichers, des Festspeichers. Dazu ist es sinnvoll vorab Schwellwerte zu ermitteln (KPI Baselining). Mögliche Reaktionsmaßnahmen bei zu hoher Auslastung sind z.B. die Lastverteilung auf mehrere Host-Rechner oder die Beschränkung der Ressourcennutzung pro Client.

### DET.4.16 – Ressourcenauslastung der Server-Dienste

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 3 · **Gefährdungen:** G 0.27, G 0.25, G 0.18

**Vorgänger:** [APP.3.6.A7-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_6_DNS_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [SYS.1.1.A23-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.1.1.A23-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion für Anwendungen KANN die Ressourcenauslastung der für die Anwendung verwendeten Server-Dienste anhand von *[Schwellwerten]* überwachen.

Hierzu zählt z.B. die Auslastung der CPU, des Arbeitsspeichers, des Festspeichers und Anzahl der verbundenen Clients. Dazu ist es sinnvoll vorab Schwellwerte zu ermitteln (KPI Baselining). Mögliche Reaktionsmaßnahmen bei zu hoher Auslastung sind z.B. die Lastverteilung auf mehrere Host-Rechner oder die Beschränkung der Ressourcennutzung pro Client.

### DET.4.17 – Anwendungsbasiertes Kapazitätsmanagement

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 3 · **Gefährdungen:** G 0.27, G 0.25, G 0.18

**Vorgänger:** [OPS.1.1.7.A15-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_7_Systemmanagement_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [OPS.3.2.A14-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_3_2_Anbieten_von_Outsourcing_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [SYS.1.1.A23-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion für Anwendungen KANN die Ressourcenauslastung systemübergreifend anhand von *[Schwellwerten]* überwachen.

Hierbei kann nicht nur die aktuelle Auslastung einzelner Server, sondern die Auslastung der Anwendung insgesamt, auch über einen längeren Zeitverlauf inklusive Lastspitzen und Durchschnittswerten, betrachtet werden.

### DET.4.18 – Öffentliche Blocklisten

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.25

**Vorgänger:** [APP.5.3.A12-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_5_3_Allgemeiner_E-Mail_Client_und_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to)

> Detektion für E-Mail KANN öffentliche Blocklisten auf Einträge für eigene E-Mail-Server *[regelmäßig]* überprüfen.

Die Überprüfung von E-Mail-Blocklisteneinträgen ist entscheidend, um sicherzustellen, dass Nachrichten zuverlässig zugestellt und nicht als Spam klassifiziert werden. Dazu kann zunächst mit Tools wie MXToolbox oder MultiRBL geprüft werden, ob und auf welchen Listen der Server geführt wird, um anschließend die genauen Ursachen zu ermitteln – häufig spielen kompromittierte Konten, unzureichende Authentifizierungsmethoden oder veraltete E-Mail-Listen eine Rolle. Nach der Identifikation können Admins die grundlegenden Probleme beheben, beispielsweise durch Implementierung von SPF-, DKIM- und DMARC-Protokollen, Bereinigung von E-Mail-Listen oder Beseitigung technischer Schwachstellen, bevor bei den jeweiligen Blocklistenbetreibern ein Antrag auf Entfernung gestellt werden kann, wobei in der Regel Nachweise für die durchgeführten Verbesserungen erforderlich sind; zur langfristigen Prävention kann eine regelmäßige Überwachung der Senderreputation, sowie die Einhaltung bewährter E-Mail-Praktiken beitragen, oder die Nutzung eines seriösen E-Mail-Dienstleisters in Betracht gezogen werden.

### DET.4.19 – Unautorisierte Sendeanlagen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.23, G 0.43, G 0.25

**Vorgänger:** [NET.2.1.A13-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_2_1_WLAN_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [NET.2.1.A18-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_2_1_WLAN_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [SYS.3.3.A15-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_3_3_Mobiltelefon_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion für Räume KANN diesen nach unautorisierten Sendeanlagen durch *[einen automatisierten Mechanismus]* überwachen.

Bleiben unautorisierte Sendeanlagen unbemerkt, so könnten hierüber Abhörversuche stattfinden oder Störungen legitimer Sender und Empfänger auftreten. Bedenklich sind beispielsweise versteckte Wanzen in Büromöbeln, manipulierte Peripheriegeräte mit eingebauten Sendern, ohne Erlaubnis mitgebrachte Access Points, modifizierte Smartphones mit verdeckten Fernzugriffsfunktionen oder getarnte IoT-Geräte mit Netzwerkverbindung, die sensible Informationen abgreifen und nach außen übertragen könnten. Zum Aufspüren können Wireless Intrusion Detection Systems (WIDS) genutzt werden, welche Sendeanagen auffinden und unbekannte Sender melden. Um unautorisierte Sender effektiv zu erkennen sind auch begleitende Maßnahmen sinnvoll: Die Implementierung von Zugangsbeschränkungen und Mitnahmeverboten für nicht geprüfte elektronische Geräte; die Schulung des Personals zur Erkennung verdächtiger Objekte; sowie die Dokumentation aller autorisierten Geräte in einem Inventar, um unbekannte Signalquellen schnell identifizieren zu können.

## DET.5 Management von Schwachstellen

### DET.5.1 – Zeitnahes Schwachstellenmanagement

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.23, G 0.39, G 0.18

**Vorgänger:** [CON.1.A15-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/03_CON_Konzepte_und_Vorgehensweisen/CON_1_Kryptokonzept_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [IND.1.A12-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [INF.13.A23-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [OPS.1.1.1.A10-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [OPS.1.1.1.A10-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (superset-of) · [OPS.1.1.1.A20-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of)

> Detektion SOLLTE Verfahren und Regelungen zur Erkennung und Behandlung von Schwachstellen verankern.

Relevant können hierbei verschiedene Arten von Schwachstellen sein (z.B. Physisch und im Netz, Orte, Adressbereiche, Anwendungen und Ports). Zur Erkennung können Schwachstellenscans, Pentests und ein Abgleich der eigenen Infrastruktur mit öffentlichen Schwachstellendatenbanken genutzt werden. Zur Beurteilung der Kritikalität können Scoring-Systeme wie CVSS oder Berichte der betroffenen Hersteller oder Dienstleister herangezogen werden. Zur Behandlung können z.B. Sicherheitspatches, die Deaktivierung betroffener (Teil-)Funktionen oder Komponenten oder die Isolierung betroffenen Systeme oder Anwendungen in Frage kommen. Für Details siehe ISO/IEC 30111.

#### DET.5.1.1 – Risikobasierte Priorisierung

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.28, G 0.23, G 0.18

**Vorgänger:** [OPS.1.1.1.A10-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [OPS.1.1.1.A22-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with)

> Detektion KANN erkannte Schwachstellen anhand von *[risikobasierten Kriterien]* innerhalb *[einer Frist]* überprüfen.

Bei einer risikobasierten Priorisierung wird nicht nur die Ausnutzbarkeit der Schwachstelle im Allgemeinen, z.B. durch einen CVS-Score, zur Priorisierung herangezogen, sondern die Beurteilung erfolgt durch eine Kombination solcher generellen Informationen mit dem individuellen Risikoprofil der betroffenen Assets. Dies ermöglicht es, Schwachstellen deutlich passgenauer zu beurteilen und die wirklich kritischen Schwachstellen zuerst zu patchen oder mitigieren. Hierzu können CVSS-Score, Informationen aus der Threat Intelligence und aus der Risikobewertung von Geschäftsprozessen kombiniert werden. Hierbei können auch automatisierte Verfahren angewendet werden, z.BMultiplikation von Kennzahlen zur Risikobewertung und von CVSS in Kombination mit Schwellwerten. Ergebnisdokument kann z.B. eine Risikomatrix, oder eine eigene CVE-Bewertungsrubrik sein.

### DET.5.2 – Schwachstellenregister

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.23, G 0.18

**Vorgänger:** [IND.1.A12-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [OPS.1.1.1.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (equivalent-to) · [OPS.1.1.1.A20-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of)

> Detektion SOLLTE Schwachstellen bei Entdeckung inklusive betroffener Komponenten, Kritikalität und Status dokumentieren.

Da die Aktualität des Schwachstellenregisters von großer Bedeutung ist, ist die manuelle Pflege von Schwachstellen in einem Dokument nicht empfehlenswert. Stattdessen können automatisiert gepflegte Datenbanken oder spezielle Schwachstellenmanagement-Tools genutzt werden. Das Schwachstellenregister kann auch als verteiltes Register gepflegt werden (z.B. in Schwachstellenscannern, Patchmanagement-Servern, etc.), allerdings ist hierbei eine einheitliche Beurteilung und Priorisierung aufwändiger.

### DET.5.3 – Schwachstellenscans

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.23, G 0.18

**Vorgänger:** [IND.1.A12-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [INF.13.A23-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [INF.13.A23-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.1.A20-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (equivalent-to) · [OPS.1.1.1.A22-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (equivalent-to)

> Detektion SOLLTE eine Vorgehensweise zum Scan nach Schwachstellen einschließlich deren Auswertung und Behandlung verankern.

Über das Netz erreichbare Schwachstellen bergen das Risiko, dass hierüber Angriffe in IT-Systeme und Anwendungen eindringen, Daten auslesen oder sich über das Netz verbreiten. Schwachstellenscans finden solche Lücken, indem sie Anfragen zu bekannten Schwachstellen im Netz stellen und die Antworten auswerten. Regelmäßige Scans tragen dazu bei, dass Sicherheitslücken entdeckt werden, bevor sie ausgenutzt werden.

#### DET.5.3.1 – Autorisierung kritischer Scans

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.39, G 0.18

**Vorgänger:** [INF.13.A23-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [INF.13.A23-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [INF.13.A23-UA.6](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [INF.13.A23-UA.8](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [ORP.5.A5-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/02_ORP_Organisation_und_Personal/ORP_5_Compliance_Management_Editon_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion SOLLTE kritische Scans durch *[zuständige Personen oder Rollen]* autorisieren.

Schwachstellenscans könnten aufgrund ihres Umfangs oder der breiten Abdeckung ihrer Aktivitäten selbst Fehlerzustände provozieren oder Schwachstellen auslösen. Wenn Scans besondere Berechtigungen benötigen - z.B. lokale Administrationsrechte oder Zugriff auf ein abgeschottetes Netz sensibler, betriebskritischer Systeme, so kann eine Autorisierung solcher Scans, vor der eine Abwägung der damit verbundenen Risiken vorgenommen wird, angezeigt sein.

#### DET.5.3.2 – Korrelation komplexer Angriffswege

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.23

**Vorgänger:** [INF.13.A23-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [INF.13.A23-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/10_INF_Infrastruktur/INF_13_Technisches_Gebaeudemanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [SYS.1.1.A24-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion KANN Schwachstellen anhand eines Abgleichs mehrerer Scans miteinander überprüfen.

Fortschrittliche Angreifer könnten mehrere, scheinbar unkritische Schwachstellen nacheinander ausnutzen, die erst in Kombination einen gefährlichen Angriff, etwa die Ausführung von Code aus der Ferne, erlauben. Um solche komplexen Angriffe zu erkennen, können Messergebnisse verschiedener Schwachstellenscanner miteinander abgeglichen werden. Komplexe Angriffswege können mit Methoden wie Attack Trees erkannt und bewertet werden.

#### DET.5.3.3 – Historische Analyse

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.18, G 0.23

**Vorgänger:** [APP.4.3.A20-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_4_3_Relationale_Datenbanksysteme_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [IND.1.A12-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [IND.1.A12-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion KANN Schwachstellen in öffentlich erreichbaren Systemen oder Anwendungen anhand bekannter Anzeichen im Audit Log testen.

Die historische Analyse von Logdateien ermöglicht es, vergangene Systemaktivitäten systematisch zu untersuchen, um potenzielle Sicherheitsvorfälle zu identifizieren, die zum Zeitpunkt ihres Auftretens unbemerkt blieben. Nach der Entdeckung einer Schwachstelle kann so rückwirkend festgestellt werden, ob und wie diese bereits ausgenutzt wurde. Die Umsetzung kann durch Etablierung eines zentralisierten Log-Managements mit langer Aufbewahrungsdauer, Implementierung automatisierter Such- und Korrelationsalgorithmen zur Erkennung bekannter Angriffsmuster und Anomalien in den Logdaten, sowie durch forensische Analyse der Zeitstempel, Quell-IPs, Benutzeraktivitäten und Zugriffsversuche erfolgen. Bei der Feststellung von Schwachstellen in öffentlich zugänglichen Systemen ist es sinnvoll die Audit-Logs gezielt nach Indikatoren zu durchsuchen, die auf entsprechende Angriffsmuster hindeuten - darunter ungewöhnliche Zugriffszeiten, auffällige Authentifizierungsversuche, verdächtige Datenbankabfragen oder charakteristische Command-Injection-Versuche, wodurch potenzielle Kompromittierungen retrospektiv aufgedeckt und in ihrem vollen Umfang bewertet werden können.

### DET.5.4 – Regelmäßige Penetrationstests

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.23

**Vorgänger:** [APP.1.4.A15-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_1_4_Mobile_Anwendungen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [NET.3.2.A24-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_2_Firewall_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [OPS.1.1.1.A20-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (superset-of) · [OPS.1.1.1.A23-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_1_Allgemeiner_IT_Betrieb_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (equivalent-to) · [OPS.1.1.6.A14-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_6_Software_Tests_und_Freigaben_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.1.1.A24-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_1_1_Allgemeiner_Server_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion für IT-Systeme KANN die tatsächliche Abwehrfähigkeit nach *[einer anerkannten Vorgehensweise]* *[regelmäßig]* überprüfen.

Ein Penetrationstest, oft auch als Pentest bezeichnet, ist eine von Sicherheitsexperten simulierte Cyberattacke, um Schwachstellen und Sicherheitslücken aufzudecken. Ziel ist es, komplexe Schwachstellen in konkreten Informationsumgebungen aufzuspüren, bevor sie von echten Angreifern ausgenutzt werden könnten. Dabei werden verschiedene Methoden und Techniken eingesetzt, die auch von Angreifern verwendet werden könnten, z.B. Informationssammlung, Scan und Ausnutzen von Schwachstellen, seitliches Ausbreiten über das Netz, sowie Versuche, durch Täuschung und Manipulation von Personen an Informationen oder Zugriff zu gelangen. Anerkannte Vorgehensweisen, die für Penetrationstests angewendet werden können, sind z.B. der BSI Praxis-Leitfaden für IS-Penetrationstests, OSSTMM, NIST SP 800-115, PTES (Penetration Testing Execution Standard), OWASP für Webanwendungen oder der Leitfaden für Penetrationstests von Large-Language-Modellen des Expertenkreises KI-Sicherheit. Pentests können von externen Dienstleistern oder internem Personal vorgenommen werden. Entscheidend für ein gutes Ergebnis ist hierbei neben einer standardisierten, strukturierten Vorgehensweise die Qualifikation der ausführenden Personen, da Penetrationstests die Ausforschung komplexer Angriffsmöglickeiten erfordern, die weit über den isolierten Einsatz einzelner Werkzeuge hinausgehen können. Pentesting von Außen enthält sowohl die Suche nach angreifbaren Schwachstellen aus dem Internet, als auch die vorhergehende Recherche, um angreifbare Informationen aufzuspüren (Open Source Intelligence). Zur konsequenten Überprüfung gehört auch, dass deren gefundene Schwachstellen im Rahmen des Schwachstellenmanagements zeitnah behandelt werden. Zweckmäßig ist es daher, gefundene Schwachstellen bestimmten zuständigen Personen oder Rollen zur Behebung zuzuweisen und diese innerhalb der Fristen des Schwachstellenmanagements zu schließen.

### DET.5.5 – Red Teaming

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.23, G 0.39, G 0.28

> Detektion für IT-Systeme KANN die tatsächliche Abwehrfähigkeit *[regelmäßig]* durch unabhängig agierende Sicherheitsexperten überprüfen.

Red Teaming ist ein strukturierter, realitätsnaher Sicherheitstest, bei dem ein sogenanntes Red Team – also ein unabhängiges, offensiv agierendes Expertenteam – versucht, unter realen Bedingungen in IT-Systeme, Netzwerke oder Anwendungen einzudringen, um Schwachstellen und Reaktionslücken aufzudecken. Dadurch wird nicht nur die technische Abwehr getestet, sondern auch organisatorische und menschliche Faktoren, etwa die Wirksamkeit von Incident-Response-Prozessen, Alarmierungsketten oder die Reaktion des Security Operations Center (SOC). Solche regelmäßigen Überprüfungen durch unabhängige Red Teams ermöglichen einen objektiven und unvoreingenommenen Blick auf die aktuellen Stärken und Schwächen der Sicherheitsmaßnahmen, wodurch Schwachstellen frühzeitig erkannt werden können. Unabhängig ist ein Red Team dabei, wenn es organisatorisch und personell getrennt vom Betriebspersonal und dessen Weisungshierarchie (Blue Team) agiert, sodass keine Interessenkonflikte die objektive Bewertung gefährden.

### DET.5.6 – Threat Hunting

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 4 · **Gefährdungen:** G 0.23, G 0.39

**Vorgänger:** [APP.4.3.A20-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_4_3_Relationale_Datenbanksysteme_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [DER.2.1.A21-UA.7](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion KANN den Informationsverbund durch Sicherheitsexperten auf Anzeichen für Angriffe *[regelmäßig]* überprüfen.

Threat Hunting bezeichnet eine proaktive Suche nach Anzeichen für Sicherheitsvorfälle durch Analyseexperten, da fortschrittliche Angriffe durch automatisierte Systeme zur Angriffserkennung häufig nicht detektiert werden können. Im Unterschied zum Penetrationstest steht dabei nicht das Aufsuchen von Schwachstellen, sondern das Finden bereits erfolgreicher Angriffe oder Bedrohungen in den eigenen Systemen und Anwendungen im Vordergrund. In einem ersten Schritt werden Hypothesen, wo und wie sich Angreifer in Infrastrukturen eingeschlichen haben könnten, aufgestellt. Dabei kann man sich etwa auf den Kontext des Informationsverbunden und existierende Bedrohungsmodellierungen stützen. Anschließend werden einschlägige Zielobjekte ausgewählt und auf Anzeichen für verdächtige Aktivitäten untersucht, etwa IT-Systeme, die direkt aus dem Internet erreichbar sind, Jumphosts oder zentrale Hostsysteme. Die Ergebnisse der Überprüfung fließen dann in die regelmäßige Auswahl und Verbesserung von Schutzmaßnahmen mit ein.

### DET.5.7 – Analyse verdeckter Kanäle

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.39

**Vorgänger:** [SYS.2.1.A45-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_1_Allgemeiner_Client_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [SYS.4.3.A18-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_4_3_Eingebettete_Systeme_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion KANN den Informationsverbund auf verdeckte Kommunikationskanäle *[bei Sicherheitsvorfällen mit verdeckten Kanälen und regelmäßig]* überprüfen.

Ein verdeckter Kanal (Covert Channel) ist ein heimlicher Kommunikationskanal, mit dem Angreifer legitime Verbindungen ausnutzen, um verdeckt Daten zu übertragen. Die Analyse verdeckter Kanäle ist insbesondere dann sinnvoll, wenn die Gefahr eines unbefugten Informationsflusses über Sicherheitsdomänen hinweg besteht, beispielsweise bei Anwendungen an externen Netzanschlüssen oder bei IT-Systemen, auf denen Daten mit hoher Sicherheitseinstufung neben anderen Daten verarbeitet werden. Relevant sind dabei sowohl Speicherkanäle (Storage Channel) als auch Zeitkanäle (Timing Channel). Um potenzielle verdeckte Kanäle zu identifizieren bietet es sich an, auf Bedrohungsmodellierungen (Threat Modelling) oder die Sicherheitsarchitektur der betrachteten IT-Produkte zurückzugreifen. Entwickler oder erfahrene Penetrationstester sind am besten in der Lage, potenzielle Schwachstellen in IT-Systemen zu identifizieren, die zu verdeckten Kanälen führen könnten. Einige verdeckte Kanäle können durch darauf spezialisierte Erkennungswerkzeuge (sog. Warden) erkannt werden. Aufgrund der Vielzahl denkbarer verdeckter Kommunikationswege können solche Kanäle jedoch kaum vollständig verhindert werden. Daher ist es zweckmäßig, sich bei der Analyse auf diejenigen potenziellen verdeckte Kanäle zu konzentrieren, die eine bestimmte Bandbreitenschwelle überschreiten. Hierbei bietet sich ein gegenseitiger Abgleich mit existierenden Bedrohungsmodellierungen oder Risikoanalysen an. Auch ergänzende Maßnahmen wie Traffic Normalization können sinnvoll sein - dadurch kann verdeckte Kommunikation zwar nicht erkannt werden, jedoch kann man sie so ausbremsen oder unerkannt eliminieren.

### DET.5.8 – Bedrohungsanalyse

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 5 · **Gefährdungen:** G 0.29, G 0.18

**Vorgänger:** [CON.8.A21-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/03_CON_Konzepte_und_Vorgehensweisen/CON_8_Software_Entwicklung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [DER.1.A12-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [DER.1.A12-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion SOLLTE verfügbare Informationen zu Bedrohungen, die für den Informationsverbund relevant sind, *[regelmäßig]* überprüfen.

Bedrohungsaufklärung (Threat Intelligence) dient dem Sammeln und Analysieren von Informationen über bestehende oder aufkommende Bedrohungen, um fundierte Maßnahmen zur Verhinderung von Schäden zu ermöglichen und die Auswirkungen solcher Bedrohungen zu reduzieren. Sie kann in drei Schichten unterteilt werden: strategische Bedrohungsaufklärung (Austausch von Informationen auf hoher Ebene über die sich verändernde Bedrohungslandschaft), taktische Bedrohungsaufklärung (Informationen über Angreifermethoden, beteiligte Werkzeuge und Technologien) und operative Bedrohungsaufklärung (Details zu spezifischen Angriffen, einschließlich technischer Indikatoren). Die gesammelten Bedrohungsinformationen können analysiert und später genutzt werden, indem Prozesse implementiert werden können, um die aus Bedrohungsaufklärungsquellen gesammelten Informationen in die Risikomanagementprozesse einzubeziehen. Sie können als zusätzlicher Input für technische Präventiv- und Erkennungskontrollen wie Firewalls, Intrusion-Detection-Systeme oder Anti-Malware-Lösungen dienen sowie als Eingabe für die Testprozesse und -techniken der Informationssicherheit verwendet werden. Die Institution kann Bedrohungsinformationen auf gegenseitiger Basis mit anderen teilen, um die allgemeine Bedrohungsaufklärung zu verbessern. Dies kann einen kooperativen Ansatz zur Stärkung der gemeinsamen Sicherheitslage fördern.

#### DET.5.8.1 – Auswertung öffentlicher Quellen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.29, G 0.18, G 0.28, G 0.23

**Vorgänger:** [DER.1.A12-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [DER.1.A12-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [IND.1.A12-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion KANN öffentliche Quellen auf Hinweise zu eigenen Schwachstellen anhand von *[Kriterien zur Suche]* *[regelmäßig]* überprüfen.

Öffentliche Quellen können Hinweise zu aktuellen Schwachstellen geben oder sogar auf die Vorbereitung von Angriffen geben, beispielsweise auf die Nachahmung von Webseiten oder Marken, sowie Typosquatting. Auch Datenleaks wie API-Keys oder falsch konfigurierte Cloud-Systeme können hierüber aufgedeckt werden. Relevante öffentliche Quellen können z.B. Schwachstellendatenbanken, Fachmedien, Security Mailing Listen, Dark Web Foren, Code Repositories, Suchmaschinen oder Soziale Medien sein. Als Kriterien zur Auswahl können verschiedene Suchbegriffe oder Suchmuster herangezogen werden, z.B. Bezeichnungen verwendeter Betriebssysteme oder Komponenten, eigene DNS-Domains, E-Mailadressen, API-Schnittstellen, Markennamen. Die Umsetzung kann durch eigenes Personal oder Threat Intelligence Dienstleister erfolgen.

##### DET.5.8.1.1 – Unautorisierte Publikation

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.29

> Detektion KANN öffentliche Quellen automatisiert auf Hinweise zur unautorisierten Veröffentlichung vertraulicher Daten überwachen.

Unautorisierte Veröffentlichungen liegen vor, wenn vertrauliche Daten ohne Autorisierung der Institution öffentlich gemacht wurden, z.B. personenbezogene Kundendaten oder Geschäftsgeheimnisse. Typische Quellen sind Soziale Netzwerke und Code-Sharing-Plattformen. Kann z.B. durch die automatisierte Suche nach unkritischen, aber in den Quelldaten vorhandenen Begriffen umgesetzt werden.

### DET.5.9 – Externe Schwachstellenmeldungen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.28, G 0.23

**Vorgänger:** [APP.3.2.A20-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [APP.3.2.A20-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion SOLLTE eine Vorgehensweise zur Entgegennahme und Behandlung von externen Schwachstellenmeldungen verankern.

Ohne klar geregelten Umgang könnte eine Institution wertvolle Hinweise übersehen oder verzögert reagieren, was die Wahrscheinlichkeit eines Angriffs auf ungepatchte Ziele erhöht. Denkbar sind etwa Szenarien, in denen eine unbekannte Schwachstelle in einer öffentlich erreichbaren Webanwendung durch Dritte entdeckt wird und die Institution zwar kontaktiert wird, aber ohne geregelten Prozess keine Reaktion erfolgt – was einen erfolgreichen Angriff begünstigen könnte. Eine Institution kann diese Anforderung umsetzen, indem sie z. B. eine leicht auffindbare Kontaktmöglichkeit für Schwachstellenmeldungen bereitstellt – etwa eine dedizierte E-Mail-Adresse wie security@…, ein webbasiertes Formular oder die Eintragung eines „Security.txt“-Hinweises im Webauftritt (nach IETF RFC 9116). Sinnvoll kann es sein, klare Erwartungshaltungen zu kommunizieren, etwa welche Informationen eine Meldung enthalten sollte oder wie Rückmeldungen an Hinweisgeber erfolgen können. Auch ein internes Verfahren zur Kategorisierung und Priorisierung der eingehenden Hinweise kann helfen, Meldungen effizient zu bearbeiten. Eine Institution kann zudem in Erwägung ziehen, standardisierte Rückmeldungen vorzubereiten, um zeitnah bestätigen zu können, dass eine Meldung eingegangen ist, selbst wenn die inhaltliche Analyse noch aussteht. Sinnvoll ist auch ein freiwilliger Verhaltenskodex (z. B. ein „Responsible Disclosure Policy“-Hinweis) auf der eigenen Website, um Hinweisgebern einen rechtlich sicheren Rahmen für ihre Meldungen zu verdeutlichen. So entsteht ein klarer, reproduzierbarer Prozess, der externe Informationen in die eigene Sicherheitsarbeit einbindet und das Risiko minimiert, dass relevante Hinweise verloren gehen oder ungenutzt bleiben. Für Details siehe ISO/IEC 29147.

#### DET.5.9.1 – Bonusprogramm

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.28, G 0.23

**Vorgänger:** [APP.3.2.A20-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_3_2_Webserver_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion KANN ein Bonusprogramm für externe Schwachstellenmeldungen verankern.

Ein Bonusprogramm für externe Schwachstellenmeldungen (englisch häufig Bug Bounty Program) bezeichnet ein strukturiertes Verfahren, bei dem eine Institution freiwilligen Sicherheitsforschenden oder interessierten Dritten eine Belohnung für das Melden bislang unbekannter Sicherheitslücken anbietet. Dabei geht es nicht nur um finanzielle Prämien, sondern auch um nicht-monetäre Anerkennungen wie öffentliche Danksagungen oder Zertifikate. Sinn und Zweck liegt darin, externen Sicherheitsforschern oder -expertenen einen Anreiz zu geben, um Schwachstellen frühzeitig zu finden und zu melden. Zur Umsetzung kann eine Institution (1) transparente Regeln definieren, welche Systeme oder Anwendungen einbezogen sind (in scope) und welche nicht, (2) einen abgestuften Belohnungsrahmen anbieten, der den Schweregrad einer Schwachstelle berücksichtigt, sowie (3) die rechtlichen Rahmenbedingungen durch eine sogenannte „Safe-Harbor-Policy“ festlegen, die den Meldenden Schutz vor rechtlichen Schritten zusichert, solange diese verantwortungsvoll handeln. Ergänzend kann die Institution durch einfache organisatorische Hilfsmittel wie Ticketnummern, automatische Eingangsbestätigungen und zeitnahe Rückmeldungen Vertrauen schaffen und den weiteren Ablauf für externe Meldende nachvollziehbar gestalten.

### DET.5.10 – Zeitnahes Patchmanagement

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.28, G 0.23

**Vorgänger:** [APP.4.2.A30-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_4_2_SAP_ERP_System_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [CON.8.A8-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/03_CON_Konzepte_und_Vorgehensweisen/CON_8_Software_Entwicklung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.3.A1-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_3_Patch_und_Aenderungsmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [OPS.1.1.3.A15-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_3_Patch_und_Aenderungsmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [SYS.2.1.A3-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_1_Allgemeiner_Client_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion SOLLTE ein zeitnahes Patchmanagement verankern.

Patches (Updates oder Sicherheitsaktualisierungen) sind neue Versionen, die Sicherheitslücken schließen. Je nach Aufbau der betroffenen Assets kann es bei der Aktualisierung auch erforderlich sein, Abhängigkeiten (Bibliotheken, Upstream Software) ebenfalls zu aktualisieren. Dies kann durch automatisierte Installation oder nach einem Test umgesetzt werden. Die Umsetzung kann auch den schrittweisen Rollout von Patches vorsehen, sodass bei Fehlern im Patch nicht alle Systeme gleichzeitig betroffen sind und auch komplexe Fehlerbilder durch Rückmeldungen frühzeitig erkannt werden können. Dies kann zum Beispiel nach dem One-Many-All-Prinzip oder Blue-Green-Deployment erfolgen. Zur Beurteilung der Kritikalität von Patches kann die Krititikalität der mit dem Patch verbundenen Schwachstellen, das Risikoprofil der zu patchenden Assets oder eine Korrelation komplexer Angriffswege herangezogen werden.

#### DET.5.10.1 – Autorisierte Bezugsquellen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 5 · **Gefährdungen:** G 0.28, G 0.20

**Vorgänger:** [APP.6.A3-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_6_Allgemeine_Software_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.3.A10-UA.5](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_3_Patch_und_Aenderungsmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion SOLLTE zuverlässige Bezugsquellen für Patches autorisieren.

Eine Quelle ist unzuverlässig, wenn zukünftig mit Verstößen gegen die Schutzziele Vertraulichkeit, Verfügbarkeit oder Integrität durch die Entität zu rechnen ist (d.h. eine Prognose der Vertrauenswürdigkeit). Dies ist insbesondere der Fall, wenn erhebliche Verstöße gegen die Schutzziele durch die Entität begangen worden sind oder Anzeichen dafür vorliegen, dass bei einer Verwendung mit solchen Verstößen zu rechnen ist.

#### DET.5.10.2 – Automatisierte Überwachung von Systemupdates

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.30, G 0.21, G 0.23, G 0.39

**Vorgänger:** [APP.4.2.A30-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_4_2_SAP_ERP_System_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (equivalent-to) · [OPS.1.1.7.A22-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_7_Systemmanagement_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with)

> Detektion für IT-Systeme SOLLTE den Patchstatus durch *[einen automatisierten Mechanismus]* überwachen.

Der Patchsstatus des Informationsverbundes kann dabei durch Kennzahlen bestimmt werden, z.B. durchschnittliche Zeit bis zum Patch (Mean Time To Patch), Prozentsatz aktuell gepatchter Assets, Anzahl offener/geschlossener Ausnahmen.

#### DET.5.10.3 – Automatisierte Überwachung von Anwendungsupdates

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 4 · **Gefährdungen:** G 0.28, G 0.23, G 0.39

**Vorgänger:** [APP.4.2.A30-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_4_2_SAP_ERP_System_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (superset-of) · [OPS.1.1.3.A15-UA.6](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_3_Patch_und_Aenderungsmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [OPS.1.1.7.A22-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_7_Systemmanagement_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (intersects-with) · [SYS.2.1.A3-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_1_Allgemeiner_Client_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion für Anwendungen KANN den Patchstatus durch *[einen automatisierten Mechanismus]* überwachen.

Eine nicht gepatchte Anwendung könnte als Einfallstor für Angreifer dienen, die bekannte Schwachstellen ausnutzen, um sich Zugang zu Systemen oder Daten zu verschaffen. Die Umsetzung kann beispielsweise auf einem Patch Management System (PMS) oder einem Vulnerability Management System (VMS) basieren. Ein Patch-Managementsystem kann beispielsweise so konfiguriert werden, dass es kontinuierlich die Versionen der installierten Software mit einer zentralen Datenbank für verfügbare Updates abgleicht. Auch die Nutzung eines Schwachstellen-Scanners, der im Netzwerk nach ungepatchten Anwendungen sucht, ist eine wirksame Maßnahme. Ein solcher Scanner könnte beispielsweise wöchentlich oder sogar täglich einen Scan durchführen und die Ergebnisse in einem Dashboard visualisieren. Wichtige prozessuale Tipps sind die Einrichtung von Benachrichtigungsworkflows, die sicherstellen, dass kritische Patch-Status-Änderungen sofort an die richtigen Personen eskaliert werden, sowie die Integration der Überwachungsergebnisse in ein zentrales Incident Response System. Dies kann helfen, die Reaktionszeit zu verkürzen, sodass die Anwendungen schnellstmöglich aktualisiert werden.

#### DET.5.10.4 – Integritätsprüfung von Patches

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.28, G 0.23, G 0.39, G 0.20

**Vorgänger:** [APP.6.A4-UA.7](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_6_Allgemeine_Software_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [IND.2.1.A20-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_2_1_Allgemeine_ICS_Komponente_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [IND.2.7.A12-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_2_7_Safety_Instrumented_Systems_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [OPS.1.1.3.A10-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_3_Patch_und_Aenderungsmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion SOLLTE Patches vor der Installation auf Integrität testen.

Wenn Patches durch Fehler bei der Übertragung oder sogar bewusst von Angreifern verändert wurden, kann dies nach der Installation zu nicht behebbaren Fehlerzuständen oder zur Verbreitung von Schadcode führen. Kann durch einen Abgleich von Prüfsummen umgesetzt werden, z.B. durch automatisierte Installationsroutinen oder einen manuellen Abgleich mit der Herstellerwebseite.

#### DET.5.10.5 – Test gemäß Änderungsmanagement

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.39, G 0.28, G 0.18

**Vorgänger:** [OPS.1.1.3.A1-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_3_Patch_und_Aenderungsmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [OPS.1.1.3.A13-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_3_Patch_und_Aenderungsmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [OPS.1.1.3.A14-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_3_Patch_und_Aenderungsmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [OPS.1.1.3.A15-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_3_Patch_und_Aenderungsmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of)

> Detektion KANN Patches entsprechend der Anforderungen der Praktik „Änderungen und Tests“ ausführen.

Stellt sicher, dass Patches zusammen mit anderen Änderungen geprüft werden und trennt zwischen „Routine“- und „Notfall“-Änderungen.

## DET.6 Vorfallserkennung

### DET.6.1 – Beurteilung von Ereignissen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.39, G 0.23, G 0.18

**Vorgänger:** [DER.2.1.A11-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_2_1_Behandlung_von_Sicherheitsvorfaellen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to)

> Detektion SOLLTE ein Verfahren zur Beurteilung von sicherheitsrelevanten Ereignissen anhand von *[Kriterien]* verankern.

Aus einer größeren Menge von sicherheitsrelevanten Ereignissen kann durch Filterung und Korrelation eine kleinere Menge sicherheitskritischer Ereignisse destilliert werden. Dies bedeutet, dass aus allen möglichen Sicherheitsereignissen (wie Zugriffsversuche, Systemänderungen, Netzwerkverkehr) besonders auf die potenziell gefährlicheren oder wichtigeren Ereignisse geachtet wird. Für die Definition eines sicherheitskritischen Ereignisses, siehe Glossar (Namensräume des Grundschutz++). Die Filterung erfolgt sinnvollerweise automatisiert, z.B. durch SIEM, EDR. Die Überwachung kann anhand von bestimmten Begriffen (z.B. "login from unknown device", "blocked malware", "permission changed") oder durch Anomalieerkennung erfolgen. Aufgrund der Vielzahl an möglichen Ereignissen sind detaillierte Kriterien nur schwer festzulegen. Die Kriterien können sich daher auch an einem überschaubaren Schema, etwa einer Abschätzung der Auswirkungen auf die Geschäftsprozesse und gesetzlichen Meldepflichten, orientieren. Sobald ein solches kritisches Ereignis erkannt wird, erfolgt eine Bewertung durch definierte Personen oder Rollen. Diese entscheiden, ob das Ereignis tatsächlich als Sicherheitsvorfall eingestuft werden kann.

#### DET.6.1.1 – Automatisierte Feststellung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.39, G 0.23

**Vorgänger:** [DER.1.A15-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with)

> Detektion SOLLTE kritische Vorfälle anhand von *[Kriterien]* durch *[einen automatisierten Mechanismus]* protokollieren.

Zur Erfüllung der Anforderung ist es nicht erforderlich, dass alle denkbaren Sicherheitsvorfälle automatisch erkannt werden, sondern nur, dass diejenigen Vorfälle, die in der vorhandenen Infrastruktur automatisch feststellbar sind und mit einem hohen Risiko verbunden sind, automatisch festgestellt werden. Beispiele sind hier ein Virenbefall des zentralen Verzeichnisdienstes, unautorisierte Datenabflüsse oder das Aufbrechen eines Fensters im Sicherheitsbereich. Ressourcen meint hier z.B. Systeme, Zugangskonten, Datenkategorien.

#### DET.6.1.2 – Automatische Alarmierung

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.25, G 0.29, G 0.27

**Vorgänger:** [DER.1.A15-UA.7](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of) · [DER.1.A17-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/05_DER_Detektion_und_Reaktion/DER_1_Detektion_von_sicherheitsrelevanten_Ereignissen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [NET.3.2.A23-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_2_Firewall_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [NET.3.2.A23-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_3_2_Firewall_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [OPS.1.1.7.A25-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_7_Systemmanagement_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of)

> Detektion SOLLTE bei sicherheitskritischen Ereignissen eine Alarmierung von *[für die Vorfallsbehandlung zuständigen Personen oder Rollen]* durch *[einen automatisierten Mechanismus]* ausführen.

Für die Definition eines sicherheitskritischen Ereignisses, siehe Glossar (Namensräume des Grundschutz++). Bewährt hat sich hierzu der Einsatz eines Security Information and Event Management Systems (SIEM), das die Audit Logs verschiedener Hersteller auf Ereignisse überprüfen und diese korrelieren kann. Passen Sie Schwellwerte und Kriterien so an, dass keine Alarmmüdigkeit (alert fatigue) beim Personal aufkommt.

#### DET.6.1.3 – Dokumentation von Ergebnissen

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 4 · **Gefährdungen:** G 0.39, G 0.18, G 0.37

**Vorgänger:** [IND.1.A10-UA.6](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/08_IND_Industrielle_IT/IND_1_Prozessleit_und_Automatisierungstechnik_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [ISMS.1.A13-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/01_ISMS_Sicherheitsmanagement/ISMS_1_Sicherheitsmanagement_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (superset-of) · [NET.2.2.A4-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/09_NET_Netze_und_Kommunikation/NET_2_2_WLAN_Nutzung_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion KANN Analyseergebnisse dokumentieren.

Die Aufzeichnung von Beurteilungsergebnissen und Entscheidungen bei Sicherheitsvorfällen dient als rechtssichere Nachweisführung und ermöglicht retrospektive Analysen zur kontinuierlichen Prozessverbesserung. Sie stellt außerdem sicher, dass die Vorfälle während und nach der Behandlung strukturiert aufgearbeitet werden können. Zweckmäßig ist es dabei, möglichst viele hilfreiche Informationen automatisch mitzuerfassen, z.B. welche Fehlermeldung genau aufgetreten ist oder welche Schwellwerte bis zu welchem Wert genau überschritten worden sind. Kann auch durch ein SIEM umgesetzt werden, welches Informationen zu kritischen Ereignissen abspeichert. Die Umsetzung kann mit einem standardisierten Dokumentationssystem erfolgen, das alle relevanten Metadaten erfasst: Zeitstempel, beteiligte Personen, Begründungen für Entscheidungen sowie konkrete Maßnahmen.

### DET.6.2 – Beurteilung von Eingängen

**Pflicht:** SOLLTE · **Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.18, G 0.39, G 0.23

**Vorgänger:** [APP.1.1.A3-UA.4](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/06_APP_Anwendungen/APP_1_1_Office_Produkte_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (equivalent-to) · [OPS.1.1.4.A13-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_4_Schutz_vor_Schadprogrammen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (subset-of)

> Detektion SOLLTE ein Verfahren zur Beurteilung von Datei-Eingängen verankern.

Kann beispielsweise ein Virenscanner eine Datei nicht überprüfen, weil sie mit einem Passwort geschützt ist, erhalten Nutzende die Datei erst, wenn sie durch das für Detektion zuständige Personal freigegeben wurde. Dazu muss die Datei aus einer vertrauenswürdigen Quelle stammen und keine Anzeichen für einen Angriff vorliegen.

#### DET.6.2.1 – Dynamische Sandbox-Analyse

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 4 · **Gefährdungen:** G 0.23, G 0.39, G 0.22, G 0.19

**Vorgänger:** [OPS.1.1.4.A10-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_4_Schutz_vor_Schadprogrammen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [OPS.1.1.4.A13-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_4_Schutz_vor_Schadprogrammen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [OPS.2.3.A25-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_2_3_Nutzung_von_Outsourcing_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [OPS.2.3.A25-UA.2](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_2_3_Nutzung_von_Outsourcing_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of) · [OPS.2.3.A25-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_2_3_Nutzung_von_Outsourcing_Edition_2023.pdf?__blob=publicationFile&v=4#download=1) (subset-of)

> Detektion KANN verdächtige Dateien in einer isolierten Umgebung mindestens anhand von aufgebauten Netzverbindungen, Systemaufrufen und Dateizugriffen testen.

Eine dynamische Sandbox Analyse ist die Ausführung des verdächtigen Codes in einer isolierten Umgebung, aus der eine Anwendung nicht durch Ausführung von Systembefehlen ausbrechen kann (Sandbox Detonation). Sie ermöglicht die sichere Untersuchung potenziell schädlicher Dateien in einer isolierten Umgebung, um deren tatsächliches Verhalten zu beobachten. Eine dynamische Analyse kann verschiedene verdächtige Aktivitäten erfassen: Dateisystemoperationen wie das Erstellen, Ändern oder Löschen von Dateien; Registry-Modifikationen, besonders in Autostart-Bereichen; Netzwerkverhalten einschließlich externer Verbindungsversuche und Datenexfiltration; Prozessverhalten wie Injektionstechniken oder unerwartete Kindprozesse; Speichermanipulationen; Persistenzmechanismen wie Dienste oder geplante Aufgaben; Anti-Analyse-Techniken zur Erkennung virtueller Umgebungen; sowie ungewöhnliche API-Aufrufe wie kryptografische Funktionen oder Sicherheitsumgehungen. Die Sandbox kann dabei mit ausreichender Laufzeit, Netzwerksimulation und Snapshot-Funktionen ausgestattet werden, um auch verzögerte oder umgebungsspezifische Schadfunktionen zu erkennen.

#### DET.6.2.2 – Datenträgerschleuse

**Pflicht:** KANN · **Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.39, G 0.23, G 0.21, G 0.14

**Vorgänger:** [OPS.1.1.4.A12-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/04_OPS_Betrieb/OPS_1_1_4_Schutz_vor_Schadprogrammen_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to) · [SYS.2.1.A24-UA.3](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_2_1_Allgemeiner_Client_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (intersects-with) · [SYS.4.5.A16-UA.1](https://www.bsi.bund.de/SharedDocs/Downloads/DE/BSI/Grundschutz/IT-GS-Kompendium_Einzel_PDFs_2023/07_SYS_IT_Systeme/SYS_4_5_Wechseldatentraeger_Edition_2023.pdf?__blob=publicationFile&v=3#download=1) (equivalent-to)

> Detektion KANN Datenträgerschleusen installieren.

Eine Datenträgerschleuse ist ein vom restlichen Netz der Institution getrenntes IT-System, das speziell zur Erkennung von Schadprogrammen dient. Der Begriff Datenträger umfasst hierbei insbesondere USB-Speichergeräte, externe Festplatten, Speicherkarten sowie optische Datenträger. Der Einsatz einer Datenträgerschleuse kann das Risiko reduzieren, dass Schadsoftware, manipulierte Dateien oder unzulässig übertragene Informationen über mobile Speichermedien in Systeme eingebracht oder aus ihnen heraus transportiert werden. Ohne entsprechende Kontrollmechanismen könnte beispielsweise Malware über USB-Datenträger eingeschleust oder eine unbemerkte Datenabgabe über Wechselspeicher erfolgen; eine Datenträgerschleuse kann solche Vorgänge sichtbar machen und zusätzliche Prüfungen ermöglichen.
