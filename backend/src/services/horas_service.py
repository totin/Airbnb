from src.db.models.saldo_horas import SaldoHoras
from src.db.models.transaccion_horas import TransaccionHoras, TipoTransaccionHoras


class HorasService:
    def __init__(self, db):
        self.db = db

    def obtener_saldo(self, usuario_id: int) -> SaldoHoras:
        saldo = self.db.query(SaldoHoras).filter(SaldoHoras.usuario_id == usuario_id).first()
        if not saldo:
            saldo = SaldoHoras(usuario_id=usuario_id, horas=1000)
            self.db.add(saldo)
            self.db.commit()
            self.db.refresh(saldo)
        return saldo

    def crear_saldo_inicial(self, usuario_id: int):
        saldo = self.db.query(SaldoHoras).filter(SaldoHoras.usuario_id == usuario_id).first()
        if not saldo:
            saldo = SaldoHoras(usuario_id=usuario_id, horas=1000)
            self.db.add(saldo)
            self.db.commit()
            self.db.refresh(saldo)
        return saldo

    def sumar_horas(self, usuario_id: int, cantidad: int, reserva_id: int, tipo: TipoTransaccionHoras):
        saldo = self.obtener_saldo(usuario_id)
        saldo.horas += cantidad
        self.db.add(TransaccionHoras(
            usuario_id=usuario_id,
            reserva_id=reserva_id,
            tipo=tipo,
            cantidad=cantidad,
        ))
        self.db.commit()
        self.db.refresh(saldo)
        return saldo

    def restar_horas(self, usuario_id: int, cantidad: int, reserva_id: int, tipo: TipoTransaccionHoras):
        saldo = self.obtener_saldo(usuario_id)
        if saldo.horas < cantidad:
            raise ValueError(
                f"Saldo de horas insuficiente. Tenés {saldo.horas}, necesitás {cantidad}"
            )
        saldo.horas -= cantidad
        self.db.add(TransaccionHoras(
            usuario_id=usuario_id,
            reserva_id=reserva_id,
            tipo=tipo,
            cantidad=cantidad,
        ))
        self.db.commit()
        self.db.refresh(saldo)
        return saldo

    def listar_historial(self, usuario_id: int):
        return (
            self.db.query(TransaccionHoras)
            .filter(TransaccionHoras.usuario_id == usuario_id)
            .order_by(TransaccionHoras.fecha.desc())
            .all()
        )