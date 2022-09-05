# Generated by Django 4.1 on 2022-08-30 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("researchers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ResearchGroup",
            fields=[
                (
                    "cod_minciencias",
                    models.CharField(
                        max_length=32,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Minciencias code",
                    ),
                ),
                (
                    "cod_hermes",
                    models.CharField(max_length=32, verbose_name="Hermes code"),
                ),
                ("name", models.CharField(max_length=64, verbose_name="Name")),
                (
                    "founded",
                    models.DateField(
                        default="django.utils.timezone.now", verbose_name="Founded"
                    ),
                ),
                (
                    "faculty",
                    models.CharField(
                        choices=[
                            ("faculty_0001", "Facultad de administración"),
                            (
                                "faculty_0002",
                                "Facultad de ciencias exactas y naturales",
                            ),
                            ("faculty_0003", "Facultad de ingeniería y arquitectura"),
                            (
                                "faculty_0004",
                                "Instituto de estudios ambientales - idea - manizales",
                            ),
                        ],
                        max_length=12,
                        verbose_name="Faculty",
                    ),
                ),
                (
                    "departament",
                    models.CharField(
                        choices=[
                            ("departament_0001", "Departamento de administración"),
                            ("departament_0002", "Departamento de ciencias humanas"),
                            ("departament_0003", "Departamento de física y química"),
                            (
                                "departament_0004",
                                "Departamento de informática y computación",
                            ),
                            ("departament_0005", "Departamento de ingeniería civil"),
                            (
                                "departament_0006",
                                "Departamento de ingeniería eléctrica, electrónica y computación",
                            ),
                            (
                                "departament_0007",
                                "Departamento de ingeniería industrial",
                            ),
                            ("departament_0008", "Departamento de ingeniería química"),
                            ("departament_0009", "Departamento de matemáticas"),
                            ("departament_0010", "Escuela de arquitectura y urbanismo"),
                            (
                                "departament_0011",
                                "Instituto de estudios ambientales - idea - manizales",
                            ),
                        ],
                        max_length=16,
                        verbose_name="Departament",
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("groups_category_0001", "A"),
                            ("groups_category_0002", "A1"),
                            ("groups_category_0003", "B"),
                            ("groups_category_0004", "C"),
                            ("groups_category_0005", "No reconcido"),
                        ],
                        max_length=20,
                        verbose_name="Category",
                    ),
                ),
                (
                    "sub_ocde",
                    models.CharField(
                        choices=[("sub_ocde_0001", "SUB_OCDE")],
                        max_length=13,
                        verbose_name="SUB_OCDE",
                    ),
                ),
                (
                    "ocde",
                    models.CharField(
                        choices=[
                            ("ocde_0001", "Ciencias agrícolas"),
                            ("ocde_0002", "Ciencias médicas y de la salud"),
                            ("ocde_0003", "Ciencias naturales"),
                            ("ocde_0004", "Ciencias sociales"),
                            ("ocde_0005", "Humanidades"),
                            ("ocde_0006", "Ingeniería y tecnología"),
                        ],
                        max_length=9,
                        verbose_name="OCDE",
                    ),
                ),
                (
                    "knowledge_area",
                    models.CharField(
                        choices=[
                            ("knowledge_0001", "Ambiente y biodiversidad"),
                            ("knowledge_0002", "Arte y culturas"),
                            ("knowledge_0003", "Biotecnología"),
                            (
                                "knowledge_0004",
                                "Ciencia y tecnología de minerales y materiales",
                            ),
                            ("knowledge_0005", "Ciencias agrarias y desarrollo rural"),
                            (
                                "knowledge_0006",
                                "Construcción de ciudadanía e inclusión social",
                            ),
                            (
                                "knowledge_0007",
                                "Desarrollo organizacional, económico e industrial",
                            ),
                            ("knowledge_0008", "Energía"),
                            (
                                "knowledge_0009",
                                "Estados, sistemas políticos y jurídicos",
                            ),
                            ("knowledge_0010", "Hábitat, ciudad y territorio"),
                            ("knowledge_0011", "Salud y vida"),
                            (
                                "knowledge_0012",
                                "Tecnologías de la información y las comunicaciones (TIC)",
                            ),
                        ],
                        max_length=14,
                        verbose_name="knowledge",
                    ),
                ),
                (
                    "leader",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="researchers.professor",
                    ),
                ),
                (
                    "researchers",
                    models.ManyToManyField(
                        related_name="researchers", to="researchers.researcher"
                    ),
                ),
            ],
            options={
                "verbose_name": "Research group",
            },
        ),
    ]