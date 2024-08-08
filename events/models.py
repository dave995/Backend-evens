from django.db import models
import qrcode 
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image

class Event(models.Model): 
    name = models.CharField(max_length=200)
    description = models.TextField()
    qr_code = models.ImageField(blank=True, upload_to='media/qrcodes/')
    date = models.DateField()
    
    def __str__(self):
        return str(self.name)
    
    def save(self, *args,  **kwargs):
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(str(self.id))  # Utiliser l'ID de l'événement comme données pour le code QR
            qr.make(fit=True)
            qrcode_img = qr.make_image(fill_color="black", back_color="white")
            fname = f'qr_code-{self.id}.png'  # Utiliser l'ID de l'événement comme nom de fichier
            buffer = BytesIO()
            qrcode_img.save(buffer, 'PNG')
            self.qr_code.save(fname, ContentFile(buffer.getvalue()), save=False)
        super().save(*args, **kwargs)
