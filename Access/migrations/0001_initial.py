# Generated by Django 5.0.4 on 2024-11-22 21:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarritoCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
                ('costo_puntos', models.DecimalField(decimal_places=2, max_digits=10)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productos', to='Access.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='CarritoProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carrito', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Access.carritocompra')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Access.producto')),
            ],
        ),
        migrations.AddField(
            model_name='carritocompra',
            name='productos',
            field=models.ManyToManyField(through='Access.CarritoProducto', to='Access.producto'),
        ),
        migrations.CreateModel(
            name='SuscripcionEmpresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('monto_total_puntos', models.DecimalField(decimal_places=2, max_digits=10)),
                ('frecuencia', models.CharField(choices=[('S', 'Semanal'), ('M', 'Mensual'), ('A', 'Anual')], max_length=50)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suscripciones', to='Access.empresa')),
            ],
        ),
        migrations.AddField(
            model_name='carritocompra',
            name='suscripcion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carritos', to='Access.suscripcionempresa'),
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_Admin', models.BooleanField(default=False)),
                ('has_Empresa', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='empresa',
            name='propietario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='empresas', to='Access.usuarios'),
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_compra', models.DateTimeField(auto_now_add=True)),
                ('costo_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_validez', models.DateField()),
                ('productos', models.ManyToManyField(to='Access.producto')),
                ('suscripcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compras', to='Access.suscripcionempresa')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='compras', to='Access.usuarios')),
            ],
        ),
        migrations.AddField(
            model_name='carritocompra',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carritos', to='Access.usuarios'),
        ),
    ]
