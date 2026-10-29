import os
import re
import tkinter as tk
from pathlib import Path
from tkinter import colorchooser, filedialog, messagebox
from urllib.parse import urlparse
import sys

import qrcode
from PIL import Image, ImageTk

import sys

if getattr(sys, "frozen", False):
    CARPETA_CODIGOS = Path(sys.executable).resolve().parent / "codigos"
else:
    CARPETA_CODIGOS = Path(__file__).resolve().parent / "codigos"


CARPETA_CODIGOS = Path(__file__).resolve().parent / "codigos"


def nombre_archivo_seguro(nombre):
    """Limpia el nombre para usarlo como archivo PNG."""
    nombre = re.sub(r'[<>:"/\\|?*]', "_", nombre).strip(" .")
    return nombre or "mi_codigo_qr"


def ruta_disponible(nombre):
    """Devuelve una ruta que no sobrescribe un archivo existente."""
    ruta = CARPETA_CODIGOS / f"{nombre}.png"
    contador = 2

    while ruta.exists():
        ruta = CARPETA_CODIGOS / f"{nombre}_{contador}.png"
        contador += 1

    return ruta


class GeneradorQR:
    def __init__(self):
        CARPETA_CODIGOS.mkdir(parents=True, exist_ok=True)

        self.color_qr = "#000000"
        self.color_fondo = "#FFFFFF"
        self.ruta_logo = None

        self.ventana = tk.Tk()
        self.ventana.title("Generador de códigos QR")
        self.ventana.geometry("900x560")
        self.ventana.minsize(820, 520)
        self.ventana.configure(bg="#f2f4f7")

        self._crear_interfaz()

    def _crear_interfaz(self):
        """Construye los elementos visuales de la aplicación."""
        titulo = tk.Label(
            self.ventana,
            text="Generador de códigos QR",
            font=("Segoe UI", 18, "bold"),
            bg="#f2f4f7",
            fg="#203047",
        )
        titulo.pack(pady=(18, 4))

        subtitulo = tk.Label(
            self.ventana,
            text="Introduce una dirección y personaliza tu código QR",
            font=("Segoe UI", 10),
            bg="#f2f4f7",
            fg="#586579",
        )
        subtitulo.pack(pady=(0, 14))

        contenido = tk.Frame(self.ventana, bg="#f2f4f7")
        contenido.pack(fill="both", expand=True, padx=24, pady=(0, 20))
        contenido.columnconfigure(0, weight=1, minsize=330)
        contenido.columnconfigure(1, weight=1, minsize=400)
        contenido.rowconfigure(0, weight=1)

        panel_izquierdo = tk.Frame(contenido, bg="#f2f4f7")
        panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(0, 16))

        panel_derecho = tk.Frame(contenido, bg="#f2f4f7")
        panel_derecho.grid(row=0, column=1, sticky="nsew")

        panel_url = tk.LabelFrame(
            panel_izquierdo,
            text="Contenido del código",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=10,
        )
        panel_url.pack(fill="x", pady=(0, 12))

        etiqueta_url = tk.Label(
            panel_url,
            text="Dirección del sitio web:",
            font=("Segoe UI", 10, "bold"),
            fg="#203047",
        )
        etiqueta_url.pack(anchor="w")

        self.entrada_url = tk.Entry(
            panel_url,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
        )
        self.entrada_url.pack(fill="x", pady=(6, 10), ipady=6)
        self.entrada_url.insert(0, "https://www.youtube.com")

        boton_generar = tk.Button(
            panel_url,
            text="Generar código QR",
            command=self.generar_qr,
            font=("Segoe UI", 11, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=9,
        )
        boton_generar.pack(anchor="w")

        self._crear_panel_personalizacion(panel_izquierdo)

        panel_vista = tk.LabelFrame(
            panel_derecho,
            text="Vista previa",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=12,
        )
        panel_vista.pack(fill="both", expand=True)

        contenedor_qr = tk.Frame(
            panel_vista,
            width=370,
            height=370,
            bg="white",
            relief="solid",
            bd=1,
        )
        contenedor_qr.pack(expand=True)
        contenedor_qr.pack_propagate(False)

        self.etiqueta_qr = tk.Label(
            contenedor_qr,
            text="Tu código QR aparecerá aquí",
            font=("Segoe UI", 10),
            bg="white",
            fg="#7b8794",
        )
        self.etiqueta_qr.pack(expand=True)

        self.etiqueta_estado = tk.Label(
            panel_derecho,
            text=f"Los archivos se guardarán en:\n{CARPETA_CODIGOS}",
            font=("Segoe UI", 9),
            bg="#f2f4f7",
            fg="#586579",
            wraplength=440,
            justify="left",
            anchor="w",
        )
        self.etiqueta_estado.pack(fill="x", pady=(8, 4))

        boton_carpeta = tk.Button(
            panel_derecho,
            text="Abrir carpeta de códigos",
            command=self.abrir_carpeta,
            font=("Segoe UI", 10),
            bg="#e0e7ef",
            fg="#203047",
            activebackground="#cbd5e1",
            relief="flat",
            cursor="hand2",
            padx=12,
            pady=7,
        )
        boton_carpeta.pack(anchor="e")

        self.entrada_url.bind("<Return>", self.generar_qr)
        self.entrada_url.focus_set()

    def _crear_panel_personalizacion(self, contenedor):
        """Agrupa los controles de color, logotipo y nombre del archivo."""
        panel = tk.LabelFrame(
            contenedor,
            text="Personalizar código QR",
            font=("Segoe UI", 10, "bold"),
            padx=10,
            pady=10,
        )
        #suputamadre20
        panel.pack(fill="x")

        tk.Label(panel, text="Color del QR:").grid(
            row=0, column=0, sticky="w", pady=4
        )

        self.boton_color_qr = tk.Button(
            panel,
            text="Elegir",
            bg=self.color_qr,
            command=self.elegir_color_qr,
        )
        self.boton_color_qr.grid(row=0, column=1, sticky="e", padx=(8, 0), pady=4)

        tk.Label(panel, text="Color de fondo:").grid(
            row=1, column=0, sticky="w", pady=4
        )

        self.boton_color_fondo = tk.Button(
            panel,
            text="Elegir",
            bg=self.color_fondo,
            command=self.elegir_color_fondo,
        )
        self.boton_color_fondo.grid(
            row=1, column=1, sticky="e", padx=(8, 0), pady=4
        )

        tk.Button(
            panel,
            text="Seleccionar logotipo",
            command=self.elegir_logo,
        ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 4))

        self.etiqueta_logo = tk.Label(panel, text="Sin logotipo", anchor="w")
        self.etiqueta_logo.grid(row=3, column=0, columnspan=2, sticky="w", pady=4)

        tk.Label(
            panel,
            text="Nombre del archivo (sin extensión):",
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(12, 2))

        self.entrada_nombre = tk.Entry(panel)
        self.entrada_nombre.grid(row=5, column=0, columnspan=2, sticky="ew")
        self.entrada_nombre.insert(0, "mi_codigo_qr")
        panel.columnconfigure(0, weight=1)
        panel.columnconfigure(1, weight=0)

    def generar_qr(self, _event=None):
        url = self.entrada_url.get().strip()

        if not url:
            messagebox.showwarning("Falta la URL", "Escribe la dirección del sitio web.")
            return

        if not urlparse(url).scheme:
            url = "https://" + url

        parsed = urlparse(url)
        if (
            parsed.scheme not in ("http", "https")
            or not parsed.netloc
            or "." not in parsed.netloc
        ):
            messagebox.showerror(
                "URL no válida",
                "Escribe una URL válida, por ejemplo: https://www.ejemplo.com",
            )
            return

        try:
            codigo = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4,
            )
            codigo.add_data(url)
            codigo.make(fit=True)

            imagen_qr = codigo.make_image(
                fill_color=self.color_qr,
                back_color=self.color_fondo,
            ).convert("RGB")

            if self.ruta_logo:
                self._insertar_logo(imagen_qr)

            nombre = nombre_archivo_seguro(self.entrada_nombre.get().strip())
            ruta = ruta_disponible(nombre)
            imagen_qr.save(ruta, format="PNG")
            self._mostrar_vista_previa(imagen_qr)

            self.etiqueta_estado.configure(
                text=f"QR guardado correctamente:\n{ruta}",
                fg="#26734d",
            )
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo generar el QR.\n\n{error}")

    def _insertar_logo(self, imagen_qr):
        logo = Image.open(self.ruta_logo).convert("RGBA")
        ancho_qr, alto_qr = imagen_qr.size
        tamano_logo = int(ancho_qr * 0.20)
        logo.thumbnail((tamano_logo, tamano_logo))

        margen = 8
        fondo_logo = Image.new(
            "RGB",
            (logo.width + margen * 2, logo.height + margen * 2),
            "white",
        )
        posicion = (
            (ancho_qr - fondo_logo.width) // 2,
            (alto_qr - fondo_logo.height) // 2,
        )

        imagen_qr.paste(fondo_logo, posicion)
        imagen_qr.paste(
            logo,
            (posicion[0] + margen, posicion[1] + margen),
            logo,
        )

    def _mostrar_vista_previa(self, imagen_qr):
        vista = imagen_qr.copy()
        vista.thumbnail((350, 350))
        self.imagen_tk = ImageTk.PhotoImage(vista)
        self.etiqueta_qr.configure(image=self.imagen_tk, text="")

    def elegir_color_qr(self):
        color = colorchooser.askcolor(
            title="Seleccionar color del QR",
            color=self.color_qr,
        )
        if color[1]:
            self.color_qr = color[1]
            self.boton_color_qr.config(bg=self.color_qr)

    def elegir_color_fondo(self):
        color = colorchooser.askcolor(
            title="Seleccionar color de fondo",
            color=self.color_fondo,
        )
        if color[1]:
            self.color_fondo = color[1]
            self.boton_color_fondo.config(bg=self.color_fondo)

    def elegir_logo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar logotipo",
            filetypes=[
                ("Imagenes", "*.png *.jpg *.jpeg"),
                ("Todos los archivos", "*.*"),
            ],
        )
        if archivo:
            self.ruta_logo = Path(archivo)
            self.etiqueta_logo.config(text=f"Logo: {self.ruta_logo.name}")

    def abrir_carpeta(self):
        os.startfile(CARPETA_CODIGOS)

    def ejecutar(self):
        self.ventana.mainloop()


if __name__ == "__main__":
    GeneradorQR().ejecutar()
