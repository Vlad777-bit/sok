const BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

async function request(path, options = {}) {
	const res = await fetch(`${BASE}${path}`, {
		headers: {
			'Content-Type': 'application/json',
			...(options.headers || {}),
		},
		...options,
	});

	const text = await res.text();
	const data = text ? JSON.parse(text) : null;

	if (!res.ok) {
		const msg = data?.detail || `HTTP ${res.status}`;
		throw new Error(msg);
	}
	return data;
}

export const api = {
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
};
