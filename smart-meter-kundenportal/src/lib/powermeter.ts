import type { Reading } from '$lib/reading';
import type { User } from '@prisma/client';
import prisma from '$lib/prisma';
import { sign_body } from './jwt';

export async function register_powermeter(powermeter_id: string, user: User): Promise<boolean> {
	if (!process.env.SECRET_PRIVATE_KEY || !user) {
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

	console.log(body);
	console.log(await sign_body(body));

	const response = await fetch('http://localhost:9001/api/stromzaehler/register', {
		method: 'POST',
		headers: {
			Authorization: 'Bearer ' + (await sign_body(body)),
			'Content-Type': 'application/json'
		},
		body
	});

	console.log(response);

	if (response.status !== 200) {
		return false;
	}

	const body2 = JSON.stringify({
		'stromzaehler-id': powermeter_id,
		start_date: '2021-01-01',
		end_date: '2024-12-31'
	});

	const readings_res = await fetch('http://localhost:9001/api/stromzaehler/history', {
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

	const { readings } = await readings_res.json();

	let highestReading = 0;
	readings.forEach((reading: Reading) => {
		if (reading.value > highestReading) {
			highestReading = reading.value;
		}
	});

	await prisma.powermeter.update({
		where: {
			id: powermeter_id
		},
		data: {
			powermeterStart: highestReading,
			registered: true
		}
	});

	return true;
}
