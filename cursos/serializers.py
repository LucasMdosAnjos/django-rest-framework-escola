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
    
    def validate_avaliacao(self,valor):
        if valor in range(1, 6): # 1, 2, 3, 4, 5
            return valor
        else:
            raise serializers.ValidationError('A avaliação precisa ser um inteiro entre 1 e 5')

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