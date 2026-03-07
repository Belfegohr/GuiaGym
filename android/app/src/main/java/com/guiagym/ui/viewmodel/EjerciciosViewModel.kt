package com.guiagym.ui.viewmodel

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.guiagym.data.api.RetrofitCliente
import com.guiagym.data.modelo.Ejercicio
import com.guiagym.util.GestorToken
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

data class EstadoEjercicios(
    val ejercicios: List<Ejercicio> = emptyList(),
    val cargando: Boolean = false,
    val error: String? = null
)

class EjerciciosViewModel(application: Application) : AndroidViewModel(application) {

    private val gestorToken = GestorToken(application)

    private val _estado = MutableStateFlow(EstadoEjercicios())
    val estado: StateFlow<EstadoEjercicios> = _estado.asStateFlow()

    fun cargarEjercicios() {
        viewModelScope.launch {
            val token = gestorToken.obtenerTokenSincrono() ?: return@launch
            _estado.value = _estado.value.copy(cargando = true, error = null)
            try {
                val api = RetrofitCliente.crearApiConToken(token)
                val response = api.listarEjercicios()
                if (response.isSuccessful) {
                    _estado.value = _estado.value.copy(
                        ejercicios = response.body() ?: emptyList(),
                        cargando = false,
                        error = null
                    )
                } else {
                    _estado.value = _estado.value.copy(
                        cargando = false,
                        error = "Error al cargar ejercicios"
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
}
