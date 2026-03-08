package com.guiagym.ui.navegacion

import androidx.compose.runtime.Composable
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.guiagym.ui.pantallas.*
import com.guiagym.ui.viewmodel.AuthViewModel
import com.guiagym.util.GestorToken

object Rutas {
    const val INICIO = "inicio"
    const val LOGIN = "login"
    const val REGISTRO = "registro"
    const val HOME = "home"
    const val EJERCICIOS = "ejercicios"
}

@Composable
fun NavegacionApp(
    authViewModel: AuthViewModel,
    gestorToken: GestorToken
) {
    val navController = rememberNavController()

    NavHost(
        navController = navController,
        startDestination = Rutas.HOME
    ) {
        composable(Rutas.HOME) {
            HomePantalla(
                authViewModel = authViewModel,
                onIrAEjercicios = { navController.navigate(Rutas.EJERCICIOS) },
                mostrarCerrarSesion = false
            )
        }

        composable(Rutas.EJERCICIOS) {
            EjerciciosPantalla(
                onVolver = { navController.popBackStack() }
            )
        }
    }
}
