import { createRouter, createWebHistory } from 'vue-router';
import { auth } from './auth';

import CreateClient from './pages/CreateClient.vue';
import CreateApplication from './pages/CreateApplication.vue';
import ApplicationStatus from './pages/ApplicationStatus.vue';

import EmployeeLogin from './pages/EmployeeLogin.vue';
import EmployeeDashboard from './pages/EmployeeDashboard.vue';

const routes = [
	{ path: '/', redirect: '/client' },
	{ path: '/client', component: CreateClient },
	{ path: '/application', component: CreateApplication },
	{ path: '/status', component: ApplicationStatus },

	{ path: '/employee/login', component: EmployeeLogin },
	{
		path: '/employee',
		component: EmployeeDashboard,
		meta: { requiresAuth: true },
	},
];

const router = createRouter({
	history: createWebHistory(),
	routes,
});

// Глобальный гард Vue Router :contentReference[oaicite:6]{index=6}
router.beforeEach((to) => {
	if (to.meta.requiresAuth && !auth.isAuthed()) {
		return '/employee/login';
	}
});

export default router;
