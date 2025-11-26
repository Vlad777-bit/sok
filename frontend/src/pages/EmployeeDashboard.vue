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

			<button
				v-if="me && me.role === 'ADMIN'"
				class="btn-secondary"
				@click="loadAudit"
			>
				Показать аудит
			</button>

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

		<!-- AUDIT -->
		<section v-if="showAudit" class="block">
			<h3>Аудит (последние 50)</h3>
			<div v-if="auditRows.length === 0" class="muted">Пусто</div>

			<div v-for="r in auditRows" :key="r.id" class="item">
				<div class="row2">
					<div>
						<b>#{{ r.id }}</b>
						{{ r.action }} ({{ r.entity }} {{ r.entity_id ?? '-' }})
					</div>
					<div class="muted">{{ formatDate(r.created_at) }}</div>
				</div>
				<div class="muted">
					actor: {{ r.actor_username ?? 'public' }} ({{
						r.actor_role ?? '-'
					}})
				</div>

				<!-- meta может быть объектом или строкой — покажем аккуратно -->
				<div class="muted" v-if="r.meta">
					meta:
					<pre class="meta">{{ prettyMeta(r.meta) }}</pre>
				</div>
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

const auditRows = ref([]);
const showAudit = ref(false);

function formatDate(value) {
	// value приходит как ISO строка – оставим простую “студенческую” обработку
	try {
		return new Date(value).toLocaleString();
	} catch {
		return String(value);
	}
}

function prettyMeta(meta) {
	try {
		// если meta уже объект - красиво форматируем
		if (typeof meta === 'object') return JSON.stringify(meta, null, 2);
		// если строка - попробуем распарсить
		const maybeObj = JSON.parse(String(meta));
		return JSON.stringify(maybeObj, null, 2);
	} catch {
		return String(meta);
	}
}

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

async function loadAudit() {
	error.value = '';
	showAudit.value = true; // важно: чтобы блок появился даже если auditRows пустой
	try {
		auditRows.value = await api.listAudit(50);
	} catch (e) {
		error.value = e.message || 'Ошибка аудита';
		auditRows.value = [];
	}
}

function logout() {
	auth.clear();
	router.push('/employee/login');
}

watch(statusFilter, () => {
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
.meta {
	margin: 8px 0 0;
	background: #0b1220;
	color: #e5e7eb;
	padding: 10px;
	border-radius: 12px;
	overflow: auto;
	font-size: 12px;
}
</style>
