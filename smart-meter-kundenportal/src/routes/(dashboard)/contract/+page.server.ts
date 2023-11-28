import { auth_guard, type AuthGuardOutput } from '$lib/auth';
import { PrismaClient } from '@prisma/client';
import { redirect, type Actions, type ServerLoad } from '@sveltejs/kit';
import z from 'zod';

export const load: ServerLoad = async (event) => {
	const auth = auth_guard(event) as AuthGuardOutput;
	const user = auth?.data?.user;

	if (!user) {
		throw redirect(302, `/auth/login`);
	}

	const prisma = new PrismaClient();
	const contracts = await prisma.user.findMany({
		where: {
			id: user.id
		},
		select: {
			contract: {}
		}
	});

	return {
		status: 200,
		data: {
			user,
			contracts
		}
	};
};

export const actions: Actions = {
	async contract({ params, request }) {
		const prisma = new PrismaClient();
		const formData = await request.formData();

		// z.object({
		// 	name: z.string(),
		// 	startDate: z.date(),
		// 	endDate: z.date()
		// }).parseSafe({
		// 	name: formData.get()
		// });

		const contract = await prisma.contract.create({
			data: {
				user: {
					connect: {
						id: params.id
					}
				}
			}
		});

		return {
			status: 200,
			body: contract
		};
	}
};
