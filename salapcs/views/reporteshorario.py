import io
from django.http import FileResponse
from rest_framework.views import APIView
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph,Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from django.utils import timezone
from datetime import timedelta

from ..models import SalaPC


from seguridad.decorators import logguer_required

class ReporteHorarioView(APIView):

    @logguer_required
    def get(self, request):

        hoy = timezone.localdate(timezone.now())
        lunes = hoy - timedelta(days=hoy.weekday())
        domingo = lunes + timedelta(days=6)


        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        doc.title = "Horarios de la Sala de Computación"
        elements = []

        styles = getSampleStyleSheet()
        titulo = Paragraph("Horarios de la Sala de Computación", styles['Title'])
        elements.append(titulo)
        elements.append(Spacer(1, 0.2*cm))
        header = Paragraph(f"Horarios de la Sala de Computación - Semana del {lunes.strftime('%d/%m/%Y')} al {domingo.strftime('%d/%m/%Y')}", styles['h3'])
        elements.append(header)
        elements.append(Spacer(1, 0.2*cm))
        
        data = [['Profesor', 'Curso', 'Asignatura', 'Fecha de uso', 'Hora de inicio']]
        
        queryset = SalaPC.objects.filter(date__range=[lunes, domingo]).order_by('profesor__nombre', 'curso', 'asignatura', 'date', 'hour').all()
        for obj in queryset:
            data.append([
                str(obj.profesor)[:20],
                obj.curso[:20],
                obj.asignatura[:20], 
                obj.date.strftime('%d/%m/%Y'), 
                obj.hour.strftime('%H:%M')
            ])
            

        tabla = Table(data,colWidths=[5*cm, 3*cm, 3*cm, 3*cm, 3*cm])
        
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
        return FileResponse(buffer, as_attachment=True, filename='reporte_horario.pdf')