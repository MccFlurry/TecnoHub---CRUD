import unittest
import threading
import time
import sys
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

# Agregar el directorio padre al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controllers.controlador_producto import (
    actualizar_stock, 
    StockError, 
    StockInsuficienteError, 
    ProductoNoEncontradoError
)
from bd import obtener_conexion

class TestConcurrenciaStock(unittest.TestCase):
    """Pruebas de concurrencia para el manejo de stock"""

    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todas las pruebas"""
        # Configurar productos de prueba
        cls.productos_test = [1, 2, 3]  # IDs de productos para pruebas
        cls.setup_productos()

    @classmethod
    def setup_productos(cls):
        """Configura los productos de prueba con stock inicial"""
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                for producto_id in cls.productos_test:
                    # Asegurar que el producto existe y tiene stock inicial
                    cursor.execute("""
                        UPDATE productos 
                        SET stock = 10
                        WHERE id = %s
                    """, (producto_id,))
            conexion.commit()
        finally:
            conexion.close()

    def setUp(self):
        """Preparación antes de cada prueba"""
        self.setup_productos()

    def test_compra_concurrente_mismo_producto(self):
        """Prueba compras concurrentes del mismo producto"""
        producto_id = self.productos_test[0]
        num_compradores = 5
        cantidad_por_compra = 2

        def intento_compra():
            try:
                return actualizar_stock(producto_id, cantidad_por_compra)
            except StockError:
                return False

        # Ejecutar compras concurrentes
        with ThreadPoolExecutor(max_workers=num_compradores) as executor:
            resultados = list(executor.map(lambda _: intento_compra(), range(num_compradores)))

        # Verificar resultados
        compras_exitosas = sum(1 for r in resultados if r)
        self.assertLessEqual(compras_exitosas * cantidad_por_compra, 10,
            "No se debería vender más del stock disponible")

        # Verificar stock final
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT stock FROM productos WHERE id = %s", (producto_id,))
                stock_final = cursor.fetchone()[0]
                self.assertGreaterEqual(stock_final, 0,
                    "El stock no debería ser negativo")
                self.assertEqual(stock_final, 10 - (compras_exitosas * cantidad_por_compra),
                    "El stock final no coincide con las compras realizadas")
        finally:
            conexion.close()

    def test_compra_concurrente_multiples_productos(self):
        """Prueba compras concurrentes de múltiples productos"""
        num_compradores = 15
        max_cantidad_por_compra = 3

        def compra_aleatoria():
            producto_id = random.choice(self.productos_test)
            cantidad = random.randint(1, max_cantidad_por_compra)
            try:
                exito = actualizar_stock(producto_id, cantidad)
                return producto_id, cantidad, exito
            except StockError:
                return producto_id, cantidad, False

        # Ejecutar compras concurrentes
        with ThreadPoolExecutor(max_workers=num_compradores) as executor:
            resultados = list(executor.map(lambda _: compra_aleatoria(), range(num_compradores)))

        # Analizar resultados por producto
        compras_por_producto = {}
        for producto_id, cantidad, exito in resultados:
            if exito:
                if producto_id not in compras_por_producto:
                    compras_por_producto[producto_id] = 0
                compras_por_producto[producto_id] += cantidad

        # Verificar stocks finales
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                for producto_id in self.productos_test:
                    cursor.execute("SELECT stock FROM productos WHERE id = %s", (producto_id,))
                    stock_final = cursor.fetchone()[0]
                    
                    self.assertGreaterEqual(stock_final, 0,
                        f"Stock negativo para producto {producto_id}")
                    
                    compras_totales = compras_por_producto.get(producto_id, 0)
                    self.assertEqual(stock_final, 10 - compras_totales,
                        f"Stock incorrecto para producto {producto_id}")
        finally:
            conexion.close()

    def test_compra_con_reintentos(self):
        """Prueba el mecanismo de reintento en compras concurrentes"""
        producto_id = self.productos_test[0]
        num_compradores = 8
        cantidad_por_compra = 2

        def compra_con_reintento():
            start_time = time.time()
            max_tiempo = 5  # Tiempo máximo de intentos en segundos
            
            while time.time() - start_time < max_tiempo:
                try:
                    resultado = actualizar_stock(producto_id, cantidad_por_compra)
                    return resultado
                except StockInsuficienteError:
                    return False
                except StockError:
                    time.sleep(0.1)  # Pequeña pausa antes de reintentar
            return False

        # Ejecutar compras concurrentes con reintentos
        with ThreadPoolExecutor(max_workers=num_compradores) as executor:
            resultados = list(executor.map(lambda _: compra_con_reintento(), range(num_compradores)))

        # Verificar resultados
        compras_exitosas = sum(1 for r in resultados if r)
        self.assertLessEqual(compras_exitosas * cantidad_por_compra, 10,
            "No se debería vender más del stock disponible")

    def test_compra_parcial(self):
        """Prueba compras parciales con diferentes cantidades"""
        producto_id = self.productos_test[0]
        patrones_compra = [3, 4, 5, 2, 1]  # Diferentes cantidades de compra

        def intento_compra(cantidad):
            try:
                return actualizar_stock(producto_id, cantidad)
            except StockError:
                return False

        # Ejecutar compras concurrentes con diferentes cantidades
        with ThreadPoolExecutor(max_workers=len(patrones_compra)) as executor:
            futuros = [executor.submit(intento_compra, cantidad) 
                      for cantidad in patrones_compra]
            resultados = [f.result() for f in as_completed(futuros)]

        # Verificar stock final
        conexion = obtener_conexion()
        try:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT stock FROM productos WHERE id = %s", (producto_id,))
                stock_final = cursor.fetchone()[0]
                self.assertGreaterEqual(stock_final, 0,
                    "El stock no debería ser negativo")
        finally:
            conexion.close()

    def test_validacion_parametros(self):
        """Prueba la validación de parámetros de entrada"""
        producto_id = self.productos_test[0]
        
        # Probar ID de producto inválido
        with self.assertRaises(ValueError):
            actualizar_stock(-1, 1)
        
        # Probar cantidad inválida
        with self.assertRaises(ValueError):
            actualizar_stock(producto_id, -1)
        
        # Probar producto inexistente
        with self.assertRaises(ProductoNoEncontradoError):
            actualizar_stock(9999, 1)
        
        # Probar stock insuficiente
        with self.assertRaises(StockInsuficienteError):
            actualizar_stock(producto_id, 11)  # Stock inicial es 10

if __name__ == '__main__':
    unittest.main()
