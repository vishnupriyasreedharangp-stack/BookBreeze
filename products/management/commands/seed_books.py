from datetime import date

from django.core.management.base import BaseCommand

from products.models import Category, Product


class Command(BaseCommand):
    help = "Seed PyShop Books with categories and sample books."

    def handle(self, *args, **options):

        categories = {
            "Programming": (
                "Books about programming, software development, and technology."
            ),
            "Fiction": (
                "Novels, stories, and imaginative works from different genres."
            ),
            "Business": (
                "Books about entrepreneurship, management, finance, and leadership."
            ),
            "Science": (
                "Books exploring science, technology, and the natural world."
            ),
            "Self Development": (
                "Books focused on productivity, habits, learning, and personal growth."
            ),
        }

        category_objects = {}

        for name, description in categories.items():
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                },
            )

            if not created and not category.description:
                category.description = description
                category.save()

            category_objects[name] = category

        books = [
            {
                "name": "Python Crash Course",
                "author": "Eric Matthes",
                "isbn": "9781593279288",
                "description": (
                    "A hands-on introduction to programming with Python, "
                    "covering fundamentals and practical projects."
                ),
                "price": 899.00,
                "stock": 20,
                "category": "Programming",
                "published_date": date(2023, 1, 1),
                "image_url": (
                    "https://covers.openlibrary.org/isbn/9781593279288-L.jpg"
                ),
            },
            {
                "name": "Clean Code",
                "author": "Robert C. Martin",
                "isbn": "9780132350884",
                "description": (
                    "A practical guide to writing readable, maintainable, "
                    "and professional software."
                ),
                "price": 799.00,
                "stock": 15,
                "category": "Programming",
                "published_date": date(2008, 8, 1),
                "image_url": (
                    "https://covers.openlibrary.org/isbn/9780132350884-L.jpg"
                ),
            },
            {
                "name": "The Pragmatic Programmer",
                "author": "David Thomas & Andrew Hunt",
                "isbn": "9780135957059",
                "description": (
                    "A classic guide to becoming a more effective and "
                    "thoughtful software developer."
                ),
                "price": 999.00,
                "stock": 12,
                "category": "Programming",
                "published_date": date(2019, 9, 13),
                "image_url": (
                    "https://covers.openlibrary.org/isbn/9780135957059-L.jpg"
                ),
            },
            {
                "name": "Atomic Habits",
                "author": "James Clear",
                "isbn": "9780735211292",
                "description": (
                    "A practical approach to building better habits and "
                    "making meaningful improvements through small changes."
                ),
                "price": 599.00,
                "stock": 25,
                "category": "Self Development",
                "published_date": date(2018, 10, 16),
                "image_url": (
                    "https://covers.openlibrary.org/isbn/9780735211292-L.jpg"
                ),
            },
            {
                "name": "The Psychology of Money",
                "author": "Morgan Housel",
                "isbn": "9780857197689",
                "description": (
                    "An exploration of how emotions and behavior influence "
                    "the way people think about money and wealth."
                ),
                "price": 549.00,
                "stock": 18,
                "category": "Business",
                "published_date": date(2020, 9, 8),
                "image_url": (
                    "https://covers.openlibrary.org/isbn/9780857197689-L.jpg"
                ),
            },
            {
                "name": "Zero to One",
                "author": "Peter Thiel",
                "isbn": "9780804139298",
                "description": (
                    "A business and entrepreneurship guide about creating "
                    "innovative companies and building something new."
                ),
                "price": 499.00,
                "stock": 10,
                "category": "Business",
                "published_date": date(2014, 9, 16),
                "image_url": (
                    "https://covers.openlibrary.org/isbn/9780804139298-L.jpg"
                ),
            },
            {
                "name": "The Alchemist",
                "author": "Paulo Coelho",
                "isbn": "9780062315007",
                "description": (
                    "A philosophical adventure about following your dreams, "
                    "discovering purpose, and listening to your heart."
                ),
                "price": 399.00,
                "stock": 30,
                "category": "Fiction",
                "published_date": date(2014, 4, 15),
                "image_url": (
                    "https://covers.openlibrary.org/isbn/9780062315007-L.jpg"
                ),
            },
            {
                "name": "1984",
                "author": "George Orwell",
                "isbn": "9780451524935",
                "description": (
                    "A dystopian novel exploring surveillance, control, "
                    "propaganda, and the struggle for individual freedom."
                ),
                "price": 299.00,
                "stock": 22,
                "category": "Fiction",
                "published_date": date(1950, 7, 1),
                "image_url": (
                    "https://covers.openlibrary.org/isbn/9780451524935-L.jpg"
                ),
            },
            {
                "name": "A Brief History of Time",
                "author": "Stephen Hawking",
                "isbn": "9780553380163",
                "description": (
                    "An accessible exploration of cosmology, black holes, "
                    "time, space, and the origins of the universe."
                ),
                "price": 449.00,
                "stock": 14,
                "category": "Science",
                "published_date": date(1998, 9, 1),
                "image_url": (
                    "https://covers.openlibrary.org/isbn/9780553380163-L.jpg"
                ),
            },
            {
                "name": "Sapiens",
                "author": "Yuval Noah Harari",
                "isbn": "9780062316097",
                "description": (
                    "A broad exploration of human history, from early humans "
                    "to the modern world."
                ),
                "price": 699.00,
                "stock": 16,
                "category": "Science",
                "published_date": date(2015, 2, 10),
                "image_url": (
                    "https://covers.openlibrary.org/isbn/9780062316097-L.jpg"
                ),
            },
        ]

        created_count = 0
        updated_count = 0

        for book_data in books:
            category_name = book_data.pop("category")
            category = category_objects[category_name]

            product, created = Product.objects.update_or_create(
                isbn=book_data["isbn"],
                defaults={
                    **book_data,
                    "category": category,
                    "is_active": True,
                },
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {product.name}"
                    )
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(
                        f"Updated: {product.name}"
                    )
                )

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Done! Created {created_count} books, "
                f"updated {updated_count} books."
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Categories available: {len(category_objects)}"
            )
        )