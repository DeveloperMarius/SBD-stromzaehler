import { redirect, type Load } from '@sveltejs/kit';

/** @type {import('@sveltejs/kit').Load} */
export const load: Load = async ({ data }) => {
	if (data?.loggedIn) {
		throw redirect(302, '/dashboard');
	}
};
