class ViagemCrazy:
    """Representa uma sugestão de viagem (destino, reserva e orçamento)."""

    def __init__(self, destino, reserva, orcamento):
        self.destino = destino
        self.reserva = reserva
        self.orcamento = orcamento

    def exibir(self):
        print(f"Destino: {self.destino}, Reserva: {self.reserva}, Orçamento: {self.orcamento}")

    def __repr__(self):
        return (
            f"ViagemCrazy(destino={self.destino!r}, "
            f"reserva={self.reserva!r}, orcamento={self.orcamento!r})"
        )
