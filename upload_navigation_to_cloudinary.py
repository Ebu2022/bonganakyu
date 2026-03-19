import os
import django
import cloudinary.uploader

# Setup Django before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bonganakyu.settings")
django.setup()


def main():
    from chatbot.models import Navigation  # Imported here safely

    n_uploaded = 0
    for nav in Navigation.objects.all():
        if nav.image and "res.cloudinary.com" not in nav.image.url:
            print(f"Uploading: {nav.image.path}")
            try:
                res = cloudinary.uploader.upload(nav.image.path)
                nav.image = res["public_id"]
                nav.save()
                n_uploaded += 1
            except Exception as e:
                print(f"Error uploading {nav.image.path}: {e}")

    print(f"✅ Done. Total images uploaded: {n_uploaded}")


if __name__ == "__main__":
    main()
