import jwt from 'jsonwebtoken';
import { redirect, type ServerLoad } from '@sveltejs/kit';
import type { User } from '@prisma/client';
import { env } from '$env/dynamic/private';

export type AuthGuardOutput = {
	status: number;
	data?: {
		user: User;
	};
};

export const auth_guard: ServerLoad = ({ cookies }) => {
	const token = cookies.get('token');

	const user = get_user_from_token(token);

	if (!user) {
		return redirect(302, `/auth/login`);
	}

	return {
		status: 200,
		data: {
			user
		}
	};
};

export const get_user_from_token = (token: string | undefined): User | null => {
	if (!token || !env.JWT_SECRET) {
		return null;
	}

	let user;
	try {
		user = jwt.verify(token, env.JWT_SECRET);
	} catch (error) {
		return null;
	}

	return user as User;
};
