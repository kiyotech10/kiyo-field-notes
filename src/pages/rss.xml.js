import { getCollection } from 'astro:content';
import rss from '@astrojs/rss';
import { SITE_DESCRIPTION, SITE_TITLE } from '../consts';

export async function GET(context) {
	const [diary, english, study, reading, nursing, lifehack] = await Promise.all([
		getCollection('diary'),
		getCollection('english'),
		getCollection('study'),
		getCollection('reading'),
		getCollection('nursing'),
		getCollection('lifehack'),
	]);

	const allPosts = [
		...diary.map((p) => ({ ...p, category: 'diary' })),
		...english.map((p) => ({ ...p, category: 'english' })),
		...study.map((p) => ({ ...p, category: 'study' })),
		...reading.map((p) => ({ ...p, category: 'reading' })),
		...nursing.map((p) => ({ ...p, category: 'nursing' })),
		...lifehack.map((p) => ({ ...p, category: 'lifehack' })),
	].sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

	return rss({
		title: SITE_TITLE,
		description: SITE_DESCRIPTION,
		site: context.site,
		items: allPosts.map((post) => ({
			...post.data,
			link: `/${post.category}/${post.id}/`,
		})),
	});
}
