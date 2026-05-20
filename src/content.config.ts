import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const postSchema = ({ image }: { image: () => z.ZodType }) =>
	z.object({
		title: z.string(),
		description: z.string(),
		pubDate: z.coerce.date(),
		updatedDate: z.coerce.date().optional(),
		heroImage: z.optional(image()),
		featured: z.boolean().optional(),
		tags: z.array(z.string()).optional(),
	});

const diary = defineCollection({
	loader: glob({ base: './src/content/diary', pattern: '**/*.{md,mdx}' }),
	schema: postSchema,
});

const english = defineCollection({
	loader: glob({ base: './src/content/english', pattern: '**/*.{md,mdx}' }),
	schema: postSchema,
});

const study = defineCollection({
	loader: glob({ base: './src/content/study', pattern: '**/*.{md,mdx}' }),
	schema: postSchema,
});

const reading = defineCollection({
	loader: glob({ base: './src/content/reading', pattern: '**/*.{md,mdx}' }),
	schema: postSchema,
});

const lifehack = defineCollection({
	loader: glob({ base: './src/content/lifehack', pattern: '**/*.{md,mdx}' }),
	schema: postSchema,
});

const nursing = defineCollection({
	loader: glob({ base: './src/content/nursing', pattern: '**/*.{md,mdx}' }),
	schema: postSchema,
});

export const collections = { diary, english, study, reading, nursing, lifehack };
