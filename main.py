# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import user_controller, guest_controller, appointment_controller, center_controller, \
    service_controller, provider_controller, room_controller, room_category_controller, product_controller, \
    employee_controller, invoice_item_controller, invoice_controller, package_controller, business_unit_controller, \
    category_controller, invoice_payment_controller, sales_controller, collection_controller

app = FastAPI(title="My FastAPI Project")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(user_controller.router)
app.include_router(guest_controller.router)
app.include_router(appointment_controller.router)
app.include_router(center_controller.router)
app.include_router(service_controller.router)
app.include_router(provider_controller.router)
app.include_router(room_controller.router)
app.include_router(room_category_controller.router)
app.include_router(product_controller.router)
app.include_router(employee_controller.router)
app.include_router(invoice_controller.router)
app.include_router(invoice_item_controller.router)
app.include_router(package_controller.router)
app.include_router(business_unit_controller.router)
app.include_router(category_controller.router)
app.include_router(invoice_payment_controller.router)
app.include_router(sales_controller.router)
app.include_router(collection_controller.router)
@app.get("/")
def root():
    return {"message": "Welcome to FastAPI 🚀"}
