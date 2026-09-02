import base64
import calendar
import os
import uuid
from datetime import date, datetime
from typing import Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.db.models.propiedad import Propiedad
from src.db.models.propiedad_imagen import PropiedadImagen
from src.db.models.propiedad_amenidad import PropiedadAmenidad
from src.db.models.amenidad import Amenidad
from src.db.models.usuario import Usuario
from src.db.models.reserva import Reserva
from src.db.models.resena import Resena
from src.dtos.propiedad_dto import PropiedadResponseDTO
from src.dtos.usuario_dto import UsuarioResponseDTO


class PropiedadService:
    def __init__(self, db: Session):
        self.db = db

    def _guardar_imagen(self, img_str: str) -> str:
        """Guarda imágenes en base64 en la carpeta uploads y devuelve la URL accesible."""
        if not img_str:
            return ""
        if img_str.startswith("http://") or img_str.startswith("https://") or img_str.startswith("/uploads/"):
            return img_str

        if img_str.startswith("data:image"):
            try:
                header, data = img_str.split(";base64,")
                ext = header.split("/")[1].split("+")[0]
                if ext == "jpeg":
                    ext = "jpg"
                filename = f"{uuid.uuid4().hex}.{ext}"
                os.makedirs("uploads", exist_ok=True)
                filepath = os.path.join("uploads", filename)
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(data))
                return f"/uploads/{filename}"
            except Exception:
                return img_str
        return img_str

    def enriquecer_propiedad(self, prop: Propiedad) -> dict:
        """Convierte una entidad Propiedad en diccionario compatible con PropiedadResponseDTO."""
        # 1. Anfitrión
        anfitrion_dto = None
        if prop.anfitrion:
            anfitrion_dto = UsuarioResponseDTO(
                id=prop.anfitrion.id,
                email=prop.anfitrion.email,
                nombre=prop.anfitrion.nombre,
                fecha_registro=prop.anfitrion.fecha_registro,
                es_anfitrion=prop.anfitrion.es_anfitrion,
            )

        # 2. Imágenes
        imgs = [img.url for img in sorted(prop.imagenes, key=lambda x: x.orden)]

        # 3. Amenidades
        amenidades_ids = [str(a.id) for a in prop.amenidades]
        amenidades_nombres = [a.nombre for a in prop.amenidades]

        # 4. Reseñas asociadas
        resenas = (
            self.db.query(Resena)
            .join(Reserva, Resena.reserva_id == Reserva.id)
            .filter(Reserva.propiedad_id == prop.id)
            .all()
        )
        cant_resenas = len(resenas)
        promedio = (
            round(sum(r.puntaje for r in resenas) / cant_resenas, 2)
            if cant_resenas > 0
            else None
        )

        return {
            "id": prop.id,
            "titulo": prop.titulo,
            "direccion": prop.direccion,
            "ciudad": prop.ciudad,
            "precio_noche": float(prop.precio_noche),
            "capacidad": prop.capacidad,
            "anfitrion_id": prop.anfitrion_id,
            "lat": prop.lat,
            "lng": prop.lng,
            "imagenes": imgs,
            "amenidades": amenidades_ids,
            "amenidades_nombres": amenidades_nombres,
            "promedio_puntaje": promedio,
            "cantidad_resenas": cant_resenas,
            "anfitrion": anfitrion_dto,
        }

    def crear_propiedad(
        self,
        titulo: str,
        direccion: str,
        ciudad: str,
        precio_noche: float,
        capacidad: int,
        anfitrion_id: int,
        amenidades: Optional[list[Any]] = None,
        imagenes: Optional[list[str]] = None,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
    ) -> dict:
        anfitrion = self.db.query(Usuario).filter(Usuario.id == anfitrion_id).first()
        if not anfitrion:
            raise ValueError(f"No existe ningún usuario con ID {anfitrion_id}")
        if not anfitrion.es_anfitrion:
            raise ValueError("Solo un anfitrión puede publicar propiedades")
        if precio_noche <= 0:
            raise ValueError("El precio por noche debe ser mayor a 0")
        if capacidad <= 0:
            raise ValueError("La capacidad debe ser mayor a 0")

        propiedad = Propiedad(
            titulo=titulo,
            direccion=direccion,
            ciudad=ciudad,
            precio_noche=precio_noche,
            capacidad=capacidad,
            anfitrion_id=anfitrion_id,
            lat=lat,
            lng=lng,
        )
        self.db.add(propiedad)
        self.db.flush()

        # Guardar imágenes
        for i, img_src in enumerate(imagenes or []):
            url_guardada = self._guardar_imagen(img_src)
            self.db.add(
                PropiedadImagen(
                    propiedad_id=propiedad.id,
                    url=url_guardada,
                    orden=i,
                    es_portada=(i == 0),
                )
            )

        # Asociar amenidades
        for am_item in amenidades or []:
            if isinstance(am_item, int) or (isinstance(am_item, str) and am_item.isdigit()):
                am = self.db.query(Amenidad).filter(Amenidad.id == int(am_item)).first()
            else:
                am = self.db.query(Amenidad).filter(Amenidad.nombre.ilike(str(am_item))).first()
            if am:
                self.db.add(PropiedadAmenidad(propiedad_id=propiedad.id, amenidad_id=am.id))

        self.db.commit()
        self.db.refresh(propiedad)
        return self.enriquecer_propiedad(propiedad)

    def obtener_por_id(self, propiedad_id: int) -> dict:
        propiedad = self.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not propiedad:
            raise ValueError(f"No existe la propiedad con ID {propiedad_id}")
        return self.enriquecer_propiedad(propiedad)

    def buscar_propiedades(
        self,
        ciudad: Optional[str] = None,
        desde: Optional[str] = None,
        hasta: Optional[str] = None,
        huespedes: Optional[int] = None,
        precio_max: Optional[float] = None,
        amenidades: Optional[list[str]] = None,
    ) -> list[dict]:
        query = self.db.query(Propiedad)

        if ciudad:
            query = query.filter(Propiedad.ciudad.ilike(f"%{ciudad.strip()}%"))

        if huespedes:
            query = query.filter(Propiedad.capacidad >= huespedes)

        if precio_max:
            query = query.filter(Propiedad.precio_noche <= precio_max)

        # Excluir propiedades con reservas confirmadas solapadas si se pasan fechas
        if desde and hasta:
            try:
                d_inicio = date.fromisoformat(desde)
                d_fin = date.fromisoformat(hasta)
                if d_inicio < d_fin:
                    solapadas = (
                        self.db.query(Reserva.propiedad_id)
                        .filter(
                            Reserva.estado == "confirmada",
                            Reserva.fecha_inicio < d_fin,
                            Reserva.fecha_fin > d_inicio,
                        )
                        .subquery()
                    )
                    query = query.filter(~Propiedad.id.in_(solapadas))
            except Exception:
                pass

        props = query.all()
        resultado = []

        for p in props:
            p_data = self.enriquecer_propiedad(p)
            # Filtro por amenidades en Python si se solicitaron
            if amenidades:
                p_am_ids = set(str(x) for x in p_data["amenidades"])
                p_am_noms = set(x.lower() for x in p_data["amenidades_nombres"])
                cumple_todas = True
                for req in amenidades:
                    req_str = str(req).strip().lower()
                    if req_str not in p_am_ids and req_str not in p_am_noms:
                        cumple_todas = False
                        break
                if not cumple_todas:
                    continue

            resultado.append(p_data)

        return resultado

    def listar_por_anfitrion(self, anfitrion_id: int) -> list[dict]:
        props = self.db.query(Propiedad).filter(Propiedad.anfitrion_id == anfitrion_id).all()
        return [self.enriquecer_propiedad(p) for p in props]

    def get_top_propiedades(self, ciudad: Optional[str] = None) -> list[dict]:
        query = self.db.query(Propiedad)
        if ciudad:
            query = query.filter(Propiedad.ciudad.ilike(f"%{ciudad.strip()}%"))

        props = query.all()
        enriquecidas = [self.enriquecer_propiedad(p) for p in props]

        # El ranking solicitado solo incluye propiedades con al menos tres reseñas.
        con_resenas = [p for p in enriquecidas if p["cantidad_resenas"] >= 3]

        con_resenas.sort(
            key=lambda x: (x["promedio_puntaje"] if x["promedio_puntaje"] is not None else 0),
            reverse=True,
        )
        return con_resenas[:10]

    def get_disponibilidad(self, propiedad_id: int, mes: str) -> list[dict]:
        """Genera el calendario del mes YYYY-MM indicando días ocupados por reservas confirmadas."""
        prop = self.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not prop:
            raise ValueError(f"No existe la propiedad con ID {propiedad_id}")

        try:
            anio, mes_num = (int(parte) for parte in mes.split("-"))
            if len(mes) != 7 or mes[4] != "-" or not 1 <= mes_num <= 12:
                raise ValueError
        except (TypeError, ValueError):
            raise ValueError("El mes debe tener el formato YYYY-MM")
        dias_mes = calendar.monthrange(anio, mes_num)[1]

        reservas = (
            self.db.query(Reserva)
            .filter(
                Reserva.propiedad_id == propiedad_id,
                Reserva.estado == "confirmada",
            )
            .all()
        )

        dias = []
        for d in range(1, dias_mes + 1):
            f_actual = date(anio, mes_num, d)
            f_str = f"{anio:04d}-{mes_num:02d}-{d:02d}"
            ocupado = any(r.fecha_inicio <= f_actual < r.fecha_fin for r in reservas)
            dias.append({"fecha": f_str, "ocupado": ocupado})

        return dias

    def actualizar_propiedad(self, propiedad_id: int, anfitrion_id: int, datos) -> dict:
        propiedad = self.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not propiedad:
            raise ValueError(f"No existe la propiedad con ID {propiedad_id}")
        if propiedad.anfitrion_id != anfitrion_id:
            raise ValueError("Solo el anfitrión dueño puede editar la propiedad")

        campos = datos.model_dump(exclude_unset=True)

        if "titulo" in campos and campos["titulo"]:
            propiedad.titulo = campos["titulo"]
        if "direccion" in campos and campos["direccion"]:
            propiedad.direccion = campos["direccion"]
        if "ciudad" in campos and campos["ciudad"]:
            propiedad.ciudad = campos["ciudad"]
        if "precio_noche" in campos and campos["precio_noche"] is not None:
            if campos["precio_noche"] <= 0:
                raise ValueError("El precio por noche debe ser mayor a 0")
            propiedad.precio_noche = campos["precio_noche"]
        if "capacidad" in campos and campos["capacidad"] is not None:
            if campos["capacidad"] <= 0:
                raise ValueError("La capacidad debe ser mayor a 0")
            propiedad.capacidad = campos["capacidad"]
        if "lat" in campos:
            propiedad.lat = campos["lat"]
        if "lng" in campos:
            propiedad.lng = campos["lng"]

        # Actualizar amenidades si se especificaron
        if "amenidades" in campos and campos["amenidades"] is not None:
            self.db.query(PropiedadAmenidad).filter(PropiedadAmenidad.propiedad_id == propiedad_id).delete()
            for am_item in campos["amenidades"]:
                if isinstance(am_item, int) or (isinstance(am_item, str) and str(am_item).isdigit()):
                    am = self.db.query(Amenidad).filter(Amenidad.id == int(am_item)).first()
                else:
                    am = self.db.query(Amenidad).filter(Amenidad.nombre.ilike(str(am_item))).first()
                if am:
                    self.db.add(PropiedadAmenidad(propiedad_id=propiedad_id, amenidad_id=am.id))

        # Actualizar imágenes si se especificaron
        if "imagenes" in campos and campos["imagenes"] is not None:
            self.db.query(PropiedadImagen).filter(PropiedadImagen.propiedad_id == propiedad_id).delete()
            for i, img_src in enumerate(campos["imagenes"]):
                url_guardada = self._guardar_imagen(img_src)
                self.db.add(
                    PropiedadImagen(
                        propiedad_id=propiedad_id,
                        url=url_guardada,
                        orden=i,
                        es_portada=(i == 0),
                    )
                )

        self.db.commit()
        self.db.refresh(propiedad)
        return self.enriquecer_propiedad(propiedad)

    def agregar_imagenes(self, propiedad_id: int, anfitrion_id: int, urls: list[str]) -> dict:
        propiedad = self.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not propiedad:
            raise ValueError(f"No existe la propiedad con ID {propiedad_id}")
        if propiedad.anfitrion_id != anfitrion_id:
            raise ValueError("No tenés permiso para modificar esta propiedad")

        orden_actual = len(propiedad.imagenes)
        for i, url in enumerate(urls):
            url_guardada = self._guardar_imagen(url)
            self.db.add(
                PropiedadImagen(
                    propiedad_id=propiedad_id,
                    url=url_guardada,
                    orden=orden_actual + i,
                    es_portada=(orden_actual + i == 0),
                )
            )
        self.db.commit()
        self.db.refresh(propiedad)
        return self.enriquecer_propiedad(propiedad)

    def eliminar_imagen(self, propiedad_id: int, imagen_id: int, anfitrion_id: int):
        propiedad = self.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not propiedad:
            raise ValueError(f"No existe la propiedad con ID {propiedad_id}")
        if propiedad.anfitrion_id != anfitrion_id:
            raise ValueError("No tenés permiso para modificar esta propiedad")

        imagen = self.db.query(PropiedadImagen).filter(
            PropiedadImagen.id == imagen_id,
            PropiedadImagen.propiedad_id == propiedad_id,
        ).first()
        if not imagen:
            raise ValueError(f"No existe la imagen con ID {imagen_id} en esta propiedad")

        self.db.delete(imagen)
        self.db.commit()

    def eliminar_propiedad(self, propiedad_id: int, anfitrion_id: int):
        propiedad = self.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not propiedad:
            raise ValueError(f"No existe la propiedad con ID {propiedad_id}")
        if propiedad.anfitrion_id != anfitrion_id:
            raise ValueError("Solo el anfitrión dueño puede borrarla")

        # Verificar si hay reservas activas
        reservas_activas = self.db.query(Reserva).filter(
            Reserva.propiedad_id == propiedad_id,
            Reserva.estado.in_(["pendiente", "confirmada"]),
        ).count()
        if reservas_activas > 0:
            raise ValueError("No podés borrar una propiedad con reservas activas")

        self.db.delete(propiedad)
        self.db.commit()
