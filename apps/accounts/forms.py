from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import CustomUser

# 회원가입 폼
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        help_text=''
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
        help_text=''
    )
    cohort = forms.IntegerField(
        label='Cohort',
        help_text='몇기인지 입력하세요.'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'profile_image', 'cohort')  # 소개 필드 제외
        help_texts = {
            'username': '',
            'email': '',
            'profile_image': '',
            'cohort': '',
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages['required'] = '이름을 입력해 주세요.'
        self.fields['password2'].error_messages['required'] = '비밀번호를 입력해 주세요.'
        self.fields['password1'].error_messages['required'] = '비밀번호를 입력해 주세요.'
        self.fields['cohort'].error_messages['required'] = '기수를 입력해 주세요.'

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.cohort = self.cleaned_data.get("cohort")  # cohort 필드를 저장
        if commit:
            user.save()
        return user

# 프로필 수정 폼
class CustomUserChangeForm(UserChangeForm):
    delete_profile_image = forms.BooleanField(required=False, label="프로필 이미지 삭제")
    password = None

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_image', 'cohort', 'intro']
        help_texts = {
            'username': '사용자 이름을 입력하세요.',
            'email': '유효한 이메일 주소를 입력하세요.',
            'profile_image': '프로필 이미지를 선택하세요.',
            'cohort': '몇기인지 입력하세요.',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-input--img'}),
            'cohort': forms.NumberInput(attrs={'class': 'form-input'}),
            'intro': forms.Textarea(attrs={'class': 'form-textarea', 'placeholder': '소개'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)

        # 이미지 삭제 처리
        if self.cleaned_data.get('delete_profile_image'):
            user.profile_image.delete(save=False)  # 이미지 파일 삭제
            user.profile_image = None  # 필드를 None으로 설정
            
        if commit:
            user.save()
        return user

# 로그인 폼
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = '아이디/비밀번호를 다시 입력해주세요!'
        self.error_messages['inactive'] = '이 계정은 비활성화되었습니다.'