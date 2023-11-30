import prisma from '$lib/prisma';
import type { Prisma } from '@prisma/client';
import { fail, type Actions, redirect } from '@sveltejs/kit';
import type { ServerLoad } from '@sveltejs/kit';
import jwt from 'jsonwebtoken';
import z from 'zod';

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
	async register({ cookies, request }) {
		const formData = await request.formData();

		if (formData.get('password') !== formData.get('confirm-password'))
			return fail(400, {
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
			return fail(400, {
				error: 'Dein Account konnte nicht angelegt werden, bitte überprüfe deine Eingaben.'
			});

		user = form.data;

		user.password = await Bun.password.hash(user.password, {
			algorithm: 'bcrypt',
			cost: 10
		});

		user = await prisma.user.create({
			data: user
		});

		if (!user)
			return fail(400, {
				error: 'Dein Account konnte nicht angelegt werden, bitte überprüfe deine Eingaben.'
			});

		type UserWithourPassword = Omit<Prisma.UserCreateInput, 'password'>;
		const jwtData: UserWithourPassword = user as UserWithourPassword;

		if (!process.env.JWT_SECRET || !jwtData) {
			return fail(500, {
				error: 'Server Fehler: Der Account wurde erfolgreich angelegt. Bitte melde dich manuell an.'
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
