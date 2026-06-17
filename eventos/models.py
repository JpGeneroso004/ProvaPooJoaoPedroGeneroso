from django.db import models
from inventario.models import Tenda, ConjuntoPalco


class Evento(models.Model):
    STATUS = [
        ('agendado',     'Agendado'),
        ('em_andamento', 'Em Andamento'),
        ('concluido',    'Concluído'),
        ('cancelado',    'Cancelado'),
    ]

    nome       = models.CharField('Nome do Evento', max_length=200)
    cliente    = models.CharField('Cliente / Responsável', max_length=200)
    telefone   = models.CharField('Telefone', max_length=20, blank=True)
    local      = models.CharField('Local / Endereço', max_length=300)
    cidade     = models.CharField('Cidade', max_length=100, default='Formosa')
    latitude   = models.DecimalField('Latitude',  max_digits=10, decimal_places=7, null=True, blank=True)
    longitude  = models.DecimalField('Longitude', max_digits=10, decimal_places=7, null=True, blank=True)
    data_inicio = models.DateField('Data de Início')
    data_fim    = models.DateField('Data de Fim')
    status      = models.CharField('Status', max_length=20, choices=STATUS, default='agendado')
    observacoes = models.TextField('Observações', blank=True)
    tendas      = models.ManyToManyField(Tenda, blank=True, verbose_name='Tendas', related_name='eventos')
    conjuntos   = models.ManyToManyField(ConjuntoPalco, blank=True,
                                         verbose_name='Conjuntos de Palco/Piso', related_name='eventos')
    criado_em   = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
        ordering = ['-data_inicio']

    def __str__(self):
        return f'{self.nome} – {self.data_inicio}'

    def get_status_class(self):
        return {
            'agendado':     'badge-agendado',
            'em_andamento': 'badge-andamento',
            'concluido':    'badge-concluido',
            'cancelado':    'badge-cancelado',
        }.get(self.status, '')

    def total_tendas(self):
        return self.tendas.count()

    def total_placas(self):
        return sum(c.quantidade_placas for c in self.conjuntos.all())

    def get_resumo(self):
        """Polimorfismo: resumo específico para Evento."""
        return (
            f'Evento: {self.nome} | Cliente: {self.cliente} | '
            f'{self.data_inicio} → {self.data_fim} | {self.get_status_display()}'
        )
