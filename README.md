# 🔎 Métodos de búsqueda bioinspirados: Colonia de Hormigas y Enfriamiento Simulado  

> Un proyecto académico sobre cómo la naturaleza inspira soluciones inteligentes para problemas complejos.

---

## Introducción

La naturaleza ha servido de modelo para crear algoritmos que resuelven problemas de optimización difíciles de abordar por métodos tradicionales. En este proyecto, exploramos dos técnicas bioinspiradas que han revolucionado la forma en que resolvemos problemas complejos:

### Colonia de hormigas (Ant Colony Optimization)

Inspirado en el comportamiento colectivo de las hormigas, este algoritmo simula cómo los individuos dejan rastros de feromonas para encontrar rutas óptimas hacia fuentes de alimento. Es ampliamente utilizado para resolver problemas como el del viajante (TSP) y otros retos combinatorios.

### Enfriamiento simulado (Simulated Annealing)

Basado en el proceso físico de enfriamiento de metales, este algoritmo busca soluciones óptimas aceptando, de forma controlada, soluciones peores para escapar de óptimos locales. Es una técnica poderosa para problemas de optimización con múltiples soluciones subóptimas.

---

## Problema de La Mochila (Knapsack Problem)

En este informe, ambas técnicas se aplican para resolver el **Problema de la Mochila**, un clásico problema de optimización combinatoria. El objetivo es seleccionar un subconjunto de objetos con diferentes valores y pesos, de modo que se maximice el valor total sin exceder la capacidad de la mochila.

Los algoritmos son evaluados en términos de eficiencia, calidad de la solución y comportamiento en múltiples ejecuciones, permitiendo comparar su desempeño en diferentes configuraciones experimentales.

---

## Instalación de librerías

Para ejecutar los algoritmos, necesitas tener Python instalado (recomendado: versión 3.8 o superior) y las siguientes librerías:

```bash
pip install pandas matplotlib openpyxl
o
pip install -r requirements.txt
```

## Ejecución de los scripts

Asegúrate de tener los archivos de datos correspondientes (.xlsx) en la misma carpeta donde están los scripts. Luego, ejecuta los programas en tu entorno de desarrollo preferido o desde tu terminal con los siguientes comandos:
```bash
python algorithm_aco.py
```
```bash
python algorithm_simulated_annealing.py
```

## Contribuidores 
Este proyecto fue desarrollado con la colaboración de:

>- [Carlos Lizarazo](https://github.com/CALR0)
>- [Carlos Romero](https://github.com/Carlos-RomeroRo)
>- [Javier Santodomingo](https://github.com/JavierS2)
