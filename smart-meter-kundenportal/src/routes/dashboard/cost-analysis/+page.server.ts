import { auth_guard, type AuthGuardOutput } from '$lib/auth';
import prisma from '$lib/prisma';
import { fail, redirect, type ServerLoad } from '@sveltejs/kit';
import { getPowermeterReadings } from '$lib/powermeter';

export const load: ServerLoad = async (event) => {
	const auth = auth_guard(event) as AuthGuardOutput;
	const user = auth?.data?.user;

	if (!user) {
		throw redirect(302, `/auth/login`);
	}

	const contracts = await prisma.contract.findMany({
		where: {
			user: {
				id: user.id
			}
		},
		select: {
			id: true,
			name: true,
			strasse: true,
			hausnr: true,
			plz: true,
			ort: true,
			iban: true,
			blz: true,
			startDate: true,
			endDate: true,
			userId: true,
			powermeter: {
				select: {
					id: true,
					powermeterStart: true,
					registered: true,
					contractId: true
				}
			}
		}
	});

	if (!process.env.SECRET_PRIVATE_KEY) {
		throw fail(500, {
			error: 'Server Fehler: Der Account wurde erfolgreich angelegt. Bitte melde dich manuell an.'
		});
	}

	const powermeterReadings = await getPowermeterReadings(contracts, user);

	return {
		status: 200,
		data: {
			user,
			contracts: contracts,
			powermeterReadings: powermeterReadings
		}
	};
};
