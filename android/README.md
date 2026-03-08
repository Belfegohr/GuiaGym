# GuiaGym - Android

App Android en Kotlin (Jetpack Compose). Sin Firebase. Abre directamente la pantalla principal.

## Abrir en Android Studio (para móvil)

1. Clona o descarga el repositorio
2. En Android Studio: **File → Open** → selecciona la carpeta del proyecto (la que contiene `build.gradle.kts`, `app/`, `settings.gradle.kts`)
3. Espera a que Gradle sincronice
4. Conecta tu móvil (depuración USB) o usa un emulador
5. Pulsa **Run** (▶)

## Requisitos

- Android Studio Ladybug (2024.2) o Hedgehog (2023.1.1) o superior
- JDK 17

## Ejecutar (con API)

1. Asegúrate de que la API esté corriendo (opcional):
   ```
   cd d:\TFG\backend
   python servidor.py
   ```

2. Abre Android Studio: `File > Open` → selecciona la carpeta `d:\TFG\android`

3. Espera a que Gradle sincronice (puede tardar unos minutos la primera vez)

4. Si falta el Gradle Wrapper: `File > Settings > Build > Gradle` y usa el Gradle embebido de Android Studio

5. Ejecuta la app: Run (▶) en emulador o dispositivo conectado

## Usar en dispositivo físico

Cambia la URL en `RetrofitCliente.kt`:
- Emulador: `http://10.0.2.2:5000/`
- Dispositivo en tu red: `http://192.168.1.44:5000/` (usa la IP de tu PC)

## Datos de prueba

Ejecuta en el backend para tener ejercicios:
```
python scripts/insertar_ejercicios_prueba.py
```
