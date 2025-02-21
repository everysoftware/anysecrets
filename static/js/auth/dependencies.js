import {backendUrl} from '../clients/config.js';
import {AuthClient} from '../clients/auth.js';

export const authClient = new AuthClient(backendUrl);
