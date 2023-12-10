import * as jose from 'jose';
import { createPrivateKey } from 'node:crypto';
import * as crypto from 'crypto';
import { env } from '$env/dynamic/private';

export async function sign_body(body: string) {
	if (!env.SECRET_PRIVATE_KEY) {
		throw new Error('No private key found');
	}

	const private_key = env.SECRET_PRIVATE_KEY;

	const secret = createPrivateKey(private_key);

	const jwt_body = {
		type: 'kundenportal',
		id: 1,
		mode: 'SHA256',
		signature: crypto.createHash('sha256').update(body).digest('hex')
	};

	return await new jose.SignJWT(jwt_body)
		.setProtectedHeader({
			alg: 'EdDSA',
			jwk: {
				crv: 'Ed25519'
			},
			typ: 'JWT'
		})
		.sign(secret);
}
