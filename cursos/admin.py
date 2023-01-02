from django.contrib import admin

from cursos.models import Avaliacao, Curso

# Register your models here.


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('titulo','url','criacao','atualizacao','ativo')
    
@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('curso','nome','email','avaliacao','criacao','atualizacao','ativo')