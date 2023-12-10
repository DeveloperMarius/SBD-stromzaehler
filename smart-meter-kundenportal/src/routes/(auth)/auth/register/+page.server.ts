import prisma from '$lib/prisma';
import type { Prisma } from '@prisma/client';
import { fail, type Actions } from '@sveltejs/kit';
import type { ServerLoad } from '@sveltejs/kit';
import jwt from 'jsonwebtoken';
import z from 'zod';
import argon2 from 'argon2';
import { env } from '$env/dynamic/private';

export const load: ServerLoad = async ({ cookies }) => {
	const token = cookies.get('token');
	let loggedIn = false;

	if (token && env.JWT_SECRET && jwt.verify(token, env.JWT_SECRET)) {
		loggedIn = true;
	}

	return {
		status: 200,
		loggedIn: loggedIn
	};
};

export const actions: Actions = {
	async register({ cookies, request }) {
		const formData = await request.formData();

		if (formData.get('password') !== formData.get('confirm-password'))
			return fail(422, {
				error: 'Dein Account konnte nicht angelegt werden, die Passwörter stimmen nicht überein.'
			});

		let user: Prisma.UserCreateInput = {} as Prisma.UserCreateInput;

		const form = z
			.object({
				vorname: z.string().min(3),
				nachname: z.string().min(3),
				email: z.string().email(),
				password: z.string().min(8),
				hausnr: z.string().min(1),
				plz: z.string().min(5).max(5),
				ort: z.string().min(1).max(50),
				strasse: z.string().min(2),
				telefon: z.string().min(2)
			})
			.safeParse({
				vorname: formData.get('vorname')?.toString() ?? '',
				nachname: formData.get('nachname')?.toString() ?? '',
				email: formData.get('email')?.toString() ?? '',
				password: formData.get('password')?.toString() ?? '',
				hausnr: formData.get('hausnr')?.toString() ?? '',
				plz: formData.get('plz')?.toString() ?? '',
				ort: formData.get('ort')?.toString() ?? '',
				strasse: formData.get('strasse')?.toString() ?? '',
				telefon: formData.get('telefon')?.toString() ?? ''
			});

		if (!form.success)
			return fail(422, {
				error: 'Dein Account konnte nicht angelegt werden: Bitte überprüfe deine Eingaben.'
			});

		user = form.data;

		user.password = await argon2.hash(user.password);

		user = await prisma.user.create({
			data: user
		});

		if (!user)
			return fail(500, {
				error: 'Dein Account konnte nicht angelegt werden: Fehler mit der Datenbank.'
			});

		type UserWithourPassword = Omit<Prisma.UserCreateInput, 'password'>;
		const jwtData: UserWithourPassword = user as UserWithourPassword;

		if (!env.JWT_SECRET || !jwtData) {
			return fail(500, {
				error: 'Server Fehler: Der Account wurde erfolgreich angelegt. Bitte melde dich manuell an.'
			});
		}

		const token = jwt.sign(jwtData, env.JWT_SECRET, { expiresIn: '12h' });

		cookies.set('token', token, {
			path: '/',
			maxAge: 60 * 60 * 12,
			sameSite: 'lax'
		});
	}
};
