from rest_framework import serializers
from cursos.models import Curso, Avaliacao


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {
            'email': {'write_only': True}
        }
        model = Avaliacao
        fields = (
            'id', 'curso', 'nome', 'email', 'comentario', 'avaliacao', 'criacao', 'ativo'
        )

class CursoSerializer(serializers.ModelSerializer):
    #Nested Relationship
    #avaliacoes = AvaliacaoSerializer(many=True, read_only=True)

    #HyperLinked Related Field
    #avaliacoes = serializers.HyperlinkedRelatedField(many=True, read_only=True,view_name='avaliacao-detail')

    #Primary Key Related Field
    #avaliacoes = serializers.PrimaryKeyRelatedField(many=True,read_only=True)

    #Slug Related Field
    avaliacoes = serializers.SlugRelatedField(many=True,read_only=True,slug_field='avaliacao')
    class Meta:
        model = Curso
        fields = ('id','titulo','url','criacao','ativo','avaliacoes')