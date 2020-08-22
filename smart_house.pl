% ========================================================================
%                       Eficientizacion de recursos
% ========================================================================

%REQUERIMIENTOS PREVIOS PARA UTILIZAR TODAS
%LAS SIGUIENTES REGLAS APROPIADAMENTE:
%-Agregar lugares
%-Agregar dispostivos si es necesario
%-Agregar el tiempo
%-Agregar temperatura a los lugares
%-Recordar el buen uso de las estructuras para los hechos

% hechos dinamicos
:-dynamic consumo/2. %(valor de consumo, dispositivo)
:-dynamic estado/3.
:-dynamic lugar/3. %(ID del lugar, Tipo, lista de dispositivos [(id dispositivo, tipo)])
:-dynamic temperatura/2. %(ID del lugar, valor en celcius)
:-dynamic tiempo/2. %(hora, minuto) basado en 24h
:-dynamic consumo/2. %(valor de consumo, dispositivo)
:-dynamic ubicacion/2. %(Persona, Lugar)
:-dynamic accion/3. %(dispositivoID, estado (ON/OFF), accion)

%Tipo de areas posibles en la casa
tipo(habitacion).
tipo(sala).
tipo(exterior).
tipo(cocina).
tipo(comedor).
tipo(techo).
tipo(entrada).

% Fuentes de energia
fuente(solar).
fuente(eolica).
fuente(fosil).

%regla para agregar elementos a listas
add_tail([],X,[X]).
add_tail([H|T],X,[H|L]):-add_tail(T,X,L).


% Definicion de hecho dispositivo para decir los que existen en diferentes lugares de la casa

ver_pregunta(X):- write(X), write('(si/no)? ').
pregunta(X, Respuesta):- ver_pregunta(X), read(Respuesta).

% resp_disp(si, X):- !, assertz(dispositivos(X)).
% resp_disp(no, _):- !, write('No se acepta ese dispositivo en esa
% habitacion.'), fail.

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

% Para tomar acciones en base a consumo se usaran las siguientes reglas
% ---

% Para modificar temperatura interna se utilizara calefaccion y aire acondicionado
% Se debe chequear si la temperatura esta por debajo de 20 grados celcius para prender la calefaccion
% y si esta por encima de 26 para prender el aire acondicionado.

% Para el control del agua se puede abrir o cerrar llaves y tambien enviar el consumo de esta a los usuarios
% Verificar la cercania de los usuarios para cerrar automaticamente las llaves que se dejen abiertas

% ========================================================================
%                       Reglas para el manejo de la casa
% ========================================================================


%Primera instancia de presencia de alguien
%en la casa.
irLugar(Persona, Lugar):-
    lugar(Lugar,_,_),
    asserta(ubicacion(Persona, Lugar)), usarDispositivos(Lugar,25,29,19,24,0,17,0).

%Regla que se utiliza para cuando una persona se desplaza dentro
%de la casa.
cambioLugar(Persona, Lugar):-
    desactivar_dispotivos(Persona),
    lugar(Lugar,_,_), retract(ubicacion(Persona, _)),
    asserta(ubicacion(Persona, Lugar)), usarDispositivos(Lugar,25,29,19,24,0,17,0),!.
cambioLugar(Persona, Lugar):-
    lugar(Lugar,_,_), retract(ubicacion(Persona, _)),
    asserta(ubicacion(Persona, Lugar)), usarDispositivos(Lugar,25,29,19,24,0,17,0).

%regla para integrar dispositivos en un lugar
agregar_disp(Disp, Lugar):-
    lugar(Lugar,T,L),
    add_tail(L,Disp, Lista),
    retract(lugar(Lugar,_,_)),
    asserta(lugar(Lugar,T,Lista)).

%regla para remover dispositivos de un lugar
eliminar_disp(Disp, Lugar):-
    lugar(Lugar,T,L),
    delete(L, Disp, NewList),
    retract(lugar(Lugar,_,_)),
    asserta(lugar(Lugar,T,NewList)).

%desactivar dispositivos del lugar donde se encontraba una persona
%si y solo si no hay nadie mas en ese lugar.
desactivar_dispotivos(Persona):-
    ubicacion(Persona,Lugar), setof(Otros, ubicacion(Otros,Lugar), ListaP),
    length(ListaP, Cant), Cant > 1,!.
desactivar_dispotivos(Persona):-
    ubicacion(Persona,Lugar), setof(Otros, ubicacion(Otros,Lugar), ListaP),
    length(ListaP, Cant), Cant =< 1, lugar(Lugar,_,Lista),
    desactivarTodos(Lugar, Lista).

%desactiva todos los dispositivos
%del lugar seleccionado
desactivarTodos(_,[]).
desactivarTodos(Lugar,[Cabe|Cola]):-
    Cabe = (Dispositivo, _),
    retractall(accion(Dispositivo,_,_)),
    asserta(accion(Dispositivo,0,'Desactivado')),
    desactivarTodos(Lugar, Cola).


%reglas que reciben constante actualizacion de sensores
%o y relojes de la casa
actualizar_temperatura(Lugar, Temp):-
    retract(temperatura(Lugar,_)), asserta(temperatura(Lugar,Temp)),!.
actualizar_temperatura(Lugar, Temp):-
    asserta(temperatura(Lugar,Temp)).

actualizar_tiempo(H, M):-
    retractall(tiempo(_,_)), asserta(tiempo(H,M)).


%Uso del Acondicionador de aire manual
encenderACManual(Lugar, TempElegida):-
    lugar(Lugar,_,L),
    member((X,controlTemp),L), retractall(accion(X,_,_)),
    asserta(accion(X,1,TempElegida)), actualizar_temperatura(Lugar,TempElegida).
apagarACManual(Lugar):-
    lugar(Lugar,_,L), temperatura(Lugar, Temp),
    member((X,controlTemp),L), retractall(accion(X,_,_)),
    asserta(accion(X,0,'Apagado')), actualizar_temperatura(Lugar,Temp).


%se enciende el AC dependiendo de la temperatura del area.
%el valor default del sistema automatico dependera de lo que se
%desee.
usarACAutomatico(Lugar, TempElegida, LimSuperior, _):-
    lugar(Lugar,_,L), temperatura(Lugar, Grados), Grados >= LimSuperior,
    member((X,controlTemp),L), retractall(accion(X,_,_)),
    asserta(accion(X,1,TempElegida)), actualizar_temperatura(Lugar,TempElegida),!.
usarACAutomatico(Lugar,TempElegida, _, LimInferior ):-
    lugar(Lugar,_,L), temperatura(Lugar, Grados), Grados =< LimInferior,
    member((X,controlTemp),L), retractall(accion(X,_,_)),
    asserta(accion(X,1,TempElegida)), actualizar_temperatura(Lugar,TempElegida),!.
usarACAutomatico(_,_,_,_):-true.
%no haga nada cuando no tiene ac o si la temperatura
%del lugar esta en el margen deseado


%encender bombillos manualmente (ya sea por la aplicacion o interruptor)
encenderLucesManual(Lugar):-
    lugar(Lugar,_,L), member((X, iluminacion),L),
    retractall(accion(X,_,_)), asserta(accion(X,1,'Iluminando area')).
apagarLucesManual(Lugar):-
    lugar(Lugar,_,L), member((X, iluminacion),L),
    retractall(accion(X,_,_)), asserta(accion(X,0,'Luces Apagadas')).


%Se enciende el bombillo en el rango seteado por default
usarLucesAutomatico(Lugar, HoraSup, MinSup, HoraInf, MinInf):-
    lugar(Lugar,_,L), member((X, iluminacion),L), tiempo(H,M),
    HoraInf =< H, M =< MinInf, H =< HoraSup, M =< MinSup,
    retractall(accion(X,_,_)), asserta(accion(X,1,'Iluminando area')),!.
%Se apaga a la hora de dormir, X PM, por default
usarLucesAutomatico(_,_,_,_,_):-true. %cuando no tenga bombillos o fuera de rango



%Uso de dispositivos de forma automatica de un lugar.
usarDispositivos(Lugar,TempControl,TempSup,TempInf, HoraSup, MinSup, HoraInf, MinInf):-
    usarACAutomatico(Lugar,TempControl,TempSup,TempInf),
    usarLucesAutomatico(Lugar, HoraSup, MinSup, HoraInf, MinInf).



%Reglas basicas de monitoreo para obtener informacion
%de la casa
getTempLugar(Lugar, Return):-
    lugar(Lugar,_,_), temperatura(Lugar, Return).
getTime(Hour, Min):-
    tiempo(Hour,Min).

getDispositivosEnUso(Id, 'Apagado', Descr):-
    accion(Id,State,Descr), State is 0,!.
getDispositivosEnUso(Id, 'Encendido', Descr):-
    accion(Id,State,Descr), State is 1,!.
getDispositivosEnUso(Id, 'Error', 'Revisar Dispositivo'):-
    accion(Id,_,_).


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
