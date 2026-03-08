package com.guiagym.ui.pantallas

import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.guiagym.ui.viewmodel.AuthViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomePantalla(
    authViewModel: AuthViewModel,
    onIrAEjercicios: () -> Unit,
    mostrarCerrarSesion: Boolean = true,
    onCerrarSesion: () -> Unit = {}
) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("GuiaGym", fontWeight = FontWeight.Bold) },
                actions = {
                    if (mostrarCerrarSesion) {
                        TextButton(onClick = {
                            authViewModel.cerrarSesion()
                            onCerrarSesion()
                        }) {
                            Text("Cerrar sesión")
                        }
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = "¡Bienvenido!",
                style = MaterialTheme.typography.headlineMedium
            )
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = "Tu app de rutinas personalizadas",
                style = MaterialTheme.typography.bodyLarge
            )
            Spacer(modifier = Modifier.height(48.dp))

            Button(
                onClick = onIrAEjercicios,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Ver ejercicios")
            }

            Spacer(modifier = Modifier.height(16.dp))

            OutlinedButton(
                onClick = onIrAEjercicios,
                modifier = Modifier.fillMaxWidth()
            ) {
                Text("Mis rutinas (próximamente)")
            }
        }
    }
}
