// Text (und optional formatierten Text) in die Zwischenablage legen, mit Rueckfallstufen.
//
// Warum Stufen: Browser und Seiten-Kontext verhalten sich verschieden. `navigator.clipboard` gibt es
// nur in sicheren Kontexten und braucht eine Nutzeraktion, `ClipboardItem` mit zwei Formaten ist nicht
// ueberall gleich verfuegbar, und aeltere Browser kennen nur `execCommand('copy')`. Der Rueckgabewert
// sagt ehrlich, was tatsaechlich passiert ist, damit die Seite nichts Falsches meldet.

export type CopyResult =
	// Text UND formatierter Text liegen in der Zwischenablage (wer einfuegt, bekommt je nach Ziel das eine oder das andere)
	| 'rich'
	// nur Text (so gewollt, oder der Browser kann kein formatiertes Kopieren)
	| 'text'
	// nur ueber den alten Weg (execCommand) kopiert
	| 'fallback'
	// nichts kopiert: die Seite sagt es und verweist auf den Download
	| 'failed';

type ClipboardApi = {
	write?: (items: unknown[]) => Promise<void>;
	writeText?: (text: string) => Promise<void>;
};

export async function copyToClipboard(text: string, html?: string): Promise<CopyResult> {
	const api = (typeof navigator !== 'undefined' ? navigator.clipboard : undefined) as ClipboardApi | undefined;
	const Item = (globalThis as { ClipboardItem?: new (data: Record<string, Blob>) => unknown }).ClipboardItem;

	if (html && api?.write && Item) {
		try {
			await api.write([
				new Item({
					'text/plain': new Blob([text], { type: 'text/plain' }),
					'text/html': new Blob([html], { type: 'text/html' }),
				}),
			]);
			return 'rich';
		} catch {
			// weiter mit der naechsten Stufe: einige Browser lehnen ClipboardItem ab, erlauben aber writeText
		}
	}
	if (api?.writeText) {
		try {
			await api.writeText(text);
			return 'text';
		} catch {
			// weiter mit dem alten Weg
		}
	}
	try {
		const area = document.createElement('textarea');
		area.value = text;
		area.setAttribute('readonly', '');
		area.style.cssText = 'position:fixed;top:0;left:0;opacity:0;pointer-events:none';
		document.body.appendChild(area);
		area.select();
		const ok = document.execCommand('copy');
		area.remove();
		return ok ? 'fallback' : 'failed';
	} catch {
		return 'failed';
	}
}
