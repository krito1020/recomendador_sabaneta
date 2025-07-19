from django.shortcuts import render, redirect
from .forms import ComercioForm
from .models import Comercio
from .recommender import RecomendadorEmpresas
from django.contrib import messages
import os
import openpyxl
import pandas as pd

# Ruta absoluta segura para producción y Railway
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE_DIR, 'apps', 'recomendador', 'data', 'base_actualizada.xlsx')

# Recomendador global
recomendador = None

# Función para cargar o recargar el modelo
def cargar_recomendador():
    global recomendador
    if os.path.exists(EXCEL_PATH):
        recomendador = RecomendadorEmpresas(EXCEL_PATH)

# Carga inicial
cargar_recomendador()


def index(request):
    recomendaciones = None

    if request.method == 'POST':
        consulta = request.POST.get('consulta', '')
        if consulta and recomendador:
            print(f">>> Consulta del usuario: {consulta}")  # 🟡 DEBUG
            resultado = recomendador.recomendar(consulta)
            print(f">>> Resultados encontrados: {len(resultado)}")  # 🟡 DEBUG
            recomendaciones = resultado.to_dict(orient='records')
            
            if not recomendaciones:
                messages.warning(request, 'No se encontraron resultados para tu búsqueda.')
        else:
            messages.error(request, 'No se pudo generar recomendaciones. Verifica la base o el texto ingresado.')

    return render(request, 'recomendador/index.html', {'recomendaciones': recomendaciones})


def registrar_comercio(request):
    if request.method == 'POST':
        form = ComercioForm(request.POST, request.FILES)
        if form.is_valid():
            comercio = form.save()

            # Agregar también al archivo Excel
            try:
                os.makedirs(os.path.dirname(EXCEL_PATH), exist_ok=True)

                nuevo_dato = {
                    'NOMBRE': comercio.nombre,
                    'SECTOR': comercio.sector,
                    'SUBSECTOR': comercio.subsector,
                    'ARTICULOS': comercio.articulos,
                    'DIRECCIÓN': comercio.direccion,
                    'CELULAR': comercio.celular,
                    'TELÉFONO': comercio.telefono,
                    'FACEBOOK': comercio.link_facebook,
                    'INSTAGRAM': comercio.link_instagram
                }

                # Cargar o crear archivo Excel
                if os.path.exists(EXCEL_PATH):
                    df = pd.read_excel(EXCEL_PATH, sheet_name='BBDD')
                    df = pd.concat([df, pd.DataFrame([nuevo_dato])], ignore_index=True)
                else:
                    df = pd.DataFrame([nuevo_dato])

                with pd.ExcelWriter(EXCEL_PATH, engine='openpyxl', mode='w') as writer:
                    df.to_excel(writer, sheet_name='BBDD', index=False)

            except Exception as e:
                print(f"⚠️ Error al guardar en Excel: {e}")
                messages.warning(request, 'Se guardó el comercio en la base de datos, pero hubo un error al actualizar el archivo Excel.')

            # Recargar modelo
            cargar_recomendador()

            messages.success(request, '¡Comercio registrado exitosamente!')
            return redirect('registro')
        else:
            messages.error(request, 'Error en el formulario. Por favor revisa los campos.')
    else:
        form = ComercioForm()

    return render(request, 'recomendador/registro.html', {'form': form})

