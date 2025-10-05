from django.db import models

class Loja(models.Model):
    """
    Modelo para representar uma loja parceira.
    """
    nome = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20)
    horario_funcionamento = models.CharField(max_length=100)
    email = models.EmailField()
    website = models.URLField(blank=True)
    foto = models.ImageField(
        upload_to='loja/fotos/', 
        blank=True, 
        null=True, 
        verbose_name="Foto da Loja"
    )

    def __str__(self):
        return self.nome
