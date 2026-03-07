package com.guiagym.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val AzulPrincipal = Color(0xFF2196F3)
private val AzulOscuro = Color(0xFF1976D2)
private val FondoClaro = Color(0xFFF5F5F5)
private val FondoOscuro = Color(0xFF121212)

@Composable
fun FitnessAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) {
        darkColorScheme(
            primary = AzulPrincipal,
            secondary = AzulOscuro,
            background = FondoOscuro
        )
    } else {
        lightColorScheme(
            primary = AzulPrincipal,
            secondary = AzulOscuro,
            background = FondoClaro
        )
    }

    MaterialTheme(
        colorScheme = colorScheme,
        content = content
    )
}
