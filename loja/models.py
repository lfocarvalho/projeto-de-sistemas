from django.db import models
from datetime import time
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator




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
    avaliacao_media = models.FloatField(default=0)
    favoritada_por = models.ManyToManyField(User, related_name='lojas_favoritadas', blank=True)

    def __str__(self):
        return self.nome

    def atualizar_media(self):
        avaliacoes = self.avaliacoes.all()
        if avaliacoes.exists():
            media = sum(a.nota for a in avaliacoes) / avaliacoes.count()
            self.avaliacao_media = round(media, 1)
        else:
            self.avaliacao_media = 0
        self.save()

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


class Avaliacao(models.Model):
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('loja', 'usuario')  # Um usuário avalia cada loja só uma vez

    def __str__(self):
        return f"{self.loja.nome} - {self.nota}⭐"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.loja.atualizar_media()

class LojaFavorita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favoritos_lojas')
    loja = models.ForeignKey('Loja', on_delete=models.CASCADE, related_name='favoritos_relacionados')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'loja')

    def __str__(self):
        return f"{self.usuario.username} ❤️ {self.loja.nome}"