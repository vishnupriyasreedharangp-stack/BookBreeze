import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from django.conf import settings
from django.core.management.base import BaseCommand

from products.models import Product


class Command(BaseCommand):
    help = 'Download book covers into static/books/'

    def download_cover(self, isbn, destination):
        url = (
            f'https://covers.openlibrary.org/'
            f'b/isbn/{isbn}-L.jpg?default=false'
        )

        request = Request(
            url,
            headers={
                'User-Agent': 'PyShopBooks/1.0'
            }
        )

        try:
            with urlopen(
                request,
                timeout=30
            ) as response:

                image_data = response.read()

            if not image_data:
                return False

            destination.write_bytes(image_data)

            return True

        except HTTPError as error:
            self.stdout.write(
                self.style.WARNING(
                    f'  HTTP error {error.code} for {isbn}'
                )
            )

        except URLError as error:
            self.stdout.write(
                self.style.WARNING(
                    f'  Network error for {isbn}: {error.reason}'
                )
            )

        except Exception as error:
            self.stdout.write(
                self.style.WARNING(
                    f'  Error for {isbn}: {error}'
                )
            )

        return False

    def handle(self, *args, **options):

        covers_directory = (
            Path(settings.BASE_DIR)
            / 'static'
            / 'books'
        )

        covers_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        products = Product.objects.filter(
            is_active=True
        ).exclude(
            isbn__isnull=True
        ).exclude(
            isbn=''
        )

        downloaded = 0
        skipped = 0
        failed = 0

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                'Downloading PyShop Books covers...'
            )
        )
        self.stdout.write('')

        for product in products:

            isbn = product.isbn.strip()

            filename = f'{isbn}.jpg'

            destination = (
                covers_directory / filename
            )

            self.stdout.write(
                f'Processing: {product.name}'
            )

            if destination.exists():
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Already downloaded: {filename}'
                    )
                )

                skipped += 1
                continue

            success = self.download_cover(
                isbn,
                destination
            )

            if success:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  Downloaded: {filename}'
                    )
                )

                downloaded += 1

            else:
                self.stdout.write(
                    self.style.ERROR(
                        f'  Cover unavailable: {isbn}'
                    )
                )

                failed += 1

            # Be gentle with the cover service.
            time.sleep(2)

        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS(
                '--------------------------------'
            )
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Cover download complete!'
            )
        )

        self.stdout.write(
            f'Downloaded: {downloaded}'
        )

        self.stdout.write(
            f'Skipped:    {skipped}'
        )

        self.stdout.write(
            f'Failed:     {failed}'
        )

        self.stdout.write('')
        self.stdout.write(
            f'Cover folder: {covers_directory}'
        )
        self.stdout.write('')