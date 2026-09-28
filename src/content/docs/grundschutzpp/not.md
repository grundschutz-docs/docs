---
title: "NOT – Notfallplanung"
---

Die Notfallplanung stellt sicher, dass bei schwerwiegenden Störungen oder Krisen schnell und koordiniert reagiert wird, um den Fortbestand kritischer Geschäftsprozesse und die Wiederherstellung der betroffenen Systeme zu gewährleisten. Notfallplanung adressiert umfassende Notfälle und Krisensituationen, während die Sicherheitsvorfallbehandlung spezifisch auf Informationssicherheitsvorfälle fokussiert ist. Notfallmanagement ist strategisch und organisatorisch umfassender, während die Vorfallbehandlung auf operative Sicherheitsprobleme eingeht.

## NOT.1 Grundlagen

### NOT.1.1 – Verfahren und Regelungen

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18

> Notfallplanung MUSS Verfahren und Regelungen zur Vorsorge für Notfälle der Informationssicherheit verankern.

Für ein Managementsystem der Informationssicherheit ist es erforderlich, dass auch für Notfälle vorgesorgt wird, z.B. durch eine Datensicherung, so dass bei einer Naturkatastrophe wichtige Daten wiederhergestellt werden können. Dies kann durch den Aufbau eines dafür vorgesehenen Managementsystems (BCMS) oder die Umsetzung der einzelnen Anforderungen dieser Praktik geschehen. Die bei der Festlegung des Verfahrens im Einzelnen zu berücksichtigenden Inhalte, die bei der Festlegung des Verfahrens zu berücksichtigen sind, ergeben sich aus den Anforderungen dieser Praktik. Es empfiehlt sich ebenfalls Wiederherstellungsmöglichkeiten und Alternativen für administrative Zugänge zu betrachten.

#### NOT.1.1.1 – Dokumentation

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.37

> Notfallplanung MUSS die Verfahren und Regelungen dokumentieren.

Ohne eine Dokumentation könnte die Einhaltung der Verfahren und Regelungen von der Tagesform oder dem individuellen Wissen einzelner Mitarbeiter abhängen, was zu inkonsistenten Entscheidungen und Fehlern führen könnte; insbesondere beim Ausscheiden eines langjährigen Administrators könnte wertvolles prozessuales Wissen verloren gehen. Eine klare Dokumentation sichert die Verbindlichkeit und Wiederholbarkeit und dient als unverzichtbare Grundlage für die Einarbeitung neuer Kollegen, für die Durchführung von Audits und zur einheitlichen Anwendung der Regeln in der gesamten Institution. Die Dokumentation kann in einem eigenständigen Dokument als Richtlinie erfolgen, aber auch als Abschnitt in einem bereits bestehenden Dokument oder über die digital strukturiere Erfassung von Maßnahmen zur Umsetzung der Anforderungen, etwa über eine Software zum Management der Informationssicherheit. Sinnvoll ist es Ort und Struktur der Dokumentation an der jeweiligen Zielgruppe, d.h. den für das Management und die Umsetzung verantwortlichen Personen oder Rollen, auszurichten.

#### NOT.1.1.2 – Zuweisung der Aufgaben

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.31

> Notfallplanung MUSS die mit den Verfahren und Regelungen verbundenen Aufgaben *[zuständigen Personen oder Rollen]* zuweisen.

Die Zuweisung von Aufgaben bezeichnet die eindeutige und verbindliche Übertragung von konkreten Tätigkeiten und Verantwortlichkeiten des Änderungsprozesses, wie etwa die Risikobewertung, die technische Umsetzung oder die finale Freigabe, an definierte Stellen in der Institution. Der Sinn dieser Vorschrift ist es, die Verantwortlichkeit ("Accountability") für jeden einzelnen Schritt im Prozess klarzustellen. Ohne eine solche Zuweisung könnten kritische Prüfungen unterbleiben, weil sich niemand explizit zuständig fühlt, was wiederum die Wahrscheinlichkeit fehlgeschlagener Änderungen erhöht. Eine klare Regelung kann sicherstellen, dass keine Aufgaben übersehen werden und jede Tätigkeit von einer dafür qualifizierten und befugten Stelle ausgeführt wird, was die Prozesssicherheit signifikant erhöht. Eine bewährte Methode zur Umsetzung ist die Erstellung einer RACI-Matrix (Responsible, Accountable, Consulted, Informed), die tabellarisch für jeden Prozessschritt darstellt, wer für die Durchführung verantwortlich ist, wer die Gesamtverantwortung trägt, wer zu konsultieren und wer zu informieren ist. Diese Zuständigkeiten können auch direkt in einem Workflow- oder Ticketsystem abgebildet werden, so dass Aufgaben, wie beispielsweise Genehmigungsschritte, automatisch an die richtige Gruppe oder Person weitergeleitet werden. Sinnvoll ist es die Zuweisung anhand von Rollen (z.B. "Anwendungsverantwortlicher", "Netzwerkadministrator", "Change Manager") vorzunehmen, statt an konkrete Personen. Dieser Ansatz stellt sicher, dass die Prozesse auch bei Personalwechseln stabil weiterlaufen, da die Zuständigkeit an die Funktion und nicht an das Individuum gebunden ist.

#### NOT.1.1.3 – Bekanntgabe

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18, G 0.31

> Notfallplanung MUSS die zuständigen Personen oder Rollen über die Verfahren und Regelungen informieren.

Wenn die Zuständigen die etablierten Verfahren nicht kennen, besteht die Gefahr, dass diese – sei es aus Unwissenheit oder Bequemlichkeit – umgangen werden, was die Schutzwirkung des gesamten Managementsystems untergräbt. So könnte ein neuer Systemadministrator eine weitreichende Konfigurationsänderung vornehmen, ohne den vorgeschriebenen Genehmigungsprozess zu durchlaufen, was zu einem unbemerkten Sicherheitsrisiko führen könnte. Eine gezielte Information kann hingegen die Akzeptanz der Regelungen fördern und sicherstellen, dass alle Beteiligten ihre Rolle im Prozess verstehen und die Abläufe korrekt anwenden. Zur Umsetzung ist es sinnvoll die Dokumentation im Rahmen eines Onboarding-Prozesses bekanntzugeben und bei allen Änderungen eine automtatische Benachrichtigung aller zuständigen Personen oder Rollen anzustoßen.

#### NOT.1.1.4 – Business Continuity Management System

**Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.18

> Notfallplanung KANN ein *[Reaktiv-, Aufbau- oder Standard-]*BCMS nach *[BSI-Standard 200-4]* verankern.

BCMS steht für Business Continuity Management System, ein Management-System, das Institutionen dabei hilft, die Kontinuität ihrer Geschäftsprozesse bei Störungen oder Krisen sicherzustellen. Es umfasst die Planung, Umsetzung und kontinuierliche Verbesserung von Strategien und Verfahren, um die Resilienz der Institution zu erhöhen und Ausfallzeiten zu minimieren. Beispiele sind der BSI-Standard 200-4 oder die DIN ISO/IEC 22301. Idealerweise werden die Anforderungen der Praktik Notfallplanung durch ein BCMS erbracht. Wenn ein BCMS aufgebaut wird, können die Anforderungen dieser Praktik in das BCMS integriert erfüllt werden. Das BSI empfiehlt dazu in einem ersten Schritt ein Reaktiv-BCMS aufzubauen und mit steigendem Reifegrad ein Standard-BCMS über die Zwischenstufe Aufbau-BCMS anzustreben. Nähere Informationen können dem BSI-Standard 200-4 Kapitel 2.6 BCMS-Stufenmodell (Reaktiv-, Aufbau- und Standard-BCMS) entnommen werden.

### NOT.1.2 – Regelmäßige Überprüfung

**Stufe:** `normal-SdT` · **Aufwand:** 0 · **Gefährdungen:** G 0.18

> Notfallplanung MUSS die Verfahren und Regelungen *[regelmäßig]* und anlassbezogen auf Aktualität überprüfen.

Eine geplante der etablierten Verfahren und Regelungen dient dazu festzustellen, ob diese noch wirksam, effizient und an die aktuellen Gegebenheiten angepasst sind. Eine anlassbezogene Überprüfung wird durch spezifische Ereignisse ausgelöst, wie etwa einen schwerwiegenden Sicherheitsvorfall, eine strategische Neuausrichtung der IT oder neue gesetzliche Anforderungen. Der Zweck dieser Anforderung ist es, die kontinuierliche Verbesserung und Anpassungsfähigkeit des Prozesses sicherzustellen, da veraltete Regelungen neuen technologischen Entwicklungen oder Bedrohungen nicht mehr gerecht werden könnten; ein vor Jahren für monolithische Anwendungen konzipierter Prozess ist beispielsweise für agile Entwicklungsmethoden oder Microservice-Architekturen ungeeignet. Die regelmäßige Überprüfung kann die Effektivität des Sicherheitsmanagements langfristig aufrechterhalten und die Resilienz der Institution stärken.

## NOT.2 Besondere Aufbauorganisation

### NOT.2.1 – Verfahren und Regelungen zur BAO

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.18

> Notfallplanung SOLLTE Verfahren und Regelungen für eine Besondere Aufbauorganisation (BAO) zur Behandlung von Notfällen und Krisen verankern.

Eine BAO ermöglicht, in Notfällen und Krisen schnellstmöglich auf das Schadensereignis zu reagieren. Eine BAO gehört zu den originären Aufgaben eines BCMS. Wird bzw. wurde ein BCMS nach BSI-Standard 200-4 aufgebaut (unabhängig von der Stufe), so sind die BAO-betreffenden Anforderungen in der Regel erfüllt und werden im Rahmen des BCMS anhand des BSI-Standards 200-4 detaillierter definiert. Nähere Informationen können dem BSI-Standard 200-4 in Kapitel 5 Aufbau und Befähigung der BAO (R+AS) entnommen werden. Die einzelnen Regelungen können den untergliederten Anforderungen entnommen werden.

#### NOT.2.1.1 – Rollen

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.18

> Notfallplanung SOLLTE Aufgaben für die BAO einschließlich BAO-Stab und Notfallteams *[zuständigen Personen oder Rollen]* zuweisen.

Die BAO besteht in der Regel aus einem Stab, der die Koordination und Entscheidungsfindung in einem Schadensereignis übernimmt. Der Stab koordiniert ferner die Tätigkeiten der Notfallteams, die die ausgefallenen Ressourcen wieder anlaufen lassen (= in einen Notbetrieb bereitstellen) und die zeitkritischen Geschäftsprozesse in einem Notbetrieb durchführen und bearbeiten. Nähere Informationen können dem BSI-Standard 200-4 in Kapitel 5.1 Aufbau der BAO (R+AS) entnommen werden.

#### NOT.2.1.2 – Alarmierung

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.18

> Notfallplanung SOLLTE die Alarmierung der BAO verankern.

In einem Schadensereignis ist es entscheidend, dass die BAO schnellstmöglich alarmiert wird und somit auch schnellstmöglich Entscheidungen treffen kann. Hierzu bedarf es entsprechender vorab vorbereiteter Alarmierungspfade bzw. Pläne. Diese legen fest, wer die BAO (typischerweise zuerst den Stab und anschließend passende Teams) anhand welcher Kriterien alarmieren kann. In der Praxis haben sich hier abgestufte Verfahren etabliert, die anhand von gezielten Fragen eine Vorfilterung ermöglichen. Nähere Informationen hierzu können dem BSI-Standard 200-4 Kapitel 5.2 Detektion, Alarmierung und Eskalation (R+AS) entnommen werden.

#### NOT.2.1.3 – Stabsraum

**Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.18

> Notfallplanung KANN einen Stabsraum für den Stab installieren.

Damit der Stab der BAO im Schadensereignis handlungsfähig ist, benötigt er einen Stabsraum. Der Stabsraum kann ein Raum vor Ort oder eine virtuelle Arbeitsumgebung sein. Nähere Informationen können dem BSI-Standard 200-4 Kapitel 5.6.3 Festlegung eines Stabsraums (R+AS) entnommen werden.

#### NOT.2.1.4 – Stabsübung

**Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.1

> Notfallplanung KANN die Funktionsfähigkeit der BAO *[regelmäßig]* durch Stabsübungen überprüfen.

Da Notfälle nur selten vorkommen, die tatsächliche Funktionstüchtigkeit der BAO dann aber von großer Bedeutung für die Informationssicherheit ist, sind regelmäßige Übungen der BAO sinnvoll. Insbesondere die festgelegte Stabsstruktur (Aufgaben und Rollen), sowie das Funktionieren der Ausstattung sind im Ernstfall von großer Bedeutung. Zur Erprobung ist es zweckmäßig bei jeder Übung typische Szenarien im vollständig besetzten Stab durchzuführen und Notfallteams nur je nach passendem Szenario in die Übung einzubeziehen. Ist eine BAO erst aufgebaut worden, genügen für die Stabsübung in der Regel relativ simple Übungsszenarien wie ein Brand im Rechenzentrum oder ein Ransomware-Vorfall. Mit wachsendem Reifegrad der BAO kann anschließend die Komplexität und Realitätsnähe der Übung steigen. Nähere Informationen können dem BSI-Standard 200-4 Kapitel 13.6 Stabsübung (R+AS) entnommen werden.

## NOT.3 Notfallvorsorge

### NOT.3.1 – Wiederanlaufplan

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.18

> Notfallplanung SOLLTE einen Wiederanlaufplan für zeitkritische Systeme und Anwendungen dokumentieren.

Ein Wiederanlaufplan legt fest, wie eine ausgefallene (IT)-Ressource auf ein vorgesehenes Notbetriebsniveau innerhalb einer Wiederanlaufzeit durch Notfallteams zur Verfügung gestellt wird. Besteht ein BCMS, dann werden die kritischen Ressourcen innerhalb der Business Impact Analyse identifiziert und in dieser entsprechende Wiederanlaufzeiten festgelegt. Die ausgewählten BC-Strategien des BCMS bieten ferner den Rahmen für die Wiederanlaufplanung. Besteht kein BCMS, dann können die zeitkritischen IT-Ressourcen anhand der Schutzbedarfsfeststellung (erhöhter Schutzbedarf in der Verfügbarkeit) identifiziert werden. Die Wiederanlaufzeit kann dann nur grob anhand der Ergebnisse der Informationssicherheitseinstufung geschätzt werden. Zeitkritisch sind IT-Systeme und Anwendungen genau dann, wenn ihre fortlaufende Verfügbarkeit für die Aufrechterhaltug des Geschäftsbetriebes auch im Notfall zwingend erforderlich ist. Nähere Informationen können dem BSI-Standard 200-4 Kapitel 12 Wiederanlauf- und Wiederherstellungsplanung (AS) entnommen werden.

### NOT.3.2 – Geschäftsfortführungsplan

**Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.18

> Notfallplanung KANN einen Geschäftsfortführungsplan für zeitkritische Geschäftsprozesse dokumentieren.

Ein Geschäftsfortführungsplan (GFP) legt fest, wie ein Geschäftsprozess in einem Notfall in einem Notbetrieb durchgeführt wird. Der Notbetrieb weicht in der Regel vom Normalbetrieb ab, z.B. indem ein geringes Geschäftsniveau (Notbetriebsniveau) angesetzt wird und/oder abweichende Ressourcen eingesetzt werden. Abweichende Ressourcen könnten darin bestehen, dass ein zuvor digital unterstützter Prozess wieder analog durchgeführt wird. Geschäftsfortführungspläne liegen in der grundlegenden Verantwortung eines BCMS und sind daher im Rahmen des ISMS nur optional. Die Ausgestaltung, Planung und näheren Anforderungen der Geschäftsfortführung werden in der Regel im Rahmen des BCMS durchgeführt. Nähere Informationen können dem BSI-Standard 200-4 Kapitel 11 Geschäftsfortführungsplanung (R+AS) entnommen werden.

### NOT.3.3 – Sensibilisierung zum Vorgehen im Notfall

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.25, G 0.27, G 0.40

> Notfallplanung für Nutzende SOLLTE zur Vorgehensweise in Notfällen und Krisen sensibilisieren.

Eine Sensibilisierung für die Vorgehensweise in Notfällen und Krisen (Contingency Training) stellt sicher, dass alle zuständigen Stellen ihre Aufgaben bei einem Schadensereignis kennen. Zweckmäßig ist es, die Detailtiefe der Sensibilisierung auf die unterschiedlichen Aufgaben bei einem Schadensereignis zuzuschneiden. Beispielsweise genügt es für manche Mitarbeitenden zu wissen, welche Erreichbarkeit bei einem Schadensereignis von ihnen erwartet wird.

### NOT.3.4 – Funktionstest

**Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.18

> Notfallplanung KANN die tatsächliche Funktionstüchtigkeit von Notfallplänen *[regelmäßig]* überprüfen.

Eine regelmäßige Überprüfung hilft zu erkennen, ob die verschiedenen Notfallpläne (z. B. Wiederanlaufplan, Geschäftsfortführungsplan) und Notbetriebsressourcen tatsächlich funktionieren und die Zuständigen die Verfahrensweisen beherrschen. Mit der tatsächlichen Funktionstüchtigkeit ist gemeint, dass nicht nur die Aktualität der Pläne theoretisch betrachtet wird, sondern soweit möglich auch die konkreten Ressourcen geprüft werden (z.B. laufen die Meldewege wie vorgesehen, lassen sich Ausfallleitungen aktivieren, sind Ersatzgeräte nutzbar). Ist hierzu noch nicht die erforderliche Reife erlangt, können in einem ersten Schritt Planbesprechungen, die nur virtuell einen Plan überprüfen, eingesetzt werden. Nähere Informationen können dem BSI-Standard 200-4 Kapitel 13.9 Funktionstest (R optional +AS) und 13.5 Planbesprechung (R optional +AS) entnommen werden.

### NOT.3.5 – Ausweich-Telekommunikation

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.18

> Notfallplanung SOLLTE Ausweich-Telekommunikationsdienste verankern.

„Ausweich-Telekommunikationsdienste“ sind alternative, im Notfall nutzbare Kommunikationswege oder -infrastrukturen, die den Fortbestand kritischer Kommunikationsprozesse gewährleisten können, wenn die primären Dienste kompromittiert oder ausgefallen sind (out-of-band communication). Der Sinn und Zweck der Regelung liegt nicht nur darin, den Informationsaustausch kritischer Geschäftsprozesse im Notfall sicherzustellen, sondern dient auch der sicherheitsbezogenen Koordination und Entscheidungsfindung bei schwerwiegenden Störungen oder Angriffen, etwa bei Ausfällen von Festnetz- oder VoIP-Diensten durch technische Defekte, Naturereignisse oder Cyberangriffe. Eine unzureichende Vorsorge könnte dazu führen, dass im Krisenfall keine Lageabstimmung, Notfallkommunikation oder Meldung an Sicherheitsbehörden möglich ist, oder dass Angreifer die eingeleiteten Gegenmaßnahmen über bereits kompromittierte Dienste mitlesen. Ausweich-Telekommunikationsdienste können z.B. über den Anschluss anderer Anbieter, Mobilfunk oder Satellitenanschlüsse umgesetzt werden. Hierbei ist sowohl an den Netzanschluss kritischer IT-Systeme als auch an die Erreichbarkeit der im Notfall zuständigen Mitarbeiter und Dienstleister zu denken.

### NOT.3.6 – Sicherheitsmechanismen

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.18

> Notfallplanung SOLLTE alternative Sicherheitsmechanismen , die in Notfällen greifen, verankern.

In Notfällen besteht das Risiko, dass manche Sicherheitsvorkehrungen nicht zur Verfügung stehen. Alternative oder ergänzende Sicherheitsvorkehrungen können in Notfällen helfen die Balance zwischen Vertraulichkeit, Integrität und Verfügbarkeit aufrechtzuerhalten (z.B. Einmalpasswörter, die in einem Safe hinterlegt werden). Hierbei ist insbesondere daran zu denken, dass alternative Sicherheitsvorkehrungen nicht die im Normalbetrieb verwendeten Sicherheitsvorkehrungen untergraben.

## NOT.4 Datensicherung

### NOT.4.1 – Dokumentation der Quellen

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.45, G 0.18, G 0.25, G 0.37

> Notfallplanung SOLLTE die zu sichernden Daten dokumentieren.

Datensicherungen dienen der Wiederherstellung von Daten nach Vorfällen. Aufgrund der besonderen Bedeutung fordert auch die ISO/IEC 27001 die Sicherung von Informationen in Übereinstimmung mit themenspezifischen Regelungen zur Datensicherung. Hierzu gehört die Regelung, welche Daten konkret gesichert werden (Quellen, Kategorien oder Klassifikation der Daten, Umfang). Relevant sind dabei auch Daten, die bei Dienstleistern oder in der Cloud aufbewahrt werden. Die Datensicherung kann auch durch die Sicherung ganzer IT-Systeme, Datenträger oder Netzlaufwerke umgesetzt werden. Es empfiehlt sich auch zu prüfen, wie die Institution ihre Daten, welche bei einem Outsourcing Dienstleister liegen, sichern will. Es ist möglich eine Datensicherung durch den Dienstleister oder auch bei sich selbst zu erstellen.

### NOT.4.2 – Sicherung des Systems

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39, G 0.25

> Notfallplanung für IT-Systeme SOLLTE deren Datensicherung *[regelmäßig]* ausführen.

Zu den erforderlichen Daten können z.B. Konfigurationsdateien des Betriebssystems, Firmware, Lizenzen, Treiber und die Systemdokumentation gehören. Bei gleichartigen Systemen kann die Anforderung auch durch die Sicherung einer Kopie erfolgen, wenn mit dieser alle IT-Systeme dieser Art funktionsfähig wiederhergestellt werden können. Die Anforderung kann auch durch die Wiederherstellung aus einem Versionskontrollsystem erfolgen.

### NOT.4.3 – Sicherung der Anwendung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39, G 0.25

> Notfallplanung für Anwendungen SOLLTE deren Datensicherung *[regelmäßig]* ausführen.

Hierzu können z.B. sowohl die Daten einer Backend-Datenbank, als auch Konfigurationsdateien oder Sicherheitseinstellungen gehören. Bei einer Verzeichnisdatenbank z.B. sind typischerweise sowohl die eigentlichen Verzeichniseinträge wie Benutzer & Gruppenzugehörigkeiten, als auch Metadaten wie Benutzerattribute, Gruppenrichtlinien und Informationen zur Integration von Drittdiensten erforderlich, um die Verzeichnisdatenbank funktionsfähig wiederherzustellen.

### NOT.4.4 – Automatische Datensicherung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39

> Notfallplanung für Daten SOLLTE die Datensicherung durch *[einen automatisierten Mechanismus]* ausführen.

Ein automatisierter Mechanismus (engl. automated mechanism) ist hier ein technisches Verfahren, das ohne manuelles Zutun in festgelegten Intervallen oder bei bestimmten Ereignissen Sicherungskopien von Daten erstellt und dokumentiert. Er kann z. B. über Skripte, Backup-Software oder systemeigene Dienste umgesetzt werden, die regelmäßig und zuverlässig ausgeführt werden. Der Zweck solcher Mechanismen liegt darin, menschliche Fehlerquellen und Auslassungen zu vermeiden, denn eine manuelle Sicherung könnte in Stresssituationen übersehen werden oder unvollständig sein. Die Vorgabe kann so verhindern, dass im Falle von Schadsoftwarebefall oder Hardwareausfall kritische Daten unwiederbringlich verloren gehen, und sie kann eine schnelle Wiederherstellung der Arbeitsfähigkeit nach einem Vorfall ermöglichen. Ohne Automatisierung könnte eine Institution etwa nach einem Ransomware-Angriff feststellen, dass keine aktuelle Sicherung vorliegt. Die Anforderung ist auch dann erfüllt, wenn zusätzlich manuelle Datensicherungen durchgeführt werden.

### NOT.4.5 – Archivierung langfristig benötigter Daten

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.45, G 0.39

> Notfallplanung für Daten SOLLTE die Archivierung langfristig benötigter Daten *[regelmäßig]* ausführen.

Archivierung meint hier die langfristige Aufbewahrung derjenigen Daten, die über längere Zeit benötigt werden, z.B. als Nachweis der Einhaltung rechtlicher Verpflichtungen oder zur Geltendmachung von Ansprüchen. Dabei kann es sich sowohl um analoge Dokumente als auch um digitale Daten handeln. Die meisten Institutionen verarbeiten Daten, die aufgrund von Compliance-Verpflichtungen langfristig gespeichert werden, z.B. handels- und steuerrechtlich relevante Dokumente oder Eigentumsurkunden. Langfristige Daten könnten durch technische Änderungen oder Vorfälle verloren gehen. Zur Umsetzung siehe BSI TR-03125. Sind keine Daten langfristig (z.B. über mehr als 10 Jahre) erforderlich, so ist die Anforderung entbehrlich. Es empfiehlt sich darüber hinaus ein verlustfreies Bildkompressionsverfahren zu nutzen, um eine beweis- und revisionssichere Archivierung zu gewährleisten.

#### NOT.4.5.1 – Zum Archiv gehörende Assets

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.45, G 0.39, G 0.25

> Notfallplanung für Daten SOLLTE die Archivierung von Assets, die zur Verwendung von archivierten Daten erforderlich sind, *[regelmäßig]* ausführen.

Je nach Art der Daten können zu deren Nutzung z.B. bestimmte (physische oder virtuelle) Assets wie Systeme oder Anwendungen erforderlich sein, z.B. bestimmte Datenbankversionen, kompatible Betriebssysteme und Lizenzen, Anwendungen zur kryptographischen Entschlüsselung der Daten, Konfigurationsdateien oder Betriebsparameter. Wenn Daten für eine lange Zeit aufbewahrt werden, könnte es vorkommen, dass sie nicht mehr lesbar und reproduzierbar sind, weil diese Assets nicht mehr existieren und auch nicht mehr beschafft werden können.

#### NOT.4.5.2 – Zum Archiv gehörende Dokumentation

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.45, G 0.39, G 0.18, G 0.37

> Notfallplanung für Daten SOLLTE die Archivierung von Dokumentationen, die zur Verwendung von archivierten Daten erforderlich sind, *[regelmäßig]* ausführen.

Hierbei geht es darum, nicht nur die Daten selbst, sondern auch alle begleitenden Informationen („metadata“ oder „supporting documentation“) regelmäßig zu sichern, um deren spätere Nutzbarkeit zu gewährleisten. Dokumentationen sind in diesem Zusammenhang beispielsweise Bedienungsanleitungen, technische Spezifikationen, Konfigurationsdateien oder Verfahrensanweisungen, die notwendig sind, um archivierte Daten auch nach Jahren noch korrekt zu interpretieren oder wiederherzustellen. Die Frequenz ist dabei abhängig von der Kritikalität der Daten und der Änderungsfrequenz der begleitenden Dokumente. Ohne solche begleitenden Unterlagen könnte ein Datenbestand zwar vorliegen, aber praktisch unbrauchbar sein, da die nötigen Kontexte oder technischen Details fehlen.

### NOT.4.6 – Geschützte Aufbewahrung

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.45, G 0.39, G 0.25, G 0.1, G 0.3

> Notfallplanung SOLLTE eine geschützte Aufbewahrung von Datensicherungen verankern.

Eine geschützte Aufbewahrung von Datensicherungen bedeutet, dass Sicherungskopien nicht nur vorhanden sind, sondern auch vor Verlust, Manipulation, versehentlicher Löschung oder unbefugtem Zugriff bewahrt werden. Dabei wird berücksichtigt, dass Datensicherungen häufig ein attraktives Ziel für Angriffe darstellen und gleichzeitig im Notfall die einzige Möglichkeit zur Wiederherstellung von Systemen und Daten sein können. Beispiele für Schutzmaßnahmen sind die Ablage von Sicherungsmedien in feuer- und wasserfesten Tresoren, die Nutzung getrennter Räumlichkeiten oder externer Rechenzentren mit physischen Sicherheitsvorkehrungen sowie die Verschlüsselung von Backups, wenn diese an externen Standorten oder in Cloud-Umgebungen gespeichert werden. Auch organisatorische Maßnahmen wie eine klare Regelung, wer Zugriff auf die Sicherungen erhält, tragen zum Schutz bei.

### NOT.4.7 – Versionierte Datensicherung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39

> Notfallplanung SOLLTE eine Versionierung der Datensicherung verankern.

Versionierung ist die Aufbewahrung nach Zeitpunkten getrennter Versionen der Datensicherung, um auch Daten wiederherstellen zu können, die in der letzten Sicherung bereits gelöscht waren. Bewährt hat sich eine Aufbewahrung von je drei Versionen für die letzten Stunden, dann Tage, dann Wochen, dann Monate – soweit nach Compliance-Anforderungen (z.B. Datenschutz) möglich.

### NOT.4.8 – Verschlüsselte Datensicherung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39, G 0.25, G 0.19

> Notfallplanung SOLLTE die Datensicherung durch *[einen anerkannten kryptographischen Algorithmus]* verschlüsseln.

Die Datensicherung enthält typischerweise eine große Menge schützenswerter Daten. Durch Verschlüsselung wird die Vertraulichkeit und Integrität geschützter Informationen auch nach einem schwerwiegenden Vorfall gewährleistet. Dies kann besonders bei einem Datenleck (engl. Data Breach) oder Diebstahl von Speichermedien helfen, da die Offenlegung sensibler Daten selbst bei unbefugtem Zugriff verhindert werden kann. Für anerkannte Algorithmen siehe BSI TR-02102. Technisch kann die Festplattenverschlüsselung auf dem Sicherungsspeicher (Disk Encryption) genutzt werden, aber auch die dateibasierte Verschlüsselung jedes einzelnen Sicherungs-Archives. Wichtig ist es, dabei auch auf die Verwaltung der kryptographischen Schlüssel (Key Management) zu achten, damit diese weder einem unbeugten Zugriff ausgesetzt sind, noch der Zugriff auf die Datensicherung im Ernstfall durch fehlende Zugangsdaten unmöglich wird.

### NOT.4.9 – Speichermedien

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39, G 0.25

> Notfallplanung SOLLTE dedizierte Speichermedien, die für den festgelegten Aufbewahrungszeitraum geeignet sind, installieren.

Dedizierte Speichermedien (engl. dedicated storage media) sind physische oder virtuelle Datenträger, die ausschließlich für Sicherungs- oder Wiederherstellungszwecke genutzt werden und nicht mit produktiven Systemen vermischt sind. Der festgelegte Aufbewahrungszeitraum (engl. retention period) bezeichnet den Zeitraum, in dem gespeicherte Sicherungen oder Kopien revisionssicher und lesbar verfügbar bleiben sollen, beispielsweise mehrere Monate für kurzfristige Recovery-Szenarien oder mehrere Jahre zur Abdeckung regulatorischer Anforderungen. Die Vorschrift zielt darauf ab, dass im Notfall tatsächlich auf funktionierende und vollständige Sicherungen zurückgegriffen werden kann; sie adressiert Risiken wie, dass Daten im Ernstfall durch unzuverlässige oder beschädigte Medien unbrauchbar sein könnten, oder dass durch unzureichende Haltbarkeit von Speichermedien eine Wiederherstellung scheitern könnte. Je nach Zeitraum und Platzbedarf bieten sich z.B. solider Festspeicher, Festplatten, Magnetbänder oder Cloudspeicher an. Bei der Nutzung von Cloudspeichern sind allerdings auch die zusätzlichen Anforderungen an Cloud-Dienste zu berücksichtigen.

### NOT.4.10 – Getrennte Aufbewahrung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39, G 0.1, G 0.25

> Notfallplanung SOLLTE die Datensicherung getrennt von den Originaldaten platzieren.

Originaldaten (engl. primary data) sind die produktiven oder operativen Daten, die unmittelbar für die laufenden Geschäftsprozesse verwendet werden. Die Anforderung adressiert damit, dass Kopien oder Sicherungen nicht am gleichen Ort wie die produktiven Systeme und deren Speicher verbleiben. Hintergrund ist, dass ein Vorfall wie ein Brand, ein Wasserschaden oder ein gezielter Einbruch gleichzeitig sowohl die produktiven Systeme als auch die dort aufbewahrten Sicherungen betreffen könnte, wodurch eine Wiederherstellung unmöglich wäre. Die physische Trennung kann dagegen die Verfügbarkeit und Wiederanlaufbarkeit der Daten nach einem Schadensereignis sicherstellen. Die Anforderung gilt auch für die Aufbewahrung bei Cloud-Diensten: Eine Aufbewahrung der Datensicherung bei einem Dienstleister, bei dem auch die Originaldaten liegen, erfüllt die Anforderung NICHT. Bei der getrennten Aufbewahrung von Datensicherung sind häufig praktische und sicherheitsrelevante Herausforderungen zu beachten: Ein ausgelagerter Speicherort ist in gleichem Maße schutzbedürftig gegenüber unbefugtem Zugriff wie der Standort der Originaldaten, da sich darauf oft vollständige und aktuelle Kopien sensibler Informationen befinden. Zudem sind längere Wiederanlaufzeiten möglich, wenn der externe Standort nicht unmittelbar erreichbar ist oder wenn logistische Verzögerungen beim Zugriff auf die ausgelagerten Datenträger auftreten. Auch die Gefahr von Inkonsistenzen steigt, wenn Backups zwar ausgelagert, aber nicht regelmäßig synchronisiert oder bei der Überprüfung beachtet werden.

### NOT.4.11 – Datenträgerarchiv

**Stufe:** `normal-SdT` · **Aufwand:** 4 · **Gefährdungen:** G 0.45, G 0.39, G 0.1

> Notfallplanung SOLLTE ein Datenträgerarchiv installieren.

Datenträgerarchive sind verschlossene Räume, die dediziert zur langfristigen Aufbewahrung von Datenträgern bestimmt sind. Die Anforderung gilt auch dann als umgesetzt, wenn zusätzlich zur Datensicherung im Datenträgerarchiv auch noch Kopien existieren, die nicht im Datenträgerarchiv aufbewahrt werden. Ein wesentlicher Mehrwert von Datenträgerarchiven ist die geschützte Aufbewahrung. Daher zählt ein Datenträgerarchiv nur dann als Mehrwert, wenn das Archiv sich auch in einem anderen Brandabschnitt befindet als die Originaldaten.

### NOT.4.12 – Georedundanz

**Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.39, G 0.5, G 0.6, G 0.7, G 0.45

> Notfallplanung KANN die georedundante Aufbewahrung mindestens einer Kopie der Datensicherung verankern.

Werden Datensicherungen in der Nähe von Originaldaten aufbewahrt, so könnten beide von Elementaren Gefährdungen wie Überflutungen betroffen sein. Georedundant bedeutet in der Regel 200km Luftlinie oder mehr von den Originaldaten entfernt. Details siehe BSI Kriterien für die Standortwahl von Rechenzentren. Die Anforderung kann auch durch die gegenseitige Aufbewahrung in georedundanten Rechenzentren erfüllt werden.

### NOT.4.13 – Datensouveränität

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39, G 0.25

> Notfallplanung für Outsourcing SOLLTE die Datensicherung von Daten, die bei einem Dienstleister verarbeitet werden, nach *[einem anerkannten Standard]* *[regelmäßig]* ausführen.

Dies dient dazu bei einem Ausfall des Dienstleisters die Daten schnell bei einem anderen Dienstleister oder intern weiterverwenden zu können (Interoperabilität in der Exitstrategie). Anerkannt ist hier ein Format, welches auch bei einem anderen Dienstleister verwendet werden kann. Mögliche anerkannte Standards zum Datenaustausch sind z.B. XML, JSON, YAML, CSV, ODF. Eine Sicherungskopie ist unter eigener Hoheit, wenn sie auf Datenträgern im Besitz der Institution aufbewahrt wird, über die dieser Dienstleister keine Kontrolle hat. Relevant sind dabei auch Konfigurationsdateien, Programmcode und Dokumentationen, die zur Verwendung der Daten erforderlich sind.

### NOT.4.14 – Offline-Kopie

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39, G 0.25, G 0.1

> Notfallplanung für Daten SOLLTE eine Offline-Kopie *[regelmäßig]* ausführen.

Eine Offline-Kopie ist eine Datensicherung, die physisch oder logisch von produktiven Systemen und dem laufenden Netzwerk getrennt ist („offline backup“ oder „air-gapped backup“). „Regelmäßig“ bedeutet, dass die Institution in Abhängigkeit von Verfügbarkeit und Kritikalität ihrer Daten feste Intervalle definiert, beispielsweise täglich, wöchentlich oder monatlich. Der Sinn und Zweck dieser Vorgabe liegt darin, sicherzustellen, dass im Falle von Schadsoftwarebefall oder gezielten Angriffen keine gleichzeitige Kompromittierung aller Sicherungskopien stattfinden kann; ein Angriff könnte sonst auch Backups verschlüsseln oder löschen. Eine Offline-Kopie kann dagegen die Wiederherstellung kritischer Systeme nach einem Ransomware-Angriff oder auch nach einem physischen Ausfall, etwa durch Stromschaden oder Brand, unterstützen. Eine Institution kann dies umsetzen, indem sie (1) Kopien in Papierform oder auf wechselbaren Medien wie externen Festplatten, RDX-Kassetten oder Bändern erstellt, die nach dem Backup-Vorgang vom Netzwerk getrennt und geschützt aufbewahrt werden, (2) Cloud-Backups so konfiguriert, dass sie durch Write-Once-Read-Many-(WORM)-Speicher geschützt und logisch von aktiven Systemen isoliert sind, oder (3) eine Rotation von Datenträgern einführt, bei der Kopien an einem separaten, physischen Standort verwahrt werden.

### NOT.4.15 – Vorgehen zur Wiederherstellung

**Stufe:** `normal-SdT` · **Aufwand:** 2 · **Gefährdungen:** G 0.45, G 0.39, G 0.25

> Notfallplanung SOLLTE die Vorgehensweise zur Wiederherstellung dokumentieren.

Die Dokumentation der Vorgehensweise zur Wiederherstellung dient dazu, im Notfall eine schnelle und geordnete Wiederinbetriebnahme von IT-Systemen und Daten zu ermöglichen. Ohne eine klare Beschreibung der Abläufe kann es zu Verzögerungen, Fehlern oder widersprüchlichen Handlungen kommen, was die Wiederherstellung erheblich erschwert. In einer solchen Dokumentation werden beispielsweise die Reihenfolge der Wiederherstellung kritischer Systeme, die benötigten Datensicherungen und Speicherorte, die erforderlichen Werkzeuge sowie die zuständigen Rollen und Kontaktwege beschrieben. Ergänzend kann auch festgehalten werden, wie die Funktionsfähigkeit nach der Wiederherstellung überprüft wird. Einfache Beispiele sind Schritt-für-Schritt-Anleitungen für die Rücksicherung bestimmter Anwendungen oder Checklisten, die während des Wiederherstellungsprozesses abgearbeitet werden.

### NOT.4.16 – Test der Datensicherung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39

> Notfallplanung für Daten SOLLTE den Erfolg der Datensicherung *[regelmäßig]* überprüfen.

Die Überprüfung der Vollständigkeit kann durch Statistiken des Datenumfangs plus Stichproben der Daten durchgeführt werden. Ein Integritätstest prüft, ob die gesicherten Daten ohne Änderungen im Vergleich zum Original vorliegen. Hierzu können je nach Daten auch Berechtigungen und Metadaten gehören, wenn diese für die Rücksicherung erforderlich sind (z.B. Wiederherstellung eines Laufwerks mit Ordnern die verschiedene Zugriffsberechtigungen haben).

#### NOT.4.16.1 – Test der Wiederherstellung

**Stufe:** `normal-SdT` · **Aufwand:** 3 · **Gefährdungen:** G 0.45, G 0.39, G 0.25

> Notfallplanung für Daten SOLLTE die Wiederherstellung mindestens anhand von repräsentativen Stichproben *[regelmäßig]* überprüfen.

Unter „Erfolg der Datensicherung“ ist hier die Vollständigkeit („completeness“) und Integrität („integrity“) der erstellten Backups zu verstehen. Eine fehlerhafte oder unvollständige Sicherung könnte unbemerkt bleiben, wenn nicht aktiv geprüft wird, während eine gezielte Validierung die Sicherheit bietet, dass sich die Daten bei Bedarf in unveränderter Form vorfinden lassen. Damit kann ein gravierender Datenverlust, etwa durch korrupte Sicherungsdateien oder abgebrochene Backup-Jobs, rechtzeitig erkannt und behoben werden. Die Anforderung zielt darauf ab, Risiken durch Scheinsicherheit zu reduzieren – etwa wenn Backup-Prozesse zwar automatisiert laufen, aber unbemerkt leere, fehlerhafte oder inkonsistente Datenbestände erzeugen könnten. Durch eine regelmäßige Überprüfung kann die Institution sicherstellen, dass die gesicherten Daten tatsächlich verwendbar bleiben, und damit das Risiko von Ausfallzeiten oder irreversiblen Informationsverlusten verringern. Konkret umgesetzt werden kann dies z. B., indem (1) Backup-Logs automatisch auf Fehlermeldungen oder Warnungen geprüft werden, (2) Prüfsummenverfahren wie Hashes (z. B. SHA-256) zur Integritätskontrolle eingesetzt werden und (3) stichprobenartige Vergleiche zwischen gesicherten und Originaldateien durchgeführt werden. Die Stichprobe kann sich dabei entweder auf die Wiederherstellung selber (= Wiederherstellung nur einiger Daten) als auch auf den deren Überprüfung (= Öffnen nur einiger Daten) beziehen. Stichproben sind repräsentativ, wenn die Zusammensetzung der Stichprobe von Test zu Test geändert wird und die Wahrscheinlichkeit der Stichprobenauswahl auch der Bedeutung der Daten entspricht. Zweckmäßig ist es dazu, bei der Stichprobenauswahl den Schutzbedarf der Daten zu berücksichtigen: Für besonders wichtige Systeme wie Verzeichnisdienste und für den Geschäftsbetrieb unerlässliche Daten ist eine häufigere Überprüfung erforderlich als für Daten und Systeme, auf die im Notfall auch verzichtet werden kann. Die Anforderung ist auch erfüllt, wenn statt einer Stichprobe eine vollständige Wiederherstellung vorgenommen und geprüft wird. Die Anforderung ist auch dann erfüllt, wenn die Überprüfung durch aktive Verwendung der Daten nach einer Wiederherstellung erfolgt (z.B. durch Inbetriebnahme neuer Server-Container, die aus einer versionierten Datensicherung automatisch angelegt werden).

### NOT.4.17 – Anwendungstest

**Stufe:** `erhöht` · **Aufwand:** 5 · **Gefährdungen:** G 0.45, G 0.39, G 0.25

> Notfallplanung für Anwendungen KANN deren Funktionsfähigkeit nach Wiederherstellung *[regelmäßig]* überprüfen.

Diese Anforderung zielt darauf ab, die Disaster-Recovery-Fähigkeiten einer Anwendung insgesamt zu gewährleisten. Durch regelmäßige Tests der Wiederherstellung aus Backups wird sichergestellt, dass im Ernstfall (Systemausfall, Datenverlust, Cyberangriff) eine funktionierende Wiederherstellung möglich ist. Dabei wird nicht nur die bloße Wiederherstellung getestet, sondern auch die Funktionalität der wiederhergestellten Anwendung verifiziert – inklusive Datenintegrität und korrekte Übernahme der Konfiguration.
