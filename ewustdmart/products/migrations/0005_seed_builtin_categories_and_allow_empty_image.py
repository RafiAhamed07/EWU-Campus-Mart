# Generated manually on 2026-04-05

from django.db import migrations, models
from django.utils.text import slugify


BUILT_IN_CATEGORIES = [
    "Electronics",
    "Computers and Accessories",
    "Smartphones and Tablets",
    "Wearable Technology",
    "Home Appliances",
    "Kitchen and Dining",
    "Furniture",
    "Home Decor",
    "Lighting",
    "Tools and Hardware",
    "Automotive",
    "Motorcycle Accessories",
    "Sports and Outdoors",
    "Fitness Equipment",
    "Camping and Hiking",
    "Cycling",
    "Books",
    "Office Supplies",
    "School Supplies",
    "Art and Craft Supplies",
    "Toys and Games",
    "Board Games and Puzzles",
    "Baby and Kids",
    "Pet Supplies",
    "Clothing",
    "Footwear",
    "Jewelry",
    "Watches",
    "Bags and Luggage",
    "Beauty and Personal Care",
    "Health and Wellness",
    "Medical Supplies",
    "Grocery and Gourmet",
    "Beverages",
    "Garden and Outdoor Living",
    "Plants and Seeds",
    "Musical Instruments",
    "Cameras and Photography",
    "Video and Audio Equipment",
    "Gaming",
    "Software",
    "Stationery",
    "Party Supplies",
    "Travel Accessories",
    "Cleaning Supplies",
    "Laundry Supplies",
    "Storage and Organization",
    "Industrial Supplies",
    "Safety Equipment",
    "Handmade Products",
    "Collectibles",
    "Antiques",
    "Eco Friendly Products",
    "Traditional and Cultural Items",
    "Seasonal Items",
    "Gift Items",
]


def seed_builtin_categories(apps, schema_editor):
    Category = apps.get_model("products", "Category")

    for name in BUILT_IN_CATEGORIES:
        slug = slugify(name)
        Category.objects.get_or_create(
            slug=slug,
            defaults={"category_name": name},
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0004_cartitem_unit_price_product_is_available_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="category_image",
            field=models.ImageField(blank=True, null=True, upload_to="categories"),
        ),
        migrations.RunPython(seed_builtin_categories, noop_reverse),
    ]
