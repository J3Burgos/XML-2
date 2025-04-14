use("futbol");



//  Equipo con más goles a favor en la historia, EN UNA SOLA TEMPORADA

db.clasificacion.find(
  {},
  { _id: 0, equipo: 1, temporada: 1, goles_favor: 1 }
).sort({ goles_favor: -1 }).limit(1);
