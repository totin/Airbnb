from typing import Optional
from src.db.models.propiedad import Propiedad
from src.db.models.propiedad_imagen import PropiedadImagen


class PropiedadService:
    def __init__(self, db):
        self.db = db

    def crear_propiedad(self, titulo, direccion, ciudad, precio_noche, capacidad, anfitrion_id, imagenes=None):
        propiedad = Propiedad(
            titulo=titulo,
            direccion=direccion,
            ciudad=ciudad,
            precio_noche=precio_noche,
            capacidad=capacidad,
            anfitrion_id=anfitrion_id,
        )
        self.db.add(propiedad)
        self.db.flush()  # para tener propiedad.id antes del commit

        for i, url in enumerate(imagenes or []):
            self.db.add(PropiedadImagen(
                propiedad_id=propiedad.id,
                url=url,
                orden=i,
                es_portada=(i == 0),
            ))

        self.db.commit()
        self.db.refresh(propiedad)
        return propiedad

    def obtener_por_id(self, propiedad_id: int) -> Propiedad:
        propiedad = self.db.query(Propiedad).filter(Propiedad.id == propiedad_id).first()
        if not propiedad:
            raise ValueError(f"No existe la propiedad con ID {propiedad_id}")
        return propiedad

    def buscar_propiedades(self, ciudad: Optional[str] = None, capacidad_minima: Optional[int] = None):
        query = self.db.query(Propiedad)
        if ciudad:
            query = query.filter(Propiedad.ciudad.ilike(f"%{ciudad}%"))
        if capacidad_minima:
            query = query.filter(Propiedad.capacidad >= capacidad_minima)
        return query.all()

    def listar_por_anfitrion(self, anfitrion_id: int):
        return self.db.query(Propiedad).filter(Propiedad.anfitrion_id == anfitrion_id).all()

    def actualizar_propiedad(self, propiedad_id: int, anfitrion_id: int, datos):
        propiedad = self.obtener_por_id(propiedad_id)
        if propiedad.anfitrion_id != anfitrion_id:
            raise ValueError("No tenés permiso para editar esta propiedad")

        campos = datos.model_dump(exclude_unset=True)
        for campo, valor in campos.items():
            setattr(propiedad, campo, valor)

        self.db.commit()
        self.db.refresh(propiedad)
        return propiedad

    def agregar_imagenes(self, propiedad_id: int, anfitrion_id: int, urls: list[str]):
        propiedad = self.obtener_por_id(propiedad_id)
        if propiedad.anfitrion_id != anfitrion_id:
            raise ValueError("No tenés permiso para modificar esta propiedad")

        orden_actual = len(propiedad.imagenes)
        for i, url in enumerate(urls):
            self.db.add(PropiedadImagen(
                propiedad_id=propiedad_id,
                url=url,
                orden=orden_actual + i,
                es_portada=(orden_actual + i == 0),
            ))
        self.db.commit()
        self.db.refresh(propiedad)
        return propiedad

    def eliminar_imagen(self, propiedad_id: int, imagen_id: int, anfitrion_id: int):
        propiedad = self.obtener_por_id(propiedad_id)
        if propiedad.anfitrion_id != anfitrion_id:
            raise ValueError("No tenés permiso para modificar esta propiedad")

        imagen = self.db.query(PropiedadImagen).filter(
            PropiedadImagen.id == imagen_id,
            PropiedadImagen.propiedad_id == propiedad_id
        ).first()
        if not imagen:
            raise ValueError(f"No existe la imagen con ID {imagen_id} en esta propiedad")

        self.db.delete(imagen)
        self.db.commit()

    def eliminar_propiedad(self, propiedad_id: int, anfitrion_id: int):
        propiedad = self.obtener_por_id(propiedad_id)
        if propiedad.anfitrion_id != anfitrion_id:
            raise ValueError("No tenés permiso para eliminar esta propiedad")

        self.db.delete(propiedad)
        self.db.commit()