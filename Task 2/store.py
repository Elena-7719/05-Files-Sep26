import json
from datetime import datetime

# Текущая дата для расчета сроков годности
TODAY_STR = "2026-10-14"
today = datetime.strptime(TODAY_STR, "%Y-%m-%d")


# 1. Экспорт товаров, срок годности которых истекает в ближайшие days дней
def export_expiring_products(json_data, filename, days):
    data = json.loads(json_data)

    with open(filename, "w", encoding="utf-8") as file:
        file.write("id, name, category, expires, days_left\n")

        for product in data["products"]:
            product_date = datetime.strptime(product["expires"], "%Y-%m-%d")
            days_left = (product_date - today).days

            if 0 <= days_left <= days:
                file.write(
                    f"{product['id']}, {product['name']}, {product['category']}, {product['expires']}, {days_left}\n"
                )


# 2. Экспорт товаров, у которых срок годности уже истёк
def export_expired_products(json_data, filename):
    data = json.loads(json_data)

    with open(filename, "w", encoding="utf-8") as file:
        file.write("id, name, category, expires, expired_days_ago\n")

        for product in data["products"]:
            product_date = datetime.strptime(product["expires"], "%Y-%m-%d")
            expired_days_ago = (today - product_date).days

            if expired_days_ago > 0:
                file.write(
                    f"{product['id']}, {product['name']}, {product['category']}, {product['expires']}, {expired_days_ago}\n"
                )


# 3*. Создание отчёта по продажам
def export_sales_report(products_json, sales_json, filename):
    products_data = json.loads(products_json)
    sales_data = json.loads(sales_json)

    with open(filename, "w", encoding="utf-8") as file:
        file.write("product_name, quantity_sold, total_revenue\n")

        for sale in sales_data["sales"]:
            for product in products_data["products"]:
                if product["id"] == sale["product_id"]:
                    name = product["name"]
                    quantity = sale["quantity"]
                    revenue = round(quantity * product["price"], 2)

                    file.write(f"{name}, {quantity}, {revenue}\n")


# 4*. Группировка товаров по категориям
def export_category_summary(json_data, filename):
    data = json.loads(json_data)

    cat_counts = {}
    cat_prices = {}

    for product in data["products"]:
        category = product["category"]
        price = product["price"]

        if category not in cat_counts:
            cat_counts[category] = 0
            cat_prices[category] = 0.0

        cat_counts[category] += 1
        cat_prices[category] += price

    with open(filename, "w", encoding="utf-8") as file:
        file.write("category, products_count, average_price\n")

        for category in cat_counts:
            count = cat_counts[category]
            total_price = cat_prices[category]
            avg_price = round(total_price / count, 2)

            file.write(f"{category}, {count}, {avg_price}\n")
