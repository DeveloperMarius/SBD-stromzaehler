import { json } from '@sveltejs/kit';
import { PrismaClient, type User } from '@prisma/client';
import bcyrpt from 'bcrypt';

const prisma = new PrismaClient();

export const POST = async ({ request }) => {
	if (!request.body) return json({ error: 'Missing body' }, { status: 400 });

	const { name, email, password, telefon, strasse, hausnr, plz, ort } =
		(await request.json()) as User;

	if (!name || !email || !password || !telefon || !strasse || !hausnr || !plz || !ort) {
		return json({ error: 'Missing fields' }, { status: 400 });
	}

	const passwordHash: string = await bcyrpt.hash(password, 10);

	const user = await prisma.user.create({
		data: {
			name,
			email,
			telefon,
			strasse,
			hausnr,
			plz,
			ort,
			password: passwordHash
		}
	});

	return json(user, { status: 201 });
};
