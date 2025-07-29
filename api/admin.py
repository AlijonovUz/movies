from django.contrib import admin

from .models import Genre, Country, Movie, MovieURL


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
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


@admin.register(Country)
class GenreAdmin(admin.ModelAdmin):
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


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
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
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'country':
            if Country.objects.all().exists():
                kwargs['empty_label'] = "Tanlang"
            else:
                kwargs['empty_label'] = "Mavjud emas"

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'age_limit' or db_field.name == 'language':
            kwargs['choices'] = db_field.get_choices(
                include_blank=True,
                blank_choice=[("", "Tanlang")]
            )
        return super().formfield_for_choice_field(db_field, request, **kwargs)