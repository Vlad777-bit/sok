<template>
	<div>
		<h2>Статус заявки</h2>

		<form class="form" @submit.prevent="load">
			<label
				>ID заявки
				<input v-model.number="appId" type="number" min="1" required
			/></label>
			<button type="submit">Проверить</button>
		</form>

		<p v-if="error" class="error">{{ error }}</p>

		<div v-if="data" class="result">
			<p><b>Статус:</b> {{ data.status }}</p>
			<p v-if="data.interest_rate">
				<b>Ставка:</b> {{ data.interest_rate }}%
			</p>
			<p class="muted">{{ data.comment }}</p>
			<pre>{{ data }}</pre>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import { api } from '../api';

const appId = ref(1);
const data = ref(null);
const error = ref('');

async function load() {
	error.value = '';
	data.value = null;
	try {
		data.value = await api.getApplication(appId.value);
	} catch (e) {
		error.value = e.message || 'Ошибка';
	}
}
</script>
