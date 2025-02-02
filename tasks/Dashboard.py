import os
import subprocess
from typing import Optional, List, Dict
import logging
from datetime import datetime

class DashboardPOO:
    """
    Dashboard para gestionar proyectos y ejercicios de Programación Orientada a Objetos.
    Permite navegar, visualizar y ejecutar scripts Python organizados en unidades y temas.
    """

    def __init__(self):
        self.ruta_base = os.path.dirname(__file__)
        self.unidades = {
            '1': 'Unidad 1 - Fundamentos POO',
            '2': 'Unidad 2 - Herencia y Polimorfismo',
            '3': 'Unidad 3 - Patrones de Diseño',
            '4': 'Unidad 4 - Proyectos Prácticos'
        }
        # Configuración del logging
        self.configurar_logging()

    def configurar_logging(self) -> None:
        """Configura el sistema de logging para registrar operaciones."""
        log_dir = os.path.join(self.ruta_base, 'logs')
        os.makedirs(log_dir, exist_ok=True)

        logging.basicConfig(
            filename=os.path.join(log_dir, f'dashboard_{datetime.now().strftime("%Y%m%d")}.log'),
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def mostrar_codigo(self, ruta_script: str) -> Optional[str]:
        """
        Muestra el contenido de un script Python y lo retorna como string.

        Args:
            ruta_script (str): Ruta al archivo Python a mostrar

        Returns:
            Optional[str]: Contenido del archivo o None si hay error
        """
        ruta_script_absoluta = os.path.abspath(ruta_script)
        try:
            with open(ruta_script_absoluta, 'r', encoding='utf-8') as archivo:
                codigo = archivo.read()
                print("\n" + "="*50)
                print(f"Código de {os.path.basename(ruta_script)}:")
                print("="*50 + "\n")
                print(codigo)
                logging.info(f"Archivo visualizado: {ruta_script}")
                return codigo
        except Exception as e:
            logging.error(f"Error al leer archivo {ruta_script}: {str(e)}")
            print(f"\n⚠️ Error: {str(e)}")
            return None

    def ejecutar_codigo(self, ruta_script: str) -> None:
        """
        Ejecuta un script Python en una nueva ventana.

        Args:
            ruta_script (str): Ruta al archivo Python a ejecutar
        """
        try:
            if os.name == 'nt':  # Windows
                subprocess.Popen(['cmd', '/k', 'python', ruta_script])
            else:  # Unix-based
                subprocess.Popen(['xterm', '-hold', '-e', 'python3', ruta_script])
            logging.info(f"Script ejecutado: {ruta_script}")
        except Exception as e:
            logging.error(f"Error al ejecutar {ruta_script}: {str(e)}")
            print(f"\n⚠️ Error al ejecutar: {str(e)}")

    def obtener_subcarpetas(self, ruta: str) -> List[str]:
        """
        Obtiene la lista de subcarpetas en una ruta dada.

        Args:
            ruta (str): Ruta a explorar

        Returns:
            List[str]: Lista de nombres de subcarpetas
        """
        return [f.name for f in os.scandir(ruta) if f.is_dir()]

    def obtener_scripts(self, ruta: str) -> List[str]:
        """
        Obtiene la lista de scripts Python en una ruta dada.

        Args:
            ruta (str): Ruta a explorar

        Returns:
            List[str]: Lista de nombres de scripts Python
        """
        return [f.name for f in os.scandir(ruta) if f.is_file() and f.name.endswith('.py')]

    def mostrar_menu_principal(self) -> None:
        """Muestra y gestiona el menú principal del dashboard."""
        while True:
            print("\n🎯 Dashboard POO - Menú Principal")
            print("="*40)
            for key, valor in self.unidades.items():
                print(f"{key} - {valor}")
            print("0 - Salir")
            print("="*40)

            eleccion = input("\nSeleccione una opción: ").strip()

            if eleccion == '0':
                print("\n👋 ¡Hasta pronto!")
                logging.info("Sesión finalizada")
                break
            elif eleccion in self.unidades:
                self.mostrar_submenu(os.path.join(self.ruta_base, self.unidades[eleccion]))
            else:
                print("\n⚠️ Opción no válida")
                logging.warning(f"Opción inválida seleccionada: {eleccion}")

    def mostrar_submenu(self, ruta_unidad: str) -> None:
        """
        Muestra y gestiona el submenú de temas para una unidad.

        Args:
            ruta_unidad (str): Ruta a la unidad seleccionada
        """
        while True:
            subcarpetas = self.obtener_subcarpetas(ruta_unidad)

            print("\n📚 Temas Disponibles")
            print("="*40)
            for i, carpeta in enumerate(subcarpetas, 1):
                print(f"{i} - {carpeta}")
            print("0 - Volver al menú principal")
            print("="*40)

            eleccion = input("\nSeleccione un tema: ").strip()

            if eleccion == '0':
                break
            try:
                idx = int(eleccion) - 1
                if 0 <= idx < len(subcarpetas):
                    self.mostrar_menu_scripts(os.path.join(ruta_unidad, subcarpetas[idx]))
                else:
                    print("\n⚠️ Tema no válido")
            except ValueError:
                print("\n⚠️ Por favor, ingrese un número válido")

    def mostrar_menu_scripts(self, ruta_tema: str) -> None:
        """
        Muestra y gestiona el menú de scripts disponibles para un tema.

        Args:
            ruta_tema (str): Ruta al tema seleccionado
        """
        while True:
            scripts = self.obtener_scripts(ruta_tema)

            print("\n📝 Scripts Disponibles")
            print("="*40)
            for i, script in enumerate(scripts, 1):
                print(f"{i} - {script}")
            print("0 - Volver al menú de temas")
            print("="*40)

            eleccion = input("\nSeleccione un script: ").strip()

            if eleccion == '0':
                break
            try:
                idx = int(eleccion) - 1
                if 0 <= idx < len(scripts):
                    ruta_script = os.path.join(ruta_tema, scripts[idx])
                    if self.mostrar_codigo(ruta_script):
                        if input("\n¿Desea ejecutar el script? (S/N): ").upper() == 'S':
                            self.ejecutar_codigo(ruta_script)
                    input("\nPresione Enter para continuar...")
                else:
                    print("\n⚠️ Script no válido")
            except ValueError:
                print("\n⚠️ Por favor, ingrese un número válido")

if __name__ == "__main__":
    dashboard = DashboardPOO()
    dashboard.mostrar_menu_principal()