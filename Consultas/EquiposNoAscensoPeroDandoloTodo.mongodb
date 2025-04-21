use("futbol");

// Equipos con más de 35 partidos jugados, más de 70 goles a favor y que NO ascendieron

db.clasificacion.find({
    partidos_jugados: { $gt: 35 },
    goles_favor: { $gt: 70 },
    ascenso: false
  }, {
    _id: 0,
    equipo: 1,
    temporada: 1,
    goles_favor: 1,
    puntos: 1,
    ascenso: 1
  }).sort({ goles_favor: -1 });
  