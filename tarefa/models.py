from django.db import models
from django.utils import timezone

class Usuario(models.Model):
    nome = models.CharField('nome', max_length=200)
    email = models.CharField('email', max_length=200)
    senha = models.CharField('senha', max_length=200)
    def save(self, *args, **kwargs):
        self.nome = self.nome
        self.email = self.email

        super(Usuario, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.nome)

class Projeto(models.Model):
    nome = models.CharField('nome', max_length=200)

    def __str__(self):
        return '{}'.format(self.nome)

class Tarefa(models.Model):
    nome = models.CharField('nome', max_length=200)
    dataEHoraDeInicio = models.DateTimeField('dataEHoraDeInicio', default=timezone.now)
    usuario = models.ForeignKey('Usuario')
    projeto = models.ForeignKey('Projeto')

    def save(self, *args, **kwargs):
        self.dataEHoraDeInicio = self.dataEHoraDeInicio

        super(Tarefa, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.usuario)

class ProjetoUsuario(models.Model):
    usuario = models.ForeignKey('Usuario')
    projeto = models.ForeignKey('Projeto')

    def __str__(self):
        return '{}'.format(self.usuario)
