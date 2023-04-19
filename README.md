# Productor-Consumidor
Implementar un merge concurrente:

- Tenemos NPROD procesos que producen nÃºmeros no negativos de forma

creciente. Cuando un proceso acaba de producir, produce un -1. 

Cada proceso almacena el valor almacenado en una variable compartida con el consumidor,

un -2 indica que el almacÃ©n estÃ¡ vacÃ­o.

- Hay un proceso merge que debe tomar los nÃºmeros y almacenarlos de

forma creciente en una Ãºnica lista (o array). El proceso debe esperar a que

los productores tengan listo un elemento e introducir el menor de

ellos.

- Se debe crear listas de semÃ¡foros. Cada productor solo maneja los

sus semÃ¡foros para sus datos. El proceso merge debe manejar todos los

semÃ¡foros.

- OPCIONAL: mente se puede hacer un bÃºffer de tamaÃ±o fijo de forma que

los productores ponen valores en el bÃºffer.
