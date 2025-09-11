# Zenoti Backend - Database Tables Documentation

This document provides a comprehensive overview of all database tables, their functionalities, and relationships in the Zenoti backend system.

## Table of Contents
1. [Core Business Tables](#core-business-tables)
2. [User Management Tables](#user-management-tables)
3. [Service & Product Tables](#service--product-tables)
4. [Financial Tables](#financial-tables)
5. [Infrastructure Tables](#infrastructure-tables)
6. [Table Relationships](#table-relationships)
7. [Business Workflows](#business-workflows)

---

## Core Business Tables

### 1. Centers (`centers`)
**Purpose**: Manages spa/wellness center locations and information.

**Key Fields**:
- `id` (UUID, Primary Key)
- `name` (String) - Center name
- `code` (String, Unique) - Center code
- `address`, `city`, `state`, `country` - Location details
- `phone`, `contact_info_phone`, `contact_info_email` - Contact information
- `display_name` - Display name for UI

**Functionality**:
- Central hub for all center-related operations
- Links to guests, providers, and appointments
- Manages center-specific configurations

**Relationships**:
- One-to-many with `guests`
- One-to-many with `providers`
- One-to-many with `appointments`
- One-to-many with `packages`

### 2. Guests (`guests`)
**Purpose**: Customer/client management system.

**Key Fields**:
- `id` (UUID, Primary Key)
- `guest_code` (String, Unique) - Auto-generated guest identifier
- `center_id` (UUID, Foreign Key) - Associated center
- `username` (String, Unique) - Login username
- `first_name`, `middle_name`, `last_name` - Personal details
- `email` (String, Unique) - Contact email
- `phone_no`, `home_no` - Contact numbers
- `gender`, `date_of_birth` - Demographics
- `is_minor` (Boolean) - Age verification
- `nationality`, `language` - Additional info

**Functionality**:
- Customer registration and profile management
- Guest code generation for easy identification
- Center association for multi-location support
- Appointment and invoice tracking

**Relationships**:
- Many-to-one with `centers`
- One-to-many with `appointments`
- One-to-many with `invoices`

### 3. Appointments (`appointments`)
**Purpose**: Booking and scheduling system.

**Key Fields**:
- `id` (UUID, Primary Key)
- `center_id`, `provider_id`, `service_id`, `guest_id` (UUID, Foreign Keys)
- `status` (String) - Appointment status
- `scheduled_time` (DateTime) - Appointment time
- `appointment_date` (Date) - Appointment date
- `notes` (Text) - Additional notes

**Functionality**:
- Core booking system
- Links guests with services and providers
- Status tracking throughout appointment lifecycle
- Auto-creates associated `Sale` record

**Relationships**:
- Many-to-one with `centers`
- Many-to-one with `guests`
- Many-to-one with `providers`
- Many-to-one with `services`
- One-to-one with `sales`

### 4. Providers (`providers`)
**Purpose**: Service provider/staff management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `first_name`, `last_name` - Provider name
- `specialization` (String) - Service specialization
- `email` (String, Unique) - Contact email
- `phone` (String) - Contact number
- `center_id` (UUID, Foreign Key) - Associated center

**Functionality**:
- Staff and service provider management
- Specialization tracking
- Center association
- Appointment scheduling

**Relationships**:
- Many-to-one with `centers`
- One-to-many with `appointments`

---

## User Management Tables

### 5. Users (`users`)
**Purpose**: System user authentication and management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `first_name`, `last_name` - User name
- `email` (String, Unique) - Login email
- `phone_number` (String, Unique) - Contact number
- `password` (String) - Hashed password
- `created_at`, `updated_at` (DateTime) - Timestamps

**Functionality**:
- System authentication
- User profile management
- Password hashing (bcrypt)
- Access control foundation

### 6. Employees (`employees`)
**Purpose**: Internal staff management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `employee_code` (String, Unique) - Employee identifier
- `name` (String) - Employee name
- `job_code`, `designation`, `department` - Job details
- `email`, `phone` - Contact information
- `center_code`, `zone` - Location details
- `is_active` (Boolean) - Employment status

**Functionality**:
- Internal staff tracking
- Department and role management
- Center and zone assignment
- Collection and invoice processing

**Relationships**:
- One-to-many with `collections`

---

## Service & Product Tables

### 7. Services (`services`)
**Purpose**: Service catalog management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `service_code` (String, Unique) - Auto-generated service code
- `name` (String) - Service name
- `description` (String) - Service description
- `duration` (Integer) - Duration in minutes
- `price` (Float) - Service price
- `category` (String) - Service category

**Functionality**:
- Service catalog management
- Pricing and duration tracking
- Appointment booking
- Sale item reference

**Relationships**:
- One-to-many with `appointments`
- Referenced in `sales` via `item_id`

### 8. Products (`products`)
**Purpose**: Product inventory management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `code` (String, Unique) - Product code
- `name` (String) - Product name
- `color`, `size`, `brand` - Product attributes
- `category`, `subcategory` - Classification
- `business_unit` (String) - Business unit
- `sale_price`, `mrp` (Float) - Pricing
- `amount` (Integer) - Stock quantity
- `status` (String) - Availability status

**Functionality**:
- Product catalog management
- Inventory tracking
- Pricing management
- Sale item reference

**Relationships**:
- Referenced in `sales` via `item_id`

### 9. Packages (`packages`)
**Purpose**: Service package management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `code` (String, Unique) - Package code
- `name` (String) - Package name
- `description` (Text) - Package description
- `type` (String) - Package type
- `category_id`, `business_unit_id` (UUID, Foreign Keys)
- `center_id` (UUID, Foreign Key)
- `time` (Integer) - Package duration
- `booking_start_date`, `booking_end_date` - Validity period
- `commission_eligible` (Boolean) - Commission settings
- `commission_factor`, `commission_value` - Commission details

**Functionality**:
- Package creation and management
- Commission tracking
- Validity period management
- Sale item reference

**Relationships**:
- Many-to-one with `categories`
- Many-to-one with `business_units`
- Many-to-one with `centers`
- Referenced in `sales` via `item_id`

### 10. Categories (`categories`)
**Purpose**: Product/service categorization.

**Key Fields**:
- `id` (UUID, Primary Key)
- `name` (String, Unique) - Category name
- `description` (Text) - Category description
- `is_active` (Boolean) - Category status

**Functionality**:
- Classification system
- Package organization
- Business logic grouping

**Relationships**:
- One-to-many with `packages`

### 11. Business Units (`business_unit`)
**Purpose**: Business unit management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `code` (String, Unique) - Business unit code
- `name` (String) - Business unit name
- `description` (Text) - Description
- `is_active` (Boolean) - Status

**Functionality**:
- Organizational structure
- Package classification
- Business logic separation

**Relationships**:
- One-to-many with `packages`

---

## Financial Tables

### 12. Sales (`sales`)
**Purpose**: Core sales transaction management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `sale_no` (String, Unique) - Auto-generated sale number
- `gross_value` (Float) - Original amount
- `discount_value` (Float) - Applied discount
- `net_value` (Float) - Final amount after discount
- `appointment_id` (UUID, Foreign Key) - Associated appointment
- `discount_id` (UUID, Foreign Key) - Applied discount/offer
- `remarks` (String) - Additional notes
- `sale_date` (DateTime) - Sale timestamp

**Functionality**:
- Sales transaction recording
- Discount application
- Value calculations
- Invoice generation trigger

**Relationships**:
- One-to-one with `appointments`
- One-to-one with `invoices`
- Many-to-one with `offers_discounts`
- One-to-many with `collections`

### 13. Invoices (`invoices`)
**Purpose**: Invoice generation and management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `invoice_no` (String, Unique) - Invoice number
- `receipt_no`, `payment_no` (String) - Payment references
- `zone`, `center_code`, `center` - Location details
- `invoice_center_code`, `invoice_center` - Invoice center
- `invoice_date`, `invoice_date_full` - Invoice dates
- `total_collection` (Float) - Total collected amount
- `gross_invoice_value` (Float) - Gross amount
- `invoice_discount` (Float) - Total discount
- `net_invoice_value` (Float) - Net amount
- `sale_id` (UUID, Foreign Key) - Associated sale
- `guest_id` (UUID, Foreign Key) - Customer
- `employee_id` (UUID, Foreign Key) - Processing employee

**Functionality**:
- Invoice generation from sales
- Payment tracking
- Financial reporting
- Collection management

**Relationships**:
- One-to-one with `sales`
- Many-to-one with `guests`
- Many-to-one with `employees`
- One-to-many with `invoice_items`
- One-to-many with `invoice_payments`
- One-to-many with `collections`

### 14. Invoice Items (`invoice_items`)
**Purpose**: Line items for invoices.

**Key Fields**:
- `id` (UUID, Primary Key)
- `item_type` (String) - Service/Product/Package
- `item_code`, `item_name` - Item details
- `item_tags`, `business_unit`, `category`, `sub_category` - Classification
- `item_quantity` (Integer) - Quantity
- `unit_price` (Float) - Unit price
- `item_discount` (Float) - Item-level discount
- `net_price` (Float) - Final price
- `row_num`, `item_row_num` (Integer) - Display order
- `invoice_id` (UUID, Foreign Key) - Parent invoice

**Functionality**:
- Detailed invoice line items
- Item-level pricing and discounts
- Invoice breakdown
- Reporting and analytics

**Relationships**:
- Many-to-one with `invoices`

### 15. Invoice Payments (`invoice_payments`)
**Purpose**: Payment tracking for invoices.

**Key Fields**:
- `id` (UUID, Primary Key)
- `payment_method` (String) - Cash/Card/UPI/Gift Card
- `amount` (Float) - Payment amount
- `transaction_no` (String) - Transaction reference
- `reference_no` (String) - Additional reference
- `remarks` (String) - Payment notes
- `created_at` (DateTime) - Payment timestamp
- `invoice_id` (UUID, Foreign Key) - Parent invoice

**Functionality**:
- Payment method tracking
- Transaction reference management
- Payment history
- Financial reconciliation

**Relationships**:
- Many-to-one with `invoices`

### 16. Collections (`collections`)
**Purpose**: Collection/receipt management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `collection_no` (String, Unique) - Auto-generated collection number
- `payment_method` (String) - Payment method
- `amount` (Float) - Collection amount
- `transaction_no` (String) - Transaction reference
- `reference_no` (String) - Additional reference
- `remarks` (String) - Collection notes
- `created_at` (DateTime) - Collection timestamp
- `sale_id` (UUID, Foreign Key) - Associated sale
- `employee_id` (UUID, Foreign Key) - Processing employee
- `invoice_id` (UUID, Foreign Key) - Associated invoice

**Functionality**:
- Collection recording
- Payment method tracking
- Receipt generation
- Financial reconciliation

**Relationships**:
- Many-to-one with `sales`
- Many-to-one with `invoices`
- Many-to-one with `employees`

### 17. Offers & Discounts (`offers_discounts`)
**Purpose**: Discount and promotional offer management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `item_type` (String) - Product/Service/Package
- `item_id` (UUID) - Target item ID
- `discount_type` (Enum) - Fixed/Percentage
- `discount_value` (Float) - Discount amount or percentage
- `description` (String) - Offer description
- `created_at`, `updated_at` (DateTime) - Timestamps

**Functionality**:
- Discount creation and management
- Item-specific offers
- Flexible discount types
- Sale integration

**Relationships**:
- One-to-many with `sales`

---

## Infrastructure Tables

### 18. Rooms (`rooms`)
**Purpose**: Room and facility management.

**Key Fields**:
- `id` (UUID, Primary Key)
- `code` (String) - Room code
- `name` (String) - Room name
- `room_category_id` (UUID, Foreign Key) - Room category
- `description` (String) - Room description
- `capacity` (Integer) - Room capacity
- `only_one_appointment` (Boolean) - Single appointment policy
- `can_exceed_capacity` (Boolean) - Capacity override
- `center_id` (UUID, Foreign Key) - Associated center
- `is_active` (Boolean) - Room status
- `dq_check_remark` (String) - Quality check notes

**Functionality**:
- Room availability management
- Capacity planning
- Appointment scheduling
- Facility management

**Relationships**:
- Many-to-one with `room_categories`
- Many-to-one with `centers`

### 19. Room Categories (`room_categories`)
**Purpose**: Room type classification.

**Key Fields**:
- `id` (UUID, Primary Key)
- `name` (String) - Category name
- `description` (String) - Category description

**Functionality**:
- Room type organization
- Facility classification
- Booking logic

**Relationships**:
- One-to-many with `rooms`

---

## Table Relationships

### Primary Relationships

```
Centers (1) ──→ (M) Guests
Centers (1) ──→ (M) Providers
Centers (1) ──→ (M) Appointments
Centers (1) ──→ (M) Packages
Centers (1) ──→ (M) Rooms

Guests (1) ──→ (M) Appointments
Guests (1) ──→ (M) Invoices

Providers (1) ──→ (M) Appointments

Services (1) ──→ (M) Appointments

Appointments (1) ──→ (1) Sales
Sales (1) ──→ (1) Invoices
Sales (1) ──→ (M) Collections

Invoices (1) ──→ (M) Invoice Items
Invoices (1) ──→ (M) Invoice Payments
Invoices (1) ──→ (M) Collections

Categories (1) ──→ (M) Packages
Business Units (1) ──→ (M) Packages

Room Categories (1) ──→ (M) Rooms

Offers & Discounts (1) ──→ (M) Sales

Employees (1) ──→ (M) Collections
```

---

## Business Workflows

### 1. Customer Onboarding
1. **Guest Registration**: Create guest record in `guests` table
2. **Center Assignment**: Link guest to specific center
3. **Profile Setup**: Complete personal and contact information

### 2. Appointment Booking
1. **Service Selection**: Choose from `services` table
2. **Provider Assignment**: Select from `providers` table
3. **Scheduling**: Create `appointment` record
4. **Auto-Sale Creation**: System creates placeholder `sale` record

### 3. Sales Processing
1. **Item Selection**: Choose product/service/package
2. **Discount Application**: Apply `offers_discounts` if applicable
3. **Value Calculation**: Compute gross, discount, and net values
4. **Sale Recording**: Create `sale` record with calculated values

### 4. Invoice Generation
1. **Sale Reference**: Use `sale_id` to create invoice
2. **Invoice Numbering**: Generate unique invoice number
3. **Value Transfer**: Copy net value from sale to invoice
4. **Guest Linking**: Associate invoice with guest

### 5. Payment Processing
1. **Payment Recording**: Create `invoice_payment` record
2. **Collection Tracking**: Record in `collections` table
3. **Reference Management**: Track transaction numbers
4. **Reconciliation**: Update invoice totals

### 6. Financial Reporting
1. **Sales Analysis**: Query `sales` table for revenue
2. **Invoice Tracking**: Monitor `invoices` for outstanding amounts
3. **Collection Reports**: Analyze `collections` for payments
4. **Discount Analysis**: Review `offers_discounts` effectiveness

---

## Key Features

### Auto-Generated Fields
- **Guest Codes**: `GUEST{6-digit-number}`
- **Service Codes**: `SERV{4-digit-number}`
- **Sale Numbers**: `SALE-{8-hex-digits}`
- **Collection Numbers**: Auto-generated with prefixes

### Business Logic
- **Appointment-Sale Link**: One-to-one relationship ensures every appointment has a sale
- **Discount Application**: Flexible fixed/percentage discounts
- **Multi-Center Support**: All entities can be center-specific
- **Audit Trail**: Created/updated timestamps on all records

### Data Integrity
- **Foreign Key Constraints**: Ensure referential integrity
- **Unique Constraints**: Prevent duplicate codes and emails
- **UUID Primary Keys**: Globally unique identifiers
- **Cascade Deletes**: Maintain data consistency

---

This documentation provides a comprehensive overview of the database structure and business logic implemented in the Zenoti backend system. Each table serves a specific purpose in the spa/wellness center management workflow, from customer onboarding to financial reporting.
