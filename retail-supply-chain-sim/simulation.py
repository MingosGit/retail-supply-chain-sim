import simpy
import random
import pandas as pd
import numpy as np

# Configuración base
SIMULATION_DAYS = 365

class ClothingStoreSimulation:
    def __init__(self, env, reorder_point, order_quantity, lead_time, initial_stock=50, 
                 demand_type="uniform", demand_mean=2.5, demand_std=1.5, seasonality=None):
        self.env = env
        self.stock = initial_stock
        self.reorder_point = reorder_point
        self.order_quantity = order_quantity
        self.lead_time = lead_time
        
        # Configuración de demanda
        self.demand_type = demand_type
        self.demand_mean = demand_mean
        self.demand_std = demand_std
        self.seasonality = seasonality  # Dict con factores por mes
        
        # Estado
        self.order_pending = False
        self.num_orders = 0  # NUEVO: Contador de pedidos
        
        # Métricas
        self.data = [] 
        self.total_sales = 0
        self.lost_sales = 0

    def check_inventory_process(self):
        while True:
            if self.stock <= self.reorder_point and not self.order_pending:
                self.env.process(self.place_order())
            yield self.env.timeout(1)

    def place_order(self):
        self.order_pending = True
        self.num_orders += 1  # NUEVO: Incrementamos contador
        yield self.env.timeout(self.lead_time) 
        self.stock += self.order_quantity
        self.order_pending = False

    def generate_demand(self):
        """Genera la demanda diaria según el tipo de distribución configurado."""
        # Demanda base
        if self.demand_type == "uniform":
            base_demand = random.randint(0, 5)
        elif self.demand_type == "normal":
            # Distribución Normal con media y desviación estándar
            demand = np.random.normal(self.demand_mean, self.demand_std)
            base_demand = max(0, int(round(demand)))  # No puede ser negativa
        elif self.demand_type == "poisson":
            # Distribución Poisson (común en retail)
            base_demand = np.random.poisson(self.demand_mean)
        else:
            base_demand = random.randint(0, 5)  # Fallback
        
        # Aplicar estacionalidad si está configurada
        if self.seasonality:
            current_day = int(self.env.now)
            current_month = (current_day // 30) % 12  # Aproximación de mes
            seasonal_factor = self.seasonality.get(current_month, 1.0)
            base_demand = int(round(base_demand * seasonal_factor))
        
        return max(0, base_demand)
    
    def customer_demand_process(self):
        while True:
            daily_demand = self.generate_demand()
            if self.stock >= daily_demand:
                self.stock -= daily_demand
                self.total_sales += daily_demand
            else:
                sold = self.stock
                lost = daily_demand - self.stock
                self.stock = 0
                self.total_sales += sold
                self.lost_sales += lost
            yield self.env.timeout(1)

    def observer_process(self):
        while True:
            timestamp = self.env.now
            self.data.append({
                "day": timestamp,
                "stock": self.stock,
                "pending_order": 1 if self.order_pending else 0
            })
            yield self.env.timeout(1)

def run_simulation(reorder_point, order_quantity, lead_time, demand_type="uniform", 
                   demand_mean=2.5, demand_std=1.5, seasonality=None):
    env = simpy.Environment()
    store = ClothingStoreSimulation(
        env, reorder_point, order_quantity, lead_time,
        demand_type=demand_type, demand_mean=demand_mean, demand_std=demand_std,
        seasonality=seasonality
    )
    env.process(store.check_inventory_process())
    env.process(store.customer_demand_process())
    env.process(store.observer_process())
    env.run(until=SIMULATION_DAYS)
    
    df = pd.DataFrame(store.data)
    # NUEVO: Devolvemos también el número de pedidos
    return df, store.lost_sales, store.total_sales, store.num_orders