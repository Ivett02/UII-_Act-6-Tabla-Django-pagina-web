from django.contrib import admin
from django.utils.html import format_html
from .models import Sucursal, Cliente, Empleado, Categoria, Producto, Venta


# ==========================
# ADMIN: Sucursal
# ==========================
class SucursalAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'ciudad', 'estado', 'thumbnail')
    readonly_fields = ('thumbnail',)
    search_fields = ('nombre', 'ciudad', 'estado')
    list_filter = ('estado', 'ciudad')

    def thumbnail(self, obj):
        if hasattr(obj, 'imagen') and obj.imagen:
            return format_html('<img src="{}" style="max-width:120px;"/>', obj.imagen.url)
        return '-'
    thumbnail.short_description = 'Imagen'


# ==========================
# ADMIN: Cliente
# ==========================
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'edad', 'telefono', 'email', 'id_sucursal')
    search_fields = ('nombre', 'apellido', 'telefono', 'email')
    list_filter = ('id_sucursal',)


# ==========================
# ADMIN: Empleado
# ==========================
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'apellido', 'edad', 'puesto', 'salario', 'id_sucursal')
    search_fields = ('nombre', 'apellido', 'puesto')
    list_filter = ('id_sucursal', 'puesto')


# ==========================
# ADMIN: Categoria
# ==========================
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'estado', 'material', 'fecha_creacion')
    list_filter = ('estado', 'material')
    search_fields = ('nombre', 'material')
    readonly_fields = ('fecha_creacion',)


# ==========================
# ADMIN: Producto
# ==========================
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'stock', 'precio', 'get_categoria')
    list_filter = ('id_categoria',)
    search_fields = ('nombre',)

    def get_categoria(self, obj):
        return obj.id_categoria.nombre if obj.id_categoria else '-'
    get_categoria.short_description = 'Categoría'


# ==========================
# ADMIN: Venta (ARREGLADO)
# ==========================
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'id_venta', 'fecha', 'cliente_nombre', 'empleado_nombre',
        'sucursal_nombre', 'metodo_pago', 'subtotal', 'total_display', 'estado'
    )
    list_filter = ('estado', 'metodo_pago', 'id_sucursal', 'id_empleado')
    search_fields = ('id_venta', 'id_cliente__nombre', 'id_empleado__nombre', 'id_sucursal__nombre')

    # usa total_display (método) como readonly en vez de 'total' directo
    readonly_fields = ('fecha', 'subtotal', 'impuesto', 'total_display')

    def cliente_nombre(self, obj):
        return f"{obj.id_cliente.nombre} {obj.id_cliente.apellido}" if obj.id_cliente else '-'
    cliente_nombre.short_description = 'Cliente'

    def empleado_nombre(self, obj):
        return f"{obj.id_empleado.nombre} {obj.id_empleado.apellido}" if obj.id_empleado else '-'
    empleado_nombre.short_description = 'Empleado'

    def sucursal_nombre(self, obj):
        return obj.id_sucursal.nombre if obj.id_sucursal else '-'
    sucursal_nombre.short_description = 'Sucursal'

    def total_display(self, obj):
        return obj.total if getattr(obj, 'total', None) is not None else '-'
    total_display.short_description = 'Total'
    total_display.admin_order_field = 'total'


# ==========================
# Registro en el panel (único registro por modelo)
# ==========================
admin.site.register(Sucursal, SucursalAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Venta, VentaAdmin)
