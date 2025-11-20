import simpy
import random
import pandas as pd
import numpy as np

SIMULATION_DAYS = 365

class MultiProductStore:
    """Simulador para múltiples productos simultáneamente."""
    
    def __init__(self, env, products_config):
        """
        products_config: Lista de diccionarios con configuración de cada producto
        Ejemplo: [
            {
                'name': 'Producto A',
                'initial_stock': 50,
                'reorder_point': 15,
                'order_quantity': 50,
                'lead_time': 5,
                'demand_type': 'normal',
                'demand_mean': 2.5,
                'demand_std': 1.5,
                'seasonality': None
            },
            ...
        ]
        """
        self.env = env
        self.products = {}
        
        for config in products_config:
            product_name = config['name']
            self.products[product_name] = {
                'stock': config.get('initial_stock', 50),
                'reorder_point': config['reorder_point'],
                'order_quantity': config['order_quantity'],
                'lead_time': config['lead_time'],
                'demand_type': config.get('demand_type', 'uniform'),
                'demand_mean': config.get('demand_mean', 2.5),
                'demand_std': config.get('demand_std', 1.5),
                'seasonality': config.get('seasonality', None),
                'order_pending': False,
                'num_orders': 0,
                'total_sales': 0,
                'lost_sales': 0,
                'data': []
            }
    
    def generate_demand(self, product_name):
        """Genera demanda para un producto específico."""
        product = self.products[product_name]
        
        # Demanda base
        if product['demand_type'] == "uniform":
            base_demand = random.randint(0, 5)
        elif product['demand_type'] == "normal":
            demand = np.random.normal(product['demand_mean'], product['demand_std'])
            base_demand = max(0, int(round(demand)))
        elif product['demand_type'] == "poisson":
            base_demand = np.random.poisson(product['demand_mean'])
        else:
            base_demand = random.randint(0, 5)
        
        # Aplicar estacionalidad
        if product['seasonality']:
            current_day = int(self.env.now)
            current_month = (current_day // 30) % 12
            seasonal_factor = product['seasonality'].get(current_month, 1.0)
            base_demand = int(round(base_demand * seasonal_factor))
        
        return max(0, base_demand)
    
    def check_inventory_process(self, product_name):
        """Proceso de revisión de inventario para un producto."""
        product = self.products[product_name]
        
        while True:
            if product['stock'] <= product['reorder_point'] and not product['order_pending']:
                self.env.process(self.place_order(product_name))
            yield self.env.timeout(1)
    
    def place_order(self, product_name):
        """Proceso de pedido para un producto."""
        product = self.products[product_name]
        product['order_pending'] = True
        product['num_orders'] += 1
        
        yield self.env.timeout(product['lead_time'])
        
        product['stock'] += product['order_quantity']
        product['order_pending'] = False
    
    def customer_demand_process(self, product_name):
        """Proceso de demanda de clientes para un producto."""
        product = self.products[product_name]
        
        while True:
            daily_demand = self.generate_demand(product_name)
            
            if product['stock'] >= daily_demand:
                product['stock'] -= daily_demand
                product['total_sales'] += daily_demand
            else:
                sold = product['stock']
                lost = daily_demand - product['stock']
                product['stock'] = 0
                product['total_sales'] += sold
                product['lost_sales'] += lost
            
            yield self.env.timeout(1)
    
    def observer_process(self, product_name):
        """Proceso de observación para un producto."""
        product = self.products[product_name]
        
        while True:
            timestamp = self.env.now
            product['data'].append({
                "day": timestamp,
                "product": product_name,
                "stock": product['stock'],
                "pending_order": 1 if product['order_pending'] else 0
            })
            yield self.env.timeout(1)

def run_multi_product_simulation(products_config):
    """Ejecuta la simulación para múltiples productos."""
    env = simpy.Environment()
    store = MultiProductStore(env, products_config)
    
    # Iniciar procesos para cada producto
    for product_name in store.products.keys():
        env.process(store.check_inventory_process(product_name))
        env.process(store.customer_demand_process(product_name))
        env.process(store.observer_process(product_name))
    
    env.run(until=SIMULATION_DAYS)
    
    # Recopilar resultados
    results = {}
    for product_name, product_data in store.products.items():
        df = pd.DataFrame(product_data['data'])
        results[product_name] = {
            'dataframe': df,
            'lost_sales': product_data['lost_sales'],
            'total_sales': product_data['total_sales'],
            'num_orders': product_data['num_orders']
        }
    
    return results
