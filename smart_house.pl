% Eficientizacion de recursos.

% Tipos de dispositivos
tipo_disp(refrigeracion).
tipo_disp(limpieza).
tipo_disp(entretenimiento).

% Tipos de lugares/habitaciones
tipo_hab(cocina).
tipo_hab(dormitorio).
tipo_hab(sala).
tipo_hab(patio).
tipo_hab(marquesina).

% Definicion de hecho dispositivo para decir los que existen en diferentes lugares de la casa

ver_pregunta(X):- write(X), write('(si/no)? ').
pregunta(X, Respuesta):- ver_pregunta(X), read(Respuesta).

resp_disp(si, X):- !, assertz(dispositivos(X)).
resp_disp(no, _):- !, write('No se acepta ese dispositivo en esa habitacion.'), fail.

tipos(tipo_hab(X)).
tipos(tipo_disp(X)).

:-dynamic dispositivos/1.
agregar_dispositivo(Disp):- tipos(Disp), 

% Definicion de hecho lugar para decir los lugares que existen en la casa
% Prototipo: lugar(<lugar>).
lugar(sala_estar).
lugar(cocina).
lugar(terraza).
lugar(marquesina).
lugar(habitacionX).
lugar(escalera).
lugar(garage).
lugar(baño_habitacionX).
lugar(patio).
lugar(quiosco).

% Definicion de hecho tiene para decir que dispositivo tiene cada lugar
% Prototipo: tiene(<lugar>, <dispositivo>).
tiene(cocina, lavaplatos).
tiene(cocina, microondas).
tiene(cocina, cafetera).
tiene(cocina, refrigerador).
tiene(cocina, luz).
tiene(baño_habitacionX, toilet).
tiene(baño_habitacionX, ducha).
tiene(baño_habitacionX, jacuzzi).
tiene(baño_habitacionX, luz).
tiene(habitacionX, aire_acondicionado).
tiene(habitacionX, calefaccion).
tiene(habitacionX, computador).
tiene(habitacionX, television).
tiene(habitacionX, radio).
tiene(habitacionX, luz).

% Definicion de acciones que tienen los dispositivos
% Prototipo: accion(<dispositivo>, <accion>).
accion(luz, power).
accion(aire_acondicionado, power).
accion(aire_acondicionado, subir_temp).
accion(aire_acondicionado, bajar_temp).
accion(television, power).
accion(television, subir_vol).
accion(television, bajar_vol).
accion(television, subir_canal).
accion(television, bajar_canal).
accion(radio, subir_vol).
accion(radio, bajar_vol).
accion(microondas, power).
accion(microondas, set_timer('tiempo')).
accion(microondas, iniciar).

% Definicion de funciones especificas para algunos dispositivos especiales
% No hay prototipo porque podrian ser unicas todas

set_timer(X):- number(X).

% Para poder verificar el uso/consumo de algun dispositivo se necesita un hecho dinamico
% Prototipo dinamico: consumo(<cantidad>, <dispositivo>).
:-dynamic consumo/2.

insertar_consumo(Consumo, Dispositivo):- retract(consumo(_, Dispositivo)), assertz(consumo(Consumo, Dispositivo)).

% Para tomar acciones en base a consumo se usaran las siguientes reglas
% ---

% Para modificar temperatura interna se utilizara calefaccion y aire acondicionado
% Se debe chequear si la temperatura esta por debajo de 20 grados celcius para prender la calefaccion
% y si esta por encima de 26 para prender el aire acondicionado.

% Para el control del agua se puede abrir o cerrar llaves y tambien enviar el consumo de esta a los usuarios
% Verificar la cercania de los usuarios para cerrar automaticamente las llaves que se dejen abiertas

% Para poder trackear la ubicacion de una persona se utilizara un hecho dinamico.
% Prototipo dinamico: ubicacion(<persona>, <lugar>).
:-dynamic ubicacion/2.

insertar_ubicacion(Persona, Lugar):- retract(ubicacion(Persona, _)), assertz(ubicacion(Persona, Lugar)).
