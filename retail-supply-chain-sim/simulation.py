import simpy
import random
import pandas as pd

# Configuración base (Valores por defecto para pruebas)
SIMULATION_DAYS = 365  # Un año de operación

class ClothingStoreSimulation:
    def __init__(self, env, reorder_point, order_quantity, lead_time, initial_stock=50):
        self.env = env
        self.stock = initial_stock
        self.reorder_point = reorder_point
        self.order_quantity = order_quantity
        self.lead_time = lead_time
        
        # Estado
        self.order_pending = False
        
        # Métricas para el análisis
        self.data = [] # Guardaremos: [Día, Stock, Pedidos Recibidos, Ventas Perdidas]
        self.total_sales = 0
        self.lost_sales = 0

    def check_inventory_process(self):
        """Proceso continuo: Revisa el stock diariamente y hace pedidos si es necesario."""
        while True:
            # Si el stock está por debajo del punto de reorden y no hay pedido en camino
            if self.stock <= self.reorder_point and not self.order_pending:
                self.env.process(self.place_order())
            
            # Revisión diaria
            yield self.env.timeout(1)

    def place_order(self):
        """Proceso de pedido: Espera el tiempo de entrega (Lead Time) y repone stock."""
        self.order_pending = True
        # Simula el tiempo que tarda el proveedor (Lead Time)
        yield self.env.timeout(self.lead_time) 
        
        # Llega el pedido
        self.stock += self.order_quantity
        self.order_pending = False

    def customer_demand_process(self):
        """Proceso continuo: Simula la llegada de clientes diariamente."""
        while True:
            # Generar demanda aleatoria del día (Ej: entre 0 y 5 camisetas)
            daily_demand = random.randint(0, 5)
            
            if self.stock >= daily_demand:
                self.stock -= daily_demand
                self.total_sales += daily_demand
            else:
                # Si no hay stock suficiente, vendemos lo que queda y el resto es venta perdida
                sold = self.stock
                lost = daily_demand - self.stock
                
                self.stock = 0
                self.total_sales += sold
                self.lost_sales += lost
            
            yield self.env.timeout(1) # Pasa al siguiente día

    def observer_process(self):
        """Proceso continuo: Registra los datos al final de cada día."""
        while True:
            timestamp = self.env.now
            self.data.append({
                "day": timestamp,
                "stock": self.stock,
                "pending_order": 1 if self.order_pending else 0
            })
            yield self.env.timeout(1)

def run_simulation(reorder_point, order_quantity, lead_time):
    """Función principal que ejecutará Streamlit."""
    
    # 1. Crear entorno SimPy
    env = simpy.Environment()
    
    # 2. Inicializar la tienda
    store = ClothingStoreSimulation(env, reorder_point, order_quantity, lead_time)
    
    # 3. Activar los procesos
    env.process(store.check_inventory_process())
    env.process(store.customer_demand_process())
    env.process(store.observer_process())
    
    # 4. Correr simulación
    env.run(until=SIMULATION_DAYS)
    
    # 5. Devolver resultados en formato DataFrame (Tabla)
    df = pd.DataFrame(store.data)
    return df, store.lost_sales, store.total_sales