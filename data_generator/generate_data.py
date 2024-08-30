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
        
        product_names = {
            'Chairs': ['Ergonomic Office Chair', 'Leather Executive Chair', 'Mesh Task Chair', 'Gaming Chair'],
            'Tables': ['Oak Dining Table', 'Glass Coffee Table', 'Folding Card Table', 'Standing Desk'],
            'Bookcases': ['5-Shelf Bookcase', 'Floating Wall Shelves', 'Ladder Bookshelf', 'Cube Organizer'],
            'Paper': ['Recycled Printer Paper', 'Legal Pads', 'Sticky Notes', 'Cardstock'],
            'Binders': ['3-Ring Binder', 'Presentation Folder', 'Document Organizer', 'Sheet Protectors'],
            'Art': ['Colored Pencil Set', 'Watercolor Paint Kit', 'Claude Monet Poster', 'Sketch Pad'],
            'Phones': ['Smartphone X12', 'Wireless Desk Phone', 'Rugged Flip Phone', 'Business VoIP Phone'],
            'Computers': ['Pro Laptop 15"', 'All-in-One Desktop', 'Gaming PC', 'Tablet Pro'],
            'Accessories': ['Wireless Mouse', 'Ergonomic Keyboard', 'USB-C Hub', 'Laptop Cooling Pad']
        }

        for i in range(num_products):
            product_id = i + 1
            category = random.choice(categories)
            sub_category = random.choice(sub_categories[category])
            product_name = random.choice(product_names[sub_category])
            price = round(random.uniform(10, 1000), 2)

            writer.writerow([product_id, product_name, category, sub_category, price])

def generate_order_data(num_orders, num_customers, num_products, addresses, zip_multipliers, output_dir):
    with open(os.path.join(output_dir, 'order_info.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['order_id', 'line_item_id', 'customer_id', 'order_date', 'ship_date', 'ship_mode', 
                         'delivery_address', 'delivery_lat', 'delivery_lon', 'product_id', 'quantity', 
                         'sales', 'discount', 'profit'])

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

            for j in range(random.randint(1, 5)):
                line_item_id = f"{order_id}-{j+1}"
                product_id = random.randint(1, num_products)
                quantity = random.randint(1, 10)
                base_sales = random.uniform(10, 1000)
                sales = round(base_sales * zip_multipliers[zip_code], 2)
                discount = round(random.uniform(0, 0.5), 2)
                profit = round(sales * (1 - discount) * random.uniform(0.1, 0.5), 2)

                writer.writerow([order_id, line_item_id, customer_id, order_date.strftime('%Y-%m-%d'), 
                                 ship_date.strftime('%Y-%m-%d'), ship_mode, delivery_address, 
                                 delivery_lat, delivery_lon, product_id, quantity, sales, discount, profit])

def generate_delivery_data(num_deliveries, output_dir):
    with open(os.path.join(output_dir, 'delivery_data.csv'), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['delivery_id', 'order_id', 'estimated_delivery_date', 'actual_delivery_date', 'delivery_status'])

        statuses = ['In Transit', 'Delivered', 'Delayed', 'Failed']

        with open(os.path.join(output_dir, 'order_info.csv'), 'r') as order_file:
            order_reader = csv.reader(order_file)
            next(order_reader)  # Skip header
            orders = list(set(row[0] for row in order_reader))  # Get unique order_ids

        for i in range(num_deliveries):
            delivery_id = i + 1
            order_id = random.choice(orders)
            
            # Find the corresponding order in the order_info.csv
            with open(os.path.join(output_dir, 'order_info.csv'), 'r') as order_file:
                order_reader = csv.reader(order_file)
                next(order_reader)  # Skip header
                for row in order_reader:
                    if row[0] == order_id:
                        ship_date = datetime.strptime(row[4], '%Y-%m-%d')
                        break

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