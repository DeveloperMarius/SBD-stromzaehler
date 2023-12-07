import { auth_guard, type AuthGuardOutput } from '$lib/auth';
import { register_powermeter } from '$lib/powermeter';
import prisma from '$lib/prisma';
import type { PowermeterReading, Reading } from '$lib/reading';
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
					powermeterStart: true,
					registered: true
				}
			}
		}
	});

	if (!process.env.SECRET_PRIVATE_KEY) {
		return new Promise(() =>
			fail(500, {
				error: 'Server Fehler: Der Account wurde erfolgreich angelegt. Bitte melde dich manuell an.'
			})
		);
	}

	const token = jwt.sign({ user }, process.env.SECRET_PRIVATE_KEY, {
		expiresIn: '12h'
	});

	const powermeterReadings: PowermeterReading[] = [];

	contracts.forEach((contract) => {
		contract.powermeter.forEach(async (powermeter) => {
			if (!powermeter.registered && !(await register_powermeter(powermeter.id, user))) {
				console.log('Failed to register powermeter');
				return fail(500, {
					error: 'Server Fehler: Die Stromzählerdaten konnten nicht abgefragt werden.'
				});
			}

			const data = await fetch('http://localhost:9001/api/stromzaehler/history', {
				method: 'POST',
				headers: {
					Authorization: 'Bearer ' + token,
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					powermeterId: powermeter.id
				})
			});

			const { readings } = await data.json();

			powermeterReadings.push({
				contract_id: contract.id,
				powermeter_id: powermeter.id,
				readings: readings as Reading[]
			});
		});
	});

	return {
		status: 200,
		data: {
			user,
			contracts: contracts,
			powermeterReadings: powermeterReadings
		}
	};
};
