import { redirect, type ServerLoad } from '@sveltejs/kit';

export const load: ServerLoad = async ({ cookies }) => {
	cookies.delete('token');

	throw redirect(302, '/auth/login');
};
