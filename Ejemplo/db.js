const sql = require('mssql'); // Importa la librería mssql

// Configuración de la conexión a la base de datos
const config = {
  user: 'sa', // Usuario de SQL Server
  password: 'root', // Contraseña del usuario
  server: 'localhost', // Dirección del servidor
  database: 'LoginApp', // Nombre de tu base de datos
  options: {
    encrypt: false, // Configuración para servidores locales
    enableArithAbort: true,
  },
};

let pool; // Variable para almacenar la conexión reutilizable

// Función para conectar a la base de datos
async function connectToDatabase() {
  if (!pool) {
    try {
      pool = await sql.connect(config); // Crea una nueva conexión si no existe
      console.log('Conexión exitosa a la base de datos.');
    } catch (err) {
      console.error('Error al conectar a la base de datos:', err);
      throw err;
    }
  }
  return pool; // Retorna la conexión existente
}

// Exporta la conexión y el objeto sql
module.exports = { connectToDatabase, sql };
