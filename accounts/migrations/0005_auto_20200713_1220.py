# Generated by Django 3.0.8 on 2020-07-13 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200711_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='counter_pass',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quiz',
            name='description',
            field=models.TextField(default='', verbose_name='Описание теста'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='accounts.Question', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='accounts.Quiz', verbose_name='Тест'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='Заголовок'),
        ),
    ]