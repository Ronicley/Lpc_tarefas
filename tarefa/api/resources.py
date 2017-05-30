from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie import fields, utils
from tarefa.models import *
from django.contrib.auth.models import User
from django.http import HttpResponse
from tastypie.exceptions import Unauthorized

class UsuarioResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        if not(Usuario.objects.filter(nome = bundle.data['nome'])):
            usuario = Usuario()
            usuario.nome = bundle.data['nome']
            usuario.email = bundle.data['email']
            usuario.senha = bundle.data['senha']
            usuario.save()
            bundle.obj = usuario
            return bundle
        else:
            raise Unauthorized('Já existe usuario com esse nome')
    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel apagar toda a lista de usuarios! ")

    class Meta:
        queryset = Usuario.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "nome": ('exact', 'startswith')
        }
        authorization= Authorization()


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['password', 'is_active']


class ProjetoResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        if not(Projeto.objects.filter(nome = bundle.data['nome'])):
            projeto = Projeto()
            projeto.nome = bundle.data['nome']
            projeto.save()
            bundle.obj = projeto
            return bundle
        else:
            raise Unauthorized('Já existe Projeto com esse nome')

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel apagar toda a lista de Projetos! ")

    class Meta:
        queryset = Usuario.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "nome": ('exact', 'startswith')
        }

class TarefaResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        u = bundle.data['usuario'].split("/")
        p = bundle.data['projeto'].split("/")
        if not(Tarefa.objects.filter(dataEHoraDeInicio= bundle.data['dataEHoraDeInicio'])):

            tarefa = Tarefa()
            tarefa.dataEHoraDeInicio = bundle.data['dataEHoraDeInicio']
            tarefa.usuario = Usuario.objects.get(pk = int(u[4]) )
            tarefa.projeto = Projeto.objects.get(pk = int(p[4]) )
            tarefa.save()
            bundle.obj = tarefa
            return bundle

        else:
            raise Unauthorized("Tarefa ja cadastrada neste dia!")

    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel apagar toda a lista de Tarefas! ")

    def obj_delete(self, bundel, **kwargs):
            if not(Tarefa.objects.filter(usuario = int(u[4]))):
                tarefa = Tarefa.objects.get(pk=bundle.data.id)
                Tarefa.objects.filter(post=tarefa.post).delete()
                return super(DeleteTarefa, self).obj_delete(bundle, user=bundle.request.user)

            else:
                raise Unauthorized("Somente o usuario dono pode excluir!")

    def obj_update(self, bundle, **kwargs):
        tarefa = Tarefa.objects.get(pk=bundle.data.id)
        Tarefa.objects.filter(post=tarefa.post).update()
        return super(DeleteTarefa, self).obj_delete(bundle, user=bundle.request.user)

    usuario = fields.ToOneField(UsuarioResource, 'usuario')
    projeto = fields.ToOneField(ProjetoResource, 'tarefa')
    class Meta:
        queryset = Tarefa.objects.all()
        allowed_methods = ['get', 'post', 'delete', 'put']
        authorization = Authorization()
        filtering = {
            "dataEHoraDeInicio": ('exact', 'startswith')
        }

class ProjetoUsuarioResource(ModelResource):
    def obj_create(self, bundle, **kwargs):
        u = bundle.data['usuario'].split("/")
        p = bundle.data['projeto'].split("/")
        if not(ProjetoUsuario.objects.filter(usuario = u[4], projeto = p[4])):


            projetoUsuario = ProjetoUsuario()
            projetoUsuario.dataEHoraDeInicio = bundle.data['dataEHoraDeInicio']
            projetoUsuario.usuario = Usuario.objects.get(pk = int(u[4]) )
            projetoUsuario.projeto = Projeto.objects.get(pk = int(p[4]) )
            projetoUsuario.save()
            bundle.obj = projetoUsuario
            return bundle
        else:
            raise Unauthorized("Projeto ou Tarefa ja cadastrada!")
    def obj_delete_list(self, bundle, **kwargs):
        raise Unauthorized("Não é possivel apagar toda a lista de Projetos e Usuarios! ")
    usuario = fields.ToOneField(UsuarioResource, 'usuario')
    tarefa = fields.ToOneField(TarefaResource, 'tarefa')
    class Meta:
        queryset = ProjetoUsuario.objects.all()
        allowed_methods =['get', 'post', 'delete', 'put']
        authorization = Authorization()
