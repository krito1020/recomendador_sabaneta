from django.shortcuts import render, redirect
from .forms import ComercioForm
from .models import Comercio
from .recommender import RecomendadorEmpresas
from django.contrib import messages
import os
import openpyxl

# Ruta segura
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCEL_PATH = os.path.join(BASE_DIR, 'apps', 'recomendador', 'data', 'base_actualizada.xlsx')

# Variable global del recomendador
recomendador = None

# Función para recargar modelo
def cargar_recomendador():
    global recomendador
    if os.path.exists(EXCEL_PATH):
        try:
            recomendador = RecomendadorEmpresas(EXCEL_PATH)
            print("✅ Recomendador recargado correctamente.")
        except Exception as e:
            print(f"⚠️ Error cargando recomendador: {e}")
            recomendador = None

# Cargar al inicio
cargar_recomendador()

def index(request):
    recomendaciones = None

    if request.method == 'POST':
        consulta = request.POST.get('consulta', '').strip()
        if consulta and recomendador:
            print(f">>> Consulta del usuario: {consulta}")
            resultado = recomendador.recomendar(consulta)
            print(f">>> Resultados encontrados: {len(resultado)}")
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

            # Crear archivo si no existe
            nuevo_archivo = False
            if not os.path.exists(EXCEL_PATH):
                os.makedirs(os.path.dirname(EXCEL_PATH), exist_ok=True)
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.title = 'BBDD'
                ws.append([
                    'NIT', 'NOMBRE', 'SECTOR', 'SUBSECTOR', 'ARTICULOS',
                    'PAIS', 'DEPARTAMENTO', 'CIUDAD', 'DIRECCIÓN',
                    'CELULAR', 'TELÉFONO', 'FACEBOOK', 'INSTAGRAM'
                ])
                nuevo_archivo = True
            else:
                wb = openpyxl.load_workbook(EXCEL_PATH)
                ws = wb['BBDD'] if 'BBDD' in wb.sheetnames else wb.active

            # Añadir fila
            ws.append([
                '',  # NIT vacío
                comercio.nombre,
                comercio.sector,
                comercio.subsector,
                comercio.articulos.lower().strip(),
                'Colombia',
                'Antioquia',
                'Sabaneta',
                comercio.direccion,
                comercio.celular,
                comercio.telefono,
                comercio.link_facebook,
                comercio.link_instagram
            ])
            wb.save(EXCEL_PATH)

            # Recargar modelo actualizado
            cargar_recomendador()

            messages.success(request, '¡Comercio registrado exitosamente!')
            return redirect('registro')
        else:
            messages.error(request, 'Error en el formulario. Por favor revisa los campos.')
    else:
        form = ComercioForm()

    return render(request, 'recomendador/registro.html', {'form': form})

