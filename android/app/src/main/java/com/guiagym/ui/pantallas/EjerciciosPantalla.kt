package com.guiagym.ui.pantallas

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.guiagym.data.modelo.Ejercicio
import com.guiagym.ui.viewmodel.EjerciciosViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun EjerciciosPantalla(
    onVolver: () -> Unit,
    viewModel: EjerciciosViewModel = viewModel()
) {
    val estado by viewModel.estado.collectAsState()

    LaunchedEffect(Unit) {
        viewModel.cargarEjercicios()
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Ejercicios", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    TextButton(onClick = onVolver) {
                        Text("← Volver")
                    }
                }
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {
            estado.error?.let { error ->
                Card(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(16.dp),
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.errorContainer)
                ) {
                    Text(
                        text = error,
                        modifier = Modifier.padding(16.dp),
                        color = MaterialTheme.colorScheme.onErrorContainer
                    )
                }
            }

            if (estado.cargando) {
                Box(
                    modifier = Modifier.fillMaxSize(),
                    contentAlignment = androidx.compose.ui.Alignment.Center
                ) {
                    CircularProgressIndicator()
                }
            } else {
                if (estado.ejercicios.isEmpty()) {
                    Box(
                        modifier = Modifier.fillMaxSize(),
                        contentAlignment = androidx.compose.ui.Alignment.Center
                    ) {
                        Column(horizontalAlignment = androidx.compose.ui.Alignment.CenterHorizontally) {
                            Text("No hay ejercicios")
                            Text("Ejecuta el script de prueba en el backend", style = MaterialTheme.typography.bodySmall)
                        }
                    }
                } else {
                    LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(12.dp)
                    ) {
                        items(estado.ejercicios) { ejercicio ->
                            TarjetaEjercicio(ejercicio)
                        }
                    }
                }
            }
        }
    }
}

@Composable
fun TarjetaEjercicio(ejercicio: Ejercicio) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(
            modifier = Modifier.padding(16.dp)
        ) {
            Text(
                text = ejercicio.nombre,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            ejercicio.grupoMuscular?.let { grupo ->
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = grupo,
                    style = MaterialTheme.typography.bodySmall
                )
            }
            ejercicio.dificultad?.let { diff ->
                Text(
                    text = "Dificultad: $diff",
                    style = MaterialTheme.typography.bodySmall
                )
            }
            ejercicio.descripcion?.takeIf { it.isNotEmpty() }?.let { desc ->
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = desc,
                    style = MaterialTheme.typography.bodyMedium
                )
            }
        }
    }
}
