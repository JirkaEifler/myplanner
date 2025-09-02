"""
Management command to load demo data into the MyPlanner database.
Usage: python manage.py load_demo_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta, date
from planner.models import TypeToDoList, Task, Tag, Comment, Reminder, Event

User = get_user_model()


class Command(BaseCommand):
    help = 'Load demo data for MyPlanner application'

    def handle(self, *args, **options):
        self.stdout.write('Loading demo data...')
        
        # Create demo user
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'User'
            }
        )
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: demo (password: demo123)'))
        else:
            self.stdout.write(self.style.WARNING('Demo user already exists'))

        # Create lists
        lists_data = [
            {'name': 'Work Projects', 'owner': demo_user},
            {'name': 'Personal', 'owner': demo_user},
            {'name': 'Shopping', 'owner': demo_user},
            {'name': 'Learning', 'owner': demo_user},
        ]
        
        lists = {}
        for list_data in lists_data:
            list_obj, created = TypeToDoList.objects.get_or_create(**list_data)
            lists[list_data['name']] = list_obj
            if created:
                self.stdout.write(f'  Created list: {list_data["name"]}')

        # Create tags (names will be converted to lowercase by model's save method)
        tags_data = [
            {'name': 'urgent', 'owner': demo_user},
            {'name': 'important', 'owner': demo_user},
            {'name': 'review', 'owner': demo_user},
            {'name': 'in progress', 'owner': demo_user},
            {'name': 'waiting', 'owner': demo_user},
        ]
        
        tags = {}
        for tag_data in tags_data:
            tag_obj, created = Tag.objects.get_or_create(**tag_data)
            tags[tag_data['name']] = tag_obj
            if created:
                self.stdout.write(f'  Created tag: {tag_data["name"]}')

        # Create tasks with various states
        today = date.today()
        tasks_data = [
            # Work Projects
            {
                'title': 'Finish quarterly report',
                'description': 'Complete the Q4 financial report and send to management',
                'list': lists['Work Projects'],
                'owner': demo_user,
                'priority': 1,
                'due_date': today + timedelta(days=2),
                'is_completed': False,
                'tags': ['urgent', 'important'],
            },
            {
                'title': 'Team meeting preparation',
                'description': 'Prepare slides for Monday team meeting',
                'list': lists['Work Projects'],
                'owner': demo_user,
                'priority': 2,
                'due_date': today + timedelta(days=5),
                'is_completed': False,
                'tags': ['important'],
            },
            {
                'title': 'Code review for PR #234',
                'description': 'Review pull request for the new feature implementation',
                'list': lists['Work Projects'],
                'owner': demo_user,
                'priority': 2,
                'due_date': today + timedelta(days=1),
                'is_completed': True,
                'tags': ['review'],
            },
            
            # Personal
            {
                'title': 'Book dentist appointment',
                'description': 'Call Dr. Smith office for annual checkup',
                'list': lists['Personal'],
                'owner': demo_user,
                'priority': 3,
                'due_date': today + timedelta(days=7),
                'is_completed': False,
                'tags': [],
            },
            {
                'title': 'Gym workout',
                'description': 'Upper body workout - chest and arms',
                'list': lists['Personal'],
                'owner': demo_user,
                'priority': 3,
                'due_date': today,
                'is_completed': False,
                'tags': ['in progress'],
            },
            {
                'title': 'Pay electricity bill',
                'description': 'Monthly utility payment',
                'list': lists['Personal'],
                'owner': demo_user,
                'priority': 1,
                'due_date': today - timedelta(days=1),
                'is_completed': True,
                'tags': ['urgent'],
            },
            
            # Shopping
            {
                'title': 'Buy groceries',
                'description': 'Milk, bread, eggs, vegetables, fruits',
                'list': lists['Shopping'],
                'owner': demo_user,
                'priority': 2,
                'due_date': today,
                'is_completed': False,
                'tags': ['important'],
            },
            {
                'title': 'Birthday gift for Sarah',
                'description': 'Look for something special - maybe a book or jewelry',
                'list': lists['Shopping'],
                'owner': demo_user,
                'priority': 2,
                'due_date': today + timedelta(days=10),
                'is_completed': False,
                'tags': [],
            },
            
            # Learning
            {
                'title': 'Complete Django tutorial',
                'description': 'Finish the advanced Django REST framework tutorial',
                'list': lists['Learning'],
                'owner': demo_user,
                'priority': 3,
                'due_date': today + timedelta(days=14),
                'is_completed': False,
                'tags': ['in progress'],
            },
            {
                'title': 'Read "Clean Code"',
                'description': 'Chapter 5-7 on functions and error handling',
                'list': lists['Learning'],
                'owner': demo_user,
                'priority': 4,
                'due_date': today + timedelta(days=21),
                'is_completed': False,
                'tags': ['waiting'],
            },
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            tag_names = task_data.pop('tags', [])
            task_obj, created = Task.objects.get_or_create(
                title=task_data['title'],
                owner=task_data['owner'],
                defaults=task_data
            )
            
            if created:
                # Add tags
                for tag_name in tag_names:
                    if tag_name in tags:
                        task_obj.tags.add(tags[tag_name])
                created_tasks.append(task_obj)
                self.stdout.write(f'  Created task: {task_data["title"]}')

        # Add comments to some tasks
        if created_tasks:
            comment_task = created_tasks[0]  # First task
            Comment.objects.get_or_create(
                task=comment_task,
                author=demo_user,
                defaults={'body': 'Remember to include the marketing metrics in the report'}
            )
            Comment.objects.get_or_create(
                task=comment_task,
                author=demo_user,
                defaults={'body': 'Finance team needs this by EOD Thursday'}
            )

        # Add reminders to urgent tasks
        now = timezone.now()
        for task in Task.objects.filter(owner=demo_user, priority=1, is_completed=False):
            Reminder.objects.get_or_create(
                task=task,
                owner=demo_user,
                defaults={
                    'remind_at': now + timedelta(days=1),
                    'note': f'Don\'t forget: {task.title}'
                }
            )

        # Add an event to one task
        if created_tasks and len(created_tasks) > 1:
            event_task = created_tasks[1]  # Second task (team meeting)
            Event.objects.get_or_create(
                task=event_task,
                defaults={
                    'start_time': now + timedelta(days=5, hours=10),
                    'end_time': now + timedelta(days=5, hours=11)
                }
            )

        self.stdout.write(self.style.SUCCESS('\nDemo data loaded successfully!'))
        self.stdout.write('\nYou can now login with:')
        self.stdout.write('  Username: demo')
        self.stdout.write('  Password: demo123')
        self.stdout.write('\nOr use the admin account:')
        self.stdout.write('  Username: admin')
        self.stdout.write('  Password: admin123')