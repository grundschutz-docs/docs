import type { APIRoute } from 'astro';
import data from '../../data/changelog.json';
import { changelogFeed, type Eintrag } from '../../lib/feed';

export const GET: APIRoute = ({ site }) =>
	new Response(changelogFeed(data.eintraege as unknown as Eintrag[], site!.href), {
		headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' },
	});
