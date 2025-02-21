import {backendUrl} from "../clients/config.js";
import {PasswordClient} from "../clients/password.js";

export const passwordClient = new PasswordClient(backendUrl);
