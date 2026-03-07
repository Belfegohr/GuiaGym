package com.guiagym.data.api

import com.guiagym.data.modelo.Ejercicio
import com.guiagym.data.modelo.RespuestaLogin
import com.guiagym.data.modelo.RespuestaRegistro
import com.guiagym.data.modelo.Usuario
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.Header
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface ApiService {

    @POST("auth/registro")
    suspend fun registrar(@Body body: Map<String, Any>): Response<RespuestaRegistro>

    @POST("auth/login")
    suspend fun login(@Body body: Map<String, String>): Response<RespuestaLogin>

    @POST("auth/google")
    suspend fun loginConGoogle(@Body body: Map<String, String>): Response<RespuestaLogin>

    @GET("usuarios/mi_perfil")
    suspend fun obtenerMiPerfil(): Response<Usuario>

    @GET("ejercicios")
    suspend fun listarEjercicios(
        @Query("grupo_muscular") grupoMuscular: String? = null,
        @Query("dificultad") dificultad: String? = null
    ): Response<List<Ejercicio>>

    @GET("ejercicios/{id}")
    suspend fun obtenerEjercicio(@Path("id") id: Int): Response<Ejercicio>
}
