import io
from django.http import FileResponse
from rest_framework.views import APIView
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.utils import timezone
from datetime import timedelta

from ..models import SalaPC

# Paleta alineada con el front (Tailwind sky / gray)
SKY_900 = colors.HexColor("#0c4a6e")
SKY_800 = colors.HexColor("#075985")
SKY_700 = colors.HexColor("#0369a1")
SKY_50 = colors.HexColor("#f0f9ff")
GRAY_200 = colors.HexColor("#e5e7eb")
GRAY_600 = colors.HexColor("#4b5563")
GRAY_800 = colors.HexColor("#1f2937")


class ReporteHorarioView(APIView):

    def get(self, request):

        hoy = timezone.localdate(timezone.now())
        lunes = hoy - timedelta(days=hoy.weekday())
        domingo = lunes + timedelta(days=6)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        doc.title = "Horarios de la Sala de Computación"
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "TituloHorario", parent=styles["Title"],
            textColor=SKY_900, fontName="Helvetica-Bold",
        )
        subtitle_style = ParagraphStyle(
            "SubtituloHorario", parent=styles["Normal"],
            textColor=GRAY_600, fontSize=11, alignment=TA_CENTER, spaceBefore=2,
        )

        elements.append(Paragraph("Horarios de la Sala de Computación", title_style))
        elements.append(Spacer(1, 0.15 * cm))
        elements.append(Paragraph(
            f"Semana del {lunes.strftime('%d/%m/%Y')} al {domingo.strftime('%d/%m/%Y')}",
            subtitle_style,
        ))
        elements.append(Spacer(1, 0.5 * cm))

        data = [['Profesor', 'Curso', 'Asignatura', 'Fecha de uso', 'Hora de inicio']]

        queryset = SalaPC.objects.filter(date__range=[lunes, domingo]).order_by(
            'profesor__nombre', 'curso', 'asignatura', '-date', '-hour'
        ).all()
        for obj in queryset:
            data.append([
                str(obj.profesor)[:20],
                (obj.curso or "")[:20],
                (obj.asignatura or "")[:20],
                obj.date.strftime('%d/%m/%Y'),
                obj.hour.strftime('%H:%M'),
            ])

        tabla = Table(data, colWidths=[5 * cm, 3 * cm, 3 * cm, 3 * cm, 3 * cm])

        style = TableStyle([
            # Cabecera
            ('BACKGROUND', (0, 0), (-1, 0), SKY_800),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('LINEBELOW', (0, 0), (-1, 0), 1, SKY_900),
            # Cuerpo
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TEXTCOLOR', (0, 1), (-1, -1), GRAY_800),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, SKY_50]),
            # Hora destacada en color de marca
            ('TEXTCOLOR', (4, 1), (4, -1), SKY_700),
            ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
            # General
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, GRAY_200),
        ])

        tabla.setStyle(style)
        elements.append(tabla)

        doc.build(elements)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='reporte_horario.pdf')
