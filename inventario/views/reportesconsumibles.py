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

from ..models import Consumible

# Paleta alineada con el front (Tailwind sky / gray / red)
SKY_900 = colors.HexColor("#0c4a6e")
SKY_800 = colors.HexColor("#075985")
SKY_50 = colors.HexColor("#f0f9ff")
GRAY_200 = colors.HexColor("#e5e7eb")
GRAY_600 = colors.HexColor("#4b5563")
GRAY_800 = colors.HexColor("#1f2937")
RED_600 = colors.HexColor("#dc2626")

# Umbral de stock bajo (igual que el front: cantidad < 4 se resalta)
STOCK_BAJO = 4


class ReporteConsumiblesView(APIView):

    def get(self, request):

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        doc.title = "Reporte de Consumibles"
        elements = []

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "TituloConsumibles", parent=styles["Title"],
            textColor=SKY_900, fontName="Helvetica-Bold",
        )
        subtitle_style = ParagraphStyle(
            "SubtituloConsumibles", parent=styles["Normal"],
            textColor=GRAY_600, fontSize=11, alignment=TA_CENTER, spaceBefore=2,
        )

        elements.append(Paragraph("Reporte de Consumibles", title_style))
        elements.append(Spacer(1, 0.15 * cm))
        elements.append(Paragraph(
            f"Inventario a la fecha: {timezone.now().strftime('%d/%m/%Y')}",
            subtitle_style,
        ))
        elements.append(Spacer(1, 0.5 * cm))

        data = [['Consumible', 'Cantidad', 'Descripción']]

        cantidad_rows = []
        queryset = Consumible.objects.order_by('name').all()
        for index, obj in enumerate(queryset, start=1):
            data.append([
                (obj.name or "")[:35],
                obj.cantidad,
                (obj.descripcion or "")[:50],
            ])
            cantidad_rows.append((index, obj.cantidad))

        tabla = Table(data, colWidths=[6 * cm, 3 * cm, 8 * cm])

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
            # General
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
            ('GRID', (0, 0), (-1, -1), 0.5, GRAY_200),
        ])

        # Resalta en rojo la cantidad cuando el stock está bajo (igual que el front)
        for row_index, cantidad in cantidad_rows:
            if cantidad < STOCK_BAJO:
                style.add('TEXTCOLOR', (1, row_index), (1, row_index), RED_600)
                style.add('FONTNAME', (1, row_index), (1, row_index), 'Helvetica-Bold')

        tabla.setStyle(style)
        elements.append(tabla)

        doc.build(elements)

        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='reporte_consumibles.pdf')
