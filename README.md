# Demostración de uso de CAS en UriachContigo

Esta aplicación muestra una pantalla que invita al usuario a acceder mediante el servicio `cas` siguiendo un link generado para
tal efecto. Ese link se construye a partir de la [variable de entorno](#variables-de-entorno) `CAS_SERVER_URL`, a la que se 
añade al final `/login`, y la variable `service` con el valor indicado por la variable de entorno `SERVICE_VERIFICATION_URL`. 
Esta última URL es a donde `cas` redirigirá al navegador del usurio cuando se finalice la autenticación.

Esta aplicación está configurada para utilizar el servidor de preproducción de _Uriach Contigo_, que implementa el protocolo 
`CAS 2.0`. En dicho servicio se ha habilitado una cuenta de pruebas con unas credenciales que se comunicarán por otro medio.

Tras regresar con éxito el navegador del usuario a la URL indicada por `SERVICE_VERIFICATION_URL`, la URL incluirá un ticket de 
sesión generado por `cas`. El último paso será verificar la validez de ese ticket haciendo una última petición GET a 
`<CAS_SERVER_URL>/serviceValidate?ticket=<TICKET>&service=<SERVICE_VERIFICATION_URL>`. El resultado de esta petición, si el 
ticket era válido, es una respuesta XML similar a la siguiente:

```xml
<cas:serviceResponse xmlns:cas="http://www.yale.edu/tp/cas">
    <cas:authenticationSuccess>
        <cas:user>test@test.com</cas:user>
        <cas:attributes>
            <cas:authenticationDate>2021-11-04T22:00:57+00:00</cas:authenticationDate>
            <cas:longTermAuthenticationRequestTokenUsed>false</cas:longTermAuthenticationRequestTokenUsed>
            <cas:isFromNewLogin>true</cas:isFromNewLogin>
            <cas:email>test@test.com</cas:email>
            <cas:first_name>Juan</cas:first_name>
            <cas:last_name>Juan</cas:last_name>
            <cas:nif>A63279152</cas:nif>
        </cas:attributes>
        <cas:attribute name="authenticationDate" value="2021-11-04T22:00:57+00:00"/>
        <cas:attribute name="longTermAuthenticationRequestTokenUsed" value="false"/>
        <cas:attribute name="isFromNewLogin" value="true"/>
        <cas:attribute name="email" value="test@test.com"/>
        <cas:attribute name="first_name" value="Juan"/>
        <cas:attribute name="last_name" value="Juan"/>
        <cas:attribute name="nif" value="A63279152"/>
    </cas:authenticationSuccess>
</cas:serviceResponse>
```

Es importante resaltar que el `nif` lo es de la farmacia a la que pertenece el farmaceútico.

## Variables de entorno

Esta aplicación necesita dos variables de entorno:

```shell
CAS_SERVER_URL=http://pre-cas.i2-sys.com/cas
```

Esta variable indica la URL del servidor `cas`. Con ella la aplicación construirá las dos rutas más relevantes
que son `/login` y `/serviceValidate`

```shell
SERVICE_VERIFICATION_URL=http://localhost:5000/verify
```

Esta es la ruta a la que el servidor `cas` redirigirá al navegador del usuario cuando éste se autentica de forma correcta.

## Ejecución en local de la aplicación de prueba

Esta aplicación puede ejecutarse en un contenedor Docker haciendo:
```shell
docker run -e PORT=5000 -e CAS_SERVER_URL=http://pre-cas.i2-sys.com/cas -e SERVICE_VERIFICATION_URL=http://localhost:5000/verify -p5000:5000 cas-test
```