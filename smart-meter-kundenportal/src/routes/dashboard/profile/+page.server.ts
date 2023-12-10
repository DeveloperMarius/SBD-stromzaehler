import jwt from 'jsonwebtoken';
import { auth_guard, type AuthGuardOutput } from '$lib/auth.server';
import prisma from '$lib/prisma';
import { redirect, type Actions, type ServerLoad, fail } from '@sveltejs/kit';
import { z } from 'zod';
import type { Prisma } from '@prisma/client';
import argon2 from 'argon2';
import { env } from '$env/dynamic/private';

export const load: ServerLoad = async (event) => {
	const auth = auth_guard(event) as AuthGuardOutput;
	const user = auth?.data?.user;

	if (!user) {
		throw redirect(302, `/auth/login`);
	}

	const userData = await prisma.user.findFirst({
		where: {
			id: user.id
		}
	});

	return {
		status: 200,
		data: {
			user: userData
		}
	};
};

export const actions: Actions = {
	update_profile_data: async ({ request, cookies }) => {
		const formData = await request.formData();

		const userUpdate = z
			.object({
				vorname: z.string().min(3),
				nachname: z.string().min(3),
				hausnr: z.string().min(1),
				plz: z.string().min(5).max(5),
				ort: z.string().min(1).max(50),
				strasse: z.string().min(2),
				telefon: z.string().min(2)
			})
			.safeParse(Object.fromEntries(formData));

		if (!userUpdate.success)
			return fail(400, {
				error: 'Deine Accountdaten wurden nicht aktualisiert.'
			});

		let user;
		const token = cookies.get('token');
		if (!token || !env.JWT_SECRET) {
			return fail(400, {
				error: 'Deine Accountdaten wurden nicht aktualisiert.'
			});
		}
		try {
			user = jwt.verify(token, env.JWT_SECRET) as Prisma.UserCreateInput;
		} catch (error) {
			console.error(error);
		}

		if (!user) {
			return fail(400, {
				error: 'Deine Accountdaten wurden nicht aktualisiert.'
			});
		}

		const updatedUser = await prisma.user.update({
			where: {
				id: user.id
			},
			data: {
				vorname: userUpdate.data.vorname,
				nachname: userUpdate.data.nachname,
				hausnr: userUpdate.data.hausnr,
				plz: userUpdate.data.plz,
				ort: userUpdate.data.ort,
				strasse: userUpdate.data.strasse,
				telefon: userUpdate.data.telefon
			}
		});

		if (!updatedUser) {
			return fail(400, {
				error: 'Deine Accountdaten wurden nicht aktualisiert.'
			});
		}

		try {
			const newToken = jwt.sign(updatedUser, env.JWT_SECRET);
			cookies.set('token', newToken);
		} catch (error) {
			console.error(error);
		}

		return {
			status: 200,
			user: updatedUser
		};
	},
	update_password: async ({ request, cookies }) => {
		const formData = await request.formData();

		const password = z
			.object({
				password: z.string().min(8)
			})
			.safeParse(Object.fromEntries(formData));

		if (!password.success)
			return fail(400, {
				error: 'Deine Accountdaten wurden nicht aktualisiert.'
			});

		const newPassword = await argon2.hash(password.data.password);

		let user;
		const token = cookies.get('token');
		if (!token || !env.JWT_SECRET) {
			return fail(400, {
				error: 'Deine Accountdaten wurden nicht aktualisiert.'
			});
		}
		try {
			user = jwt.verify(token, env.JWT_SECRET) as Prisma.UserCreateInput;
		} catch (error) {
			console.error(error);
		}

		if (!user) {
			return fail(400, {
				error: 'Deine Accountdaten wurden nicht aktualisiert.'
			});
		}

		const updatedUser = await prisma.user.update({
			where: {
				id: user.id
			},
			data: {
				password: newPassword
			}
		});

		if (!updatedUser) {
			return fail(400, {
				error: 'Deine Accountdaten wurden nicht aktualisiert.'
			});
		}

		return {
			status: 200,
			user: updatedUser
		};
	}
};
