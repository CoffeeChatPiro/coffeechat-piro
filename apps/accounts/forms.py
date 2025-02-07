from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, AuthenticationForm
from .models import User

# 회원가입 폼
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput,
    )
    cohort = forms.IntegerField(
        label='Cohort',
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'profile_image', 'cohort')  # 소개 필드 제외
        
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
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-input--img'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_image', 'cohort']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'cohort': forms.NumberInput(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_image'].required = False

# 로그인 폼
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages['invalid_login'] = '아이디/비밀번호를 다시 입력해주세요!'
        self.error_messages['inactive'] = '이 계정은 비활성화되었습니다.'