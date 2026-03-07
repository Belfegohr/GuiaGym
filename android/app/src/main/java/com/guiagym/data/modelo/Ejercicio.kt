package com.guiagym.data.modelo

import com.google.gson.annotations.SerializedName

data class Ejercicio(
    @SerializedName("id_ejercicio") val idEjercicio: Int,
    @SerializedName("nombre") val nombre: String,
    @SerializedName("descripcion") val descripcion: String? = null,
    @SerializedName("grupo_muscular") val grupoMuscular: String? = null,
    @SerializedName("tipo_equipo") val tipoEquipo: String? = null,
    @SerializedName("dificultad") val dificultad: String? = null,
    @SerializedName("url_video") val urlVideo: String? = null
)
