from django.db import models

# Create your models here.
class ReseñaSite(models.Model):
    email = models.EmailField()
    message = models.TextField()
    create_at= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Usuario: {self.email}'
    
    
    class Meta:
        verbose_name = 'reseña'
        verbose_name_plural = 'reseñas'