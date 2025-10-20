from django.db import models
from datetime import time


class Loja(models.Model):
    """
    Modelo para representar uma loja parceira.
    """
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    horario_abertura = models.TimeField(default=time(9, 0))
    horario_fechamento = models.TimeField(default=time(18, 0))
    atendimento_emergencia = models.BooleanField(
        default=False, 
        verbose_name="Atende Emergências (24h)"
    )
    descricao = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Descrição",
        help_text="Fale um pouco sobre a loja, seus serviços e diferenciais."
    )
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    foto = models.ImageField(
        upload_to='loja/fotos/', 
        blank=True, 
        null=True, 
        verbose_name="Foto da Loja"
    )

    def __str__(self):
        return self.nome


class CarouselImage(models.Model):
    """
    Modelo para armazenar as imagens do carrossel da página inicial.
    """
    image = models.ImageField(upload_to='carousel_images/', verbose_name="Imagem", help_text="Use imagens com proporção de 1200x400 pixels.")
    caption_title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Título da Legenda")
    caption_text = models.CharField(max_length=200, blank=True, null=True, verbose_name="Texto da Legenda")
    order = models.PositiveIntegerField(default=0, help_text="Ordem de aparição (números menores primeiro).")

    class Meta:
        ordering = ['order']
        verbose_name = "Imagem do Carrossel"
        verbose_name_plural = "Imagens do Carrossel"

    def __str__(self):
        return self.caption_title or f"Imagem {self.id}"
