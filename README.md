# contasaurioBot

## Descripción

Bot de Telegram para controlar la recepción de documentos, control de timbrados, color de carpetas y más cosas.

Contasario va ser capaz de guardar los mensajes de recepcion de los documentos en un excel, los guardará por:

- Id
- Fecha
- Cliente - nombre y apellido
- Recepcion de documento: que contará con dos opciones:
    - Recepción
    - Retiro
- Vencimiento de Timbrado: deberá enviar un mensaje 30 dias antes de su vencimiento, avisando así la caducidad del mismo.

## Funciones

- /ayuda
    - Tendrá todas la funciones enlistadas
- /nuevocliente
    - nombre y apellido
- /listaclientes

### Editar Clientes

- /agregartimbrado
    - N°
    - fecha fin
- /recepciondocumentos
    - obs
    - /retirodocumentos
        - obs
- /colorcarpeta
- /export
- Formatea y exporta en zip los archivos para adjuntar a la R-90
