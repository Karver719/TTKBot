<template>
    <div class="login-container">
      <h2>Вход</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="login">Логин</label>
          <input v-model="login" type="text" id="login" placeholder="Введите логин" required>
        </div>
        <div class="form-group">
          <label for="password">Пароль</label>
          <input v-model="password" type="password" id="password" placeholder="Введите пароль" required>
        </div>
        <button type="submit">Войти</button>
      </form>
    </div>
</template>
  
<script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import axios from 'axios';
  
  const login = ref('');
  const password = ref('');
  const router = useRouter();
  
  const handleLogin = async () => {
    try {
      const response = await axios.post('http://localhost:3000/admins/login', { login: login.value, password: password.value });
      if (response.data.success) {
        // Сохранение токена или данных пользователя, если это необходимо
        localStorage.setItem('adminToken', response.data.token);
        router.push('/tables');
      } else {
        alert('Неверный логин или пароль');
      }
    } catch (error) {
      console.error('There was an error!', error);
      alert('Произошла ошибка при авторизации');
    }
  };
</script>

<style scoped>
  .login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  
  .form-group {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input {
    width: 100%;
    padding: 8px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
</style>