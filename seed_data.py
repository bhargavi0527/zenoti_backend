#!/usr/bin/env python3
"""
Seed script to populate the database with sample data
"""
import asyncio
import httpx
import json

# Sample data
SAMPLE_CENTERS = [
    {
        "name": "Corporate Training Center",
        "address": "123 Main Street",
        "city": "Mumbai",
        "phone": "+91-22-12345678"
    },
    {
        "name": "Beauty & Wellness Center",
        "address": "456 Park Avenue",
        "city": "Delhi",
        "phone": "+91-11-87654321"
    }
]

SAMPLE_SERVICES = [
    {
        "name": "Face Peel",
        "description": "Glow skin treatment",
        "duration": 40,
        "price": 500.0,
        "category": "Facial"
    },
    {
        "name": "Hair Treatment",
        "description": "Professional hair care",
        "duration": 60,
        "price": 800.0,
        "category": "Hair"
    },
    {
        "name": "Massage Therapy",
        "description": "Relaxing body massage",
        "duration": 90,
        "price": 1200.0,
        "category": "Body"
    },
    {
        "name": "Skin Consultation",
        "description": "Expert skin analysis",
        "duration": 30,
        "price": 300.0,
        "category": "Consultation"
    }
]

async def seed_data():
    """Seed the database with sample data"""
    base_url = "http://127.0.0.1:8000"
    
    async with httpx.AsyncClient() as client:
        print("🌱 Seeding database...")
        
        # Create centers
        centers = []
        for center_data in SAMPLE_CENTERS:
            try:
                response = await client.post(f"{base_url}/centers/", json=center_data)
                if response.status_code == 200:
                    center = response.json()
                    centers.append(center)
                    print(f"✅ Created center: {center['name']}")
                else:
                    print(f"❌ Failed to create center: {center_data['name']}")
            except Exception as e:
                print(f"❌ Error creating center {center_data['name']}: {e}")
        
        # Create services
        services = []
        for service_data in SAMPLE_SERVICES:
            try:
                response = await client.post(f"{base_url}/services/", json=service_data)
                if response.status_code == 200:
                    service = response.json()
                    services.append(service)
                    print(f"✅ Created service: {service['name']}")
                else:
                    print(f"❌ Failed to create service: {service_data['name']}")
            except Exception as e:
                print(f"❌ Error creating service {service_data['name']}: {e}")
        
        # Create providers (doctors)
        if centers:
            provider_data = [
                {
                    "first_name": "Dr Meghana",
                    "last_name": "Komsani",
                    "specialization": "Dermatology",
                    "email": "dr.meghana@example.com",
                    "phone": "+91-9876543210",
                    "center_id": centers[0]["id"]
                },
                {
                    "first_name": "Dr Sanjita",
                    "last_name": "Tripathy",
                    "specialization": "Cosmetology",
                    "email": "dr.sanjita@example.com",
                    "phone": "+91-9876543211",
                    "center_id": centers[0]["id"]
                },
                {
                    "first_name": "Dr Pragathi",
                    "last_name": "Chadalavada",
                    "specialization": "Aesthetics",
                    "email": "dr.pragathi@example.com",
                    "phone": "+91-9876543212",
                    "center_id": centers[0]["id"]
                }
            ]
            
            for provider_data_item in provider_data:
                try:
                    response = await client.post(f"{base_url}/providers/", json=provider_data_item)
                    if response.status_code == 200:
                        provider = response.json()
                        print(f"✅ Created provider: {provider['first_name']} {provider['last_name']}")
                    else:
                        print(f"❌ Failed to create provider: {provider_data_item['first_name']}")
                except Exception as e:
                    print(f"❌ Error creating provider {provider_data_item['first_name']}: {e}")
        
        print("🎉 Seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_data())
