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
	async login({ cookies, request }) {
		const formData = await request.formData();

		const formUser = z
			.object({
				email: z.string().email(),
				password: z.string().min(8)
			})
			.safeParse(Object.fromEntries(formData));

		if (!formUser.success)
			return fail(422, {
				error: 'Bitte überprüfe deine Eingaben.'
			});

		const user = await prisma.user.findUnique({
			where: {
				email: formUser.data.email
			}
		});

		if (!user) {
			return fail(422, {
				error: 'Anmeldung fehlgeschlagen, Nutzername oder Passwort falsch.'
			});
		}

		try {
			!argon2.verify(user.password, formUser.data.password);
		} catch (error) {
			return fail(422, {
				error: 'Anmeldung fehlgeschlagen, Nutzername oder Passwort falsch.'
			});
		}

		type UserWithourPassword = Omit<Prisma.UserCreateInput, 'password'>;
		const jwtData: UserWithourPassword = user as UserWithourPassword;

		if (!env.JWT_SECRET || !jwtData) {
			return fail(500, {
				error: 'Server Fehler: Anmeldevorgang fehlgeschlagen.'
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
