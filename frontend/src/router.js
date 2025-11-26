import { createRouter, createWebHistory } from 'vue-router';
import CreateClient from './pages/CreateClient.vue';
import CreateApplication from './pages/CreateApplication.vue';
import ApplicationStatus from './pages/ApplicationStatus.vue';

const routes = [
	{ path: '/', redirect: '/client' },
	{ path: '/client', component: CreateClient },
	{ path: '/application', component: CreateApplication },
	{ path: '/status', component: ApplicationStatus },
];

export default createRouter({
	history: createWebHistory(),
	routes,
});
