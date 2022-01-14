from rest_framework import serializers

from video.models import Genre, Video, Anime, Comment, Favorites, Rating


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AnimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anime
        fields = '__all__'

    def in_favorite(self, anime):
        try:
            user = self.context.get('request').user
            return user.favorites.filter(anime=anime).exists()
        except Exception:
            return False

    def sr_rating(self, anime):
        user = self.context.get('request').user
        return user.rating.filter(anime=anime).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['in_favorite'] = self.in_favorite(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            representation['in_favorite'] = self.in_favorite(instance)
        representation['fav_count'] = instance.favorites.count()
        representation['rating_avg'] = RatingSerializer(instance.rating.all(), many=True).data
        a = 0
        for ord_dict in representation['rating_avg']:
            a += ord_dict.get('rating')
            print(a)
            representation['rating_avg'] = a/len(RatingSerializer(instance.rating.all(), many=True).data)
        return representation


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

    def is_liked(self, video):
        try:
            user = self.context.get('request').user
            return user.liked.filter(video=video).exists()
        except Exception:
            return False

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['is_liked'] = self.is_liked(instance)
        user = self.context.get('request').user
        if user.is_authenticated:
            representation['is_liked'] = self.is_liked(instance)
        representation['likes_count'] = instance.liked.count()
        return representation


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)


class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        exclude = ['user']

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError('Введите от 1 до 5')
        return rating

    def validate(self, attrs):
        user = self.context.get('request').user
        order = Rating.objects.filter(user=user)
        if order:
            raise serializers.ValidationError('Пощел нахер')
        # if user in order
        print(len(order))
        return attrs


    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user
        return super().create(validated_data)
