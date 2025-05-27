import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Base de datos local de significados por carta en contexto amoroso
significados_amor = {
    "El Loco": "Una etapa de incertidumbre o impulsividad. Puede representar una nueva aventura amorosa, aunque sin garantías de compromiso estable.",
    "El Mago": "Capacidad de atraer a alguien con carisma y comunicación. Esta carta habla de poder personal y oportunidades amorosas que se pueden concretar si se actúa con decisión.",
    "La Papisa": "Un vínculo que se está gestando en el silencio. Relación profunda que requiere paciencia, confianza en la intuición y evitar juicios apresurados.",
    "La Emperatriz": "Relación con gran potencial de crecimiento. Expansión, belleza, placer y fertilidad emocional en el vínculo afectivo.",
    "El Emperador": "Estabilidad basada en estructuras firmes. Puede indicar una pareja seria o la necesidad de ordenar y consolidar la vida amorosa.",
    "El Papa": "Compromiso espiritual o moral. Unión que respeta normas tradicionales y busca consolidarse desde la comprensión y el consejo.",
    "Los Enamorados": "Una elección crucial. Tensión entre razón y corazón. Puede hablar de una relación apasionada o de la necesidad de elegir entre dos opciones.",
    "El Carro": "Avance decidido. El consultante tiene el control emocional para conquistar o reafirmar una relación con determinación.",
    "La Justicia": "Balance emocional. Relaciones justas, pero también la necesidad de tomar decisiones racionales en temas afectivos.",
    "El Ermitaño": "Tiempo de introspección. Puede representar una soledad buscada o una etapa de reflexión para fortalecer la relación con uno mismo.",
    "La Rueda de la Fortuna": "Cambios imprevistos. Giro del destino que puede traer una nueva relación, reencuentros o finales inesperados.",
    "La Fuerza": "Capacidad de dominar pasiones con ternura. Fortaleza emocional para sostener una relación con paciencia y cuidado.",
    "El Colgado": "Estancamiento o sacrificio. La relación requiere ver las cosas desde otro ángulo o hacer concesiones para evolucionar.",
    "La Muerte": "Transformación radical. Cierre de un ciclo amoroso que permite el nacimiento de una nueva forma de amar.",
    "La Templanza": "Armonía, paz y conexión espiritual. Tiempo favorable para reconciliaciones o para consolidar vínculos sanos.",
    "El Diablo": "Relación pasional, pero con riesgos de dependencia o manipulación. Invita a revisar los deseos y límites personales.",
    "La Torre": "Ruptura necesaria. Derrumbe de ilusiones que libera para construir desde una verdad más sólida.",
    "La Estrella": "Esperanza renovada. Amor sincero, inspirador y protector. Posibilidad de sanar heridas del pasado.",
    "La Luna": "Ilusiones, inseguridades o secretos. La situación puede estar nublada y requiere esperar claridad antes de actuar.",
    "El Sol": "Alegría compartida. Amor correspondido, sincero y con posibilidad de proyectarse hacia el futuro.",
    "El Juicio": "Llamado al despertar. Reconciliación, evaluación del pasado y nuevas oportunidades que surgen desde la comprensión mutua.",
    "El Mundo": "Cierre exitoso de un ciclo amoroso. Realización plena en pareja o logro emocional significativo."
}

class TarotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tarot del Amor - Arcanos Mayores")
        self.root.geometry("1200x800")
        self.root.configure(bg="black")

        self.pregunta = tk.StringVar()
        self.cartas = list(significados_amor.keys())
        random.shuffle(self.cartas)
        self.seleccionadas = []
        self.botones_cartas = {}

        self.imagen_trasera = ImageTk.PhotoImage(Image.open("imagenes/trasera.png").resize((90, 150)))

        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.root, text="Escribe tu pregunta sobre el amor:", font=("Arial", 12), bg="black", fg="white").pack(pady=10)
        tk.Entry(self.root, textvariable=self.pregunta, width=60).pack(pady=5)

        self.botones_frame = tk.Frame(self.root, bg="black")
        self.botones_frame.pack(pady=10)
        self.mostrar_cartas_ocultas()

        self.btn_reset = tk.Button(self.root, text="Nueva Lectura", command=self.reiniciar)
        self.btn_reset.pack(pady=10)

    def mostrar_cartas_ocultas(self):
        for widget in self.botones_frame.winfo_children():
            widget.destroy()

        self.botones_cartas = {}
        columnas = 6
        for index, carta in enumerate(self.cartas):
            fila = index // columnas
            columna = index % columnas
            btn = tk.Button(
                self.botones_frame,
                image=self.imagen_trasera,
                command=lambda c=carta: self.seleccionar_carta(c),
                relief="raised",
                borderwidth=2
            )
            btn.grid(row=fila, column=columna, padx=4, pady=4)
            self.botones_cartas[carta] = btn

    def seleccionar_carta(self, carta):
        if len(self.seleccionadas) < 3 and carta not in self.seleccionadas:
            self.seleccionadas.append(carta)
            self.botones_cartas[carta].config(relief="sunken", borderwidth=4, bg="red")
            if len(self.seleccionadas) == 3:
                self.interpretar()

    def interpretar(self):
        pregunta = self.pregunta.get().strip().lower()
        texto = f"Consulta realizada: \"{pregunta}\"\n\n"
        texto += "Cartas seleccionadas:\n"
        for carta in self.seleccionadas:
            texto += f"- {carta}: {significados_amor[carta]}\n"

        tema = "una situación amorosa general"
        if "ex" in pregunta:
            tema = "una relación del pasado"
        elif "volver" in pregunta:
            tema = "una reconciliación esperada"
        elif "pareja" in pregunta:
            tema = "una relación estable"
        elif "nuevo" in pregunta or "conocer" in pregunta:
            tema = "un amor potencial o nuevo vínculo"

        texto += f"\nInterpretación especializada para {tema}:"
        texto += f"La carta principal, '{self.seleccionadas[0]}', nos habla de {significados_amor[self.seleccionadas[0]]} Esto refleja tu situación emocional actual o tu enfoque consciente.\n"
        texto += f"Como energía de fondo o influencia subconsciente, aparece '{self.seleccionadas[1]}', que representa {significados_amor[self.seleccionadas[1]]}\n"
        texto += f"Finalmente, la dirección que marca esta lectura está simbolizada por '{self.seleccionadas[2]}', indicando que {significados_amor[self.seleccionadas[2]]}\n"

        # Recomendación según carta final
        recomendaciones = {
            "El Loco": "Confía, pero pon límites claros en tus relaciones.",
            "El Mago": "Actúa con seguridad: tienes el poder de influir en tu vida amorosa.",
            "La Papisa": "Escucha tu intuición y no apresures decisiones.",
            "La Emperatriz": "Cuida tu autoestima y abre tu corazón con generosidad.",
            "El Emperador": "Establece bases sólidas y sé firme en tus valores.",
            "El Papa": "Busca guía sabia y mantén la ética en tu actuar.",
            "Los Enamorados": "Reflexiona profundamente antes de tomar decisiones amorosas.",
            "El Carro": "Sigue adelante con determinación: el éxito es posible.",
            "La Justicia": "Actúa con honestidad, incluso si eso requiere sacrificio.",
            "El Ermitaño": "Tómate un tiempo a solas si necesitas claridad interior.",
            "La Rueda de la Fortuna": "Acepta los cambios: todo ocurre por una razón.",
            "La Fuerza": "Domina tus impulsos con amor y paciencia.",
            "El Colgado": "Observa desde otra perspectiva: no todo es como parece.",
            "La Muerte": "Suelta lo que ya no sirve: algo nuevo vendrá.",
            "La Templanza": "Busca el equilibrio emocional y evita los extremos.",
            "El Diablo": "Libérate de dependencias y obsesiones emocionales.",
            "La Torre": "Reconstruye sobre bases firmes: lo auténtico prevalecerá.",
            "La Estrella": "Ten fe: lo mejor aún está por llegar.",
            "La Luna": "No tomes decisiones aún. Espera que todo se aclare.",
            "El Sol": "Disfruta plenamente del presente: el amor es real.",
            "El Juicio": "Acepta tu pasado y permite que florezca una nueva etapa.",
            "El Mundo": "Reconoce lo logrado y abrete a la plenitud emocional."
        }

        carta_final = self.seleccionadas[2]
        texto += f"\nRecomendación final:\n{recomendaciones.get(carta_final, '')}"

        messagebox.showinfo("Interpretación de la lectura", texto)

    def reiniciar(self):
        self.seleccionadas = []
        self.pregunta.set("")
        random.shuffle(self.cartas)
        self.mostrar_cartas_ocultas()

if __name__ == "__main__":
    root = tk.Tk()
    app = TarotApp(root)
    root.mainloop()
