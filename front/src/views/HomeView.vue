<template>
  <div id="app">
    <h1>Тарифы</h1>
    <ul>
      <li v-for="tarif in tarifs" :key="tarif.id">
        {{ tarif.name_tarif }} - Интернет пакет: {{ tarif.inter_packet_mb }} MB - Стоимость: {{ tarif.cost_tarif }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'App',
  data() {
    return {
      tarifs: []
    };
  },
  mounted() {
    axios.get('http://localhost:3000/data')
      .then(response => {
        this.tarifs = response.data;
      })
      .catch(error => {
        console.error('There was an error!', error);
      });
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>