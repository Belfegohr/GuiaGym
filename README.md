# GuiaGym

App de rutinas de ejercicios. Así se pone en marcha.

---

## 1. Abrir el servidor (backend)

El servidor es lo que hace funcionar todo. Sin él, la app no va.

1. Abre una terminal en la carpeta del proyecto.
2. Escribe:
   ```
   cd backend
   python -m pip install -r requirements.txt
   python servidor.py
   ```
3. Si ves algo como "Running on http://...", está bien. No lo cierres.

---

## 2. Abrir la app en el móvil/emulador

1. Abre **Android Studio**.
2. `File` → `Open` → elige la carpeta `android`.
3. Espera a que cargue (puede tardar).
4. Pulsa el botón verde ▶ (Run).
5. Elige un emulador o móvil conectado.

---

## Si quieres usar "Continuar con Google"

Necesitas el archivo `google-services.json`:

1. Entra en [Firebase Console](https://console.firebase.google.com).
2. Abre tu proyecto.
3. Configuración (⚙️) → **Tus apps** → descarga `google-services.json`.
4. Pon ese archivo dentro de `android/app/`.

---

## Resumen rápido

| Qué quieres hacer | Qué tienes que hacer |
|-------------------|----------------------|
| Poner el servidor | `cd backend` → `python servidor.py` |
| Poner la app      | Abrir `android` en Android Studio → ▶ Run |
