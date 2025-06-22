from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from backoffice.models import  Column, Chat, Help, Meeting, MeetingResult, Project, Supercolumn, Task


# Register your models here.

from backoffice.models import(Column)
from backoffice.models import(Chat)
from backoffice.models import(Help)
from backoffice.models import(Meeting)
from backoffice.models import(MeetingResult)
from backoffice.models import(Project)
from backoffice.models import(Supercolumn)
from backoffice.models import(Task)



admin.site.register(Column)
admin.site.register(Chat)
admin.site.register(Help)
admin.site.register(Meeting)
admin.site.register(MeetingResult)
admin.site.register(Project)
admin.site.register(Supercolumn)
admin.site.register(Task)









