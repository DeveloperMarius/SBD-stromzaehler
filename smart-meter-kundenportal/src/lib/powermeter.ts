import jwt from 'jsonwebtoken';
import type { Reading } from '$lib/reading';
import type { User } from '@prisma/client';
import prisma from '$lib/prisma';

export async function register_powermeter(powermeter_id: string, user: User): Promise<boolean> {
	if (!process.env.SECRET_PRIVATE_KEY || !user) {
		return false;
	}

	const serverToken = jwt.sign({ action: 'register_powermeter' }, process.env.SECRET_PRIVATE_KEY, {
		expiresIn: '5min'
	});

	const response = await fetch('http://localhost:9001/api/stromzaehler/register', {
		method: 'POST',
		headers: {
			Authorization: 'Bearer ' + serverToken,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			powermeterId: powermeter_id,
			person: {
				first_name: user.vorname,
				last_name: user.nachname,
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
		})
	});

	if (response.status !== 200) {
		return false;
	}

	const readings_res = await fetch('http://localhost:9001/api/stromzaehler/history', {
		method: 'POST',
		headers: {
			Authorization: 'Bearer ' + serverToken,
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({
			powermeterId: powermeter_id
		})
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
