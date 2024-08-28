import csv
import random
from datetime import datetime, timedelta
import uuid
import os

def create_output_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    return directory_name

def load_addresses(filename):
    addresses = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            addresses.append({
                'full_address': row['full_address'],
                'lat': float(row['lat']),
                'lon': float(row['lon']),
                'zip': row['zip']
            })
    return addresses

def generate_zip_multipliers(addresses):
    unique_zips = set(address['zip'] for address in addresses)
    return {zip_code: random.uniform(0.8, 1.5) for zip_code in unique_zips}

def generate_customer_data(num_customers, output_dir):
    with open(os.path.join(output_dir, 'crm_customers.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['customer_id', 'customer_name', 'email', 'phone', 'segment'])
        
        segments = ['Consumer', 'Corporate', 'Home Office']
        
        for i in range(num_customers):
            customer_id = i + 1
            customer_name = f"Customer {customer_id}"
            email = f"customer{customer_id}@example.com"
            phone = f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            segment = random.choice(segments)
            
            writer.writerow([customer_id, customer_name, email, phone, segment])

def generate_product_data(num_products, output_dir):
    with open(os.path.join(output_dir, 'ecommerce_products.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['product_id', 'product_name', 'category', 'sub_category', 'price'])
        
        categories = ['Furniture', 'Office Supplies', 'Technology']
        sub_categories = {
            'Furniture': ['Chairs', 'Tables', 'Bookcases'],
            'Office Supplies': ['Paper', 'Binders', 'Art'],
            'Technology': ['Phones', 'Computers', 'Accessories']
        }
        
        for i in range(num_products):
            product_id = i + 1
            category = random.choice(categories)
            sub_category = random.choice(sub_categories[category])
            product_name = f"{sub_category} Item {product_id}"
            price = round(random.uniform(10, 1000), 2)
            
            writer.writerow([product_id, product_name, category, sub_category, price])

def generate_order_data(num_orders, num_customers, num_products, addresses, zip_multipliers, output_dir):
    with open(os.path.join(output_dir, 'ecommerce_orders.csv'), 'w', newline='') as order_file, \
         open(os.path.join(output_dir, 'ecommerce_order_details.csv'), 'w', newline='') as detail_file:
        
        order_writer = csv.writer(order_file)
        detail_writer = csv.writer(detail_file)
        
        order_writer.writerow(['order_id', 'customer_id', 'order_date', 'ship_date', 'ship_mode', 'delivery_address', 'delivery_lat', 'delivery_lon'])
        detail_writer.writerow(['order_id', 'product_id', 'quantity', 'sales', 'discount', 'profit'])
        
        ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']
        
        for i in range(num_orders):
            order_id = str(uuid.uuid4())
            customer_id = random.randint(1, num_customers)
            order_date = datetime.now() - timedelta(days=random.randint(0, 365))
            ship_date = order_date + timedelta(days=random.randint(1, 7))
            ship_mode = random.choice(ship_modes)
            
            address_info = random.choice(addresses)
            delivery_address = address_info['full_address']
            delivery_lat = address_info['lat']
            delivery_lon = address_info['lon']
            zip_code = address_info['zip']
            
            order_writer.writerow([order_id, customer_id, order_date.strftime('%Y-%m-%d'), 
                                   ship_date.strftime('%Y-%m-%d'), ship_mode, delivery_address, 
                                   delivery_lat, delivery_lon])
            
            for _ in range(random.randint(1, 5)):
                product_id = random.randint(1, num_products)
                quantity = random.randint(1, 10)
                base_sales = random.uniform(10, 1000)
                sales = round(base_sales * zip_multipliers[zip_code], 2)
                discount = round(random.uniform(0, 0.5), 2)
                profit = round(sales * (1 - discount) * random.uniform(0.1, 0.5), 2)
                
                detail_writer.writerow([order_id, product_id, quantity, sales, discount, profit])

def generate_delivery_data(num_deliveries, output_dir):
    with open(os.path.join(output_dir, 'delivery_data.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['delivery_id', 'order_id', 'estimated_delivery_date', 'actual_delivery_date', 'delivery_status'])
        
        statuses = ['In Transit', 'Delivered', 'Delayed', 'Failed']
        
        with open(os.path.join(output_dir, 'ecommerce_orders.csv'), 'r') as order_file:
            order_reader = csv.reader(order_file)
            next(order_reader)  # Skip header
            orders = list(order_reader)
        
        for i in range(num_deliveries):
            delivery_id = i + 1
            order = random.choice(orders)
            order_id = order[0]
            ship_date = datetime.strptime(order[3], '%Y-%m-%d')
            
            estimated_delivery_date = ship_date + timedelta(days=random.randint(1, 5))
            actual_delivery_date = estimated_delivery_date + timedelta(days=random.randint(-1, 3))
            delivery_status = random.choice(statuses)
            
            writer.writerow([delivery_id, order_id, estimated_delivery_date.strftime('%Y-%m-%d'), 
                             actual_delivery_date.strftime('%Y-%m-%d'), delivery_status])

# Main execution
if __name__ == "__main__":
    num_customers = 1000
    num_products = 500
    num_orders = 5000
    num_deliveries = 5000

    # Create output directory
    output_dir = create_output_directory('generated_data')

    # Load addresses
    addresses = load_addresses('sample_addresses.csv')

    # Generate zip code multipliers
    zip_multipliers = generate_zip_multipliers(addresses)

    generate_customer_data(num_customers, output_dir)
    generate_product_data(num_products, output_dir)
    generate_order_data(num_orders, num_customers, num_products, addresses, zip_multipliers, output_dir)
    generate_delivery_data(num_deliveries, output_dir)

    print(f"Data generation complete. CSV files have been created in the '{output_dir}' directory.")