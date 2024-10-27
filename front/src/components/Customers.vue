<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const customers = ref([]);
const newCustomer = ref({
  num_dog: '',
  fio: '',
  telephone: '',
  mail: ''
});
const editingCustomer = ref(null);

const fetchCustomers = async () => {
  try {
    const response = await axios.get('http://localhost:3000/customers');
    customers.value = response.data;
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const addCustomer = async () => {
  try {
    const response = await axios.post('http://localhost:3000/customers', newCustomer.value);
    customers.value.push(response.data);
    newCustomer.value = {
      num_dog: '',
      fio: '',
      telephone: '',
      mail: ''
    };
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const deleteCustomer = async (id) => {
  try {
    await axios.delete(`http://localhost:3000/customers/${id}`);
    customers.value = customers.value.filter(customer => customer.id !== id);
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const startEditing = (customer) => {
  editingCustomer.value = { ...customer };
};

const cancelEditing = () => {
  editingCustomer.value = null;
};

const saveEditing = async () => {
  try {
    const response = await axios.put(`http://localhost:3000/customers/${editingCustomer.value.id}`, editingCustomer.value);
    const index = customers.value.findIndex(customer => customer.id === response.data.id);
    customers.value[index] = response.data;
    editingCustomer.value = null;
  } catch (error) {
    console.error('There was an error!', error);
  }
};

onMounted(() => {
  fetchCustomers();
});
</script>

<template>
  <div>
    <h2>Клиенты</h2>

    <!-- Форма добавления нового клиента -->
    <div class="add-form">
      <input 
        v-model="newCustomer.num_dog" 
        placeholder="Номер договора"
        type="text"
      >
      <input 
        v-model="newCustomer.fio" 
        placeholder="ФИО"
        type="text"
      >
      <input 
        v-model="newCustomer.telephone" 
        placeholder="Телефон"
        type="text"
      >
      <input 
        v-model="newCustomer.mail" 
        placeholder="Email"
        type="email"
      >
      <button @click="addCustomer">Добавить</button>
    </div>

    <!-- Таблица клиентов -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Номер договора</th>
          <th>ФИО</th>
          <th>Телефон</th>
          <th>Email</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="customer in customers" :key="customer.id">
          <td>{{ customer.id }}</td>
          <td v-if="editingCustomer && editingCustomer.id === customer.id">
            <input v-model="editingCustomer.num_dog" type="text">
          </td>
          <td v-else>{{ customer.num_dog }}</td>
          <td v-if="editingCustomer && editingCustomer.id === customer.id">
            <input v-model="editingCustomer.fio" type="text">
          </td>
          <td v-else>{{ customer.fio }}</td>
          <td v-if="editingCustomer && editingCustomer.id === customer.id">
            <input v-model="editingCustomer.telephone" type="text">
          </td>
          <td v-else>{{ customer.telephone }}</td>
          <td v-if="editingCustomer && editingCustomer.id === customer.id">
            <input v-model="editingCustomer.mail" type="email">
          </td>
          <td v-else>{{ customer.mail }}</td>
          <td>
            <button v-if="editingCustomer && editingCustomer.id === customer.id" @click="saveEditing">Сохранить</button>
            <button v-else @click="startEditing(customer)">Редактировать</button>
            <button @click="deleteCustomer(customer.id)" class="delete-btn">Удалить</button>
            <button v-if="editingCustomer && editingCustomer.id === customer.id" @click="cancelEditing">Отмена</button>
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