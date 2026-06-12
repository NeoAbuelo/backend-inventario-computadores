import io
from django.http import FileResponse
from rest_framework.views import APIView
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from django.utils import timezone

from ..models import Equipo


from seguridad.decorators import logguer_required

class ReporteEquiposView(APIView):

    @logguer_required
    def get(self, request):

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        doc.title = "Reporte Detallado de Registros"
        elements = []

        styles = getSampleStyleSheet()
        titulo = Paragraph("Reporte Detallado de Registros", styles['Title'])
        elements.append(titulo)
        elements.append(Spacer(1, 0.2*cm))
        header = Paragraph(f"Inventario a la fecha: {timezone.now().strftime('%d/%m/%Y')}", styles['h3'])
        elements.append(header)
        elements.append(Spacer(1, 0.2*cm))
        
        data = [['Estación', 'Dispositivo', 'Marca', 'Modelo', 'N° ID', 'Estado', 'Registro','Descripcion']]
        
        queryset = Equipo.objects.order_by('estacion', 'dispositivo__name', 'identificador', 'date_reg').all()
        for obj in queryset:
            data.append([
                obj.estacion,
                obj.dispositivo.name[:10],
                obj.marca[:10], 
                obj.modelo[:10], 
                obj.identificador[:10], 
                str(obj.is_active), 
                obj.date_reg.strftime('%d/%m/%Y'),
                obj.descripcion[:20]
            ])
            

        tabla = Table(data,colWidths=[1.8*cm, 2.5*cm, 2.4*cm, 2*cm, 1.8*cm, 1.4*cm, 2.1*cm, 5*cm])
        
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey), 
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), 
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'), 
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), 
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige), 
            ('GRID', (0, 0), (-1, -1), 1, colors.black) 
        ])
        tabla.setStyle(style)
        elements.append(tabla)

        doc.build(elements)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='reporte_tabla.pdf')