from django.contrib import admin
from .models import TypeToDoList, Task, Reminder, Tag, Event

admin.site.register(TypeToDoList)
admin.site.register(Task)
admin.site.register(Reminder)
admin.site.register(Tag)
admin.site.register(Event)