from django.forms import ModelForm
from .models import BookInstance, Author
from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # for checking renewal date range.


class RenewBookForm(forms.Form):
    """
    a form design class
    """

    renewal_date = forms.DateField(
        help_text="输入从现在到4周的日期（默认为3）。", widget=forms.TextInput(attrs={'type': 'date'}), label='设置归还日期')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('无效的日期 - 无法采用过去的时间段'))

        # Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('无效的日期 - 续借超过4周'))

        # Remember to always return the cleaned data.
        return data


class RenewBookModelForm(ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data

    class Meta:
        model = BookInstance
        fields = ['due_back', ]
        labels = {'due_back': _('设置归还日期'), }
        help_texts = {'due_back': _('输入从现在到4周的日期（默认为3周）。'), }


class AuthorModelForm(ModelForm):
    def clean_first_name(self):
        data = self.cleaned_data['first_name']

        if data == ' ':
            raise ValidationError(_('无效名字'))
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']

        if data == ' ':
            raise ValidationError(_('无效姓氏'))

        # Remember to always return the cleaned data.
        return data

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']
        return data

    def clean_date_of_death(self):
        data = self.cleaned_data['date_of_death']
        return data

    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
        help_texts = {'date_of_birth': _(
            '时间格式：2019/10/04'), 'date_of_death': _('时间格式：2019/10/04'), }


class RentOutForm(ModelForm):
    """
    a form design class
    """
    # status = forms.CharField(
    #     help_text="更改当前图书状态。", widget=forms.Select(), label='图书状态')
    # borrower = forms.CharField(
    #     help_text="请选择借书用户。", widget=forms.Select(), label='借书用户')

    # due_back = forms.DateField(
    #     help_text="输入从现在到4周的日期（默认为3）。", widget=forms.TextInput(attrs={'type': 'date'}), label='设置归还日期')

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        # if data == None:
        #     # return data
        #     raise ValidationError(_('没有值！'))

        # Check date is not in past.
        if data != None:
            if data < datetime.date.today():
                raise ValidationError(_('无效的日期 - 无法采用过去的时间段'))
            # Check date is in range librarian allowed to change (+4 weeks).
            if data > datetime.date.today() + datetime.timedelta(weeks=4):
                raise ValidationError(_('无效的日期 - 续借超过4周'))

        # Remember to always return the cleaned data.
        return data

    def clean_status(self):
        data = self.cleaned_data['status']
        if data == '':
            raise ValidationError(
                _('请选择合适图书状态'))
        return data

    def clean_borrower(self):
        data = self.cleaned_data['borrower']
        nums = BookInstance.objects.filter(borrower=data).count()
        # print(nums)
        if nums > 5 and data:
            raise ValidationError(_('超过了借书数目'))
        # if not data:
        #     raise ValidationError(_('一定要确认借书用户'))
        return data

    def clean_appointment(self):
        data = self.cleaned_data['appointment']
        nums = BookInstance.objects.filter(appointment=data).count()
        print(nums)
        if nums > 5 and data:
            raise ValidationError(_('超过了预约数目'))
        # if not data:
        #     raise ValidationError(_('一定要确认预约用户'))
        return data

    def clean_appointment_time(self):
        data = self.cleaned_data['appointment_time']
        return data

    class Meta:
        model = BookInstance
        fields = ['status', 'borrower', 'appointment',
                  'due_back', 'appointment_time']
        labels = {'status': _('图书状态'), 'borrower': _(
            '借书用户'), 'due_back': _('设置归还日期'), 'appointment': _('预约用户'), }
        help_texts = {'due_back': _('输入从现在到4周的日期（默认为3周）。'), }
        widgets = {
            'due_back': forms.TextInput(attrs={'type': 'date', },),
            'appointment_time': forms.HiddenInput()
        }


class BookinstanceForm1(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'imprint',
                  'status']
        labels = {'status': _('图书状态'), 'book': _('图书'), 'imprint': _('打印社信息')}


class Statistical(forms.Form):
    """
    a form design class by Statistical
    """
    CHO = ((0, 'ALL'), (1, '图书类别'), (2, '借阅图书'),
           )

    threeChoice = forms.ChoiceField(
        label=u'统计对象', choices=CHO, )

    def clean_threeChoice(self):
        data = self.cleaned_data['threeChoice']
        # Remember to always return the cleaned data.
        return data