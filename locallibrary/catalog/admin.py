from django.contrib.auth.models import User
from .models import UserExtension1
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Informations
from django.utils.safestring import mark_safe
from django.contrib import admin

# Register your models here.
from .models import Author, Book, BookInstance, Genre, Language, History, HistoryByManager
# 在管理界面去改变一个模型的展示方式，当你定义了 ModelAdmin 类（描述布局）和将其注册到模型中
# admin.site.register(Author)
# define the admin class


class BookInline(admin.StackedInline):
    model = Book
    extra = 0
    # exclude = ('isbn',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name',
                    'date_of_birth', 'date_of_death')
    search_fields = ('last_name', 'first_name')
    fields = ['last_name', 'first_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
    list_per_page = 10


# 还可以使用exclude属性来声明要从表单中排除的属性列表（将显示模型中的所有其他属性）。
# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)

# 使用@register 装饰器来注册模型（这和 admin.site.register() 语法作用一样)
# admin.site.register(Book)
# Register the Admin classes for Book using the decorator
# 可以通过声明 inlines, 类型 TabularInline (水平布局 ) or StackedInline (垂直布局 ，就像默认布局)这样做. 您可以通过在您的以下的粗体中添加以下行，将内容中的BookInstance信息添加到我们的Book详细信息中BookAdmin


class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    list_display = ('title', 'author', 'display_genre',
                    'isbn', 'language', 'image_data')
    list_filter = ('genre',)
    readonly_fields = ('image_data',)  # 必须加这行 否则访问编辑页面会报错
    inlines = [BookInstanceInline]
    list_per_page = 10

    def image_data(self, obj):
        if obj.pic:
            return mark_safe(u'<img src="%s" width="100px" />' % obj.pic.url)

    # 页面显示的字段名称
    image_data.short_description = u'图书图片'


# admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'id', 'imprint', 'status', 'borrower',
                    'appointment', 'appointment_time', 'due_back')
    search_fields = ('book__title',)
    list_filter = ('status', 'due_back', 'appointment_time')
    fieldsets = (
        (None, {'fields': ('book', 'imprint', 'id',)}),
        ('Availability', {'fields': ('status', 'due_back',
                                     'borrower', 'appointment', 'appointment_time')})
        # 对相关的模型信息进行分组
    )
    list_per_page = 10


# admin.site.register(History)
@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('master', 'books', 'rent_time',)
    search_fields = ('master__username',)
    list_filter = ('rent_time',)
    fieldsets = (
        (None, {'fields': ('master', 'books', 'rent_time',)}),

        # 对相关的模型信息进行分组
    )
    list_per_page = 10


@admin.register(HistoryByManager)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('master', 'books', 'rent_time',)
    search_fields = ('master__username',)
    list_filter = ('rent_time',)
    fieldsets = (
        (None, {'fields': ('master', 'books', 'rent_time',)}),

        # 对相关的模型信息进行分组
    )
    list_per_page = 10


@admin.register(Informations)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'info', 'Release_time',)
    search_fields = ('title',)
    list_filter = ('Release_time',)
    list_per_page = 10


admin.site.register(Genre)
admin.site.register(Language)


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class UserExtensionInline(admin.StackedInline):
    model = UserExtension1
    can_delete = False
    verbose_name_plural = 'UserExtension'

# Define a new User admin


class UserAdmin(BaseUserAdmin):
    inlines = (UserExtensionInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
