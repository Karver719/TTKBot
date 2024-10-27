<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const services = ref([]);
const newService = ref({
  name_service: '',
  cost_service: ''
});
const editingService = ref(null);

const fetchServices = async () => {
  try {
    const response = await axios.get('http://localhost:3000/services');
    services.value = response.data;
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const addService = async () => {
  try {
    const response = await axios.post('http://localhost:3000/services', newService.value);
    services.value.push(response.data);
    newService.value = {
      name_service: '',
      cost_service: ''
    };
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const deleteService = async (id) => {
  try {
    await axios.delete(`http://localhost:3000/services/${id}`);
    services.value = services.value.filter(service => service.id !== id);
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const startEditing = (service) => {
  editingService.value = { ...service };
};

const cancelEditing = () => {
  editingService.value = null;
};

const saveEditing = async () => {
  try {
    const response = await axios.put(`http://localhost:3000/services/${editingService.value.id}`, editingService.value);
    const index = services.value.findIndex(service => service.id === response.data.id);
    services.value[index] = response.data;
    editingService.value = null;
  } catch (error) {
    console.error('There was an error!', error);
  }
};

onMounted(() => {
  fetchServices();
});
</script>

<template>
  <div>
    <h2>Услуги</h2>

    <!-- Форма добавления новой услуги -->
    <div class="add-form">
      <input 
        v-model="newService.name_service" 
        placeholder="Название услуги"
        type="text"
      >
      <input 
        v-model="newService.cost_service" 
        placeholder="Стоимость услуги"
        type="number"
      >
      <button @click="addService">Добавить</button>
    </div>

    <!-- Таблица услуг -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Название услуги</th>
          <th>Стоимость услуги</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="service in services" :key="service.id">
          <td>{{ service.id }}</td>
          <td v-if="editingService && editingService.id === service.id">
            <input v-model="editingService.name_service" type="text">
          </td>
          <td v-else>{{ service.name_service }}</td>
          <td v-if="editingService && editingService.id === service.id">
            <input v-model="editingService.cost_service" type="number">
          </td>
          <td v-else>{{ service.cost_service }}</td>
          <td>
            <button v-if="editingService && editingService.id === service.id" @click="saveEditing">Сохранить</button>
            <button v-else @click="startEditing(service)">Редактировать</button>
            <button @click="deleteService(service.id)" class="delete-btn">Удалить</button>
            <button v-if="editingService && editingService.id === service.id" @click="cancelEditing">Отмена</button>
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