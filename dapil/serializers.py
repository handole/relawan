from rest_framework import serializers
from dapil.models import Kabupaten, Kecamatan, Kelurahan

class KelurahanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Kelurahan
        fields = ("__all__")


class KecamatanSerializer(serializers.ModelSerializer):
    kelurahan = KelurahanSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Kecamatan
        fields = ("__all__")

class KabupatenSerializer(serializers.ModelSerializer):
    kecamatan = KecamatanSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Kabupaten
        fields = ("__all__")