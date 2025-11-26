<template>
  <div>
    <h2>Вход сотрудника</h2>
    <p class="muted">Для MVP: admin / admin123</p>

    <form class="form" @submit.prevent="onLogin">
      <label>Логин <input v-model="username" autocomplete="username" required /></label>
      <label>Пароль <input v-model="password" type="password" autocomplete="current-password" required /></label>

      <button type="submit">Войти</button>
      <button type="button" class="btn-secondary" @click="onLogout">Выйти</button>
    </form>

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="me" class="result">
      <p><b>Вы вошли как:</b> {{ me.username }} ({{ me.role }})</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { api } from "../api";
import { auth } from "../auth";

const router = useRouter();

const username = ref("admin");
const password = ref("admin123");
const error = ref("");
const me = ref(null);

async function onLogin() {
  error.value = "";
  me.value = null;

  try {
    await api.login(username.value, password.value);
    me.value = await api.me();
    router.push("/employee");
  } catch (e) {
    error.value = e.message || "Ошибка входа";
  }
}

function onLogout() {
  auth.clear();
  me.value = null;
  error.value = "";
}
</script>

<style scoped>
.btn-secondary {
  background: #ffffff;
  color: #1f2a44;
  border: 1px solid #dfe6fb;
}
</style>
