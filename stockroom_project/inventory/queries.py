from django.db.models import Avg, Count, F, Q, Sum

from .models import Category, Customer, Order, OrderItem, Product


#  Section 8: QuerySets and field lookups 

# Question: which products are active?
def active_products():
    return Product.objects.filter(is_active=True)


# Question: which products have stock less than or equal to 5?
def low_stock_products():
    return Product.objects.filter(stock__lte=5)


# Question: which products cost between 60 and 130?
def products_in_price_range():
    return Product.objects.filter(price__gte=60, price__lte=130)


# Question: which product names contain beans (case-insensitive)?
def search_products_by_name():
    return Product.objects.filter(name__icontains="BEANS")


# Question: which products remain after excluding the inactive ones?
def products_excluding_inactive():
    return Product.objects.exclude(is_active=False)


# Question: how do products look ordered by category name then product name?
def products_ordered_by_category_and_name():
    return Product.objects.order_by('category__name', 'name')


# Question: what are the five most recently created orders?
def five_latest_orders():
    return Order.objects.order_by('-created_at')[:5]


# Question: which products have grinder in the name or EY in the SKU? (Q)
def products_by_name_or_sku():
    return Product.objects.filter(
        Q(name__icontains="grinder") | Q(sku__icontains="EY")
    )


# Question: which order items have a quantity >= the product's current stock? (F)
def items_quantity_at_least_stock():
    return OrderItem.objects.filter(quantity__gte=F('product__stock'))


# Section 9: Relationship queries 

# Question: what is the category of product 1? (forward)
def product_category():
    return Product.objects.get(pk=1).category


# Question: which products belong to the "Coffee Beans" category? (reverse)
def category_products():
    return Category.objects.get(name="Coffee Beans").products.all()


# Question: which orders belong to customer 1?
def customer_orders():
    return Customer.objects.get(pk=1).orders.all()


# Question: which items are in order 1?
def order_items():
    return Order.objects.get(pk=1).items.all()


# Question: which product does order item 1 refer to?
def order_item_product():
    return OrderItem.objects.get(pk=1).product


# Question: which products are contained in order 1?
def order_products():
    return Order.objects.get(pk=1).products.all()


# Question: which orders contain product 1?
def product_orders():
    return Product.objects.get(pk=1).orders.all()


# Section 10: Annotation and aggregation 

# Question: how many products are stored?
def total_products():
    return Product.objects.aggregate(total_products=Count('id'))


# Question: what is the average price of active products?
def average_active_price():
    return Product.objects.filter(is_active=True).aggregate(avg_price=Avg('price'))


# Question: what is the total stock of active products?
def total_active_stock():
    return Product.objects.filter(is_active=True).aggregate(total_stock=Sum('stock'))


# Question: how many products belong to each category?
def products_per_category():
    return Category.objects.annotate(
        product_count=Count('products')
    ).values_list('name', 'product_count')


# Question: how many order items belong to each order?
def items_per_order():
    return Order.objects.annotate(
        item_count=Count('items')
    ).values_list('id', 'item_count')


# Question: what is the total value of each order (quantity x unit_price)?
def total_value_per_order():
    return Order.objects.annotate(
        total_value=Sum(F('items__quantity') * F('items__unit_price'))
    ).values_list('id', 'total_value')


#  Optional challenge

# Question: which category has the highest number of active products?
def category_with_most_active_products():
    return Category.objects.filter(
        products__is_active=True
    ).annotate(
        active_count=Count('products')
    ).order_by('-active_count').first()