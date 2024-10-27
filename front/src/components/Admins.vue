<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const admins = ref([]);
const newAdmin = ref({
  login: '',
  fio: '',
  telephone: '',
  mail: ''
});
const editingAdmin = ref(null);

const fetchAdmins = async () => {
  try {
    const response = await axios.get('http://localhost:3000/admins');
    admins.value = response.data;
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const addAdmin = async () => {
  try {
    const response = await axios.post('http://localhost:3000/admins', newAdmin.value);
    admins.value.push(response.data);
    newAdmin.value = {
      login: '',
      fio: '',
      telephone: '',
      mail: ''
    };
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const deleteAdmin = async (id) => {
  try {
    await axios.delete(`http://localhost:3000/admins/${id}`);
    admins.value = admins.value.filter(admin => admin.id !== id);
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const startEditing = (admin) => {
  editingAdmin.value = { ...admin };
};

const cancelEditing = () => {
  editingAdmin.value = null;
};

const saveEditing = async () => {
  try {
    const response = await axios.put(`http://localhost:3000/admins/${editingAdmin.value.id}`, editingAdmin.value);
    const index = admins.value.findIndex(admin => admin.id === response.data.id);
    admins.value[index] = response.data;
    editingAdmin.value = null;
  } catch (error) {
    console.error('There was an error!', error);
  }
};

onMounted(() => {
  fetchAdmins();
});
</script>

<template>
  <div>
    <h2>Админы</h2>

    <!-- Форма добавления нового админа -->
    <div class="add-form">
      <input 
        v-model="newAdmin.login" 
        placeholder="Логин"
        type="text"
      >
      <input 
        v-model="newAdmin.fio" 
        placeholder="ФИО"
        type="text"
      >
      <input 
        v-model="newAdmin.telephone" 
        placeholder="Телефон"
        type="text"
      >
      <input 
        v-model="newAdmin.mail" 
        placeholder="Email"
        type="email"
      >
      <button @click="addAdmin">Добавить</button>
    </div>

    <!-- Таблица админов -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Логин</th>
          <th>Пароль</th>
          <th>ФИО</th>
          <th>Телефон</th>
          <th>Email</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="admin in admins" :key="admin.id">
          <td>{{ admin.id }}</td>
          <td v-if="editingAdmin && editingAdmin.id === admin.id">
            <input v-model="editingAdmin.login" type="text">
          </td>
          <td v-else>{{ admin.login }}</td>
          <td v-if="editingAdmin && editingAdmin.id === admin.id">
            <input v-model="editingAdmin.password" type="text">
          </td>
          <td v-else>{{ admin.password }}</td>
          <td v-if="editingAdmin && editingAdmin.id === admin.id">
            <input v-model="editingAdmin.fio" type="text">
          </td>
          <td v-else>{{ admin.fio }}</td>
          <td v-if="editingAdmin && editingAdmin.id === admin.id">
            <input v-model="editingAdmin.telephone" type="text">
          </td>
          <td v-else>{{ admin.telephone }}</td>
          <td v-if="editingAdmin && editingAdmin.id === admin.id">
            <input v-model="editingAdmin.mail" type="email">
          </td>
          <td v-else>{{ admin.mail }}</td>
          <td>
            <button v-if="editingAdmin && editingAdmin.id === admin.id" @click="saveEditing">Сохранить</button>
            <button v-else @click="startEditing(admin)">Редактировать</button>
            <button @click="deleteAdmin(admin.id)" class="delete-btn">Удалить</button>
            <button v-if="editingAdmin && editingAdmin.id === admin.id" @click="cancelEditing">Отмена</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.add-form {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

button {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 57px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
}

.delete-btn {
  background-color: #f44336;
}

.delete-btn:hover {
  background-color: #da190b;
}
</style>