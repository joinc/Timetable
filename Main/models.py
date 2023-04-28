from django.db import models

######################################################################################################################


class Building(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=124,
        default='',
    )
    address = models.CharField(
        verbose_name='Адрес здания',
        max_length=512,
        default='',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания записи о здании',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = 'title',
        verbose_name = 'Здание'
        verbose_name_plural = 'Здания'
        managed = True


######################################################################################################################


class Classroom(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=16,
        default='',
    )
    building = models.ForeignKey(
        Building,
        verbose_name='Здание',
        null=True,
        related_name='ClassroomBuilding',
        on_delete=models.SET_NULL,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания записи об аудитории',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = 'title',
        verbose_name = 'Аудитория'
        verbose_name_plural = 'Аудитории'
        managed = True


######################################################################################################################


class Faculty(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=64,
        default='',
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания записи о направлении обучения',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = 'title',
        verbose_name = 'Направление обучения'
        verbose_name_plural = 'Направления обучения'
        managed = True


######################################################################################################################


class Group(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=64,
        default='',
    )
    faculty = models.ForeignKey(
        Faculty,
        verbose_name='Направление обучения',
        null=True,
        related_name='GroupFaculty',
        on_delete=models.SET_NULL,
    )
    is_active = models.BooleanField(
        verbose_name='Состояние группы: активна или нет',
        default=True,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания записи о группе',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = 'title',
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        managed = True


######################################################################################################################


class Subject(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=64,
        default='',
    )
    is_active = models.BooleanField(
        verbose_name='Состояние предмета: активен или нет',
        default=True,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания записи о предмете',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = 'title',
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        managed = True


######################################################################################################################


class Teacher(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    family = models.CharField(
        verbose_name='Фамилия',
        max_length=64,
        default='',
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=64,
        default='',
    )
    second_name = models.CharField(
        verbose_name='Отчество',
        max_length=64,
        default='',
    )
    position = models.CharField(
        verbose_name='Должность',
        max_length=128,
        default='',
    )
    is_active = models.BooleanField(
        verbose_name='Состояние преподавателя: работает или нет',
        default=True,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания записи о преподавателе',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f'{self.family} {self.first_name} {self.second_name}'

    class Meta:
        ordering = 'family',
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        managed = True


######################################################################################################################


class Dates(models.Model):
    date = models.DateField(
        verbose_name='Дата',
        null=True,
        blank=True,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания записи о дате',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f'{self.date}'

    class Meta:
        ordering = 'date',
        verbose_name = 'Дата'
        verbose_name_plural = 'Даты'
        managed = True


######################################################################################################################


class Lesson(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    subject = models.ForeignKey(
        Subject,
        verbose_name='Предмет',
        null=True,
        related_name='LessonSubject',
        on_delete=models.SET_NULL,
    )
    date = models.ForeignKey(
        Dates,
        verbose_name='Дата занятия',
        null=True,
        related_name='LessonDate',
        on_delete=models.SET_NULL,
    )
    start_time = models.TimeField(
        verbose_name='Время начала',
        null=True,
        blank=True,
    )
    end_time = models.TimeField(
        verbose_name='Время окончания',
        null=True,
        blank=True,
    )
    create_date = models.DateTimeField(
        verbose_name='Дата создания записи о занятии',
        auto_now_add=True,
        null=True,
    )

    def __str__(self):
        return f'{self.subject} {self.date}'

    class Meta:
        ordering = 'date', 'subject',
        verbose_name = 'Занятие'
        verbose_name_plural = 'Занятия'
        managed = True


######################################################################################################################


# class LessonTeacher(models.Model):
#     lesson = models.ForeignKey(
#         Lesson,
#         verbose_name='Предмет ',
#         null=True,
#         related_name='LessonSubject',
#         on_delete=models.SET_NULL,
#     )


######################################################################################################################
# class LessonGroup

######################################################################################################################

# class SubjectTeacher

######################################################################################################################
