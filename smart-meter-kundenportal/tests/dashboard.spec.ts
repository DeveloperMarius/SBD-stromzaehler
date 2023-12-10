import { test, expect } from '@playwright/test';

const email = `test${crypto.randomUUID()}@test.de`;
let test_pw = '12345678';

test.beforeAll(async ({ page }) => {
	await page.goto('http://localhost:3001/');
	await page.getByRole('button', { name: 'Anmelden' }).click();

	await page.waitForURL('http://localhost:3001/auth/register');
	await page.getByLabel('Vorname').fill('Test');
	await page.getByLabel('Nachname').fill('Test');
	await page.getByLabel('Deine E-Mail').fill(email);
	await page.getByLabel('Deine Telefonnummer').fill('069 123456789');
	await page.getByLabel('Dein Passwort').fill(test_pw);
	await page.getByLabel('Passwort bestätigen').fill(test_pw);
	await page.getByLabel('Straße').fill('Schlossallee');
	await page.getByLabel('Hausnummer').fill('400');
	await page.getByLabel('Ort', { exact: true }).fill('Monopoly');
	await page.getByLabel('Postleitzahl').fill('12345');

	await page.getByLabel('Ich akzeptiere die').click();

	await page.getByText('Account erstellen').click();

	await page.waitForURL('http://localhost:3001/dashboard');

	expect(page.url()).toBe('http://localhost:3001/dashboard');
});

test.beforeEach(async ({ page }) => {
	await page.goto('http://localhost:3001/auth/login');
	await page.getByLabel('Deine E-Mail').fill(email);
	await page.getByLabel('Dein Passwort').fill(test_pw);
	await page.getByText('Jetzt Anmelden').click();
	await page.waitForURL('http://localhost:3001/dashboard');
	expect(page.url()).toBe('http://localhost:3001/dashboard');
});

test.afterEach(async ({ page }) => {
	await page.goto('http://localhost:3001/auth/logout');
	await page.waitForURL('http://localhost:3001/auth/login');
	expect(page.url()).toBe('http://localhost:3001/auth/login');
});

test.describe('test contract page', async () => {
	test.describe.configure({ mode: 'serial' });

	test('test create_contract', async ({ page }) => {
		await page.goto('http://localhost:3001/dashboard/contracts');
		await page.getByText('Vertrag abschließen').click();
		await page.getByLabel('Powermeter').fill('1');
		await page.getByLabel('IBAN').fill('DE123456789');
		await page.getByLabel('BIC').fill('COM12387626');
		await page.getByLabel('Ich stimme dem SEPA').check();
		await page.getByLabel('Ich akzeptiere die AGBs und').check();
		await page.getByRole('button', { name: 'Stromvertrag abschließen' }).click();

		await page.waitForTimeout(250);

		const vertraege = page.getByText('Vertrag kündigen');

		expect(vertraege).toHaveCount(1);
	});

	test('test edit_contract', async ({ page }) => {
		await page.goto('http://localhost:3001/dashboard/contracts');

		await page.getByText('Bankverbindung').click();
		await page.getByLabel('IBAN').fill('DE1234567890');

		await page.getByLabel('Ich stimme dem SEPA').check();
		await page.getByLabel('Ich akzeptiere die AGBs und').check();

		await page
			.getByRole('dialog')
			.getByRole('document')
			.getByRole('button', { name: 'Bankverbindung ändern' })
			.click();

		await page.waitForTimeout(250);

		expect(await page.getByText('IBAN: *********').textContent()).toBe('IBAN: *********90');
	});

	test('test delete_contract', async ({ page }) => {
		await page.goto('http://localhost:3001/dashboard/contracts');

		const vertraege = page.getByText('Vertrag kündigen');

		expect(vertraege).toHaveCount(1);

		await page.getByText('Vertrag kündigen').click();

		await page
			.getByRole('dialog')
			.getByRole('document')
			.getByRole('button', { name: 'Vertrag kündigen' })
			.click();

		await page.waitForTimeout(250);

		const vertraegeAfter = page.getByText('Vertrag kündigen');

		expect(vertraegeAfter).toHaveCount(0);
	});
});

test.describe('test edit profile page', async () => {
	test.describe.configure({ mode: 'serial' });

	test('test edit profile', async ({ page }) => {
		await page.goto('http://localhost:3001/dashboard/profile');
		await page.getByLabel('Vorname').fill('Test2');
		await page.getByLabel('Nachname').fill('Test2');
		await page.getByLabel('Deine Telefonnummer').fill('069 1234567892');
		await page.getByLabel('Straße').fill('Schlossallee2');
		await page.getByLabel('Hausnummer').fill('4002');
		await page.getByLabel('Ort', { exact: true }).fill('Monopoly2');
		await page.getByLabel('Postleitzahl').fill('12346');
		await page.getByRole('button', { name: 'Daten aktualisieren' }).click();

		await page.waitForTimeout(250);

		expect(await page.getByLabel('Vorname').inputValue()).toBe('Test2');
		expect(await page.getByLabel('Nachname').inputValue()).toBe('Test2');
		expect(await page.getByLabel('Deine Telefonnummer').inputValue()).toBe('069 1234567892');
		expect(await page.getByLabel('Straße').inputValue()).toBe('Schlossallee2');
		expect(await page.getByLabel('Hausnummer').inputValue()).toBe('4002');
		expect(await page.getByLabel('Ort', { exact: true }).inputValue()).toBe('Monopoly2');
		expect(await page.getByLabel('Postleitzahl').inputValue()).toBe('12346');
	});

	test('test edit password', async ({ page }) => {
		await page.goto('http://localhost:3001/dashboard/profile');
		await page.getByLabel('Dein Passwort').fill('testtest');
		await page.getByLabel('Passwort bestätigen').fill('testtest');
		await page.getByRole('button', { name: 'Passwort ändern' }).click();

		await page.waitForTimeout(250);

		test_pw = 'testtest';

		await page.goto('http://localhost:3001/auth/logout');
		await page.waitForURL('http://localhost:3001/auth/login');

		await page.getByLabel('Deine E-Mail').fill(email);
		await page.getByLabel('Dein Passwort').fill(test_pw);
		await page.getByText('Jetzt Anmelden').click();

		await page.waitForURL('http://localhost:3001/dashboard');

		expect(page.url()).toBe('http://localhost:3001/dashboard');
	});
});
