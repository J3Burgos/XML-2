use("futbol");


// Ranking de equipos que no ascendieron pero quedaron en el Top 5 de su grupo,
//  ordenados por eficiencia ofensiva (goles por partido)
db.clasificacion.aggregate([
  {
    $match: {
      ascenso: false,
      posicion: { $lte: 5 }
    }
  },
  {
    $addFields: {
      goles_por_partido: {
        $round: [
          { $divide: ["$goles_favor", "$partidos_jugados"] },
          2
        ]
      }
    }
  },
  {
    $project: {
      _id: 0,
      equipo: 1,
      temporada: 1,
      grupo: 1,
      posicion: 1,
      puntos: 1,
      goles_favor: 1,
      partidos_jugados: 1,
      goles_por_partido: 1
    }
  },
  {
    $sort: {
      goles_por_partido: -1,
      puntos: -1
    }
  }
]);
