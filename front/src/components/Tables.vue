<template>
    <div id="app">
      <h1 class="main-title">База данных TTKTarif</h1>
      <div class="container">
        <Tarifs />
        <Services />
        <Customers />
        <Admins />
      </div>
    </div>
  </template>
  
  <script>
  import Tarifs from './Tarifs.vue';
  import Services from './Services.vue';
  import Customers from './Customers.vue';
  import Admins from './Admins.vue';
  
  export default {
    name: 'Tables',
    components: {
      Tarifs,
      Services,
      Customers,
      Admins
    }
  };
  </script>
  
  <style scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: relative;
  padding-top: 120px; /* Добавлено для отступа от абсолютно позиционированного заголовка */
}

.main-title {
  position: absolute;
  width: 441px;
  height: 58px;
  left: 420px;
  right: 419px;
  top: 46px;
  bottom: 696px;
  font-size: 48px;
  line-height: 58px;
  margin: 0;
  /* Дополнительные стили для центрирования текста */
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  font-size: 2em;
  margin-top: 40px;
  margin-bottom: 20px;
}

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
  border-radius: 4px;
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