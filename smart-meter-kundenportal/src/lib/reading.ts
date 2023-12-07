export type Reading = {
	stromzaehler_id: string;
	timestamp: number;
	value: number;
};

export type PowermeterReading = {
	contract_id: string;
	powermeter_id: string;
	readings: Reading[];
};
