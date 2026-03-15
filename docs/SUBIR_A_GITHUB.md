# Cómo subir OmniStock a tu cuenta de GitHub

Sigue estos pasos para publicar el proyecto en tu GitHub.

---

## 1. Crear el repositorio en GitHub

1. Entra en **https://github.com** e inicia sesión.
2. Clic en **"+"** (arriba a la derecha) → **"New repository"**.
3. Configura:
   - **Repository name:** `OmniStock` (o el nombre que quieras).
   - **Description (opcional):** "Sistema de Gestión de Inventario y Ventas - Proyecto académico (ACA)".
   - **Visibilidad:** Public o Private.
   - **No** marques "Add a README", "Add .gitignore" ni "Choose a license" (el proyecto ya tiene archivos).
4. Clic en **"Create repository"**.
5. En la página del repo recién creado, copia la **URL del repositorio**, por ejemplo:
   - `https://github.com/TU_USUARIO/OmniStock.git`
   - o `git@github.com:TU_USUARIO/OmniStock.git` (SSH)

---

## 2. Abrir terminal en la carpeta del proyecto

En **PowerShell** o **CMD**:

```powershell
cd c:\NetBeans\AppCursos\OmniStock
```

---

## 3. Inicializar Git y hacer el primer commit

Si en esta carpeta **aún no hay** un repositorio Git, ejecuta:

```powershell
git init
git add .
git commit -m "Initial commit: OmniStock - Gestión de inventario y ventas (ACA)"
```

Si Git te pide configurar nombre y email (solo la primera vez):

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

---

## 4. Conectar con GitHub y subir

Sustituye `TU_USUARIO` y `OmniStock` por tu usuario de GitHub y el nombre del repo si lo cambiaste:

```powershell
git remote add origin https://github.com/TU_USUARIO/OmniStock.git
git branch -M main
git push -u origin main
```

Te pedirá **usuario y contraseña** de GitHub. Si usas autenticación en dos pasos, en lugar de la contraseña normal usa un **Personal Access Token** (GitHub → Settings → Developer settings → Personal access tokens).

**Si prefieres SSH** (y ya tienes clave configurada en GitHub):

```powershell
git remote add origin git@github.com:TU_USUARIO/OmniStock.git
git branch -M main
git push -u origin main
```

---

## 5. Comprobar

Entra en `https://github.com/TU_USUARIO/OmniStock` y verifica que aparecen todos los archivos del proyecto.

---

## Nota sobre contraseñas

El archivo `config.py` tiene la contraseña de MySQL en blanco. **No pongas tu contraseña real en `config.py` si vas a subir el repo a GitHub.** Cada quien debe usar su propio `config.py` en local. Si quieres, puedes crear un `config.example.py` con valores de ejemplo y añadir `config.py` al `.gitignore` para no subir datos sensibles; en ese caso documenta en el README que hay que copiar `config.example.py` a `config.py` y rellenar los datos.
