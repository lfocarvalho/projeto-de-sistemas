from django.db import models
from loja.models import Loja
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

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
