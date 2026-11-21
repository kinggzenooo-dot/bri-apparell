/**
 * BRI APPARELL — Staff Interface Data Store
 * Realistic Philippine Retail Operations Data & LocalStorage Initialization
 */

const INITIAL_STAFF_DATA = {
  user: {
    id: "EMP-0012",
    name: "Alexander Vance",
    email: "alexander.vance@briapparell.com",
    phone: "+63 917 892 4567",
    role: "Retail Operations Staff",
    department: "Retail Operations & Logistics",
    shift: "Day Shift (08:00 AM – 05:00 PM PHT)",
    joinedDate: "January 15, 2025",
    permissions: [
      "orders:view", "orders:process", "products:view",
      "inventory:view", "customers:view", "reviews:view",
      "reviews:flag", "profile:edit"
    ]
  },

  orders: [
    {
      orderId: "BRI-00125",
      customer: {
        id: "CUST-001",
        name: "John Dela Cruz",
        email: "john@email.com",
        phone: "+63 917 123 4567",
        address: "Unit 14A, Grand Residences, Banilad, Cebu City, 6000, Philippines"
      },
      date: "2026-08-24T14:15:00Z",
      status: "Processing",
      statusStep: 3, // 1: Placed, 2: Confirmed, 3: Processing, 4: Packed, 5: Ready to Ship, 6: Shipped, 7: Delivered
      paymentMethod: "GCASH E-WALLET",
      paymentStatus: "Paid",
      subtotal: 3497,
      discount: 200,
      shippingFee: 100,
      total: 3397,
      items: [
        {
          productId: "bri-001",
          sku: "BRI-OS-001-BLK-M",
          name: "Essential Oversized Heavyweight Tee",
          variant: "Pitch Black",
          size: "M",
          quantity: 2,
          price: 1195,
          total: 2390
        },
        {
          productId: "bri-003",
          sku: "BRI-TR-003-SMK-M",
          name: "Everyday Pleated Wide-Leg Trousers",
          variant: "Smoke Charcoal",
          size: "M",
          quantity: 1,
          price: 2195,
          total: 2195
        }
      ],
      notes: "Please pack with extra tissue paper. Gift order.",
      trackingNumber: null,
      courier: "LBC Express",
      history: [
        { time: "2026-08-24T14:15:00Z", event: "Order placed by customer online", staff: "System" },
        { time: "2026-08-24T14:30:00Z", event: "Payment verified via GCash gateway", staff: "System" },
        { time: "2026-08-24T15:00:00Z", event: "Order confirmed and moved to processing", staff: "Alexander Vance" }
      ]
    },
    {
      orderId: "BRI-00124",
      customer: {
        id: "CUST-002",
        name: "Maria Santos",
        email: "maria.santos@email.com",
        phone: "+63 918 234 5678",
        address: "74 Scout Rallos St., Diliman, Quezon City, Metro Manila, 1103"
      },
      date: "2026-08-24T13:40:00Z",
      status: "Pending",
      statusStep: 1,
      paymentMethod: "CASH ON DELIVERY",
      paymentStatus: "Pending",
      subtotal: 1899,
      discount: 0,
      shippingFee: 0,
      total: 1899,
      items: [
        {
          productId: "bri-012",
          sku: "BRI-SH-012-BLK-M",
          name: "Everyday Relaxed Heavyweight Shorts",
          variant: "Ink Black",
          size: "M",
          quantity: 1,
          price: 1495,
          total: 1495
        }
      ],
      notes: "Call upon arrival at guardhouse.",
      trackingNumber: null,
      courier: "J&T Express",
      history: [
        { time: "2026-08-24T13:40:00Z", event: "Order placed by customer via COD", staff: "System" }
      ]
    },
    {
      orderId: "BRI-00123",
      customer: {
        id: "CUST-004",
        name: "Ana Reyes",
        email: "ana.reyes@email.com",
        phone: "+63 920 456 7890",
        address: "Tower 2, McKinley Hill, Fort Bonifacio, Taguig, 1634"
      },
      date: "2026-08-24T11:20:00Z",
      status: "Ready to Ship",
      statusStep: 5,
      paymentMethod: "CREDIT CARD",
      paymentStatus: "Paid",
      subtotal: 1295,
      discount: 100,
      shippingFee: 0,
      total: 1195,
      items: [
        {
          productId: "bri-011",
          sku: "BRI-CP-011-BLK-OS",
          name: "Monochrome Low-Profile Minimalist Cap",
          variant: "Washed Black",
          size: "One Size",
          quantity: 1,
          price: 1195,
          total: 1195
        }
      ],
      notes: "",
      trackingNumber: "BRI-EXP-890214",
      courier: "Ninja Van",
      history: [
        { time: "2026-08-24T11:20:00Z", event: "Order placed online", staff: "System" },
        { time: "2026-08-24T11:30:00Z", event: "Order confirmed", staff: "Alexander Vance" },
        { time: "2026-08-24T12:00:00Z", event: "Items picked and packed in signature pouch", staff: "Alexander Vance" },
        { time: "2026-08-24T12:30:00Z", event: "Manifest generated, awaiting courier pickup", staff: "Alexander Vance" }
      ]
    },
    {
      orderId: "BRI-00122",
      customer: {
        id: "CUST-003",
        name: "Carlos Mendoza",
        email: "carlos.m@email.com",
        phone: "+63 919 345 6789",
        address: "32B Ayala Avenue, Bel-Air, Makati City, 1209"
      },
      date: "2026-08-23T16:10:00Z",
      status: "Packed",
      statusStep: 4,
      paymentMethod: "MAYA E-WALLET",
      paymentStatus: "Paid",
      subtotal: 4995,
      discount: 500,
      shippingFee: 0,
      total: 4495,
      items: [
        {
          productId: "bri-007",
          sku: "BRI-BL-007-BLK-M",
          name: "Minimalist Single-Breasted Tailored Blazer",
          variant: "Midnight Black",
          size: "M",
          quantity: 1,
          price: 3995,
          total: 3995
        }
      ],
      notes: "Garment bag included.",
      trackingNumber: null,
      courier: "LBC Express",
      history: [
        { time: "2026-08-23T16:10:00Z", event: "Order placed", staff: "System" },
        { time: "2026-08-23T16:25:00Z", event: "Order confirmed", staff: "Alexander Vance" },
        { time: "2026-08-24T09:15:00Z", event: "Suit bag pressed & packed", staff: "Alexander Vance" }
      ]
    },
    {
      orderId: "BRI-00121",
      customer: {
        id: "CUST-006",
        name: "Elena Gomez",
        email: "elena.g@email.com",
        phone: "+63 922 678 9012",
        address: "Penthouse 1, Malate Bayview, Manila, 1004"
      },
      date: "2026-08-23T14:30:00Z",
      status: "Confirmed",
      statusStep: 2,
      paymentMethod: "CREDIT CARD",
      paymentStatus: "Paid",
      subtotal: 6495,
      discount: 600,
      shippingFee: 0,
      total: 5895,
      items: [
        {
          productId: "bri-013",
          sku: "BRI-CT-013-BLK-M",
          name: "Architectural Double-Breasted Wool Coat",
          variant: "Pure Black",
          size: "M",
          quantity: 1,
          price: 5195,
          total: 5195
        }
      ],
      notes: "Deliver on weekday morning only.",
      trackingNumber: null,
      courier: "LBC Express",
      history: [
        { time: "2026-08-23T14:30:00Z", event: "Order placed", staff: "System" },
        { time: "2026-08-23T15:00:00Z", event: "Stock reserved in warehouse", staff: "Alexander Vance" }
      ]
    },
    {
      orderId: "BRI-00120",
      customer: {
        id: "CUST-005",
        name: "David Lim",
        email: "david.lim@email.com",
        phone: "+63 921 567 8901",
        address: "18 Onyx Road, Ortigas Center, Pasig City, 1605"
      },
      date: "2026-08-23T09:15:00Z",
      status: "Shipped",
      statusStep: 6,
      paymentMethod: "GCASH E-WALLET",
      paymentStatus: "Paid",
      subtotal: 2195,
      discount: 0,
      shippingFee: 150,
      total: 2345,
      items: [
        {
          productId: "bri-005",
          sku: "BRI-CS-005-WHT-L",
          name: "Architectural Relaxed Camp Collar Shirt",
          variant: "Chalk White",
          size: "L",
          quantity: 1,
          price: 1795,
          total: 1795
        }
      ],
      notes: "",
      trackingNumber: "NINJA-PH-9921401",
      courier: "Ninja Van",
      history: [
        { time: "2026-08-23T09:15:00Z", event: "Order placed & paid", staff: "System" },
        { time: "2026-08-23T10:00:00Z", event: "Order packed", staff: "Alexander Vance" },
        { time: "2026-08-23T14:00:00Z", event: "Handed over to courier driver", staff: "Alexander Vance" }
      ]
    },
    {
      orderId: "BRI-00119",
      customer: {
        id: "CUST-001",
        name: "John Dela Cruz",
        email: "john@email.com",
        phone: "+63 917 123 4567",
        address: "Unit 14A, Grand Residences, Banilad, Cebu City, 6000"
      },
      date: "2026-08-22T10:00:00Z",
      status: "Delivered",
      statusStep: 7,
      paymentMethod: "CREDIT CARD",
      paymentStatus: "Paid",
      subtotal: 3190,
      discount: 0,
      shippingFee: 0,
      total: 3190,
      items: [
        {
          productId: "bri-001",
          sku: "BRI-OS-001-WHT-L",
          name: "Essential Oversized Heavyweight Tee",
          variant: "Chalk Off-White",
          size: "L",
          quantity: 2,
          price: 1195,
          total: 2390
        }
      ],
      notes: "",
      trackingNumber: "LBC-CEB-7890123",
      courier: "LBC Express",
      history: [
        { time: "2026-08-22T10:00:00Z", event: "Order completed", staff: "System" },
        { time: "2026-08-24T10:30:00Z", event: "Package signed and received by customer", staff: "Courier API" }
      ]
    }
  ],

  inventoryVariants: [
    {
      id: "var-001",
      productId: "bri-001",
      name: "Essential Oversized Heavyweight Tee",
      sku: "BRI-OS-001-BLK-M",
      category: "Tops",
      color: "Pitch Black",
      size: "M",
      stock: 2,
      threshold: 5,
      status: "Low Stock",
      location: "Rack A-01"
    },
    {
      id: "var-002",
      productId: "bri-001",
      name: "Essential Oversized Heavyweight Tee",
      sku: "BRI-OS-001-BLK-L",
      category: "Tops",
      color: "Pitch Black",
      size: "L",
      stock: 18,
      threshold: 5,
      status: "In Stock",
      location: "Rack A-01"
    },
    {
      id: "var-003",
      productId: "bri-001",
      name: "Essential Oversized Heavyweight Tee",
      sku: "BRI-OS-001-WHT-M",
      category: "Tops",
      color: "Chalk Off-White",
      size: "M",
      stock: 0,
      threshold: 5,
      status: "Out of Stock",
      location: "Rack A-02"
    },
    {
      id: "var-004",
      productId: "bri-006",
      name: "Technical Utility Relaxed Cargo Pants",
      sku: "BRI-CP-006-BLK-L",
      category: "Bottoms",
      color: "Stealth Black",
      size: "L",
      stock: 1,
      threshold: 5,
      status: "Low Stock",
      location: "Rack B-04"
    },
    {
      id: "var-005",
      productId: "bri-004",
      name: "Signature French Terry Heavyweight Hoodie",
      sku: "BRI-HD-004-BLK-XL",
      category: "Outerwear",
      color: "Void Black",
      size: "XL",
      stock: 3,
      threshold: 5,
      status: "Low Stock",
      location: "Rack C-02"
    },
    {
      id: "var-006",
      productId: "bri-005",
      name: "Architectural Relaxed Camp Collar Shirt",
      sku: "BRI-CS-005-WHT-S",
      category: "Tops",
      color: "Chalk White",
      size: "S",
      stock: 2,
      threshold: 5,
      status: "Low Stock",
      location: "Rack A-05"
    },
    {
      id: "var-007",
      productId: "bri-002",
      name: "Minimalist Structured Boxy Overshirt",
      sku: "BRI-OS-002-BLK-L",
      category: "Outerwear",
      color: "Matte Black",
      size: "L",
      stock: 24,
      threshold: 5,
      status: "In Stock",
      location: "Rack C-01"
    },
    {
      id: "var-008",
      productId: "bri-003",
      name: "Everyday Pleated Wide-Leg Trousers",
      sku: "BRI-TR-003-SMK-M",
      category: "Bottoms",
      color: "Smoke Charcoal",
      size: "M",
      stock: 14,
      threshold: 5,
      status: "In Stock",
      location: "Rack B-02"
    },
    {
      id: "var-009",
      productId: "bri-007",
      name: "Minimalist Single-Breasted Tailored Blazer",
      sku: "BRI-BL-007-BLK-M",
      category: "Outerwear",
      color: "Midnight Black",
      size: "M",
      stock: 9,
      threshold: 5,
      status: "In Stock",
      location: "Rack C-05"
    },
    {
      id: "var-010",
      productId: "bri-009",
      name: "Minimalist Heavy Cotton Canvas Tote",
      sku: "BRI-AC-009-ECR-OS",
      category: "Accessories",
      color: "Raw Ecru",
      size: "One Size",
      stock: 35,
      threshold: 5,
      status: "In Stock",
      location: "Rack D-01"
    }
  ],

  stockHistory: [
    {
      id: "STK-LOG-1042",
      date: "2026-08-24T14:15:00Z",
      productName: "Essential Oversized Heavyweight Tee",
      sku: "BRI-OS-001-BLK-M",
      variant: "Pitch Black / M",
      action: "SALE",
      quantity: -2,
      reason: "Customer Online Order",
      reference: "BRI-00125",
      staff: "Alexander Vance"
    },
    {
      id: "STK-LOG-1041",
      date: "2026-08-24T11:30:00Z",
      productName: "Technical Utility Cargo Pants",
      sku: "BRI-CP-006-BLK-L",
      variant: "Stealth Black / L",
      action: "SALE",
      quantity: -1,
      reason: "Customer Online Order",
      reference: "BRI-00122",
      staff: "Alexander Vance"
    },
    {
      id: "STK-LOG-1040",
      date: "2026-08-23T16:00:00Z",
      productName: "Basic Crewneck Tee",
      sku: "BRI-BT-001-WHT-M",
      variant: "Chalk Off-White / M",
      action: "RESTOCK",
      quantity: 20,
      reason: "Batch Receipt from Atelier",
      reference: "RESTOCK-108",
      staff: "Inventory Manager"
    },
    {
      id: "STK-LOG-1039",
      date: "2026-08-23T10:20:00Z",
      productName: "Signature French Terry Hoodie",
      sku: "BRI-HD-004-BLK-XL",
      variant: "Void Black / XL",
      action: "ADJUSTMENT",
      quantity: -1,
      reason: "Damaged Fabric Discard",
      reference: "ADJ-009",
      staff: "Alexander Vance"
    },
    {
      id: "STK-LOG-1038",
      date: "2026-08-22T09:00:00Z",
      productName: "Pleated Wide-Leg Trousers",
      sku: "BRI-TR-003-SMK-M",
      variant: "Smoke Charcoal / M",
      action: "RESTOCK",
      quantity: 15,
      reason: "Scheduled Restock",
      reference: "RESTOCK-107",
      staff: "Inventory Manager"
    }
  ],

  customers: [
    {
      id: "CUST-001",
      name: "John Dela Cruz",
      email: "john@email.com",
      phone: "+63 917 123 4567",
      address: "Unit 14A, Grand Residences, Banilad, Cebu City, 6000",
      ordersCount: 8,
      totalSpent: 12450,
      lastOrderDate: "2026-08-24T14:15:00Z",
      status: "Active",
      preferredSize: "M",
      notes: "Prefers oversized fit, VIP repeat client."
    },
    {
      id: "CUST-002",
      name: "Maria Santos",
      email: "maria.santos@email.com",
      phone: "+63 918 234 5678",
      address: "74 Scout Rallos St., Diliman, Quezon City, 1103",
      ordersCount: 4,
      totalSpent: 6890,
      lastOrderDate: "2026-08-24T13:40:00Z",
      status: "Active",
      preferredSize: "S",
      notes: "COD verified customer."
    },
    {
      id: "CUST-003",
      name: "Carlos Mendoza",
      email: "carlos.m@email.com",
      phone: "+63 919 345 6789",
      address: "32B Ayala Avenue, Bel-Air, Makati City, 1209",
      ordersCount: 6,
      totalSpent: 14280,
      lastOrderDate: "2026-08-23T16:10:00Z",
      status: "Active",
      preferredSize: "L",
      notes: "Tailoring customer."
    },
    {
      id: "CUST-004",
      name: "Ana Reyes",
      email: "ana.reyes@email.com",
      phone: "+63 920 456 7890",
      address: "Tower 2, McKinley Hill, Fort Bonifacio, Taguig, 1634",
      ordersCount: 2,
      totalSpent: 2490,
      lastOrderDate: "2026-08-24T11:20:00Z",
      status: "Active",
      preferredSize: "S",
      notes: ""
    },
    {
      id: "CUST-005",
      name: "David Lim",
      email: "david.lim@email.com",
      phone: "+63 921 567 8901",
      address: "18 Onyx Road, Ortigas Center, Pasig City, 1605",
      ordersCount: 5,
      totalSpent: 9850,
      lastOrderDate: "2026-08-23T09:15:00Z",
      status: "Active",
      preferredSize: "L",
      notes: ""
    },
    {
      id: "CUST-006",
      name: "Elena Gomez",
      email: "elena.g@email.com",
      phone: "+63 922 678 9012",
      address: "Penthouse 1, Malate Bayview, Manila, 1004",
      ordersCount: 3,
      totalSpent: 8190,
      lastOrderDate: "2026-08-23T14:30:00Z",
      status: "Active",
      preferredSize: "M",
      notes: "Outerwear capsule collector."
    }
  ],

  reviews: [
    {
      id: "REV-001",
      customerName: "John Dela Cruz",
      productName: "Essential Oversized Heavyweight Tee",
      productId: "bri-001",
      rating: 5,
      date: "2026-08-24T10:00:00Z",
      comment: "The 280 GSM weight is extraordinary. Drapes exactly like luxury Japanese minimal labels. Collar stays crisp after 5 washes.",
      status: "Published",
      verifiedPurchase: true
    },
    {
      id: "REV-002",
      customerName: "Maria Santos",
      productName: "Everyday Pleated Wide-Leg Trousers",
      productId: "bri-003",
      rating: 5,
      date: "2026-08-23T18:20:00Z",
      comment: "Perfect drape over my loafers. Elastic back waistband makes it comfortable for full workdays in the studio.",
      status: "Published",
      verifiedPurchase: true
    },
    {
      id: "REV-003",
      customerName: "Carlos Mendoza",
      productName: "Minimalist Single-Breasted Tailored Blazer",
      productId: "bri-007",
      rating: 5,
      date: "2026-08-22T14:15:00Z",
      comment: "Impeccable unstructured shoulders and subtle horn buttons. Worth every peso.",
      status: "Published",
      verifiedPurchase: true
    },
    {
      id: "REV-004",
      customerName: "Guest Reviewer",
      productName: "Technical Utility Relaxed Cargo Pants",
      productId: "bri-006",
      rating: 1,
      date: "2026-08-24T08:10:00Z",
      comment: "Spam link promo visit external site www.example-scam.com for cheap clothes.",
      status: "Under Review",
      verifiedPurchase: false
    }
  ],

  notifications: [
    {
      id: "NOTIF-001",
      type: "order",
      title: "NEW ORDER RECEIVED",
      message: "Order #BRI-00125 from John Dela Cruz is ready for processing.",
      timestamp: "2026-08-24T14:15:00Z",
      read: false,
      link: "order-details.html?id=BRI-00125"
    },
    {
      id: "NOTIF-002",
      type: "stock",
      title: "CRITICAL LOW STOCK ALERT",
      message: "Cargo Pants — Stealth Black / L has only 1 unit remaining in Rack B-04.",
      timestamp: "2026-08-24T13:00:00Z",
      read: false,
      link: "low-stock.html"
    },
    {
      id: "NOTIF-003",
      type: "stock",
      title: "OUT OF STOCK ALERT",
      message: "Essential Heavyweight Tee — Chalk Off-White / M is completely depleted.",
      timestamp: "2026-08-24T11:45:00Z",
      read: false,
      link: "low-stock.html"
    },
    {
      id: "NOTIF-004",
      type: "system",
      title: "SHIFT SCHEDULE LOGGED",
      message: "Your day shift for August 24, 2026 has been marked active.",
      timestamp: "2026-08-24T08:00:00Z",
      read: true,
      link: "profile.html"
    }
  ]
};
