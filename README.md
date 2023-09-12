# Ruleta de Casino en Python

Este proyecto es una simulación de una ruleta de casino en Python. Permite a los jugadores realizar apuestas en números y colores, y simula el giro de la ruleta para determinar los resultados.

## Requisitos

Para ejecutar este proyecto, necesitarás tener instaladas las siguientes bibliotecas de Python:

- `pygame`: Biblioteca para crear juegos en 2D. Se utiliza para la interfaz gráfica.

## Instalación

Puedes instalar las bibliotecas requeridas utilizando `pip`, el administrador de paquetes de Python. Ejecuta los siguientes comandos en tu terminal:

```bash
pip install pygame
```

## Uso

1. Ejecutar el programa

2. Aparecera una ventana en la cual se mostraran dos opciones:

   ![imagen_2023-09-12_165553190](https://github.com/programadorisgod/Ruleta-Espanola/assets/116904412/0104f7cd-99bf-4144-80d3-f9b94b744daa)

3. En el `Modo Estándar` cada ficha tendra un valor de $10.000, mientras que en el `Modo Premium` cada ficha tiene un valor de $50.000

4. Despues de seleccionar el modo de juego, se mostrara el juego:

   ![imagen_2023-09-12_170043908](https://github.com/programadorisgod/Ruleta-Espanola/assets/116904412/628e953e-5aad-4beb-943a-ba6fce803fc1)
   
5. Al iniciar el juego, cada jugador tendra 5 fichas como se muestra en la derecha, y el monto de cada jugador se podra ver a la izquierda de la ventana

   ![267477097-7923a88d-5205-49b6-90aa-e7498b33feb9 (2)](https://github.com/programadorisgod/Ruleta-Espanola/assets/116904412/d942332d-8cec-42c6-bc1d-f442adc3cd70)

6. El juego funciona dando `Click izquierdo` sobre una ficha para seleccionarla o `Click derecho` para seleccionar 4 a la vez:

   ![267477097-7923a88d-5205-49b6-90aa-e7498b33feb9 (1)](https://github.com/programadorisgod/Ruleta-Espanola/assets/116904412/336b8090-2dc8-47bf-ac4c-4a2af0c1668a)

7. Despues de haber seleccionado alguna ficha, se podra poner en el tablero de apuestas con `Click izquierdo`:

   ![267477097-7923a88d-5205-49b6-90aa-e7498b33feb9 (3)](https://github.com/programadorisgod/Ruleta-Espanola/assets/116904412/3b61768f-8869-4af6-b88b-a22a011bcb92)

8. Igualmente se podran retirar las fichas del tablero de apuestas con `Click izquierdo` para una y `Click derecho` para 4, sobre las fichas que se quieran retirar:
   
   ![267477097-7923a88d-5205-49b6-90aa-e7498b33feb9](https://github.com/programadorisgod/Ruleta-Espanola/assets/116904412/3e5bb95a-2311-425d-a529-3db75af2de5f)

9. Las apuestas disponibles son:
    - *Numero especifico*
      - El pago es de 35:1 es decir, 35 fichas mas la apostada (36)
    - *1 a 18* / *19 a 36*
      - El pago es de 1:1 es decir, 1 ficha mas la apostada (2)
    - *Rojo* / *Negro*
      - El pago es de 1:1 es decir, 1 ficha mas la apostada (2)
    - *Par* / *Impar*
      - El pago es de 1:1 es decir, 1 ficha mas la apostada (2)
        
       Cada apuesta de cada ficha es individual y se pueden ganar varias apuestas en un giro.

10. Ahora solo queda hacer apuestas y girar la ruleta; la ruleta se gira dando `Click izquierdo` en el borde de la ruleta:

    ![267477097-7923a88d-5205-49b6-90aa-e7498b33feb9 (4)](https://github.com/programadorisgod/Ruleta-Espanola/assets/116904412/ecafacc5-ac2d-45fa-b536-0234f9b1ef78)

11. Al finalizar de girar la ruleta, se podra ver en que numero de la ruleta cayo la bola, y a la izquierda saldran los resultados de las apuestas:

    ![267477097-7923a88d-5205-49b6-90aa-e7498b33feb9 (5)](https://github.com/programadorisgod/Ruleta-Espanola/assets/116904412/f126d740-6147-4207-9770-7d75ee40d85d)


