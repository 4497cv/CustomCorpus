# Representación de Texto en Espacio Vectorial

Este repositorio contiene la práctica de **Minería de Textos** realizada para el **INSTITUTO TECNOLÓGICO DE ESTUDIOS SUPERIORES DE OCCIDENTE**, enfocada en la **representación algebraica de textos mediante modelos de espacio vectorial**. El proyecto incluye herramientas para generar matrices de Bag of Words, TF-IDF y calcular métricas de similitud entre documentos como la distancia coseno y euclidiana.

## Autor
- **César Villarreal Hernández**, 707560  
- Curso: Minería de Textos  
- Profesor: Dr. Víctor Hugo Zaldivar Carrillo  
- Fecha: Miércoles 25 de febrero de 2026

## Objetivo
Representar diversos textos de forma algebraica como **Vector Space Models** y medir la similitud entre documentos utilizando diferentes métricas:  

- Matriz Bag of Words (presencia/ausencia y conteo)  
- TF-IDF  
- Distancia coseno y euclidiana  

## Descripción del Proyecto
1. **Construcción del vocabulario:**  
   - Se procesaron artículos de *The Guardian* para extraer un conjunto único de palabras, asegurando consistencia mediante preprocesamiento (normalización y limpieza de texto).

2. **Bag of Words (BoW):**  
   - Se generaron matrices de BoW a partir del vocabulario, tanto binarias (presencia/ausencia) como por conteo, guardadas en archivos CSV para su análisis posterior.

3. **TF-IDF:**  
   - A partir de la matriz BoW, se calculó la importancia relativa de cada término en relación con todo el corpus.

4. **Métricas de similitud:**  
   - Se calcularon las distancias coseno y euclidianas para cuantificar la similitud entre documentos.

## Alcances y Limitaciones
- BoW binaria: útil para identificar la presencia de términos comunes entre documentos.  
- BoW con conteo: más adecuado para identificar palabras clave frecuentes.  
- TF-IDF: permite distinguir términos relevantes que diferencian los documentos.  
- Limitación: La calidad de la representación depende de la limpieza y normalización previa del corpus.

## Conclusiones
- Se logró construir un vocabulario consistente y generar matrices BoW y TF-IDF.  
- La comparación entre documentos mediante distancias coseno y euclidianas permitió medir la similitud de manera efectiva.  
- El proyecto demuestra cómo los modelos de espacio vectorial permiten representar textos algebraicamente y extraer información relevante de un corpus.

## Bibliografía
- Real Academia Española. (s. f.). **CORPES XXI**. [https://www.rae.es/banco-de-datos/corpes-xxi](https://www.rae.es/banco-de-datos/corpes-xxi)
