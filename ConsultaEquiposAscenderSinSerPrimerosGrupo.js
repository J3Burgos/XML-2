

use("futbol");

// Equipos que ascendieron pero no fueron primeros en su grupo

db.clasificacion.find({
  ascenso: true,
  posicion: { $ne: 1 }
}, {
  _id: 0,
  equipo: 1,
  temporada: 1,
  grupo: 1,
  posicion: 1,
  ascenso: 1
}).sort({ temporada: 1, grupo: 1, posicion: 1 });