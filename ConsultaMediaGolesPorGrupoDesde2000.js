use("futbol");

// Media de goles a favor por grupo en temporadas posteriores al año 2000

db.clasificacion.aggregate([
    {
      $match: {
        temporada: { $regex: "^20" }  // Temporadas desde 2000 en adelante
      }
    },
    {
      $group: {
        _id: "$grupo",
        media_goles_favor: { $avg: "$goles_favor" },
        equipos: { $sum: 1 }
      }
    },
    { $sort: { media_goles_favor: -1 } }
  ]);