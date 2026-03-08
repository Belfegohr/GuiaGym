package com.guiagym

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import com.guiagym.ui.navegacion.NavegacionApp
import com.guiagym.ui.theme.FitnessAppTheme
import com.guiagym.util.GestorToken

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            FitnessAppTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    val authViewModel: com.guiagym.ui.viewmodel.AuthViewModel = viewModel()
                    val gestorToken = GestorToken(applicationContext)
                    NavegacionApp(
                        authViewModel = authViewModel,
                        gestorToken = gestorToken
                    )
                }
            }
        }
    }
}
