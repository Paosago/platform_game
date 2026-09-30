DOCUMENTACIÓN DEL PROYECTO: TACTICAL CAPI

1. DESCRIPCIÓN TÉCNICA Y BIBLIOTECAS UTILIZADAS

El proyecto es un videojuego de plataformas en 2D desarrollado bajo las normativas de estilo PEP 8 y estructurado mediante programación 
orientada a objetos. El entorno de desarrollo depende exclusivamente de las siguientes bibliotecas:

- Pygame Zero (pgzero): Motor gráfico y lógico principal utilizado para la gestión del ciclo de juego (game loop), 
renderización de sprites (mediante la clase Actor), manejo de eventos de entrada (teclado y eventos de ratón) y 
reproducción del sistema de audio.

- Math: Biblioteca estándar de Python implementada para cálculos trigonométricos. Específicamente, se utiliza la función math.
Sin para generar físicas de flotación fluidas y dinámicas en los objetos interactivos.

- Pygame (Uso restringido): La única directiva utilizada es la importación de la clase geométrica Rect (from pygame import Rect). 
Su implementación fue estrictamente necesaria para generar hitboxes (cajas de colisión) personalizados e independientes de las dimensiones 
visuales de los sprites, garantizando interacciones y físicas precisas.

2. REQUISITOS DEL SISTEMA

- Intérprete de Python 3.x.

Dependencia principal: Pygame Zero. Para su instalación mediante el gestor de paquetes de Python, ejecutar en consola: pip install pgzero
Nota: en sistemas como macOS o Linux, puede ser necesario utilizar: pip3 install pgzero 

3. INSTRUCCIONES DE DESPLIEGUE Y EJECUCIÓN

- Abrir la terminal del sistema o la consola integrada del editor de código.(ejemplo:Visual Studio Code)

- Paso opcional: Si el proyecto se está ejecutando dentro de un entorno virtual (venv), 
  asegúrese de que el entorno esté activo antes de continuar.

- Navegar hasta el directorio raíz del proyecto (la carpeta principal llamada (juego), que contiene el script de ejecución y 
  los subdirectorios de recursos como images/ y music/).

- Inicializar el entorno gráfico ejecutando el siguiente comando: pgzrun main.py

NOTA: Si la terminal arroja un error indicando que "pgzrun no se reconoce como un comando", 
puede ejecutar el juego directamente a través del módulo de Python utilizando:

python -m pgzero main.py o python3 -m pgzero main.py

4. CONTROLES Y NAVEGACIÓN

- Navegación de Menú: Interacción estándar por eventos de puntero (Ratón / Clic izquierdo).

- Desplazamiento Lateral: Flecha direccional Izquierda (Left) / Flecha direccional Derecha (Right).

- Mecánica de Salto: Flecha direccional Arriba (Up).

5. MECÁNICAS DE JUEGO (VICTORIA Y DERROTA)

Condición de Victoria: El nivel se considera completado exitosamente cuando el jugador logra evadir los obstáculos, 
escalar el sistema de plataformas y realizar contacto directo con el botín (recompensa flotante) ubicado en la cima 
de la torre estructural final.

Condición de Derrota: El ciclo de juego se interrumpe y cambia al estado de finalización (Game Over) si el personaje principal 
intercepta el área de los pelicanos o del caimán  (guardias en estado de patrullaje o estáticos) 
distribuida a lo largo del nivel.