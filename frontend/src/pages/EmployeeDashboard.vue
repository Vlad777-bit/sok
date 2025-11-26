<template>
	<div>
		<h2>Кабинет сотрудника</h2>

		<p v-if="me" class="muted">
			Вошли как: <b>{{ me.username }}</b> ({{ me.role }})
		</p>

		<div class="toolbar">
			<label class="small">
				Фильтр заявок:
				<select v-model="statusFilter">
					<option value="">ALL</option>
					<option value="NEW">NEW</option>
					<option value="APPROVED">APPROVED</option>
					<option value="REJECTED">REJECTED</option>
				</select>
			</label>

			<button @click="loadAll">Обновить</button>
			<button class="btn-secondary" @click="logout">Выйти</button>
		</div>

		<p v-if="error" class="error">{{ error }}</p>

		<section class="block">
			<h3>Заявки</h3>
			<div v-if="apps.length === 0" class="muted">Пока пусто</div>

			<div v-for="a in apps" :key="a.id" class="item">
				<div class="row2">
					<div>
						<b>#{{ a.id }}</b> (client {{ a.client_id }})
					</div>
					<div class="status">{{ a.status }}</div>
				</div>
				<div class="muted">{{ a.purpose }}</div>
				<div class="muted">
					Сумма: {{ a.requested_amount }} | срок:
					{{ a.term_months }} мес.
				</div>
				<div class="muted" v-if="a.comment">
					Комментарий: {{ a.comment }}
				</div>
			</div>
		</section>

		<section class="block">
			<h3>Клиенты</h3>
			<div v-if="clients.length === 0" class="muted">Пока пусто</div>

			<div v-for="c in clients" :key="c.id" class="item">
				<div class="row2">
					<div>
						<b>#{{ c.id }}</b> {{ c.full_name }}
					</div>
					<div class="muted">{{ c.phone }}</div>
				</div>
				<div class="muted">{{ c.email }}</div>
				<div class="muted">Доход: {{ c.monthly_income }}</div>
			</div>
		</section>
	</div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { api } from '../api';
import { auth } from '../auth';

const router = useRouter();

const me = ref(null);
const apps = ref([]);
const clients = ref([]);
const error = ref('');

const statusFilter = ref(''); // "" = ALL

async function loadAll() {
	error.value = '';
	try {
		me.value = await api.me();
		apps.value = await api.listApplications(50, 0, statusFilter.value);
		clients.value = await api.listClients(50, 0);
	} catch (e) {
		error.value = e.message || 'Ошибка загрузки';
	}
}

function logout() {
	auth.clear();
	router.push('/employee/login');
}

watch(statusFilter, () => {
	// фильтр меняется — перезагружаем список с query-параметром
	loadAll();
});

onMounted(loadAll);
</script>

<style scoped>
.toolbar {
	display: flex;
	gap: 10px;
	margin: 12px 0 18px;
	align-items: end;
	flex-wrap: wrap;
}
.small {
	font-size: 14px;
	display: grid;
	gap: 6px;
}
select {
	padding: 10px 12px;
	border-radius: 12px;
	border: 1px solid #dfe6fb;
	background: #fff;
}
.btn-secondary {
	background: #ffffff;
	color: #1f2a44;
	border: 1px solid #dfe6fb;
}
.block {
	margin-top: 18px;
}
.item {
	border: 1px solid #e8ecf5;
	border-radius: 14px;
	padding: 10px 12px;
	margin-top: 10px;
	background: #fff;
}
.row2 {
	display: flex;
	justify-content: space-between;
	gap: 10px;
}
.status {
	font-weight: 700;
}
</style>
