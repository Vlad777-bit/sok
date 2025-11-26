<template>
	<div class="container">
		<header class="header">
			<div>
				<h1>СОК (Система обработки кредитных заявок)</h1>
				<p class="muted">Клиент → Заявка → Решение</p>
			</div>

			<nav class="nav">
				<RouterLink to="/client">Клиент</RouterLink>
				<RouterLink to="/application">Заявка</RouterLink>
				<RouterLink to="/status">Статус</RouterLink>
				<RouterLink to="/employee">Сотрудник</RouterLink>
			</nav>
		</header>

		<main class="card">
			<RouterView />
		</main>
	</div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>
