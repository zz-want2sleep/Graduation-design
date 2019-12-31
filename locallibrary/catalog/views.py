from django.contrib.auth.decorators import permission_required
from .models import Author
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.forms.utils import ErrorList
from .forms import RenewBookForm, AuthorModelForm,RentOutForm,BookinstanceForm1
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.views import generic
from django.shortcuts import render
from .models import Book, BookInstance, Author, Genre, Language,History,HistoryByManager
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.urls import reverse
import hashlib
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mass_mail
import datetime
from django.contrib.auth.decorators import login_required
# Create your views here.


def sendEmail(request, names):
    """
    a send email view function
    """
    datas = ()
    i = 1
    for name in [name for name in names.split(',')]:
        # user1 = get_object_or_404(User, username='徐超伟')
        # print(user1.email)
        if name:
            # print(name)
            user = get_object_or_404(User, username__exact=name)
            if not user.email:
                request.session['res'] = '0'
                # print(res)
                return HttpResponseRedirect(reverse('catalog:all-borrowed'))

            message = (u'还书提示', u'你已经超出了还书期限,请尽快归还图书。',
                       'LocalLibrarySystem<670736258@qq.com>', [user.email])
            datas += (message,)

    res = send_mass_mail(datas, fail_silently=False,)
    # print(res)
    request.session['res'] = res
    return HttpResponseRedirect(reverse('catalog:all-borrowed'))


@permission_required('auth.can_add')
def addusers(request):
    if request.method == "GET":
        return render(request, "addusers.html")
    elif request.method == "POST":
        # print(int(request.POST.get('firstnum')))
        nums = int(request.POST.get('nums'))
        # print(nums)

        firstnum = int(request.POST.get('firstnum'))
        # print(firstnum)
        # if request.session.get('success'):
        #     del request.session['success']
        # print(request.session['nums'])
        # return redirect(reverse('catalog:addusers1'))
        user_list = []
        for i in range(0, nums):
            str_user = str(firstnum) + '****'
            user_list.append(str_user)
            firstnum += 1
            if i == nums - 1:
                break        
        user_list = [User(username=line.split('****')[0].encode('utf-8').decode('utf-8'),
                          password=make_password("123456")) for line in user_list]
        try:

            User.objects.bulk_create(user_list)
        except Exception:
            request.session['error'] = 'error'
            return redirect(reverse('catalog:addusers'))
    if request.session.get('error'):
        del request.session['error']

    # request.session['success'] = '1'
    return redirect('/admin/auth/user/?e=1')



# @permission_required('auth.can_add')
# def addusers1(request):
#     """
#     viw function for add users of admin
#     """
#     nums = request.session.get('nums')
#     firstnum = request.session.get('firstnum')
#     firstnum = int(firstnum)
#     # print(firstnum)
#     f = open('users.txt', "w+")
#     for i in range(0, nums):

#         str_user = str(firstnum) + '****\n'
#         f.write(str_user)
#         firstnum += 1
#         if i == nums-1:
#             break
#     f.close()

#     user_list = []
#     with open(u'./users.txt', 'r', encoding='UTF-8') as f:
#         # for line in f:
#         #     print(line.split('****')[0].encode('gbk').decode('utf-8'))

#         user_list = [User(username=line.split('****')[0].encode('utf-8').decode('utf-8'),
#                           password=make_password("123456")) for line in f]
#         try:

#             User.objects.bulk_create(user_list)
#         except Exception:
#             request.session['error'] = 'error'
#             return redirect(reverse('catalog:addusers'))
#     del request.session['nums']
#     del request.session['firstnum']
#     if request.session.get('error'):
#         del request.session['error']

    # request.session['success'] = '1'
    # return redirect('/admin/auth/user/?e=1')

from .models import Informations
def index(request):
    """
    Viw function for home page of site.
    """
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books(status = 'a')
    num_instances_available = BookInstance.objects.filter(
        status__exact='a').count()
    num_authors = Author.objects.count()  # The all() is 'implied' by default
    information = Informations.objects.all()
    informations = information[0:5]

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors, 'num_visits': num_visits,
                 'informations':informations}
    )


# def test(request,name):
#     return render(
#         request,
#         'catalog/author_list1.html'
#     )


class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genres = Genre.objects.all()
        context['genres']=genres
        return context


class BookDetailView(generic.DetailView):
    model = Book
    


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5


class AuthorDetailView(generic.DetailView):
    model = Author


class AuthorListView1(generic.ListView):
    def get_queryset(self):
        if not self.kwargs['name']:
            self.authot_list = Author.objects.all()
        else:
            print(self.kwargs['name'])
            self.author_list = Author.objects.filter(Q(first_name__icontains=self.kwargs['name']) | Q(
                last_name__icontains=self.kwargs['name']))
            name = self.kwargs['name']

        return self.author_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    paginate_by = 5


class BookListView1(generic.ListView):
    def get_queryset(self):
        if not self.kwargs['name']:
            self.book_list = Book.objects.all()
        else:
            print(self.kwargs['name'])
            self.book_list = Book.objects.filter(
                title__icontains=self.kwargs['name'])
            name = self.kwargs['name']
        return self.book_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
import re
# Genre search
def genre_books(request, name):
    book_list=[]
    book_list1 = Book.objects.all()
    for book in book_list1:
        genre_name = book.display_genre1()
        # print(book.display_genre())
        # print(re.search(name,genre_name))
        if re.search(name,genre_name)!=None:
            book_list.append(book)
            print(book_list)
    return render(
        request,
        'catalog/book_list_genre.html',
        context={'book_list': book_list,'title':name,}
    )
def genre_books1(request, name,name1):
    book_list=[]
    book_list1 = Book.objects.all()
    book_list2 = []
    for book in book_list1:
        genre_name = book.display_genre()
        # print(book.display_genre())
        # print(re.search(name,genre_name))
        if re.search(name,genre_name)!=None:
            book_list2.append(book)
            print(book_list)
    for book in book_list2:
        genre_name = book.title
        # print(book.display_genre())
        # print(re.search(name,genre_name))
        if re.search(name1,genre_name)!=None:
            book_list.append(book)
            print(book_list)
    return render(
        request,
        'catalog/book_list_genre.html',
        context={'book_list': book_list,'title':name,}
    )


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


class LoanedBooksByUserListView1(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user. 
    """

    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 5

    def get_queryset(self):
        if not self.kwargs['name']:
            self.bookinstance_list = BookInstance.objects.all()
        else:
            print(self.kwargs['name'])
            self.bookinstance_list = BookInstance.objects.filter(
                book__title__icontains=self.kwargs['name']).filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
            name = self.kwargs['name']
        return self.bookinstance_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


class LoanedBooksAllListView1(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 5

    def get_queryset(self):
        if not self.kwargs['name']:
            self.bookinstance_list = BookInstance.objects.all()
        else:
            print(self.kwargs['name'])
            self.bookinstance_list = BookInstance.objects.filter(
                book__title__icontains=self.kwargs['name']).filter(status__exact='o').order_by('due_back')
            name = self.kwargs['name']
        return self.bookinstance_list


# myself setting form error css


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return '<div class="errorlist">%s</div>' % ''.join(['<div class="alert alert-warning" role="alert">%s</div>' % e for e in self])

# form design function
from django.contrib.auth.decorators import login_required
@login_required
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST, error_class=DivErrorList)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('catalog:all-borrowed')+
            '?m=1')

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(
            initial={'renewal_date': proposed_renewal_date, }, error_class=DivErrorList)

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst': book_inst})


# classes created for the general forms views


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = '__all__'
    initial = {}

    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('catalog:authors')
    permission_required = 'catalog.can_mark_returned'


class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = '__all__'
    initial = {}

    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language','pic']
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('catalog:books')
    permission_required = 'catalog.can_mark_returned'


# setting popup to add author
def p1(request):

    if request.method == "GET":
        form = AuthorModelForm(request.POST, error_class=DivErrorList)
        return render(request, "p1.html", {'form': form, })
    elif request.method == "POST":
                # Create a form instance and populate it with data from the request (binding):
        form = AuthorModelForm(request.POST, error_class=DivErrorList)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            author = Author.objects.create()
            author.first_name = form.cleaned_data['first_name']
            author.last_name = form.cleaned_data['last_name']
            author.date_of_birth = form.cleaned_data['date_of_birth']
            author.date_of_death = form.cleaned_data['date_of_death']
            author.save()

            # redirect to a new URL:
            return render(request, "popup_response.html", {"author": author,'id':author.pk})

#setting update user password

from django.views.generic.base import TemplateView

class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('catalog:password_change_done')
    template_name = 'catalog/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'registration/password_change_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
# looking for self information
class UserDetailView(LoginRequiredMixin,generic.DetailView):
    model = User
    template_name = 'catalog/user_profile.html'

# update user profile
class UserUpdate(LoginRequiredMixin,UpdateView):
    model = User
    success_url = reverse_lazy('catalog:index')
    fields = ['first_name', 'last_name', 'email']
    template_name = 'catalog/user_form.html'
# setting rent out 
# class RentOutUpdate(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
#     model = BookInstance
#     fields = ['status', 'borrower','due_back']
#     template_name = 'catalog/bookinstance_form.html'
#     permission_required = 'catalog.can_mark_returned'
#     def get_success_url(self):
#         print(self.kwargs['pk'])
#         return reverse_lazy('catalog:book-detail', args=[self.kwargs['pk']])
#     def get_object(self):
#         if not self.kwargs['id']:
#             raise Http404(u"Book not instances!") 
#         else:
#             # print(self.kwargs['id'])
#             return get_object_or_404(BookInstance,id=self.kwargs['id'])

@login_required
@permission_required('catalog.can_mark_returned')
def rent_out(request,id,pk):
    book_inst = get_object_or_404(BookInstance, id=id)
    

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RentOutForm(request.POST, error_class=DivErrorList)
        

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.status = form.cleaned_data['status']
            book_inst.borrower = form.cleaned_data['borrower']
            book_inst.appointment = form.cleaned_data['appointment']
            book_inst.due_back = form.cleaned_data['due_back']
            book_inst.appointment_time = form.cleaned_data['appointment_time']
            book_inst.save()
            history = History.objects.create(master=book_inst.borrower)
            history1 = HistoryByManager.objects.create(master=book_inst.borrower)
            history.rent_time = datetime.date.today()
            history.books = book_inst.book.title
            history1.rent_time = datetime.date.today()
            history1.books = book_inst.book.title
            history.save()
            history1.save()

            #record log
            from django.contrib.admin.options import ModelAdmin
            object=book_inst
            message = '成功修改当前图书副本'
            ModelAdmin.log_change(request,request,object,message)

            # redirect to a new URL:
            return HttpResponseRedirect(reverse_lazy('catalog:book-detail', args=(pk,))+'?success=4')

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RentOutForm(
            initial={'status':book_inst.status,'borrower':book_inst.borrower,'due_back': proposed_renewal_date,'appointment':book_inst.appointment, }, error_class=DivErrorList)

    return render(request, 'catalog/bookinstance_form.html', {'form': form, 'bookinst': book_inst})


@login_required
def appointmentBook(request, pk, id, pk1):
    nums=BookInstance.objects.filter(appointment__exact=request.user)
    if (len(nums) >= 5):
        return redirect(reverse_lazy('catalog:book-detail', args=(pk,)) + '?success=5') 
    bookinst = get_object_or_404(BookInstance, id=id)
    # print(bookinst.appointment)
    if  bookinst.appointment!=None:
        return redirect(reverse_lazy('catalog:book-detail', args=(pk,)) + '?success=2')
    else:
        bookinst.appointment = get_object_or_404(User, pk=pk1)
        bookinst.status = 'r'
        bookinst.appointment_time = datetime.date.today()
        bookinst.save()
        return redirect(reverse_lazy('catalog:book-detail', args=(pk,)) + '?success=3')
    return HttpResponseRedirect(reverse_lazy('catalog:book-detail', args=(pk,)))


#auto clear over_appointment
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import os
#开启定时工作
try:
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # 设置定时任务，选择方式为interval，时间间隔为10s
    # 另一种方式为每天固定时间执行任务，对应代码为：
    # @register_job(scheduler, 'cron', day_of_week='mon-fri', hour='9', minute='30', second='10',id='task_time')
    @register_job(scheduler,"interval", seconds=10)
    def my_job():
        bookinsts = BookInstance.objects.filter(status__exact='r')
        if bookinsts:
            for bookinst in bookinsts:
                if bookinst.is_overappointment:
                    bookinst.appointment = None
                    bookinst.appointment_time = None
                    bookinst.status = 'a'
                    bookinst.save()
    @register_job(scheduler, 'cron', day_of_week='mon-sun', hour='8', minute='30', second='10', id='delete_stale_data')  # 定时执行：这里定时为周一到周日每天早上8：30执行一次
    def time_task():
        os.system('py manage.py clearsessions')
    
    register_events(scheduler)
    scheduler.start()
except Exception as e:
    print(e)
    # 有错误就停止定时器
    scheduler.shutdown()

#setting appointment views
class AppointmentByUserListView(LoginRequiredMixin,generic.ListView):
    """
    Generic class-based view listing books on appointment to current user. 
    """
    model = BookInstance
    template_name = 'catalog/bookinstance_list_appointment_user.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(appointment=self.request.user).filter(status__exact='r').order_by('appointment_time')

class AppointmentByUserListView1(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on Appointment to current user. 
    """

    template_name = 'catalog/bookinstance_list_appointment_user.html'
    paginate_by = 5

    def get_queryset(self):
        if not self.kwargs['name']:
            self.bookinstance_list = BookInstance.objects.all()
        else:
            # print(self.kwargs['name'])
            self.bookinstance_list = BookInstance.objects.filter(
                book__title__icontains=self.kwargs['name']).filter(appointment=self.request.user).filter(status__exact='r').order_by('appointment_time')
            name = self.kwargs['name']
        return self.bookinstance_list

class AppointmentAllListView(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all books on appointment. Only visible to users with can_mark_returned permission.
    """
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_appointment_all.html'
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='r').order_by('appointment_time')


class AppointmentAllListView1(PermissionRequiredMixin, generic.ListView):
    """
    Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission.
    """
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_appointment_all.html'
    paginate_by = 5

    def get_queryset(self):
        if not self.kwargs['name']:
            self.bookinstance_list = BookInstance.objects.all()
        else:
            print(self.kwargs['name'])
            self.bookinstance_list = BookInstance.objects.filter(
                book__title__icontains=self.kwargs['name']).filter(status__exact='r').order_by('appointment_time')
            name = self.kwargs['name']
        return self.bookinstance_list

# setting history by user
class HistoryListView(LoginRequiredMixin, generic.ListView):
    model = History
    template_name = 'catalog/history_list.html'
    paginate_by = 5
    def get_queryset(self):
        if self.request.user.history_set.all():
            self.history_list = self.request.user.history_set.all()
        else:
            self.history_list= []
        return self.history_list

#delete history recoder
def deleteHistory(request):
    history = History.objects.filter(master=request.user)
    if request.method == "GET":
        return render(request,'catalog/history_confirm_delete.html',{history:history})
    elif request.method == "POST":
        request.user.history_set.clear()
        return redirect(reverse_lazy('catalog:my_history'),{'history_list':[]})

# bulk create bookinstance

@permission_required('catalog.can_mark_returned')
def BulkCreateBookinstance(request, pk):

    book = get_object_or_404(Book, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':
        form = BookinstanceForm1(request.POST, error_class=DivErrorList)
        
        nums = int(request.POST.get('nums'))
        book_inst_list = []       
        book_inst_list = [BookInstance(book=book,imprint=request.POST.get('imprint'),status=request.POST.get('status'),) for i in range(0, nums)]
        try:
            BookInstance.objects.bulk_create(book_inst_list)
            return HttpResponseRedirect(reverse('catalog:book-detail',args=[pk,]),{'errors':'1'})
        except Exception:
            return HttpResponseRedirect(reverse('catalog:book-detail',args=[pk,]),{'errors':'2'})

        # Create a form instance and populate it with data from the request (binding):

            # redirect to a new URL:
        

    # If this is a GET (or any other method) create the default form.
    else:
        form = BookinstanceForm1(
            initial={'status':'a','book':book, }, error_class=DivErrorList)

    return render(request, 'catalog/addbookinstance.html', {'form': form,})

# one user
from .models import Visitor1
from django.http import JsonResponse
def is_thatone(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]#所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')#这里获得代理ip
    if request.user.is_authenticated:
        key_from_cookie = request.session.session_key
        # print(request.session.get('sessionid'))   
        # print(hasattr(request.user, 'visitor1'))
        if hasattr(request.user, 'visitor1'):
            # session_ip = request.user.visitor1.ip
            # print(session_key_in_visitor_db)
            # print(session_key_in_visitor_db != key_from_cookie)
            # print(key_from_cookie)
            if request.user.visitor1.session_key != key_from_cookie:
                request.user.visitor1.session_key = key_from_cookie
                request.user.visitor1.save()
                return JsonResponse({'code':2})
            if request.session.get('oldip') != str(ip):               
                return JsonResponse({'code': 0})
            else:
                return JsonResponse({'code': 1})
    else:
        return JsonResponse({'code':1})

# statistical state统计
from .forms import Statistical
import json
def statistical(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    borrowers = HistoryByManager.objects.all()
    dic = {}
    list1 = []
    for borrower in borrowers:
        if not borrower.books in list1:
            list1.append(borrower.books)
    for list in list1:
        dic[list] = HistoryByManager.objects.filter(books=list).count()
    dic1 = {}
    list2 = []
    num_genre_book = 0
    books_num = 0
    for genre in genres:
        if not genre.name in list2:
            list2.append(genre.name)
    for name in list2:
        for book in books:
            genre_name = book.display_genre1()
            if re.search(name, genre_name) != None:
                num_genre_book+=1
        dic1[name] = num_genre_book
        books_num+=num_genre_book
        # print(num_genre_book)
        num_genre_book=0
       

    if request.method == 'GET':
        title1 = '所有时间段'
        title2 = '图书类别份额'

        form = Statistical(initial={'threeChoice':0,}, error_class=DivErrorList)
        return render(request, 'catalog/statistical.html', {'form': form, 'dic':json.dumps(dic),'dic1':json.dumps(dic1),'books_num':json.dumps(books_num),'date':datetime.date.today,'title1':title1,'title2':title2},)
            
                       