package com.guiagym.ui.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.guiagym.data.api.RetrofitCliente
import com.guiagym.util.GestorToken
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

data class EstadoAuth(
    val token: String? = null,
    val cargando: Boolean = false,
    val error: String? = null
)

class AuthViewModel(application: Application) : AndroidViewModel(application) {

    private val gestorToken = GestorToken(application)
    private val api = RetrofitCliente.crearApi()

    private val _estado = MutableStateFlow(EstadoAuth())
    val estado: StateFlow<EstadoAuth> = _estado.asStateFlow()

    init {
        viewModelScope.launch {
            gestorToken.token.collect { token ->
                _estado.value = _estado.value.copy(token = token)
            }
        }
    }

    fun login(email: String, contraseña: String) {
        viewModelScope.launch {
            _estado.value = _estado.value.copy(cargando = true, error = null)
            try {
                val response = api.login(mapOf(
                    "email" to email,
                    "contraseña" to contraseña
                ))
                if (response.isSuccessful) {
                    val body = response.body()!!
                    gestorToken.guardarToken(body.token)
                    _estado.value = _estado.value.copy(cargando = false, token = body.token, error = null)
                } else {
                    val errorBody = response.errorBody()?.string() ?: "Error desconocido"
                    _estado.value = _estado.value.copy(
                        cargando = false,
                        error = "Email o contraseña incorrectos"
                    )
                }
            } catch (e: Exception) {
                _estado.value = _estado.value.copy(
                    cargando = false,
                    error = "Error de conexión: ${e.message}"
                )
            }
        }
    }

    fun registrar(nombre: String, email: String, contraseña: String) {
        viewModelScope.launch {
            _estado.value = _estado.value.copy(cargando = true, error = null)
            try {
                val response = api.registrar(mapOf(
                    "nombre" to nombre,
                    "email" to email,
                    "contraseña" to contraseña
                ))
                if (response.isSuccessful) {
                    val body = response.body()!!
                    gestorToken.guardarToken(body.token)
                    _estado.value = _estado.value.copy(cargando = false, token = body.token, error = null)
                } else {
                    val errorBody = response.errorBody()?.string() ?: ""
                    _estado.value = _estado.value.copy(
                        cargando = false,
                        error = "El email ya está registrado o datos incorrectos"
                    )
                }
            } catch (e: Exception) {
                _estado.value = _estado.value.copy(
                    cargando = false,
                    error = "Error de conexión: ${e.message}"
                )
            }
        }
    }

    fun cerrarSesion() {
        viewModelScope.launch {
            gestorToken.limpiarToken()
            _estado.value = EstadoAuth()
        }
    }

    fun loginConGoogle(idToken: String) {
        viewModelScope.launch {
            _estado.value = _estado.value.copy(cargando = true, error = null)
            try {
                val response = api.loginConGoogle(mapOf("id_token" to idToken))
                if (response.isSuccessful) {
                    val body = response.body()!!
                    gestorToken.guardarToken(body.token)
                    _estado.value = _estado.value.copy(cargando = false, token = body.token, error = null)
                } else {
                    _estado.value = _estado.value.copy(
                        cargando = false,
                        error = "Error al iniciar sesión con Google"
                    )
                }
            } catch (e: Exception) {
                _estado.value = _estado.value.copy(
                    cargando = false,
                    error = "Error: ${e.message}"
                )
            }
        }
    }

    fun limpiarError() {
        _estado.value = _estado.value.copy(error = null)
    }

    fun hayToken(): Boolean = runBlocking { gestorToken.obtenerTokenSincrono() != null }
}
