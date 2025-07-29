from django.contrib import admin

from .models import Genres, Movies, MovieURL


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    list_filter = ('id', 'name')
    list_per_page = 10
    search_fields = ('id', 'name')
    actions_on_top = False
    actions_on_bottom = True

    prepopulated_fields = {
        'slug': ('name',)
    }


class MovieURLAdmin(admin.StackedInline):
    model = MovieURL
    extra = 0
    min_num = 1
    validate_min = True
    readonly_fields = ['embed_url']

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == "type":
            kwargs['choices'] = db_field.get_choices(
                include_blank=True,
                blank_choice=[("", "Tanlang")]
            )
        return super().formfield_for_choice_field(db_field, request, **kwargs)


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'like', 'dislike', 'view', 'created_at')
    list_display_links = ('id', 'title')
    list_filter = ('id', 'title')
    list_per_page = 10
    search_fields = ('id', 'title')
    readonly_fields = ('like', 'dislike', 'view')
    date_hierarchy = 'created_at'
    actions_on_top = False
    actions_on_bottom = True

    prepopulated_fields = {
        'slug': ('title',)
    }

    inlines = [MovieURLAdmin]