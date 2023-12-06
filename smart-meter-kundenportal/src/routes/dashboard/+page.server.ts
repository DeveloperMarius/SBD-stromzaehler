import { auth_guard, type AuthGuardOutput } from '$lib/auth';
import prisma from '$lib/prisma';
import { redirect, type ServerLoad } from '@sveltejs/kit';

export const load: ServerLoad = async (event) => {
	const auth = auth_guard(event) as AuthGuardOutput;
	const user = auth?.data?.user;

	if (!user) {
		throw redirect(302, `/auth/login`);
	}

	const contracts = await prisma.user.findFirst({
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
			contracts: contracts?.contract
		}
	};
};
