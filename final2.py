from tkinter import *
import heapq
from PIL import ImageTk, Image
#Es necesario instalar la librería PIL (pip install Pillow) en el termina

class DijkstraGUI:

  def __init__(self, master):
    self.master = master
    self.master.title("Dijkstra GUI")

    self.mapa_img = Image.open(r'.\mapa.jpeg')
    self.mapa_img = self.mapa_img.resize((600, 600))
    self.mapa_tk = ImageTk.PhotoImage(self.mapa_img)

    self.canvas = Canvas(self.master, width=800, height=600)
    self.canvas.place(x=0, y=0)

    self.canvas.create_image(0, 0, anchor=NW, image=self.mapa_tk)

    self.original_graph = {
        'LIMA': {
            'ICA': 1.40,
            'CUZCO': 7.22,
            'ANCASH': 2.88,
            'PASCO': 1.68
        },
        'ICA': {
            'LIMA': 1.40,
            'AREQUIPA': 4.72
        },
        'CUZCO': {
            'TACNA': 5.32,
            'LIMA': 7.22,
            'MADRE DE DIOS': 2.27,
            'AREQUIPA': 3.37
        },
        'PIURA': {
            'SAN MARTIN': 6.27,
            'LORETO': 11.15,
            'ANCASH': 4.71
        },
        'TACNA': {
            'AREQUIPA': 2.70,
            'CUZCO': 5.32
        },
        'AREQUIPA': {
            'CUZCO': 3.37,
            'ICA': 4.72,
            'TACNA': 2.70
        },
        'LORETO': {
            'PIURA': 11.15,
            'SAN MARTIN': 3.70
        },
        'UCAYALI': {
            'SAN MARTIN': 3.34,
            'PASCO': 4.77,
            'MADRE DE DIOS': 13.28
        },
        'ANCASH': {
            'PIURA': 4.71,
            'SAN MARTIN': 4.15,
            'PASCO': 2.78,
            'LIMA': 2.88
        },
        'SAN MARTIN': {
            'PIURA': 6.27,
            'LORETO': 3.70,
            'ANCASH': 4.15,
            'PASCO': 3.91,
            'UCAYALI': 3.34
        },
        'MADRE DE DIOS': {
            'UCAYALI': 13.28,
            'CUZCO': 2.27
        },
        'PASCO': {
            'SAN MARTIN': 3.91,
            'ANCASH': 2.78,
            'LIMA': 1.68,
            'UCAYALI': 4.77
        }
    }

    self.node_positions = {
        'LIMA': (200, 380),
        'ICA': (250, 450),
        'PIURA': (100, 180),
        'TACNA': (500, 580),
        'AREQUIPA': (400, 500),
        'CUZCO': (400, 430),
        'LORETO':(380, 130),
        'UCAYALI':(350, 300),
        'ANCASH':(180, 310),
        'SAN MARTIN':(240, 250),
        'MADRE DE DIOS':(470, 380),
        'PASCO':(270, 325),
    }

    # Cargar mapa del mapa del Perú

    self.dibujar_grafico(self.original_graph)

    self.origen_label = Label(self.master, text="ORIGEN:", font=("Arial", 12))
    self.origen_label.place(x=10, y=10)
    self.origen_entry = Entry(self.master, font=("Arial", 12))
    self.origen_entry.place(x=80, y=10)

    self.destino_label = Label(self.master,text="DESTINO:",font=("Arial", 12))
    self.destino_label.place(x=10, y=40)
    self.destino_entry = Entry(self.master, font=("Arial", 12))
    self.destino_entry.place(x=90, y=40)

    self.calcular_button = Button(self.master,text="Calcular",command=self.calcular_dijkstra,font=("Arial", 12),bg="#4CAF50",fg="white")
    self.calcular_button.place(x=250, y=10)

    self.borrar_button = Button(self.master,text="Borrar",command=self.borrar_calculo,font=("Arial", 12),bg="#f44336",fg="white")
    self.borrar_button.place(x=350, y=10)

    self.result_label = Label(self.master,text="",font=("Arial", 18),fg="#333333")
    self.result_label.place(x=10, y=700)

  
  def dibujar_grafico(self, graph):
    
    self.rout_img = Image.open(r'.\rout.png')
    self.rout_img = self.rout_img.resize((70, 70))
    self.rout_tk = ImageTk.PhotoImage(self.rout_img)

    for node, neighbors in graph.items():
      for neighbor, peso in neighbors.items():
        inicio_pos = self.node_positions[node]
        fin_pos = self.node_positions[neighbor]
        line = self.canvas.create_line(inicio_pos,fin_pos,fill="#333333",width=3)
        self.canvas.tag_raise(line)
        mid_x = (inicio_pos[0] + fin_pos[0]) / 2
        mid_y = (inicio_pos[1] + fin_pos[1]) / 2
        self.canvas.create_text(mid_x,mid_y - 1,text=str(peso),font=("Arial", 12),fill="#333333")

    for node, pos in self.node_positions.items():
        x, y = pos

        self.canvas.create_image(pos, anchor=CENTER, image=self.rout_tk)
        
        self.canvas.create_text(pos,text=node,font=("Arial", 16),fill="#0A0A0A")

#MI PARTE
        
  def calcular_dijkstra(self):
    origen = self.origen_entry.get().upper()
    destino = self.destino_entry.get().upper()

    if origen not in self.original_graph or destino not in self.original_graph:
      self.result_label.config(
          text="Los nodos de origen y destino deben estar en el grafo.",fg="#f44336")
      return

    distancia_minima, ruta_minima = self.dijkstra(origen, destino)
    self.result_label.config(text=f"La latencia mínima desde '{origen}' hasta '{destino}' es: {distancia_minima}",fg="#333333")
    self.ruta_minima(ruta_minima)
    

  def dijkstra(self, inicio, fin):
    graph_copy = self.original_graph.copy()
    distancia = {node: float('inf') for node in graph_copy}
    distancia[inicio] = 0
    lista_prioridad = [(0, inicio)]
    predecesores = {}

    while lista_prioridad:
      dist_actual, nodo_actual = heapq.heappop(lista_prioridad)
      if nodo_actual == fin:
        break

      if dist_actual > distancia[nodo_actual]:
        continue

      for neighbor, peso in graph_copy[nodo_actual].items():
        distance = dist_actual + peso
        if distance < distancia[neighbor]:
          distancia[neighbor] = distance
          heapq.heappush(lista_prioridad, (distance, neighbor))
          predecesores[neighbor] = nodo_actual

    # Reconstruir la ruta mínima
    path = []
    node = fin
    while node != inicio:
      path.insert(0, node)
      node = predecesores[node]
    path.insert(0, inicio)

    return distancia[fin], path

  def ruta_minima(self, path):
    for i in range(len(path) - 1):
      inicio_pos = self.node_positions[path[i]]
      fin_pos = self.node_positions[path[i + 1]]
      self.canvas.create_line(inicio_pos,fin_pos,fill="#FF5722",width=4,dash=(5, 3))

  def borrar_calculo(self):
    self.dibujar_grafico(self.original_graph)
    self.result_label.config(text="", fg="#333333")


def main():
  raiz = Tk()
  app = DijkstraGUI(raiz)
  raiz.mainloop()


if __name__ == "__main__":
  main()