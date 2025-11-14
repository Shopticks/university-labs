# Medicines sales company

50 classes, 150 fields, 100 unique behaviours (transfer of money from one card to another, verification of the correct password, etc.), the code must include 30 examples of class associations (inclusion of one class in another as a field or method parameters) the code must include 12 personal exceptions

## Project tree:
.\
├── docs\
│ ├── make.bat\
│ ├── Makefile\
│ └── source\
│     ├── conf.py\
│     └── index.rst\
├── pyproject.toml\
├── README.md\
├── src\
│ └── pharmacy_distribution\
│     ├── __init__.py\
│     ├── cli\
│     │ ├── __init__.py\
│     │ ├── demo_scenarios.py\
│     │ └── main.py\
│     ├── config.py\
│     ├── domain\
│     │ ├── __init__.py\
│     │ ├── compliance\
│     │ │ ├── __init__.py\
│     │ │ ├── audit_log.py\
│     │ │ ├── prescription.py\
│     │ │ └── restriction.py\
│     │ ├── customer\
│     │ │ ├── __init__.py\
│     │ │ ├── contact.py\
│     │ │ ├── customer.py\
│     │ │ ├── loyalty.py\
│     │ │ └── segment.py\
│     │ ├── finance\
│     │ │ ├── __init__.py\
│     │ │ ├── account.py\
│     │ │ ├── card.py\
│     │ │ ├── payment.py\
│     │ │ ├── refund.py\
│     │ │ └── transaction.py\
│     │ ├── hr\
│     │ │ ├── __init__.py\
│     │ │ ├── employee.py\
│     │ │ ├── permission.py\
│     │ │ ├── role.py\
│     │ │ └── shift.py\
│     │ ├── inventory\
│     │ │ ├── __init__.py\
│     │ │ ├── inventory_audit.py\
│     │ │ ├── stock_item.py\
│     │ │ ├── stock_movement.py\
│     │ │ └── warehouse.py\
│     │ ├── logistics\
│     │ │ ├── __init__.py\
│     │ │ ├── employee.py\
│     │ │ ├── permission.py\
│     │ │ ├── role.py\
│     │ │ └── shift.py\
│     │ ├── product\
│     │ │ ├── __init__.py\
│     │ │ ├── category.py\
│     │ │ ├── dosage_form.py\
│     │ │ ├── manufacturer.py\
│     │ │ ├── medicine.py\
│     │ │ └── registry.py\
│     │ └── sales\
│     │     ├── __init__.py\
│     │     ├── discount.py\
│     │     ├── invoice.py\
│     │     ├── order_item.py\
│     │     └── order.py\
│     ├── exceptions.py\
│     ├── services\
│     │ ├── __init__.py\
│     │ ├── inventory_service.py\
│     │ ├── notification_service.py\
│     │ ├── order_service.py\
│     │ ├── payment_service.py\
│     │ └── reporting_service.py\
│     └── utils\
│         └── validator.py\
├── task.md\
└── tests\
    ├── __init__.py\
    ├── test_compliance_domain.py\
    ├── test_customer_domain.py\
    ├── test_example.py\
    ├── test_finance_domain.py\
    ├── test_hr_domain.py\
    ├── test_inventory_domain.py\
    ├── test_logistics_domain.py\
    ├── test_product_domain.py\
    ├── test_sales_domain.py\
    └── test_services.py\

18 directories, 73 files