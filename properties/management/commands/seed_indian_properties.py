import os
import shutil
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from agents.models import Agent
from properties.models import Property, PropertyImage

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds realistic Indian properties (2BHK, 3BHK, 4BHK, Studio, Residence Estates) and copies AI-generated images'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Clearing existing properties, images, and agents for fresh seed..."))
        PropertyImage.objects.all().delete()
        Property.objects.all().delete()
        Agent.objects.all().delete()

        # 1. Create or get default Agent User
        self.stdout.write("Setting up agent profile...")
        agent_user, created = User.objects.get_or_create(
            username='agent_ayush',
            defaults={
                'email': 'ayush.agent@realestate.in',
                'first_name': 'Ayush',
                'last_name': 'Sharma',
                'user_type': User.UserType.AGENT,
                'phone_number': '+91 98765 43210'
            }
        )
        if created:
            agent_user.set_password('password123')
            agent_user.save()

        # Set user_type to AGENT if user already existed
        if agent_user.user_type != User.UserType.AGENT:
            agent_user.user_type = User.UserType.AGENT
            agent_user.save()

        agent, _ = Agent.objects.get_or_create(
            user=agent_user,
            defaults={
                'license_number': 'RE-IND-2026-009',
                'agency_name': 'Antigravity Premium Estates',
                'bio': 'Expert real estate consultant specializing in premium Indian residences, luxury villas, and studio apartments.',
                'experience_years': 8,
                'specializations': 'residential, villas, luxury estates, studios',
                'is_verified': True
            }
        )

        # 2. Source Images Details
        source_dir = os.path.join(settings.BASE_DIR, 'properties', 'seed_assets')
        dest_dir = os.path.join(settings.MEDIA_ROOT, 'property_images')
        
        # Ensure media directory exists
        os.makedirs(dest_dir, exist_ok=True)

        images_mapping = {
            'mumbai_2bhk': 'mumbai_2bhk.png',
            'bangalore_3bhk': 'bangalore_3bhk.png',
            'delhi_4bhk': 'delhi_4bhk.png',
            'pune_studio': 'pune_studio.png',
            'chennai_estate': 'chennai_estate.png'
        }

        # Helper function to copy image
        def copy_property_image(key, filename):
            src_path = os.path.join(source_dir, filename)
            dest_filename = f"{key}.png"
            dest_path = os.path.join(dest_dir, dest_filename)
            
            if os.path.exists(src_path):
                shutil.copy2(src_path, dest_path)
                self.stdout.write(self.style.SUCCESS(f"Successfully copied image: {dest_filename}"))
                return f"property_images/{dest_filename}"
            else:
                self.stdout.write(self.style.ERROR(f"Source file not found for: {filename} at {src_path}"))
                return None

        # Copy all images
        copied_images = {}
        for key, name in images_mapping.items():
            copied_images[key] = copy_property_image(key, name)

        # 3. Seed Properties
        properties_data = [
            {
                'title': 'Elegant 2 BHK Ocean-View Apartment',
                'description': 'A beautifully designed 2 BHK apartment in Worli, Mumbai. Features a spacious living area, premium modular kitchen, modern bathrooms, and breathtaking views of the Arabian Sea. Ideal for professionals and small families.',
                'property_type': Property.PropertyType.APARTMENT,
                'listing_type': Property.ListingType.SALE,
                'price': 27500000.00,  # 2.75 Crores
                'bedrooms': 2,
                'bathrooms': 2,
                'area_sqft': 1100.00,
                'address': '24th Floor, Sea Breeze Towers, Worli',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'zip_code': '400018',
                'latitude': 19.0178,
                'longitude': 72.8173,
                'is_featured': True,
                'image_key': 'mumbai_2bhk'
            },
            {
                'title': 'Premium 3 BHK High-Rise Sky Residence',
                'description': 'Luxury living in Whitefield, Bangalore. This 3 BHK flat offers spacious bedrooms, elegant balconies with green canopy views, access to a luxury clubhouse, swimming pool, and excellent proximity to IT parks.',
                'property_type': Property.PropertyType.APARTMENT,
                'listing_type': Property.ListingType.SALE,
                'price': 16500000.00,  # 1.65 Crores
                'bedrooms': 3,
                'bathrooms': 3,
                'area_sqft': 1850.00,
                'address': '12th Floor, Prestige Heights, Whitefield',
                'city': 'Bangalore',
                'state': 'Karnataka',
                'zip_code': '560066',
                'latitude': 12.9698,
                'longitude': 77.7499,
                'is_featured': True,
                'image_key': 'bangalore_3bhk'
            },
            {
                'title': 'Spectacular 4 BHK Luxurious Villa & Estate',
                'description': 'An ultra-luxury 4 BHK independent villa estate located in Vasant Vihar, New Delhi. Complete with a private swimming pool, landscaped lawn, expansive glass facades, double-height ceilings, smart home automation, and 24/7 private security.',
                'property_type': Property.PropertyType.HOUSE,
                'listing_type': Property.ListingType.SALE,
                'price': 85000000.00,  # 8.5 Crores
                'bedrooms': 4,
                'bathrooms': 5,
                'area_sqft': 4500.00,
                'address': 'Block C, Vasant Vihar',
                'city': 'Delhi',
                'state': 'Delhi',
                'zip_code': '110057',
                'latitude': 28.5606,
                'longitude': 77.1627,
                'is_featured': True,
                'image_key': 'delhi_4bhk'
            },
            {
                'title': 'Chic & Cozy Modern Studio Apartment',
                'description': 'A fully furnished contemporary studio apartment in Koregaon Park, Pune. Optimized for space efficiency with high-quality modular furniture, integrated workspace, high-speed Wi-Fi, and walking distance to popular cafes.',
                'property_type': Property.PropertyType.APARTMENT,
                'listing_type': Property.ListingType.RENT,
                'price': 35000.00,  # 35k Rent per month
                'bedrooms': 1,
                'bathrooms': 1,
                'area_sqft': 450.00,
                'address': 'Lane 7, Near German Bakery, Koregaon Park',
                'city': 'Pune',
                'state': 'Maharashtra',
                'zip_code': '411001',
                'latitude': 18.5362,
                'longitude': 73.8940,
                'is_featured': True,
                'image_key': 'pune_studio'
            },
            {
                'title': 'Luxurious Coastal Residence Estate',
                'description': 'Exquisite beachfront contemporary residence estate in ECR, Chennai. This stunning home offers scenic sea vistas, beautiful palm gardens, massive floor-to-ceiling windows, open terrace deck, and private beach access.',
                'property_type': Property.PropertyType.HOUSE,
                'listing_type': Property.ListingType.SALE,
                'price': 52000000.00,  # 5.2 Crores
                'bedrooms': 4,
                'bathrooms': 4,
                'area_sqft': 3800.00,
                'address': 'Sea Cliff Enclave, East Coast Road',
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'zip_code': '600115',
                'latitude': 12.8465,
                'longitude': 80.2435,
                'is_featured': True,
                'image_key': 'chennai_estate'
            }
        ]

        self.stdout.write("Creating property listings...")
        for prop_info in properties_data:
            image_key = prop_info.pop('image_key')
            prop = Property.objects.create(agent=agent, **prop_info)
            
            # Associate image
            image_rel_path = copied_images.get(image_key)
            if image_rel_path:
                PropertyImage.objects.create(
                    property=prop,
                    image=image_rel_path,
                    is_primary=True,
                    auto_tags={"location": prop.city, "bedrooms": prop.bedrooms, "type": prop.property_type}
                )
                self.stdout.write(self.style.SUCCESS(f"Created Property '{prop.title}' in {prop.city} with image."))
            else:
                self.stdout.write(self.style.WARNING(f"Created Property '{prop.title}' without image."))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
