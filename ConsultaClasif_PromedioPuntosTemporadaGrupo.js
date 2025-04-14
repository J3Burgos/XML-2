use('futbol');

// Promedio de puntos por temporada solo del Grupo 1

db.clasificacion.aggregate([
    { $match: { grupo: 1 } },
    {
      $group: {
        _id: "$temporada",
        promedio_puntos: { $avg: "$puntos" }
      }
    },
    { $sort: { _id: 1 } }
  ]);