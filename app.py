import customtkinter as ctk
from tkinter import filedialog
import pandas as pd
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import yagmail
import os
import time

# =========================
# CONFIGURACIÓN VISUAL
# =========================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# =========================
# VENTANA
# =========================

app = ctk.CTk()
app.geometry("850x690")
app.title("Envío Automático de Certificados")

excel_path = ""
plantilla_path = ""

# =========================
# CARPETA DE SALIDA
# =========================

carpeta_salida = ""

# =========================
# SELECCIONAR EXCEL
# =========================

def seleccionar_excel():
    global excel_path

    excel_path = filedialog.askopenfilename(
        title="Seleccionar Excel",
        filetypes=[("Excel files", "*.xlsx")]
    )

    label_excel.configure(text=excel_path)

# =========================
# SELECCIONAR PLANTILLA PNG
# =========================

def seleccionar_plantilla():
    global plantilla_path

    plantilla_path = filedialog.askopenfilename(
        title="Seleccionar Plantilla PNG",
        filetypes=[
            ("PNG", "*.png"),
            ("Imagen", "*.png *.jpg *.jpeg")
        ]
    )

    label_plantilla.configure(text=plantilla_path)

# =========================
# SELECCIONAR CARPETA
# =========================

def seleccionar_carpeta():

    global carpeta_salida

    carpeta_salida = filedialog.askdirectory(
        title="Seleccionar carpeta de salida"
    )

    if carpeta_salida:

        label_carpeta.configure(
            text=carpeta_salida
        )



# =========================
# CONFIGURACIÓN DEL NOMBRE
# =========================

TAMANO_LETRA = 85
COLOR_LETRA = (93, 42, 141)

POSICION_Y = 655

DESPLAZAMIENTO_X = 180

ANCHO_MAXIMO = 1300


# =========================
# DIVIDIR NOMBRE
# =========================

def dividir_nombre_si_es_necesario(
        draw,
        nombre,
        font):

    bbox = draw.textbbox(
        (0, 0),
        nombre,
        font=font
    )

    ancho = bbox[2] - bbox[0]

    if ancho <= ANCHO_MAXIMO:
        return nombre

    palabras = nombre.split()

    mejor_texto = nombre
    mejor_diferencia = float("inf")

    for i in range(1, len(palabras)):

        linea1 = " ".join(
            palabras[:i]
        )

        linea2 = " ".join(
            palabras[i:]
        )

        ancho1 = draw.textbbox(
            (0, 0),
            linea1,
            font=font
        )[2]

        ancho2 = draw.textbbox(
            (0, 0),
            linea2,
            font=font
        )[2]

        diferencia = abs(
            ancho1 - ancho2
        )

        if diferencia < mejor_diferencia:

            mejor_diferencia = diferencia

            mejor_texto = (
                linea1 +
                "\n" +
                linea2
            )

    return mejor_texto



# =========================
# GENERAR PDF
# =========================

def generar_certificado(
        plantilla_png,
        nombre,
        pdf_salida):

    img = Image.open(
        plantilla_png
    ).convert("RGB")

    draw = ImageDraw.Draw(img)

    try:

        font = ImageFont.truetype(
            "times.ttf",
            TAMANO_LETRA
        )

    except:

        font = ImageFont.load_default()

    # =========================
    # DIVISIÓN AUTOMÁTICA
    # =========================

    nombre_mostrar = dividir_nombre_si_es_necesario(
     draw,
     nombre,
     font
    )

    lineas = nombre_mostrar.split("\n")

    espaciado = 25

    cantidad_lineas = len(lineas)

    # Si hay dos líneas, subir el bloque completo
    if cantidad_lineas > 1:
     posicion_inicial_y = POSICION_Y - 70
    else:
     posicion_inicial_y = POSICION_Y

    for indice, linea in enumerate(lineas):

     bbox = draw.textbbox(
         (0, 0),
         linea,
         font=font
        )

     ancho_linea = bbox[2] - bbox[0]

     x = (
         (img.width - ancho_linea) / 2
         + DESPLAZAMIENTO_X
        )

     y = (
         posicion_inicial_y
         + (indice * (TAMANO_LETRA + espaciado))
       )

     draw.text(
         (x, y),
         linea,
         fill=COLOR_LETRA,
         font=font
       )
     
    img.save(
     pdf_salida,
     "PDF",
     resolution=300
    ) 


# =========================
# VISTA PREVIA
# =========================

def vista_previa_certificado():

    try:

        if not excel_path:

            estado.configure(
                text="⚠️ Selecciona un Excel"
            )

            return

        if not plantilla_path:

            estado.configure(
                text="⚠️ Selecciona una plantilla"
            )

            return
        
        if not carpeta_salida:

            estado.configure(
                text="⚠️ Selecciona una carpeta de salida"
            )

            return

        df = pd.read_excel(excel_path)

        nombres = (
            df["Nombre Completo"]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        ventana = ctk.CTkToplevel(app)

        ventana.title("Vista previa")

        ventana.geometry("600x200")

        ventana.grab_set()

        titulo = ctk.CTkLabel(
            ventana,
            text="Selecciona un nombre",
            font=("Arial", 18)
        )

        titulo.pack(pady=15)

        combo_nombres = ctk.CTkComboBox(
            ventana,
            values=nombres,
            width=500
        )

        combo_nombres.pack(pady=15)

        if nombres:
            combo_nombres.set(
                nombres[0]
            )

        def generar_preview():

            try:

                nombre = (
                    combo_nombres.get()
                )

                pdf_preview = os.path.join(
                    carpeta_salida,
                    "VISTA_PREVIA.pdf"
                )

                generar_certificado(
                    plantilla_path,
                    nombre,
                    pdf_preview
                )

                os.startfile(
                    pdf_preview
                )

                estado.configure(
                    text=(
                        f"Vista previa generada:\n"
                        f"{nombre}"
                    )
                )

            except Exception as e:

                estado.configure(
                    text=f"Error: {e}"
                )

        btn_generar = ctk.CTkButton(
            ventana,
            text="Generar Vista Previa",
            command=generar_preview
        )

        btn_generar.pack(
            pady=20
        )

    except Exception as e:

        estado.configure(
            text=f"Error: {e}"
        )


# =========================
# ENVIAR CERTIFICADOS
# =========================

def enviar_certificados():

    try:

        if not excel_path:

            estado.configure(
                text="⚠️ Selecciona un Excel"
            )

            return

        if not plantilla_path:

            estado.configure(
                text="⚠️ Selecciona una plantilla PNG"
            )

            return
        
        if not carpeta_salida:

            estado.configure(
                text="⚠️ Selecciona una carpeta de salida"
            )

            return
        

        EMAIL = entry_email.get().strip()
        PASSWORD = entry_password.get().strip()

        if not EMAIL or not PASSWORD:

            estado.configure(
                text="⚠️ Ingresa correo y contraseña"
            )

            return

        df = pd.read_excel(
            excel_path
        )
        df["Nombre Completo"] = (
             df["Nombre Completo"]
             .astype(str)
             .str.strip()
        )
        df = df.head(2)
        

        total = len(df)

        correo = yagmail.SMTP(
            EMAIL,
            PASSWORD
        )

        progressbar.set(0)

        for i, row in df.iterrows():

            try:

                nombre = str(
                    row["Nombre Completo"]
                ).strip()

                email = str(
                    row["Dirección de correo electrónico"]
                ).strip()

                if (
                    not nombre
                    or not email
                    or email == "nan"
                ):
                    continue

                nombre_archivo = (
                    nombre
                    .replace(" ", "_")
                    .replace(".", "")
                    .replace("/", "")
                    .replace("\\", "")
                )

                pdf_path = os.path.join(
                    carpeta_salida,
                    f"{nombre_archivo}.pdf"
                )

                # =========================
                # GENERAR PDF
                # =========================

                generar_certificado(
                    plantilla_path,
                    nombre,
                    pdf_path
                )

                if not os.path.exists(
                    pdf_path
                ):

                    estado.configure(
                        text=f"❌ No se generó PDF para {nombre}"
                    )

                    app.update()

                    continue

                # =========================
                # ENVIAR CORREO
                # =========================

                correo.send(
                    to=email,
                    subject="Constancia de Evento - Comisión de Bioética del Estado de Tlaxcala",
                    contents=(
                        f"Hola {nombre},\n\n"
                        "La Comisión de Bioética del Estado de Tlaxcala le hace entrega de su constancia de participación en el evento mencionado dentro de la misma.\n\n"
                        "Favor de acusar de recibido.\n\n"
                        "Gracias por su participación.\n\n"
                    ),
                    attachments=pdf_path
                )

                estado.configure(
                    text=(
                        f"✅ {i+1}/{total} "
                        f"Enviado: {nombre}"
                    )
                )

                progressbar.set(
                    (i + 1) / total
                )

                app.update()

                time.sleep(2)

            except Exception as e:

                estado.configure(
                    text=f"❌ Error fila {i}: {e}"
                )

                app.update()

                continue

        estado.configure(
            text=(
                "🚀 Proceso terminado\n\n"
                f"PDFs guardados en:\n"
                f"{carpeta_salida}"
            )
        )

    except Exception as e:

        estado.configure(
            text=f"❌ Error general: {e}"
        )

# =========================
# GENERAR SOLO CERTIFICADOS
# =========================

def generar_solo_certificados():

    try:

        if not excel_path:

            estado.configure(
                text="⚠️ Selecciona un Excel"
            )

            return

        if not plantilla_path:

            estado.configure(
                text="⚠️ Selecciona una plantilla PNG"
            )

            return

        if not carpeta_salida:

            estado.configure(
                text="⚠️ Selecciona una carpeta de salida"
            )

            return

        df = pd.read_excel(excel_path)

        total = len(df)

        os.makedirs(
            carpeta_salida,
            exist_ok=True
        )

        progressbar.set(0)

        for i, row in df.iterrows():

            try:

                nombre = str(
                    row["Nombre Completo"]
                ).strip()

                if not nombre:
                    continue

                nombre_archivo = (
                    nombre
                    .replace(" ", "_")
                    .replace(".", "")
                    .replace("/", "")
                    .replace("\\", "")
                )

                pdf_path = os.path.join(
                    carpeta_salida,
                    f"{nombre_archivo}.pdf"
                )

                generar_certificado(
                    plantilla_path,
                    nombre,
                    pdf_path
                )

                estado.configure(
                    text=(
                        f"📄 {i+1}/{total} "
                        f"Generado: {nombre}"
                    )
                )

                progressbar.set(
                    (i + 1) / total
                )

                app.update()

            except Exception as e:

                estado.configure(
                    text=f"❌ Error fila {i}: {e}"
                )

                app.update()

                continue

        estado.configure(
            text=(
                "✅ Certificados generados correctamente\n\n"
                f"Guardados en:\n"
                f"{carpeta_salida}"
            )
        )

    except Exception as e:

        estado.configure(
            text=f"❌ Error general: {e}"
        )

# =========================
# INTERFAZ
# =========================

titulo = ctk.CTkLabel(
    app,
    text="ENVÍO AUTOMÁTICO DE CERTIFICADOS",
    font=("Arial", 24)
)

titulo.pack(pady=20)

btn_excel = ctk.CTkButton(
    app,
    text="Seleccionar Excel",
    command=seleccionar_excel
)

btn_excel.pack(pady=10)

label_excel = ctk.CTkLabel(
    app,
    text="Ningún Excel seleccionado",
    wraplength=750
)

label_excel.pack()

btn_plantilla = ctk.CTkButton(
    app,
    text="Seleccionar Plantilla PNG",
    command=seleccionar_plantilla
)

btn_plantilla.pack(pady=10)

label_plantilla = ctk.CTkLabel(
    app,
    text="Ninguna plantilla seleccionada",
    wraplength=750
)

label_plantilla.pack()

btn_carpeta = ctk.CTkButton(
    app,
    text="Seleccionar Carpeta de Salida",
    command=seleccionar_carpeta
)

btn_carpeta.pack(pady=10)

label_carpeta = ctk.CTkLabel(
    app,
    text="Ninguna carpeta seleccionada",
    wraplength=750
)

label_carpeta.pack()

entry_email = ctk.CTkEntry(
    app,
    placeholder_text="Correo Gmail",
    width=350
)

entry_email.pack(pady=15)

entry_password = ctk.CTkEntry(
    app,
    placeholder_text="Contraseña de aplicación",
    show="*",
    width=350
)

entry_password.pack(pady=10)

btn_enviar = ctk.CTkButton(
    app,
    text="GENERAR Y ENVIAR CERTIFICADOS",
    command=enviar_certificados,
    height=45,
    width=250
)

btn_enviar.pack(pady=15)

btn_preview = ctk.CTkButton(
    app,
    text="VISTA PREVIA",
    command=vista_previa_certificado,
    height=45,
    width=250
)

btn_preview.pack(pady=10)

btn_generar = ctk.CTkButton(
    app,
    text="SOLO GENERAR CERTIFICADOS",
    command=generar_solo_certificados,
    height=45,
    width=250
)

btn_generar.pack(pady=10)


progressbar = ctk.CTkProgressBar(
    app,
    width=500
)

progressbar.pack(pady=10)

progressbar.set(0)

estado = ctk.CTkLabel(
    app,
    text="",
    wraplength=750
)

estado.pack(pady=20)

app.mainloop()