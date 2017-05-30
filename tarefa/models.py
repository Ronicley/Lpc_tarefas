from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nome = models.CharField('nome', max_length=200)
    email = models.CharField('email', max_length=200)
    senha = models.CharField('senha', max_length=200)
    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        self.email = self.email.upper()

        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nome)

class Projeto(models.Model):
    nome = models.CharField('nome', max_length=200)

    def __str__(self):
        return '{}'.format(self.nome)

class Tarefa(models.Model):
    dataEHoraDeInicio =  models.DateTimeField('dataEHoraDeInicio', default=timezone.now)
    usuario = models.ForeignKey('Usuario')
    projeto = models.ForeignKey('Projeto')

    def __str__(self):
        return '{}'.format(self.dataEHoraDeInicio)
class ProjetoUsuario(models.Model):
    usuario = models.ForeignKey('Usuario')
    projeto = models.ForeignKey('Projeto')

    def __str__(self):
        return '{}'.format(self.Usuario)
