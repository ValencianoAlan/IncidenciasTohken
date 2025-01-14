const express = require('express'); // Importa Express
const bodyParser = require('body-parser'); // Importa body-parser
const cors = require('cors'); // Importa cors
const { connectToDatabase, sql } = require('./js/bd'); // Importa la conexión desde db.js

const app = express();
const port = 3000;

app.use(cors()); // Configura CORS
app.use(bodyParser.json()); // Configura Express para procesar datos JSON

// Ruta de login
app.post('/login', async (req, res) => {
  const { username, password } = req.body;

  try {
    const pool = await connectToDatabase(); // Reutiliza la conexión existente
    const result = await pool
      .request()
      .input('username', sql.NVarChar, username)
      .input('password', sql.NVarChar, password)
      .query('SELECT * FROM Credenciales WHERE Username = @username AND Password = @password');

    if (result.recordset.length > 0) {
      res.status(200).send({ message: 'Login exitoso' });
    } else {
      res.status(401).send({ message: 'Credenciales inválidas' });
    }
  } catch (err) {
    console.error('Error al procesar la solicitud:', err);
    res.status(500).send({ message: 'Error del servidor' });
  }
});

// Inicia el servidor
app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
