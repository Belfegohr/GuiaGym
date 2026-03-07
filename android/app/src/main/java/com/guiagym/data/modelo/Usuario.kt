package com.guiagym.data.modelo

import com.google.gson.annotations.SerializedName

data class Usuario(
    @SerializedName("id_usuario") val idUsuario: Int,
    @SerializedName("nombre") val nombre: String,
    @SerializedName("email") val email: String? = null,
    @SerializedName("fecha_nacimiento") val fechaNacimiento: String? = null,
    @SerializedName("genero") val genero: String? = null,
    @SerializedName("altura") val altura: Double? = null,
    @SerializedName("peso_actual") val pesoActual: Double? = null,
    @SerializedName("objetivo") val objetivo: String? = null,
    @SerializedName("nivel_experiencia") val nivelExperiencia: String? = null,
    @SerializedName("fecha_registro") val fechaRegistro: String? = null
)
