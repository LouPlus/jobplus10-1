from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError, IntegerField, TextAreaField
from wtforms.validators import Length, Email, EqualTo, DataRequired
from jobplus.models import db, User, CompanyDetail

class LoginForm(FlaskForm):
        email = StringField('邮箱', validators=[DataRequired(), Email()])
        password = PasswordField('密码', validators=[DataRequired(), Length(6, 24)])
        remember_me = BooleanField('记住我')
        submit = SubmitField('提交')

        def validate_email(self, field):
            if not User.query.filter_by(email=field.data).first():
                raise ValidationError('邮箱未注册')

        def validate_password(self, field):
            user = User.query.filter_by(email=self.email.data).first()
            if user and not user.check_password(field.data):
                raise ValidationError('密码错误')


class UserProfileForm(FlaskForm):
    username = StringField('姓名')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码（不填写保持不变）')
    phone = StringField('手机号')
    work_years = IntegerField('工作年限')
    resume = StringField('简历')
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phont = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('请输入有效的手机号')

    def updated_profile(self, user):
        user.username = self.username.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data
        user.phone = self.phone.data
        user.work_years = self.work_years.data
        user.resume = self.resumn.data
        db.session.add(user)
        db.session.commit()

class CompanyProfileForm(FlaskForm):
    name = StringField('企业名称')
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码（不填写保持不变）')
    slug = StringField('Slug', validators=[DataRequired(), Length(3, 24)])
    location = StringField('地址', validators=[Length(0, 64)])
    site = StringField('公司网站', validators=[Length(0, 64)])
    logo = StringField('Logo')
    description = StringField('一句话描述', validators=[Length(0, 100)])
    about = TextAreaField('公司详情', validators=[Length(0, 1024)])
    submit = SubmitField('提交')

    def validate_phone(self, field):
        phont = field.data
        if phone[:2] not in ('13', '15', '18') and len(phone) != 11:
            raise ValidationError('请输入有效的手机号')

    def updated_profile(self, user):
        user.username = self.username.data
        user.email = self.email.data
        if self.password.data:
            user.password = self.password.data

        if user.company_detail:
            company_detail = user.company_detail
        else:
            company_detail = CompanyDetail()
            company_detail.user_id = user.id

        self.populate_obj(company_detail)
        db.session.add(user)
        db.session.add(company_detail)
        db.session.commit()


