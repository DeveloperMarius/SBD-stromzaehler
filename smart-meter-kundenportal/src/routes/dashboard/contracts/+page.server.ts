import { auth_guard, type AuthGuardOutput } from '$lib/auth';
import prisma from '$lib/prisma';
import { redirect, type Actions, type ServerLoad, fail } from '@sveltejs/kit';
import z from 'zod';
import dayjs from 'dayjs';

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
	async create_contract({ request }) {
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

		const user_id = formData.get('user_id')?.toString();

		if (!user_id || !newContract.success) {
			return fail(400, {
				error: 'Fehler bei der Erstellung eines Vertrages. Überprüfe deine Eingaben.'
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
						id: user_id
					}
				}
			}
		});

		const powermeter = await prisma.powermeter.create({
			data: {
				Contract: {
					connect: {
						id: createdContract.id
					}
				},
				powermeterStart: 0
			}
		});

		// TODO: Get Stromzähler stand from API and save it to the powermeter

		await prisma.powermeter.update({
			where: {
				id: powermeter.id
			},
			data: {
				powermeterStart: 1000
			}
		});

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
