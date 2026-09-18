# سامانه ثبت‌نام دانش‌آموزان ایران

سامانه Django برای پیش‌ثبت‌نام دانش‌آموزان، همراه با رابط فارسی راست‌به‌چپ، API و پنل مدیریت.

## اجرا در محیط توسعه

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

سپس سایت در `http://127.0.0.1:8000` و پنل مدیر در `http://127.0.0.1:8000/admin/` در دسترس است.

برای ساخت مدیر:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

## API

| عملیات | نشانی | توضیح |
| --- | --- | --- |
| ثبت درخواست | `POST /api/v1/registrations/` | داده‌های فرم را به صورت JSON می‌پذیرد و `tracking_code` برمی‌گرداند. |
| پیگیری درخواست | `GET /api/v1/registrations/{tracking_code}/?national_id={national_id}` | فقط با کد ملی منطبق وضعیت را برمی‌گرداند. |

اعتبارسنجی کد ملی، شماره همراه ایران، رضایت کاربر و تاریخ هجری شمسی در سرور انجام می‌شود. داده‌ها در SQLite (`db.sqlite3`) ذخیره می‌شوند؛ برای استقرار واقعی، SQLite را با PostgreSQL جایگزین کنید و `DJANGO_SECRET_KEY`، `DJANGO_DEBUG=0` و `DJANGO_ALLOWED_HOSTS` را تنظیم کنید.

## آزمون

```powershell
.\.venv\Scripts\python.exe manage.py test
```
