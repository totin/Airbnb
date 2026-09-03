# StayFinder Pro

realiza el frontend en type script basándote en: Proyecto 1 — Airbnb

Plataforma de alquileres temporarios. Los anfitriones publican propiedades, los huéspedes buscan por ciudad y fechas, reservan estadías y dejan reseñas.

Entidades sugeridas

Usuario (id, email, nombre, fecha_registro, es_anfitrion)

Propiedad (id, titulo, direccion, ciudad, precio_noche, capacidad, anfitrion_id)

Reserva (id, propiedad_id, huesped_id, fecha_inicio, fecha_fin, estado, total)

Resena (id, reserva_id, autor_id, puntaje, comentario, fecha)

Amenidad (id, nombre)

Relación N a M propiedad_amenidades (propiedad_id, amenidad_id)

Relación N a M favoritos (usuario_id, propiedad_id, fecha)

Historias de usuario

HU1 — Registro de usuario

Como visitante, quiero registrarme con email para reservar o publicar propiedades.

El email es único.

es_anfitrion es un booleano (por defecto false).

fecha_registro se guarda automáticamente.

POST /usuarios devuelve 201 y el usuario creado.

HU2 — Publicar propiedad

Como anfitrión, quiero publicar propiedades para recibir reservas.

Solo un usuario con es_anfitrion = true puede crear propiedades.

precio_noche y capacidad deben ser mayores a 0.

Toda propiedad tiene ciudad, dirección y título.

GET /anfitriones/{id}/propiedades devuelve todas sus publicaciones.

HU3 — Búsqueda por ciudad y fechas

Como huésped, quiero buscar propiedades por ciudad y rango de fechas.

GET /propiedades?ciudad=X&desde=YYYY-MM-DD&hasta=YYYY-MM-DD&huespedes=N filtra por ciudad, capacidad y disponibilidad.

Se excluyen propiedades con reservas que se solapan al rango pedido.

Se puede filtrar además por precio_max.

HU4 — Crear reserva

Como huésped, quiero reservar una propiedad en un rango de fechas.

fecha_inicio debe ser menor a fecha_fin.

No se puede reservar si el rango se solapa con otra reserva confirmada.

total = precio_noche * cantidad_noches.

La reserva inicia en estado pendiente.

Un huésped no puede reservar su propia propiedad.

HU5 — Confirmar y cancelar reservas

Como anfitrión, quiero aceptar o rechazar las reservas de mi propiedad.

Solo el anfitrión dueño puede confirmar o rechazar.

Transiciones válidas: pendiente → confirmada, pendiente → rechazada, confirmada → cancelada.

Si se cancela con menos de 7 días de antelación, se pierde el 50% del total; con menos de 48hs, el 100%.

HU6 — Reseñas post-estadía

Como huésped, quiero dejar una reseña luego de mi estadía.

Solo se puede reseñar si la reserva está confirmada y fecha_fin < hoy.

puntaje entre 1 y 5.

Una reserva tiene como máximo una reseña.

GET /propiedades/{id}/resenas devuelve todas las reseñas de la propiedad.

HU7 — Favoritos

Como huésped, quiero marcar propiedades como favoritas.

Un usuario no puede marcar dos veces la misma propiedad.

GET /usuarios/{id}/favoritos devuelve la lista de propiedades favoritas.

Se puede quitar con DELETE /usuarios/{id}/favoritos/{propiedad_id}.

HU8 — Amenidades

Como anfitrión, quiero indicar qué comodidades tiene mi propiedad.

Existe una lista fija de amenidades (wifi, pileta, estacionamiento, etc).

Una propiedad puede tener varias; una amenidad puede estar en varias propiedades.

La búsqueda de HU3 acepta filtrar por amenidades=wifi,pileta (deben cumplir todas).

HU9 — Calendario de disponibilidad

Como huésped, quiero ver qué fechas están libres para una propiedad.

GET /propiedades/{id}/disponibilidad?mes=YYYY-MM devuelve los días libres y ocupados del mes.

Cuentan como ocupadas solo las reservas confirmadas.

HU10 — Ingresos del anfitrión

Como anfitrión, quiero saber cuánto facturé en un período.

GET /anfitriones/{id}/ingresos?desde=...&hasta=... devuelve el total facturado y el detalle por propiedad.

Solo cuentan reservas confirmadas con fecha_fin dentro del rango.

HU11 — Top propiedades por ciudad

Como huésped, quiero ver las propiedades mejor calificadas de una ciudad.

GET /propiedades/top?ciudad=X devuelve las 10 propiedades con mayor promedio de puntaje.

Solo se consideran propiedades con al menos 3 reseñas.

Ordenadas de mayor a menor promedio.

HU12 — Historial de huésped

Como huésped, quiero consultar todas mis reservas.

GET /usuarios/{id}/reservas devuelve reservas ordenadas por fecha_inicio descendente.

Se puede filtrar por estado.

Incluye datos de la propiedad y del anfitrión.
deja los endpoints consumibles comentados que después yo lo modifico

This project was built with [Lovable](https://lovable.dev).

## Build with Lovable

Continue developing this project in the [Lovable editor](https://lovable.dev/projects/c3428d95-46e3-4931-8403-c56480e0cd75).

- **Ship faster**: describe what you want to build and Lovable handles the code.
- **Stay in sync**: every change made in Lovable is committed straight to this repository.
- **Full ownership**: this code is yours. Push to `main` on GitHub and your changes sync back into Lovable, ready for your next prompt.

## Development

Prefer working locally? You need Node.js and npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating).

```sh
git clone <this-repository-url>
cd <repository-name>
npm i
npm run dev
```
