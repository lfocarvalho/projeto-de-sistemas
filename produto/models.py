from django.db import models
from django.contrib.auth.models import User
from loja.models import Loja, CarouselImage
from .consts import ANIMAL_CHOICES, IDADE_CHOICES, PORTE_CHOICES


class Categoria(models.Model):
    """
    Modelo para categorizar os produtos e serviços.
    Ex: Ração, Vacina, Brinquedo, Banho e Tosa.
    """
    nome = models.CharField(max_length=100, unique=True, help_text="Nome da categoria (ex: Ração, Brinquedos, Higiene)")
    descricao = models.TextField(blank=True, null=True, help_text="Descrição sobre a categoria.")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nome


class Produto(models.Model):
    """
    Modelo para representar produtos ou serviços oferecidos pelas lojas.
    """

    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='produtos')
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True, related_name='produtos')
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0, help_text="Quantidade em estoque. Para serviços, pode ser 0.")
    disponivel = models.BooleanField(default=True)

    # Campos para filtro
    animal_destino = models.CharField(max_length=10, choices=ANIMAL_CHOICES, default='TODOS')
    porte_animal = models.CharField(max_length=10, choices=PORTE_CHOICES, default='TODOS', blank=True)
    idade_animal = models.CharField(max_length=10, choices=IDADE_CHOICES, default='TODOS', blank=True)

    foto = models.ImageField(
        upload_to='produtos_fotos/', 
        blank=True, 
        null=True, 
        verbose_name="Foto do Produto"
    )

    # Interações
    curtido_por = models.ManyToManyField(User, related_name='produtos_curtidos', blank=True)
    avaliacao_media = models.FloatField(default=0)

    def atualizar_media(self):
        avaliacoes = self.avaliacoes.all()
        if avaliacoes.exists():
            media = sum(a.nota for a in avaliacoes) / avaliacoes.count()
            self.avaliacao_media = round(media, 1)
        else:
            self.avaliacao_media = 0
        self.save(update_fields=['avaliacao_media'])

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


class AvaliacaoProduto(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='avaliacoes_produto')
    nota = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('produto', 'usuario')
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.usuario} - {self.produto} ({self.nota})"
