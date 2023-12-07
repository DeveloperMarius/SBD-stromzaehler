import prisma from '$lib/prisma';
import type { Prisma } from '@prisma/client';
import { fail, type Actions, redirect } from '@sveltejs/kit';
import type { ServerLoad } from '@sveltejs/kit';
import jwt from 'jsonwebtoken';
import z from 'zod';
import bcrypt from 'bcrypt';

export const load: ServerLoad = async ({ cookies }) => {
	const token = cookies.get('token');

	try {
		if (token && process.env.JWT_SECRET && jwt.verify(token, process.env.JWT_SECRET)) {
			throw redirect(302, `/dashboard`);
		}
	} catch (error) {
		console.error(error);
	}

	return {
		status: 200
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
			return fail(400, {
				error: 'Bitte überprüfe deine Eingaben.'
			});

		const user = await prisma.user.findUnique({
			where: {
				email: formUser.data.email
			}
		});

		if (!user || !(await bcrypt.compare(formUser.data.password, user.password))) {
			return fail(400, {
				error: 'Anmeldung fehlgeschlagen, bitte überprüfe deine Eingaben.'
			});
		}

		type UserWithourPassword = Omit<Prisma.UserCreateInput, 'password'>;
		const jwtData: UserWithourPassword = user as UserWithourPassword;

		if (!process.env.JWT_SECRET || !jwtData) {
			return fail(500, {
				error: 'Server Fehler: Anmeldevorgang fehlgeschlagen.'
			});
		}

		const token = jwt.sign(jwtData, process.env.JWT_SECRET, { expiresIn: '12h' });

		cookies.set('token', token, {
			path: '/',
			maxAge: 60 * 60 * 12,
			sameSite: 'lax'
		});

		throw redirect(302, `/dashboard`);
	}
};
