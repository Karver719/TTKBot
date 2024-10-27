const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');

const app = express();
const port = 3000;

app.use(cors());
app.use(express.json());

const pool = new Pool({
  user: 'postgres',
  host: '192.168.30.92',
  database: 'TTKTarif',
  password: 'mypassword',
  port: 5435,
});

// Получение данных
app.get('/tarifs', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT * FROM tarifs');
    const data = result.rows;
    client.release();
    res.json(data);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.get('/services', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT * FROM services');
    const data = result.rows;
    client.release();
    res.json(data);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.get('/customers', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT * FROM customers');
    const data = result.rows;
    client.release();
    res.json(data);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.get('/admins', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('SELECT * FROM admins');
    const data = result.rows;
    client.release();
    res.json(data);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

// Добавление данных
app.post('/tarifs', async (req, res) => {
  try {
    const { name_tarif, inter_packet_mb, cost_tarif } = req.body;
    const client = await pool.connect();
    const result = await client.query(
      'INSERT INTO tarifs (name_tarif, inter_packet_mb, cost_tarif) VALUES ($1, $2, $3) RETURNING *',
      [name_tarif, inter_packet_mb, cost_tarif]
    );
    client.release();
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.post('/services', async (req, res) => {
  try {
    const { name_service, cost_service } = req.body;
    const client = await pool.connect();
    const result = await client.query(
      'INSERT INTO services (name_service, cost_service) VALUES ($1, $2) RETURNING *',
      [name_service, cost_service]
    );
    client.release();
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.post('/customers', async (req, res) => {
  try {
    const { num_dog, fio, telephone, mail } = req.body;
    const client = await pool.connect();
    const result = await client.query(
      'INSERT INTO customers (num_dog, fio, telephone, mail) VALUES ($1, $2, $3, $4) RETURNING *',
      [num_dog, fio, telephone, mail]
    );
    client.release();
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.post('/admins', async (req, res) => {
  try {
    const { login, fio, telephone, mail } = req.body;
    const client = await pool.connect();
    const result = await client.query(
      'INSERT INTO admins (login, fio, telephone, mail) VALUES ($1, $2, $3, $4) RETURNING *',
      [login, fio, telephone, mail]
    );
    client.release();
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

// Обновление данных
app.put('/tarifs/:id', async (req, res) => {
  try {
    const { name_tarif, inter_packet_mb, cost_tarif } = req.body;
    const client = await pool.connect();
    const result = await client.query(
      'UPDATE tarifs SET name_tarif = $1, inter_packet_mb = $2, cost_tarif = $3 WHERE id = $4 RETURNING *',
      [name_tarif, inter_packet_mb, cost_tarif, req.params.id]
    );
    client.release();
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.put('/services/:id', async (req, res) => {
  try {
    const { name_service, cost_service } = req.body;
    const client = await pool.connect();
    const result = await client.query(
      'UPDATE services SET name_service = $1, cost_service = $2 WHERE id = $3 RETURNING *',
      [name_service, cost_service, req.params.id]
    );
    client.release();
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.put('/customers/:id', async (req, res) => {
  try {
    const { num_dog, fio, telephone, mail } = req.body;
    const client = await pool.connect();
    const result = await client.query(
      'UPDATE customers SET num_dog = $1, fio = $2, telephone = $3, mail = $4 WHERE id = $5 RETURNING *',
      [num_dog, fio, telephone, mail, req.params.id]
    );
    client.release();
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.put('/admins/:id', async (req, res) => {
  try {
    const { login, fio, telephone, mail } = req.body;
    const client = await pool.connect();
    const result = await client.query(
      'UPDATE admins SET login = $1, fio = $2, telephone = $3, mail = $4 WHERE id = $5 RETURNING *',
      [login, fio, telephone, mail, req.params.id]
    );
    client.release();
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

// Удаление

// Удаление данных
app.delete('/tarifs/:id', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('DELETE FROM tarifs WHERE id = $1', [req.params.id]);
    client.release();
    res.json({ message: 'Tarif deleted' });
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.delete('/services/:id', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('DELETE FROM services WHERE id = $1', [req.params.id]);
    client.release();
    res.json({ message: 'Service deleted' });
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.delete('/customers/:id', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('DELETE FROM customers WHERE id = $1', [req.params.id]);
    client.release();
    res.json({ message: 'Customer deleted' });
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

app.delete('/admins/:id', async (req, res) => {
  try {
    const client = await pool.connect();
    const result = await client.query('DELETE FROM admins WHERE id = $1', [req.params.id]);
    client.release();
    res.json({ message: 'Admin deleted' });
  } catch (err) {
    console.error(err);
    res.send("Error " + err);
  }
});

// Эндпоинт для авторизации
app.post('/admins/login', async (req, res) => {
    try {
      const { login, password } = req.body;
      const client = await pool.connect();
      const result = await client.query(
        'SELECT * FROM admins WHERE login = $1 AND password = $2',
        [login, password]
      );
      client.release();
  
      if (result.rows.length > 0) {
        // Админ найден, генерируем токен (в реальном приложении используйте JWT)
        const token = 'your-token-here'; // Замените на реальный механизм генерации токена
        res.json({ success: true, token });
      } else {
        res.status(401).json({ success: false, message: 'Неверный логин или пароль' });
      }
    } catch (err) {
      console.error(err);
      res.status(500).send("Error " + err);
    }
  });

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});