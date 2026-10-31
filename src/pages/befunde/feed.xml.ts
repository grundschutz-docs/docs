import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { befundeFeed, type Befund } from '../../lib/feed';

export const GET: APIRoute = async ({ site }) => {
	const eintraege = await getCollection('docs', (e) => e.id.startsWith('befunde/') && e.data.befund);
	const befunde: Befund[] = eintraege.map((e) => ({
		slug: e.id.replace('befunde/', ''),
		titel: e.data.title,
		beschreibung: e.data.description ?? '',
		...e.data.befund!,
	}));
	return new Response(befundeFeed(befunde, site!.href), {
		headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' },
	});
};
