import { auth } from './auth';

const BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

async function request(path, options = {}) {
	const headers = { ...(options.headers || {}) };

	// JSON по умолчанию, но для /auth/token будет form-urlencoded
	if (
		!headers['Content-Type'] &&
		options.body &&
		typeof options.body === 'string'
	) {
		headers['Content-Type'] = 'application/json';
	}

	const token = auth.getToken();
	if (token) {
		headers['Authorization'] = `Bearer ${token}`; // стандартный Authorization header :contentReference[oaicite:4]{index=4}
	}

	const res = await fetch(`${BASE}${path}`, { ...options, headers });

	const text = await res.text();
	const data = text ? JSON.parse(text) : null;

	if (!res.ok) {
		const msg = data?.detail || `HTTP ${res.status}`;
		throw new Error(msg);
	}
	return data;
}

export const api = {
	// публичные
	createClient(payload) {
		return request('/clients', {
			method: 'POST',
			body: JSON.stringify(payload),
		});
	},
	getClient(id) {
		return request(`/clients/${id}`, { method: 'GET' });
	},
	createApplication(payload) {
		return request('/applications', {
			method: 'POST',
			body: JSON.stringify(payload),
		});
	},
	getApplication(id) {
		return request(`/applications/${id}`, { method: 'GET' });
	},

	// auth
	async login(username, password) {
		// OAuth2 password flow требует form-data "username" + "password" :contentReference[oaicite:5]{index=5}
		const body = new URLSearchParams({ username, password }).toString();

		const res = await fetch(`${BASE}/auth/token`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
			body,
		});

		const data = await res.json().catch(() => null);
		if (!res.ok) throw new Error(data?.detail || `HTTP ${res.status}`);

		auth.setToken(data.access_token);
		return data;
	},

	me() {
		return request('/auth/me', { method: 'GET' });
	},

	// защищённые списки (сотрудник)
	listClients(limit = 20, offset = 0) {
		return request(`/clients?limit=${limit}&offset=${offset}`, {
			method: 'GET',
		});
	},
	listApplications(limit = 20, offset = 0) {
		return request(`/applications?limit=${limit}&offset=${offset}`, {
			method: 'GET',
		});
	},
};
