import {ApiClient} from './base.js';

export class PasswordClient extends ApiClient {
    async createPassword(data) {
        return this.post('/passwords', {}, data, {}, this.handleCreatePasswordErrors);
    }

    async editPassword(passwordId, data) {
        return this.patch(`/passwords/${passwordId}`, {}, data, {}, this.handleSavePasswordErrors);
    }

    async deletePassword(passwordId) {
        return this.delete(`/passwords/${passwordId}`, {}, {}, this.handleDeletePasswordErrors);
    }

    handleCreatePasswordErrors(status, data) {
        if (status === 422) {
            alert('Validation error.');
        } else {
            super.handleErrors(status, data);
        }
    }

    handleSavePasswordErrors(status, data) {
        if (status === 404) {
            alert('The requested password was not found.');
        } else if (status === 422) {
            alert('Validation error.');
        } else {
            super.handleErrors(status, data);
        }
    }

    handleDeletePasswordErrors(status, data) {
        if (status === 404) {
            alert('The requested password was not found.');
        } else if (status === 422) {
            alert('Validation error.');
        } else {
            super.handleErrors(status, data);
        }
    }

    generatePassword(length = 12) {
        const charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+<>?";
        let password = "";
        for (let i = 0, n = charset.length; i < length; ++i) {
            password += charset.charAt(Math.floor(Math.random() * n));
        }
        return password;
    }
}
