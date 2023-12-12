import type { PowermeterReading, Reading } from '$lib/reading';
import type { Contract, Powermeter, User } from '@prisma/client';
import prisma from '$lib/prisma';
import { sign_body } from './jwt.server';
import { error } from '@sveltejs/kit';
import { env } from '$env/dynamic/private';

export async function register_powermeter(
	powermeter_id: string,
	contract_id: string,
	user: User
): Promise<boolean> {
	if (!env.SECRET_PRIVATE_KEY || !env.MESSSTELLENBETREIBER_URL || !user) {
		return false;
	}

	const body = JSON.stringify({
		id: powermeter_id,
		person: {
			firstname: user.vorname,
			lastname: user.nachname,
			gender: 1,
			phone: user.telefon,
			email: user.email
		},
		address: {
			street: `${user.strasse} ${user.hausnr}`,
			plz: user.plz,
			city: user.ort,
			state: 'Mallorca',
			country: 'Germany'
		}
	});

	const response = await fetch(`${env.MESSSTELLENBETREIBER_URL}/api/stromzaehler/register`, {
		method: 'POST',
		headers: {
			Authorization: 'Bearer ' + (await sign_body(body)),
			'Content-Type': 'application/json'
		},
		body
	});

	if (response.status !== 200) {
		return false;
	}

	const body2 = JSON.stringify({
		stromzaehler_id: powermeter_id,
		start_date: '2021-01-01',
		end_date: '2024-12-10'
	});

	const readings_res = await fetch(`${env.MESSSTELLENBETREIBER_URL}/api/stromzaehler/history`, {
		method: 'POST',
		headers: {
			Authorization: 'Bearer ' + (await sign_body(body2)),
			'Content-Type': 'application/json'
		},
		body: body2
	});

	if (response.status !== 200) {
		return false;
	}

	const { readings } = (await readings_res.json()) as { readings: Reading[] };

	let highestReading = 0;
	readings.forEach((reading: Reading) => {
		if (reading.value > highestReading) {
			highestReading = reading.value;
		}
	});

	await prisma.powermeter.upsert({
		where: {
			id: powermeter_id
		},
		create: {
			id: powermeter_id,
			powermeterStart: highestReading,
			registered: true,
			Contract: {
				connect: {
					id: contract_id
				}
			}
		},
		update: {
			powermeterStart: highestReading,
			registered: true,
			Contract: {
				connect: {
					id: contract_id
				}
			}
		},
		select: {
			id: true,
			powermeterStart: true
		}
	});

	return true;
}

type ContractWithPowermeter = Contract & {
	powermeter: Powermeter[];
};

export async function getPowermeterReadings(
	contracts: ContractWithPowermeter[],
	user: User
): Promise<PowermeterReading[]> {
	const powermeterReadings: PowermeterReading[] = [];

	for (const contract of contracts) {
		for (const powermeter of contract.powermeter) {
			if (
				!powermeter.registered &&
				!(await register_powermeter(powermeter.id, contract.id, user))
			) {
				throw error(500, 'Server Fehler: Der Stromzähler konnte nicht registriert werden.');
			}

			const body = JSON.stringify({
				stromzaehler_id: powermeter.id,
				start_date: '2021-01-01',
				end_date: '2024-12-10'
			});

			const data = await fetch(`${env.MESSSTELLENBETREIBER_URL}/api/stromzaehler/history`, {
				method: 'POST',
				headers: {
					Authorization: 'Bearer ' + (await sign_body(body)),
					'Content-Type': 'application/json'
				},
				body
			});

			const { readings } = await data.json();

			powermeterReadings.push({
				contract_id: contract.id,
				powermeter_id: powermeter.id,
				readings: readings as Reading[]
			});
		}
	}

	return powermeterReadings;
}
