% ========================================================================
%                       Eficientizacion de recursos
% ========================================================================

% hechos dinamicos
:-dynamic tipoDisp/1.
:-dynamic lugar/1.
:-dynamic lugar/3. %(ID del lugar, Tipo, lista de dispositivos (id dispositivo, tipo))
:-dynamic temperatura/2. %(ID del lugar, valor en celcius)
:-dynamic tiempo/2. %(hora, minuto) basado en 24h
:-dynamic consumo/2. %(valor de consumo, dispositivo)
:-dynamic ubicacion/2. %(Persona, Lugar)
:-dynamic estado/3.
:-dynamic accion/3. %(dispositivoID, estado (ON/OFF), accion)
:-dynamic opcion/2.
:-dynamic verEstadoCasa/1.

% Definicion de hecho dispositivo para decir los que existen en diferentes lugares de la casa

ver_pregunta(X):- write(X), write('(si/no)? ').
pregunta(X, Respuesta):- ver_pregunta(X), read(Respuesta).

% resp_disp(si, X):- !, assertz(dispositivos(X)).
% resp_disp(no, _):- !, write('No se acepta ese dispositivo en esa
% habitacion.'), fail.

% agregar_dispositivo(X):- \+ (dispositivo(X)), assertz(dispositivo(X)).
% agregar_lugar(X):- \+ (lugar(X)), assertz(lugar(X)).
% agregar_disp_lugar(Disp, Lugar):- dispositivo(Disp), lugar(Lugar),
%                         \+ (dispositivo_lugar(Disp, Lugar)), assertz(dispositivo_lugar(Disp, Lugar)).

add_tail([],X,[X]).
add_tail([H|T],X,[H|L]):-add_tail(T,X,L).

agregar_lugar(Lugar,Tipo):-
    tipo(Tipo),
    retractall(lugar(Lugar,_,_)),
    assertz(lugar(Lugar, Tipo, [])).

agregar_disp_lugar(Disp, Lugar):-
    lugar(Lugar,T,L),
    add_tail(L,Disp, Lista),
    retract(lugar(Lugar,_,_)),
    asserta(lugar(Lugar,T,Lista)).


tipo(habitacion).
tipo(sala).
tipo(exterior).
tipo(cocina).
tipo(comedor).

tipoDisp(iluminacion).
tipoDisp(controlTemp).
tipoDisp(other).

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

insertar_consumo(Consumo, Dispositivo, Lugar, Resultado):-
    lugar(Lugar,_,Lista), member((Dispositivo,_), Lista), retract(consumo(_, Dispositivo)),
    assertz(consumo(Consumo, Dispositivo)),
    verificar_consumo(Consumo, Dispositivo, Lugar, Resultado), !.
% Si no existe el consumo, se hace esto:
insertar_consumo(Consumo, Dispositivo, Lugar, Resultado):-
    lugar(Lugar,_,Lista), member((Dispositivo,_), Lista),
    assertz(consumo(Consumo, Dispositivo)),
    verificar_consumo(Consumo, Dispositivo, Lugar, Resultado).

verificar_consumo(regular, _, _):- write('Se mantiene el mismo estado en el dispositivo'), !.
verificar_consumo(alto, Dispositivo, Lugar, Resultado):-
    retract(estado(Dispositivo, Lugar, _)), assertz(estado(Dispositivo, Lugar, 0)),
    Resultado = 'Se apago el dispositivo para eficientizar los recursos.'.
verificar_consumo(alto, Dispositivo, Lugar, Resultado):-
    assertz(estado(Dispositivo, Lugar, 0)),
    Resultado = 'Se apago el dispositivo para eficientizar los recursos.'.

actualizar_temperatura(Lugar, Temp):-
    retract(temperatura(Lugar,_)), asserta(temperatura(Lugar,Temp)).

% Para tomar acciones en base a consumo se usaran las siguientes reglas
% ---

% Para modificar temperatura interna se utilizara calefaccion y aire acondicionado
% Se debe chequear si la temperatura esta por debajo de 20 grados celcius para prender la calefaccion
% y si esta por encima de 26 para prender el aire acondicionado.

% Para el control del agua se puede abrir o cerrar llaves y tambien enviar el consumo de esta a los usuarios
% Verificar la cercania de los usuarios para cerrar automaticamente las llaves que se dejen abiertas


cambioLugar(Persona, Lugar):-
    desactivar_dispositivos(Persona),
    lugar(Lugar,_,_), retract(ubicacion(Persona, _)),
    asserta(ubicacion(Persona, Lugar)), usarDispositivos(Lugar).

%desactivar dispositivos del lugar donde se encontraba una persona
%si y solo si no hay nadie mas en ese lugar.
desactivar_dispotivos(Persona):-
    ubicacion(Persona,Lugar), setof(Otros, ubicacion(Otros,Lugar), ListaP),
    length(ListaP, Cant), Cant =< 1, lugar(Lugar,_,Lista),
    desactivarTodos(Lugar, Lista).

%se verifica si el dispositivo esta activo
%si lo esta, de apaga.
desactivarTodos(_,[]).
desactivarTodos(Lugar,[Cabe|Cola]):-
    accion(Cabe,1,_),
    retract(accion(Cabe,1,_)),
    asserta(accion(Cabe,0,'Desactivado')),
    desactivarTodos(Lugar, Cola).



usarDispositivos(Lugar):-
    usarACAutomatico(Lugar,25),
    usarLucesAutomatico(Lugar).


%se enciende el AC dependiendo de la temperatura del area.
%el valor default del sistema automatico dependera de lo que se
%desee.
usarACAutomatico(Lugar, TempDefault):-
    lugar(Lugar,_,L), temperatura(Lugar, Grados), Grados > 29,
    member((X,controlTemp),L), retract(accion(X,_,_)),
    asserta(accion(X,1,TempDefault)), actualizar_temperatura(Lugar, TempDefault),!.
usarACAutomatico(Lugar, TempDefault):-
    lugar(Lugar,_,L), temperatura(Lugar, Grados), Grados =< 19,
    member((X,controlTemp),L), retract(accion(X,_,_)),
    asserta(accion(X,1,TempDefault)), actualizar_temperatura(Lugar, TempDefault),!.
usarACAutomatico(Lugar, _):-
    lugar(Lugar,_,L), temperatura(Lugar, Grados), Grados =< 29, Grados > 19,
    member((X,controlTemp),L), retract(accion(X,_,_)),
    asserta(accion(X,0,Grados)), actualizar_temperatura(Lugar, Grados).


%Se prende el bombillo desde la 5 PM en adelante
usarLucesAutomatico(Lugar):-
    lugar(Lugar,_,L), member((X, iluminacion),L), tiempo(H,_),
    H > 17,
    retract(accion(X,_,_)), asserta(accion(X,1,'Iluminando area')).
%Se apaga a la hora de dormir, 11 PM, por default
usarLucesAutomatico(Lugar):-
    lugar(Lugar,_,L), member((X, iluminacion),L), tiempo(H,_),
    H > 23,
    retract(accion(X,_,_)), asserta(accion(X,0,'Manteniendo oscuridad')).

% Fuentes de energia
fuente(solar).
fuente(eolica).
fuente(fosil).



% ========================================================================
%                               Seguridad
% ========================================================================

abertura(puerta).
abertura(ventana).
abertura(garaje).


% Definición de estados que tienen las aberturas
% Prototipo: accion(<abertura>, <accion>).

accion(puerta,bloqueada).
accion(puerta,desbloqueada).
accion(ventana,bloqueada).
accion(ventana,desbloqueada).
accion(garaje,bloqueada).
accion(garaje,desbloqueada).


% Definicion de entradas que tiene un lugar
% entrada(<lugar>,<abertura>).

entrada(sala_estar,puerta).
entrada(terraza,puerta).
entrada(patio,puerta).
entrada(cocina,ventana).
entrada(habitacionX,ventana).
entrada(patio, ventana).
entrada(quiosco, ventana).
entrada(garaje, ventana).
entrada(garaje, garaje).

%definicion de acciones de bloqueos para todas las aberturas de la casa

bloquear:- abertura(X), retractall(accion(X,_)),assertz(accion(X,bloqueada));
              writeln("Bloqueado").

desbloquear:- abertura(X),retractall(accion(X,_)),assertz(accion(X,desbloqueada));
                 writeln("Desbloqueado").

habilitarSeg(Result):- verEstadoCasa(Result), Result = vacia, setAlarma(on).

setEstadoCasa(Estado):- retractall(verEstadoCasa(_)),assert(verEstadoCasa(Estado)).

setLucesDelPatio:- verEstadoCasa(X), X = noche, retractall(opcion(luz,_)), assert(opcion(luz,power)).

bloquearGaraje():- accion(garaje,bloqueada),!.
desbloquearGaraje():- accion(garaje,bloqueada),!.