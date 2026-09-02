from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import text, inspect
from src.db.connection import Base, engine, SessionLocal
from src.db.models import (
    Usuario,
    Amenidad,
    Propiedad,
    PropiedadAmenidad,
    PropiedadImagen,
    Reserva,
    Resena,
    Favorito,
    SaldoHoras,
    TransaccionHoras,
)
from src.db.models.transaccion_horas import TipoTransaccionHoras


def init_database():
    print("Iniciando verificación y migración de base de datos PostgreSQL...")

    with engine.connect() as conn:
        # 1. Asegurar columnas en tabla propiedad
        insp = inspect(engine)
        tables = insp.get_table_names()

        if "propiedad" in tables:
            cols = [c["name"] for c in insp.get_columns("propiedad")]
            if "lat" not in cols:
                conn.execute(text("ALTER TABLE propiedad ADD COLUMN lat DOUBLE PRECISION;"))
                conn.commit()
            if "lng" not in cols:
                conn.execute(text("ALTER TABLE propiedad ADD COLUMN lng DOUBLE PRECISION;"))
                conn.commit()

        # 2. Asegurar columnas en tabla reserva
        if "reserva" in tables:
            conn.execute(text("ALTER TABLE reserva ALTER COLUMN estado TYPE VARCHAR(50) USING estado::text;"))
            conn.commit()
            cols = [c["name"] for c in insp.get_columns("reserva")]
            if "metodo_pago" not in cols:
                conn.execute(text("ALTER TABLE reserva ADD COLUMN metodo_pago VARCHAR(20) DEFAULT 'dinero' NOT NULL;"))
                conn.commit()
            if "horas_utilizadas" not in cols:
                conn.execute(text("ALTER TABLE reserva ADD COLUMN horas_utilizadas INTEGER;"))
                conn.commit()
            if "horas_ganadas" not in cols:
                conn.execute(text("ALTER TABLE reserva ADD COLUMN horas_ganadas INTEGER;"))
                conn.commit()

        # 3. Eliminar tablas duplicadas si existieran
        for dup in ["propiedades", "amenidades", "resenas"]:
            if dup in tables:
                try:
                    conn.execute(text(f"DROP TABLE IF EXISTS {dup} CASCADE;"))
                    conn.commit()
                except Exception as e:
                    print(f"Nota: No se pudo eliminar {dup}: {e}")

    # Crear todas las tablas definidas en los modelos ORM
    Base.metadata.create_all(bind=engine)
    print("Tablas sincronizadas correctamente.")

    db = SessionLocal()
    try:
        # 1. Asegurar usuarios demo sin borrar los existentes
        usuarios_demo = [
            ("lucia@mail.com", "Lucía Fernández", True),
            ("martin@mail.com", "Martín Sosa", True),
            ("cami@mail.com", "Camila Ruiz", False),
            ("diego@mail.com", "Diego Paz", False),
        ]
        usuarios_agregados = False
        for email, nombre, es_anfitrion in usuarios_demo:
            if not db.query(Usuario).filter(Usuario.email == email).first():
                db.add(Usuario(email=email, nombre=nombre, es_anfitrion=es_anfitrion))
                usuarios_agregados = True
        if usuarios_agregados:
            print("Asegurando usuarios demo...")
            db.commit()

        # 2. Asegurar saldo de horas para todos los usuarios
        for u in db.query(Usuario).all():
            saldo = db.query(SaldoHoras).filter(SaldoHoras.usuario_id == u.id).first()
            if not saldo:
                db.add(SaldoHoras(usuario_id=u.id, horas=1000))
                db.add(
                    TransaccionHoras(
                        usuario_id=u.id,
                        tipo=TipoTransaccionHoras.GANADA,
                        cantidad=1000,
                        fecha=datetime.now(),
                    )
                )
        db.commit()

        # 3. Asegurar amenidades
        amenidades_data = [
            "Wifi",
            "Pileta",
            "Estacionamiento",
            "Aire acondicionado",
            "Acepta mascotas",
            "Cocina equipada",
            "Lavarropas",
            "Parrilla",
        ]
        amenidades_objs = {}
        for nom in amenidades_data:
            am = db.query(Amenidad).filter(Amenidad.nombre.ilike(nom)).first()
            if not am:
                am = Amenidad(nombre=nom)
                db.add(am)
                db.flush()
            amenidades_objs[nom] = am
        db.commit()

        # 4. Asegurar coordenadas en propiedades existentes o crearlas
        coords_map = {
            "buenos aires": (-34.5885, -58.4306),
            "córdoba": (-31.38, -64.53),
            "cordoba": (-31.38, -64.53),
            "bariloche": (-41.118, -71.34),
            "mar del plata": (-38.01, -57.535),
            "mendoza": (-33.05, -68.88),
        }
        for prop in db.query(Propiedad).all():
            if prop.lat is None or prop.lng is None:
                c_key = prop.ciudad.strip().lower()
                lat, lng = coords_map.get(c_key, (-34.6037, -58.3816))
                prop.lat = lat
                prop.lng = lng
        db.commit()

        # Si no hay propiedades, crearlas
        if db.query(Propiedad).count() == 0:
            u_anf1 = db.query(Usuario).filter(Usuario.es_anfitrion == True).first()
            u_anf2 = db.query(Usuario).filter(Usuario.es_anfitrion == True).order_by(Usuario.id.desc()).first()
            p1 = Propiedad(
                titulo="Loft luminoso en Palermo Soho",
                direccion="Gurruchaga 1840",
                ciudad="Buenos Aires",
                precio_noche=Decimal("48000.00"),
                capacidad=3,
                anfitrion_id=u_anf1.id,
                lat=-34.5885,
                lng=-58.4306,
            )
            p2 = Propiedad(
                titulo="Casa con pileta y parrilla",
                direccion="Los Álamos 320",
                ciudad="Córdoba",
                precio_noche=Decimal("72000.00"),
                capacidad=6,
                anfitrion_id=u_anf1.id,
                lat=-31.38,
                lng=-64.53,
            )
            p3 = Propiedad(
                titulo="Cabaña de montaña frente al lago",
                direccion="Camino de los Nogales 55",
                ciudad="Bariloche",
                precio_noche=Decimal("95000.00"),
                capacidad=4,
                anfitrion_id=u_anf2.id,
                lat=-41.118,
                lng=-71.34,
            )
            p4 = Propiedad(
                titulo="Depto frente al mar",
                direccion="Bv. Marítimo 2100",
                ciudad="Mar del Plata",
                precio_noche=Decimal("56000.00"),
                capacidad=5,
                anfitrion_id=u_anf2.id,
                lat=-38.01,
                lng=-57.535,
            )
            p5 = Propiedad(
                titulo="Estudio minimalista en San Telmo",
                direccion="Defensa 780",
                ciudad="Buenos Aires",
                precio_noche=Decimal("32000.00"),
                capacidad=2,
                anfitrion_id=u_anf2.id,
                lat=-34.62,
                lng=-58.372,
            )
            p6 = Propiedad(
                titulo="Finca con viñedos y pileta",
                direccion="Ruta 15 km 4",
                ciudad="Mendoza",
                precio_noche=Decimal("110000.00"),
                capacidad=8,
                anfitrion_id=u_anf1.id,
                lat=-33.05,
                lng=-68.88,
            )
            db.add_all([p1, p2, p3, p4, p5, p6])
            db.flush()

            relaciones = [
                (p1, ["Wifi", "Aire acondicionado", "Cocina equipada", "Lavarropas"]),
                (p2, ["Wifi", "Pileta", "Parrilla", "Estacionamiento", "Cocina equipada"]),
                (p3, ["Wifi", "Estacionamiento", "Acepta mascotas", "Parrilla"]),
                (p4, ["Wifi", "Aire acondicionado", "Cocina equipada", "Estacionamiento"]),
                (p5, ["Wifi", "Cocina equipada"]),
                (p6, ["Wifi", "Pileta", "Parrilla", "Estacionamiento", "Acepta mascotas", "Cocina equipada"]),
            ]
            for prop, am_nombres in relaciones:
                for nom in am_nombres:
                    if nom in amenidades_objs:
                        db.add(PropiedadAmenidad(propiedad_id=prop.id, amenidad_id=amenidades_objs[nom].id))
            db.commit()

        # 5. Asegurar reservas iniciales
        if db.query(Reserva).count() == 0:
            props = db.query(Propiedad).all()
            users = db.query(Usuario).all()
            if len(props) >= 2 and len(users) >= 2:
                r1 = Reserva(
                    propiedad_id=props[0].id,
                    huesped_id=users[0].id,
                    fecha_inicio=date(2026, 8, 20),
                    fecha_fin=date(2026, 8, 24),
                    estado="confirmada",
                    total=Decimal("192000.00"),
                    metodo_pago="dinero",
                    horas_ganadas=960,
                )
                r2 = Reserva(
                    propiedad_id=props[1].id,
                    huesped_id=users[1].id,
                    fecha_inicio=date(2026, 9, 2),
                    fecha_fin=date(2026, 9, 6),
                    estado="pendiente",
                    total=Decimal("288000.00"),
                    metodo_pago="dinero",
                    horas_ganadas=1440,
                )
                db.add_all([r1, r2])
                db.flush()

                # Reseña de ejemplo
                re1 = Resena(
                    reserva_id=r1.id,
                    autor_id=users[0].id,
                    puntaje=5,
                    comentario="Excelente estadía, muy cómodo y limpio.",
                    fecha=date(2026, 8, 25),
                )
                db.add(re1)
                db.commit()

        print("Verificación y siembra de base de datos finalizada con éxito!")
    except Exception as e:
        db.rollback()
        print(f"Error durante la inicialización: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    init_database()