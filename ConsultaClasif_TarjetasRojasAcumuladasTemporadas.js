use("futbol");


//  Top 5 equipos con más tarjetas rojas acumuladas en todas las temporadas

db.clasificacion.aggregate([
  {
    $group: {
      _id: "$equipo",
      total_rojas: { $sum: "$tarjetas_rojas" }
    }
  },
  { $sort: { total_rojas: -1 } },
  { $limit: 5 }
]);