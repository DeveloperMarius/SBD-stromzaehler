import jwt from 'jsonwebtoken';
import { redirect, type ServerLoad } from '@sveltejs/kit';
import type { Prisma } from '@prisma/client';

export type AuthGuardOutput = {
	status: number;
	data?: {
		user: Prisma.UserCreateInput;
	};
};

export const auth_guard: ServerLoad = ({ cookies }) => {
	const token = cookies.get('token');

	if (!token || !process.env.JWT_SECRET) {
		throw redirect(302, `/auth/login`);
	}

	const user = jwt.verify(token, process.env.JWT_SECRET);

	return {
		status: 200,
		data: {
			user
		}
	};
};
