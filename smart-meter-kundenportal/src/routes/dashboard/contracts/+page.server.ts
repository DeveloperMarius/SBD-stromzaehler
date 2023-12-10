import { auth_guard, type AuthGuardOutput, get_user_from_token } from '$lib/auth.server';
import prisma from '$lib/prisma';
import { redirect, type Actions, type ServerLoad, fail } from '@sveltejs/kit';
import z from 'zod';
import dayjs from 'dayjs';
import { register_powermeter } from '$lib/powermeter.server';
import { env } from '$env/dynamic/private';

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
			powermeter: {
				select: {
					id: true,
					powermeterStart: true
				}
			}
		}
	});

	return {
		status: 200,
		data: {
			user,
			contracts: contracts
		}
	};
};

export const actions: Actions = {
	async create_contract({ request, cookies }) {
		const formData = await request.formData();

		const newContract = z
			.object({
				strasse: z.string(),
				hausnr: z.string(),
				plz: z.string(),
				ort: z.string(),
				iban: z.string(),
				blz: z.string()
			})
			.safeParse(Object.fromEntries(formData));

		const user = get_user_from_token(cookies.get('token'));
		const powermeter_id = formData.get('powermeter_id')?.toString();

		if (!user || !user.id || !newContract.success || !powermeter_id) {
			return fail(400, {
				error: 'Fehler bei der Erstellung eines Vertrages. Überprüfe deine Eingaben.'
			});
		}

		if (!env.SECRET_PRIVATE_KEY) {
			return fail(500, {
				error: 'Server Fehler: Bitte versuchen Sie es später erneut.'
			});
		}

		const createdContract = await prisma.contract.create({
			data: {
				name: 'Smartvertrag',
				...newContract.data,
				startDate: dayjs().toISOString(),
				endDate: dayjs().add(1, 'year').toISOString(),
				user: {
					connect: {
						id: user.id
					}
				}
			}
		});

		if (!(await register_powermeter(powermeter_id, createdContract.id, user))) {
			await prisma.contract.delete({
				where: {
					id: createdContract.id
				}
			});
			return fail(500, {
				error:
					'Server Fehler: Smart-Meter konnte nicht eingerichtet werden. Daten sind noch nicht verfügbar.'
			});
		}

		const contract = await prisma.contract.findFirst({
			where: {
				id: createdContract.id
			},
			select: {
				id: true,
				strasse: true,
				hausnr: true,
				plz: true,
				ort: true,
				iban: true,
				blz: true,
				startDate: true,
				endDate: true,
				powermeter: {
					select: {
						id: true,
						powermeterStart: true
					}
				}
			}
		});

		return {
			status: 200,
			body: {
				message: 'created',
				contract
			}
		};
	},
	async update_contract({ request }) {
		const formData = await request.formData();

		const contract = z
			.object({
				id: z.string(),
				iban: z.string(),
				blz: z.string()
			})
			.safeParse(Object.fromEntries(formData));

		if (!contract.success) {
			return fail(400, {
				error: 'Fehler beim Aktualisieren des Vertrages. Überprüfe deine Eingaben.'
			});
		}

		const updatedContract = await prisma.contract.update({
			where: {
				id: contract.data.id
			},
			data: {
				...contract.data
			}
		});

		return {
			status: 200,
			body: {
				message: 'updated',
				contract: updatedContract
			}
		};
	},
	async delete_contract({ request }) {
		const formData = await request.formData();
		const contract_id = formData.get('contract_id')?.toString();

		if (!contract_id) {
			return fail(400, {
				error: 'Fehler beim Löschen des Vertrages. Überprüfe deine Eingaben.'
			});
		}

		await prisma.contract.delete({
			where: {
				id: contract_id
			}
		});

		return {
			status: 200,
			body: {
				message: 'deleted',
				contract_id
			}
		};
	}
};
