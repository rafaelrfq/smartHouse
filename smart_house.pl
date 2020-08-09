% Eficientizacion de recursos.

% hechos dinamicos
:-dynamic dispositivo/1.
:-dynamic lugar/1.
:-dynamic lugar/3.
:-dynamic dispositivo_lugar/2.
:-dynamic consumo/3.
:-dynamic ubicacion/2.
:-dynamic estado/3.

% Definicion de hecho dispositivo para decir los que existen en diferentes lugares de la casa

ver_pregunta(X):- write(X), write('(si/no)? ').
pregunta(X, Respuesta):- ver_pregunta(X), read(Respuesta).

resp_disp(si, X):- !, assertz(dispositivos(X)).
resp_disp(no, _):- !, write('No se acepta ese dispositivo en esa habitacion.'), fail.

agregar_dispositivo(X):- \+ (dispositivo(X)), assertz(dispositivo(X)).
% agregar_lugar(X):- \+ (lugar(X)), assertz(lugar(X)).
% agregar_disp_lugar(Disp, Lugar):- dispositivo(Disp), lugar(Lugar),
%                         \+ (dispositivo_lugar(Disp, Lugar)), assertz(dispositivo_lugar(Disp, Lugar)).

add_tail([],X,[X]).
add_tail([H|T],X,[H|L]):-add_tail(T,X,L).

agregar_lugar(Lugar,Tipo):-
    tipo(Tipo),
    retractall(lugar(Lugar,,)),
    assertz(lugar(Lugar, Tipo, [])).

agregar_disp_lugar(Disp, Lugar):-
    lugar(Lugar,T,L),
    add_tail(L,Disp, Lista),
    retract(lugar(Lugar,,)),
    asserta(lugar(Lugar,T,Lista)).


tipo(habitacion).
tipo(sala).
tipo(exterior).
tipo(cocina).
tipo(comedor).

% Definicion de hecho lugar para decir los lugares que existen en la casa en caso que no se 
% inserte uno por uno
% Prototipo: lugar(<lugar>).
% lugar(sala_estar).
% lugar(cocina).
% lugar(terraza).
% lugar(marquesina).
% lugar(habitacionX).
% lugar(escalera).
% lugar(garage).
% lugar(baño_habitacionX).
% lugar(patio).
% lugar(quiosco).

% Definicion de acciones que tienen los dispositivos
% Prototipo: accion(<dispositivo>, <accion>).
% accion(luz, power).
% accion(aire_acondicionado, power).
% accion(aire_acondicionado, subir_temp).
% accion(aire_acondicionado, bajar_temp).
% accion(television, power).
% accion(television, subir_vol).
% accion(television, bajar_vol).
% accion(television, subir_canal).
% accion(television, bajar_canal).
% accion(radio, subir_vol).
% accion(radio, bajar_vol).
% accion(microondas, power).
% accion(microondas, set_timer('tiempo')).
% accion(microondas, iniciar).

% Definicion de funciones especificas para algunos dispositivos especiales
% No hay prototipo porque podrian ser unicas todas

% set_timer(X):- number(X).

% Para poder verificar el uso/consumo de algun dispositivo se necesita un hecho dinamico
% Prototipo dinamico: consumo(<cantidad>, <dispositivo>).

insertar_consumo(Consumo, Dispositivo, Lugar, Resultado):- dispositivo_lugar(Dispositivo, Lugar), retract(consumo(_, Dispositivo, Lugar)), 
                                                           assertz(consumo(Consumo, Dispositivo, Lugar)), verificar_consumo(Consumo, Dispositivo, Lugar, Resultado), !.
% Si no existe el consumo, se hace esto:
insertar_consumo(Consumo, Dispositivo, Lugar, Resultado):- dispositivo_lugar(Dispositivo, Lugar), assertz(consumo(Consumo, Dispositivo, Lugar)),
                                                           verificar_consumo(Consumo, Dispositivo, Lugar, Resultado).

verificar_consumo(regular, _, _):- write('Se mantiene el mismo estado en el dispositivo'), !.
verificar_consumo(alto, Dispositivo, Lugar, Resultado):- retract(estado(Dispositivo, Lugar, _)), assertz(estado(Dispositivo, Lugar, 0)), 
                                                         Resultado = 'Se apago el dispositivo para eficientizar los recursos.'.
verificar_consumo(alto, Dispositivo, Lugar, Resultado):- assertz(estado(Dispositivo, Lugar, 0)), Resultado = 'Se apago el dispositivo para eficientizar los recursos.'.

% Para tomar acciones en base a consumo se usaran las siguientes reglas
% ---

% Para modificar temperatura interna se utilizara calefaccion y aire acondicionado
% Se debe chequear si la temperatura esta por debajo de 20 grados celcius para prender la calefaccion
% y si esta por encima de 26 para prender el aire acondicionado.

% Para el control del agua se puede abrir o cerrar llaves y tambien enviar el consumo de esta a los usuarios
% Verificar la cercania de los usuarios para cerrar automaticamente las llaves que se dejen abiertas

% Para poder trackear la ubicacion de una persona se utilizara un hecho dinamico.
% Prototipo dinamico: ubicacion(<persona>, <lugar>).

insertar_ubicacion(Persona, Lugar):- lugar(Lugar), retract(ubicacion(Persona, _)), assertz(ubicacion(Persona, Lugar)).
