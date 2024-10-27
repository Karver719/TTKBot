<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const tarifs = ref([]);
const newTarif = ref({
  name_tarif: '',
  inter_packet_mb: '',
  cost_tarif: ''
});
const editingTarif = ref(null);

const fetchTarifs = async () => {
  try {
    const response = await axios.get('http://localhost:3000/tarifs');
    tarifs.value = response.data;
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const addTarif = async () => {
  try {
    const response = await axios.post('http://localhost:3000/tarifs', newTarif.value);
    tarifs.value.push(response.data);
    newTarif.value = {
      name_tarif: '',
      inter_packet_mb: '',
      cost_tarif: ''
    };
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const deleteTarif = async (id) => {
  try {
    await axios.delete(`http://localhost:3000/tarifs/${id}`);
    tarifs.value = tarifs.value.filter(tarif => tarif.id !== id);
  } catch (error) {
    console.error('There was an error!', error);
  }
};

const startEditing = (tarif) => {
  editingTarif.value = { ...tarif };
};

const cancelEditing = () => {
  editingTarif.value = null;
};

const saveEditing = async () => {
  try {
    const response = await axios.put(`http://localhost:3000/tarifs/${editingTarif.value.id}`, editingTarif.value);
    const index = tarifs.value.findIndex(tarif => tarif.id === response.data.id);
    tarifs.value[index] = response.data;
    editingTarif.value = null;
  } catch (error) {
    console.error('There was an error!', error);
  }
};

onMounted(() => {
  fetchTarifs();
});
</script>

<template>
  <div>
    <h2>Тарифы</h2>

    <!-- Форма добавления нового тарифа -->
    <div class="add-form">
      <input 
        v-model="newTarif.name_tarif" 
        placeholder="Название тарифа"
        type="text"
      >
      <input 
        v-model="newTarif.inter_packet_mb" 
        placeholder="Интернет пакет (MB)"
        type="number"
      >
      <input 
        v-model="newTarif.cost_tarif" 
        placeholder="Стоимость тарифа"
        type="number"
      >
      <button @click="addTarif">Добавить</button>
    </div>

    <!-- Таблица тарифов -->
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Название тарифа</th>
          <th>Интернет пакет (MB)</th>
          <th>Стоимость тарифа</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="tarif in tarifs" :key="tarif.id">
          <td>{{ tarif.id }}</td>
          <td v-if="editingTarif && editingTarif.id === tarif.id">
            <input v-model="editingTarif.name_tarif" type="text">
          </td>
          <td v-else>{{ tarif.name_tarif }}</td>
          <td v-if="editingTarif && editingTarif.id === tarif.id">
            <input v-model="editingTarif.inter_packet_mb" type="number">
          </td>
          <td v-else>{{ tarif.inter_packet_mb }}</td>
          <td v-if="editingTarif && editingTarif.id === tarif.id">
            <input v-model="editingTarif.cost_tarif" type="number">
          </td>
          <td v-else>{{ tarif.cost_tarif }}</td>
          <td>
            <button v-if="editingTarif && editingTarif.id === tarif.id" @click="saveEditing">Сохранить</button>
            <button v-else @click="startEditing(tarif)">Редактировать</button>
            <button @click="deleteTarif(tarif.id)" class="delete-btn">Удалить</button>
            <button v-if="editingTarif && editingTarif.id === tarif.id" @click="cancelEditing">Отмена</button>
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