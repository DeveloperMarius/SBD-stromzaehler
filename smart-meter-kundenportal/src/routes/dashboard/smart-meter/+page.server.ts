import { auth_guard, type AuthGuardOutput } from '$lib/auth';
import prisma from '$lib/prisma';
import { fail, redirect, type ServerLoad } from '@sveltejs/kit';
import jwt from 'jsonwebtoken';

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
			powermeter: {
				select: {
					id: true,
					powermeterStart: true
				}
			}
		}
	});

	if (!process.env.SECRET_PRIVATE_KEY) {
		return fail(500, {
			error: 'Server Fehler: Der Account wurde erfolgreich angelegt. Bitte melde dich manuell an.'
		});
	}

	const token = jwt.sign({ user }, process.env.SECRET_PRIVATE_KEY, {
		expiresIn: '12h'
	});

	contracts.forEach((contract) => {
		contract.powermeter.forEach((powermeter) => {
			fetch('http://localhost:9001/api/stromzaehler/history', {
				method: 'POST',
				headers: {
					Authorization: 'Bearer ' + token,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					powermeterId: powermeter.id
				})
			});
		});
	});

	return {
		status: 200,
		data: {
			user,
			contracts: contracts
		}
	};
};
