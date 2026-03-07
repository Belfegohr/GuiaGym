package com.guiagym.data.modelo

import com.google.gson.annotations.SerializedName

data class RespuestaLogin(
    @SerializedName("token") val token: String,
    @SerializedName("usuario") val usuario: Usuario
)

data class RespuestaRegistro(
    @SerializedName("mensaje") val mensaje: String,
    @SerializedName("token") val token: String,
    @SerializedName("usuario") val usuario: Usuario
)
