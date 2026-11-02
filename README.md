# DataLab — Proyecto Integrador
**Espacio académico:** Lógica Computacional  
**Programa:** Ingeniería de Datos e Inteligencia Artificial  
**Institución:** Universidad Santo Tomás

## 1. Descripción

DataLab es un proyecto integrador que se construirá progresivamente durante las semanas 10 a 14 del espacio académico. Su propósito es aplicar los conceptos de programación estudiados y evolucionar una misma solución para procesar registros.

El proyecto **no comienza desde cero en la semana 10**. Se parte de una base de código que recoge los conocimientos y funcionalidades trabajados durante las semanas 1 a 9. Cada entrega incorpora nuevos conceptos y conserva lo desarrollado anteriormente.

## 2. Repositorio base

El repositorio oficial que el docente utilizará como línea base del proyecto es:

<https://github.com/jarb-santoto/proyecto_red_iot>

El repositorio se encuentra inicialmente vacío. El docente y los estudiantes construirán progresivamente su estructura y código fuente.

### Crear el repositorio del equipo

1. Ingresar al repositorio base compartido por el docente.
2. Seleccionar **Use this template** y luego **Create a new repository**.
3. Crear un repositorio independiente para el equipo, con el nombre indicado por el docente.
4. Un integrante crea el repositorio y agrega a sus compañeros desde **Settings → Collaborators**.
5. Cada integrante clona el repositorio del equipo (no el repositorio base del docente).

**No se debe trabajar directamente sobre el repositorio del docente.** Cada equipo tendrá su propio repositorio.

## 3. Organización del equipo

- Los equipos tendrán máximo **tres estudiantes**.
- Todos los integrantes deben participar en programación, integración y pruebas.
- Los roles de desarrollo, pruebas, integración y revisión deben rotar entre las entregas.
- Ningún integrante tendrá como única responsabilidad la documentación o la administración del repositorio.
- Cada estudiante debe poder explicar individualmente el código integrado.

## 4. Entregas del proyecto

| Semana | Entrega | Versión | Alcance principal |
|---|---|---|---|
| 10 | Proyecto Integrador 1 | DataLab 1.0 | Cadenas, normalización y validación de registros |
| 11 | Proyecto Integrador 2 | DataLab 1.1 | Manejo de errores y excepciones |
| 12 | Proyecto Integrador 3 | DataLab 1.2 | Lectura de archivos CSV y carga de datos |
| 13 | Proyecto Integrador 4 | DataLab 1.3 | Módulos y refactorización |
| 14 | Proyecto Integrador 5 | DataLab 1.4 | Pruebas integrales, documentación y sustentación |

Cada entrega amplía la versión anterior. No se deben crear cinco proyectos independientes ni eliminar funcionalidades que ya estén implementadas.

## 5. Herramientas de desarrollo

Se puede trabajar con cualquiera de estos entornos:

- **Visual Studio Code (VS Code):** <https://code.visualstudio.com/>
- **PyCharm:** <https://www.jetbrains.com/pycharm/>

También se requiere:

- Python, en la versión que indique el docente.
- Git, para el control de versiones.
- Una cuenta de GitHub y acceso al repositorio del equipo.

El editor es una elección del estudiante. La estructura del proyecto y los comandos deben funcionar independientemente de que se utilice VS Code o PyCharm.

## 6. Preparación del entorno

### 6.1. Verificar Python y Git

En una terminal, ejecutar:

```bash
python --version
git --version
```

En algunos sistemas Windows, el comando de Python puede ser:

```powershell
py --version
```

Si alguno de los comandos no se reconoce, se debe instalar la herramienta correspondiente y verificar que esté disponible en el PATH del sistema.

### 6.2. Clonar el repositorio del equipo

Una vez creado el repositorio del equipo en GitHub:

```bash
git clone URL_DEL_REPOSITORIO_DEL_EQUIPO
cd NOMBRE_DEL_REPOSITORIO
```

Reemplazar los valores de ejemplo por la URL y el nombre reales del repositorio del equipo.

### 6.3. Crear un entorno virtual

Se recomienda utilizar un entorno virtual para aislar las dependencias del proyecto.

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

**Linux o macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Cuando el entorno esté activo, el nombre `(.venv)` suele aparecer al inicio de la línea de comandos.

Para salir del entorno virtual:

```bash
deactivate
```

> Si el docente entrega un archivo de dependencias (`requirements.txt`), instalar las dependencias dentro del entorno virtual con `pip install -r requirements.txt`. No instalar paquetes adicionales sin verificar que sean necesarios para la entrega.

## 7. Flujo de trabajo con Git y GitHub

La rama `main` debe mantenerse estable. Cada tarea se desarrolla en una rama independiente.

Ejemplo:

```bash
git switch main
git pull
git switch -c feature/normalizar-registros
```

Después de implementar y probar los cambios:

```bash
git status
git add .
git commit -m "Agrega normalizacion de registros"
git push -u origin feature/normalizar-registros
```

A continuación, abrir un **Pull Request (PR)** en GitHub hacia `main`. Otro integrante debe revisar los cambios, solicitar ajustes cuando sea necesario y aprobar la integración.

Convenciones sugeridas para ramas:

- `feature/`: nueva funcionalidad.
- `fix/`: corrección de errores.
- `refactor/`: reorganización del código sin cambiar su comportamiento esperado.
- `test/`: creación o ajuste de pruebas.
- `docs/`: documentación.

Conviene realizar commits pequeños, relacionados con un cambio concreto y con mensajes descriptivos.

## 8. Criterios generales de desarrollo

1. Respetar los conceptos estudiados hasta la semana correspondiente.
2. Reutilizar las funciones existentes; no duplicar lógica.
3. Mantener las funcionalidades de las entregas anteriores.
4. Probar los escenarios correctos e incorrectos definidos para cada entrega.
5. Separar progresivamente la lectura de datos, el procesamiento y la presentación.
6. Revisar los cambios de otro integrante antes de integrarlos.
7. Asegurar que todos los integrantes comprendan el código.

La función `clasificar_valor(valor)` que forme parte de la base entregada deberá reutilizarse cuando corresponda, evitando implementar nuevamente la misma lógica de clasificación.

## 9. Interfaz de visualización

La interfaz de visualización y prueba se apoyará en **Streamlit**, preparada principalmente por el docente. El trabajo central de los estudiantes estará en implementar y conectar la lógica de procesamiento, además de verificar su funcionamiento.

No se espera que los equipos dediquen el esfuerzo principal a diseñar o desarrollar la interfaz gráfica.

## 10. Estado del README

Este README presenta las instrucciones generales de inicio y colaboración. Los comandos específicos para ejecutar la aplicación, la estructura definitiva de carpetas y las dependencias se completarán cuando se incorpore la base de código del proyecto.

---

**DataLab — Proyecto Integrador de Lógica Computacional**  
Universidad Santo Tomás · Ingeniería de Datos e Inteligencia Artificial
