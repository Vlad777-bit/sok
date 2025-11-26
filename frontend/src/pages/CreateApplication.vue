<template>
	<div>
		<h2>Подать заявку</h2>

		<form class="form" @submit.prevent="onSubmit">
			<label
				>ID клиента
				<input
					v-model.number="form.client_id"
					type="number"
					min="1"
					required
			/></label>

			<div class="row">
				<label
					>Сумма
					<input
						v-model.number="form.requested_amount"
						type="number"
						min="1"
						required
				/></label>
				<label
					>Срок (мес.)
					<input
						v-model.number="form.term_months"
						type="number"
						min="1"
						required
				/></label>
			</div>

			<label>Цель <input v-model="form.purpose" required /></label>

			<button type="submit">Отправить</button>
		</form>

		<p v-if="error" class="error">{{ error }}</p>

		<div v-if="created" class="result">
			<p>
				<b>Решение:</b> {{ created.status }}
				<span v-if="created.interest_rate"
					>({{ created.interest_rate }}%)</span
				>
			</p>
			<p class="muted">{{ created.comment }}</p>
			<p>id заявки: {{ created.id }}</p>
			<pre>{{ created }}</pre>
		</div>
	</div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { api } from '../api';

const form = reactive({
	client_id: 1,
	requested_amount: 200000,
	term_months: 24,
	purpose: 'Покупка техники',
});

const created = ref(null);
const error = ref('');

async function onSubmit() {
	error.value = '';
	created.value = null;
	try {
		created.value = await api.createApplication({ ...form });
	} catch (e) {
		error.value = e.message || 'Ошибка';
	}
}
</script>
