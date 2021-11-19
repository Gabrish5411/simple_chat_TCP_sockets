1. Arquitectura de red: cliente-servidor, P2P, híbrida.

 Clientes-servidor. El servidor valida y ejecuta mensajes de un usuario a un grupo o directo a otro usuario. Ademas, controla las credenciales de administrador y revisa si es que es un administrador quien quiere ejecutar las distintas acciones para el manejo de grupo.

2. Tipos de acciones realizables por los nodos.

Con respecto a los tipos de acciones realizables por los nodos definidos como usuarios serían:
 1. Requerir al servidor encontrar usuarios con determinadas credenciales para la creacion de grupo, mediante un request al servidor.(usuario hace esto al querer crear un grupo y servidor le retorna nombres de usuarios disponibles para agregar al grupo.)
 2. Iniciar conversación con usuarios.
 3. Creación de grupos, agregar usuarios al grupo, enviar mensajes de texto al grupo, eliminar usuario del grupo, eliminar el grupo.
 
En cambio para los nodos definidos como servidor:
 1. Búsqueda de usuarios con determinadas credenciales (admin o usuarios disponible para agregar a grupos).
 2. Autentificar credenciales correctas al inicio de sesión de administrador y de usuarios normales (sin credencial de administrador). 

3. Tipos de mensaje: Formato detallado, p.ej., cabecera, cuerpo, apéndice.

Con respecto a los tipos de mensajes serían:
 1. Usuario envía USER_REQUEST al servidor y requiere una cabecera con campo identificar (N_PERSONA) para el usuario que se quiere encontrar con un número de teléfono. 
 2. Usuario envía START_CONVERSATION otro usuario y requiere una cabecera con campo USR_CREDENTIALS (con las credenciales de quién inició la conversación) y se incluye un cuerpo con el texto que se quiere enviar.
 3. Usuario envía GROUP_MANAGE al servidor y requiere una cabecera con campo USR_CREDENTIALS (con las credenciales de quién es el admin del grupo) ahi el servidor retorna GROUP_OPTIONS con una cabecera con campo GROUP_CREDENTIALS (credenciales del grupo) y contiene además un cuerpo con las opciones de manejo de grupo ya sea agregar a usuario, eliminar usuario o eliminar grupo.
 3. Usuario envía SEND_MSG a usuarios parte del grupo requiriendo cabecera USR_CREDENTIALS (credenciales de quién envía el mensaje) y contiene un cuerpo con el texto a enviar.
 4. Servidor envía USER_DATA como respuesta USER_REQUEST, incluyendo cabecera con campo USR_CREDENTIALS (credenciales de usuario buscado).
 5. Servidor envía NOTIFICATION a usuario offline, incluyendo como cabecera con campo MSG (mensaje recibido) y con cuerpo el texto del mensaje.
 6. Servidor envía ANSWER  a usuario haciendo log in, incluyendo como cabecera STATUS (estado según log in exitoso o fallado) y con cuerpo exito en caso de log in exitoso o fallo en caso de log in fallido.
 7. En el caso de querer enviar un mensaje, USUARIO envía SEND_MSG al servidor y campo con contenido del mensaje.

4. Modelamiento del estado en los nodos y representación de la pizarra compartida. 

Con respecto al estado del servidor puede encontrarse en dos estados, arriba o caído. Si es que se encuentra cáido, se retornara con un mensaje de error al usuario ante cualquier tipo de acción.

Con respecto al usuario puede encontrarse online u offline. Online si es que se autentifican sus credenciales y existe una conexión a la red. Offline si es que no es posible autetificar sus credenciales y/o no existe conección a la red.
Ademas un usuario puede ser administrador o no. Para esto, quien haga log in con nombre admin debe ingresar la contraseña correcta (sistemas).


5. Tipos de servicios de comunicación de Internet utilizados para las distintas acciones.

Siguiendo la enumeración del punto 2 serían:
Acciones usuarios:
 1. Transmisión de datos confiables.
 2. Transmisión de datos confiables.
 3. Transmisión de datos confiables.

Acciones servidor:
 1. Transmisión de datos confiables.
 2. Transmisión de datos confiables.
 3. Transmisión de datos confiables.

 Al ser una aplicación de mensajería instantánea el objetivo final de este es lograr la comunicación efectiva entre usuarios.

6. Limitaciones del protocolo: Cantidad máxima de conversaciones y grupos por usuario, número máximo de usuarios por grupo, etc.

Dado que se utiliza el tipo de transporte TCP, la carga del servidor sera muy alta y dependera del buffer disponible de la CPU en que se encuentre el servidor. Por esto mismo, dependera de la CPU en que se encuentre el servidor para establecer la cantidad maxima de conversaciones, grupos por usuario o numero maximo de usuarios por grupo.


7. Tipos de transporte necesarios y números de puerto (o rangos de puertos) que deben considerarse.

El tipo de trasnporte necesario es el de TCP. Utilización del puerto TCP 60000, dado que se necesita evitar una potencial colisión con otros protocolos bien conocidos (que se encuentran entre 0-1023).


FUNCIONAMIENTO PROGRAMA
-Se debe correr primero el servidor para que los clientes sean capaces de conectarse a este.
-El cliente que se conecte debe elegir un apodo
-Se puede empezar a comunicar con los demas clientes conectados al servidor de inmediato mandando mensajes
-Si queremos mandar un mensaje privado primero:
    +Escribimos "SHOW" en la consola
    +*Enter*
    +Nos muestra los usuarios conectados
    +Ahora escribimos el nombre del usuario al que deseamos mandarle un mensaje
    +*Enter*
    +Procedemos a escribir el mensaje que deseamos enviarle
    +*Enter*
    +Y listo. El mensaje enviado solo lo recibira el cliente destinatario
-Si queremos hacer un grupo:
    ++Escribimos "CREATEGROUP" en la consola
    +*Enter*
    +Nos muestra los usuarios conectados
    +Ahora escribimos los usuarios que deseamos agregar con un espacio de separacion
    +*Enter*
    +Procedemos a escribir el nombre que deseamos ponerle al grupo
    +*Enter*
    +Y listo. Grupo creado
-Si queremos enviar un mensaje a un grupo al que pertenecemos (nos tira error si deseamos enviar un mensaje a un grupo al cual no pertenecemos)
    +Escribimos "MSGGROUP" en la consola
    +*Enter*
    +Nos muestra los grupos existentes 
    +Ahora escribimos el nombre del grupo al que deseamos mandarle un mensaje 
    +*Enter*
    +Procedemos a escribir el mensaje que deseamos enviarle
    +*Enter*
    +Y listo. El mensaje se envia a todos los miembros del grupo.
-Si se quiere ingresar como administrador, en usuario llamarse admin e ingresar clave sistemas, para echar a alguien del servidor, escribir como mensaje /kick (nombre de usuario a echar).