package com.guiagym.ui.navegacion

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
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
    val tokenActual by gestorToken.token.collectAsState(initial = null)

    LaunchedEffect(tokenActual) {
        if (tokenActual != null) {
            navController.navigate(Rutas.HOME) {
                popUpTo(Rutas.INICIO) { inclusive = true }
            }
        }
    }

    NavHost(
        navController = navController,
        startDestination = Rutas.INICIO
    ) {
        composable(Rutas.INICIO) {
            if (tokenActual != null) {
                Box(Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else {
                LoginPantalla(
                    onLoginExitoso = {
                        navController.navigate(Rutas.HOME) {
                            popUpTo(Rutas.INICIO) { inclusive = true }
                        }
                    },
                    onIrARegistro = { navController.navigate(Rutas.REGISTRO) }
                )
            }
        }
        composable(Rutas.REGISTRO) {
            RegistroPantalla(
                onRegistroExitoso = {
                    navController.navigate(Rutas.HOME) {
                        popUpTo(Rutas.REGISTRO) { inclusive = true }
                    }
                },
                onIrALogin = { navController.popBackStack() }
            )
        }

        composable(Rutas.HOME) {
            HomePantalla(
                authViewModel = authViewModel,
                onIrAEjercicios = { navController.navigate(Rutas.EJERCICIOS) },
                onCerrarSesion = {
                    navController.navigate(Rutas.INICIO) {
                        popUpTo(0) { inclusive = true }
                    }
                }
            )
        }

        composable(Rutas.EJERCICIOS) {
            EjerciciosPantalla(
                onVolver = { navController.popBackStack() }
            )
        }
    }
}
