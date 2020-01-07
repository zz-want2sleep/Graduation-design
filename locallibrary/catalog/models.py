from django.dispatch import receiver
from django.db.models.signals import post_save
import uuid  # Required for unique book instances
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.


class Genre(models.Model):
    """
    Model representing a book genre(e.g.Science Fiction,Non Fiction).
    """
    name = models.CharField(
        max_length=200, help_text="Enter a book genre (e.g. Science Fiction,French Poetry etc.)")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name


class Language(models.Model):
    """
    Model representing a language(e.g. English,French etc.)
    """
    language = models.CharField(
        max_length=100, help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        return self.language


class Book(models.Model):
    """
    Model representing a book(but not a specific copy of a book)
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField(
        'ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(
        Genre, help_text="Select a genre for this book 按住 ”Control“，或者Mac上的 “Command”，可以选择多个。")
    # ManyToManyField used because genre can contain many books. Books can cover many genres.
    # Genre class has already been defined so we can specify the object above.
    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)
    pic = models.ImageField('picture', upload_to='BookImage', null=True,
                            blank=True, help_text='上传相应的图片。', default='defaultImage/404.png')

    class Meta:
        ordering = ["-title"]

    def __str__(self):
        """
        String for representing the Model object
        """
        return self.title

    def get_absolute_url(self):
        """
        Return the url to access a particular book instance.
        """
        return reverse('catalog:book-detail', args=[(str(self.id))])

    def display_genre(self):
        """
        create a string for the Genre.This is required to display genre in Admin.
        """
        return ','.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'

    def display_genre1(self):
        """
        create a string for the Genre.This is required to display genre in Admin.+1
        """
        return ','.join([genre.name for genre in self.genre.all()])
    display_genre1.short_description = 'Genre1'


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    appointment_time = models.DateField(null=True, blank=True)
    appointment = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointment')
    borrower = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='borrower')

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS,
                              blank=True, default='m', help_text='当前图书副本状态')

    class Meta:
        ordering = ["status"]
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id, self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and datetime.date.today() > self.due_back:
            return True
        return False

    @property
    def is_overappointment(self):
        if self.appointment_time and datetime.date.today() > self.appointment_time+datetime.timedelta(days=1):
            return True
        return False

    @property
    def calculate_due_back(self):
        return datetime.date.today().__rsub__(self.due_back).days


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(
        help_text='时间格式：2019/10/04', null=True, blank=True)
    date_of_death = models.DateField(
        'died', help_text='时间格式：2019/10/04',  null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('catalog:author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name']


class History(models.Model):
    master = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    books = models.CharField(
        max_length=200, help_text="Enter some book titles",)
    rent_time = models.DateField(
        help_text='时间格式：2019/12/11', null=True, blank=True)

    class Meta:
        ordering = ['rent_time']


class HistoryByManager(models.Model):
    master = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    books = models.CharField(
        max_length=200, help_text="Enter some book titles",)
    rent_time = models.DateField(
        help_text='时间格式：2019/12/11', null=True, blank=True)

    class Meta:
        ordering = ['rent_time']


class Visitor1(models.Model):
    user = models.OneToOneField(
        User, null=False, related_name='visitor1', on_delete=models.CASCADE)
    session_key = models.CharField(null=True, max_length=40)
    ip = models.CharField(null=True, max_length=200)
# information


class Informations(models.Model):
    title = models.CharField(
        verbose_name=u'标题', null=True, blank=True, max_length=20, help_text=u"通知的标题")
    info = models.TextField(verbose_name=u'通知', null=True,
                            blank=True, max_length=200, help_text=u"通知的内容")
    Release_time = models.DateField(
        verbose_name=u'发布时间', null=True, blank=True, help_text='时间格式：2019/12/11', default=datetime.date.today)

    class Meta:
        ordering = ['Release_time']

# relate user profile


class UserExtension1(models.Model):
    # 定义一个一对一的外键
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='extension')
    telephone = models.CharField(
        max_length=11, unique=True, null=True, blank=True,)
    school = models.CharField(
        max_length=100, null=True, blank=True, default='中南林业科技大学涉外学院')


# 这是一个信号函数，即每创建一个User对象时，就会新建一个userextionsion进行绑定，使用了receiver这个装饰器
@receiver(post_save, sender=User)
def handler_user_extension(sender, instance, created, **kwargs):
    if created:  # 如果是第一次创建user对象，就创建一个userextension对象进行绑定
        UserExtension1.objects.create(user=instance)
    else:  # 如果是修改user对象，那么也要将extension进行保存
        instance.extension.save()
# old session


class OldSession(models.Model):
    session_key = models.CharField(null=True, max_length=150)

# old ip


class OldIp(models.Model):
    ip = models.CharField(null=True, max_length=100)
