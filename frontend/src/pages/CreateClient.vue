<template>
	<div>
		<h2>Создать клиента</h2>

		<form class="form" @submit.prevent="onSubmit">
			<label>ФИО <input v-model="form.full_name" required /></label>
			<label
				>Дата рождения
				<input v-model="form.date_of_birth" type="date" required
			/></label>

			<div class="row">
				<label
					>Паспорт серия
					<input
						v-model="form.passport_series"
						placeholder="1234"
						required
				/></label>
				<label
					>Паспорт номер
					<input
						v-model="form.passport_number"
						placeholder="567890"
						required
				/></label>
			</div>

			<label
				>Адрес регистрации
				<input v-model="form.address_registration" required
			/></label>

			<div class="row">
				<label>Телефон <input v-model="form.phone" required /></label>
				<label
					>Email <input v-model="form.email" type="email" required
				/></label>
			</div>

			<div class="row">
				<label
					>Место работы <input v-model="form.workplace" required
				/></label>
				<label
					>Должность <input v-model="form.position" required
				/></label>
			</div>

			<label
				>Ежемесячный доход
				<input
					v-model.number="form.monthly_income"
					type="number"
					min="1"
					required
			/></label>

			<button type="submit">Сохранить</button>
		</form>

		<p v-if="error" class="error">{{ error }}</p>

		<div v-if="created" class="result">
			<p><b>Готово!</b> id клиента: {{ created.id }}</p>
			<pre>{{ created }}</pre>
		</div>
	</div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { api } from '../api';

const form = reactive({
	full_name: '',
	date_of_birth: '',
	passport_series: '',
	passport_number: '',
	address_registration: '',
	phone: '',
	email: '',
	workplace: '',
	position: '',
	monthly_income: 50000,
});

const created = ref(null);
const error = ref('');

async function onSubmit() {
	error.value = '';
	created.value = null;
	try {
		created.value = await api.createClient({ ...form });
	} catch (e) {
		error.value = e.message || 'Ошибка';
	}
}
</script>
