/**
 * BRI APPARELL - Product Catalog & Store Data
 * Realistic Philippine Peso (₱) pricing & curated editorial fashion imagery
 */

const PRODUCTS = [
  {
    id: "bri-001",
    name: "Essential Oversized Heavyweight Tee",
    category: "Tops",
    gender: "Unisex",
    price: 1495,
    salePrice: 1195,
    isSale: true,
    isNew: true,
    isFeatured: true,
    rating: 4.9,
    reviewCount: 84,
    collection: "essentials",
    tag: "Best Seller",
    shortDesc: "280 GSM luxury combed cotton with dropped shoulders and a boxy contemporary silhouette.",
    description: "The Essential Oversized Tee is crafted from an ultra-heavyweight 280 GSM combed organic cotton, designed to maintain its structural drape wash after wash. Featuring a ribbed crew collar with reinforced double-needle stitching, dropped shoulders, and a relaxed boxy cut tailored for everyday confidence.",
    materials: "100% Combed Heavyweight Organic Cotton (280 GSM)",
    care: [
      "Machine wash cold inside out with like colors",
      "Do not bleach or tumble dry",
      "Warm iron on reverse side",
      "Dry flat in shade to preserve structural drape"
    ],
    details: [
      "280 GSM heavyweight custom-milled jersey",
      "Double-stitched reinforced collar that will not bacon",
      "Subtle tonal BRI APPARELL embroidery at the left hip",
      "Pre-shrunk fabric to minimize post-wash shrinkage",
      "Ethically crafted in limited batches"
    ],
    colors: [
      { name: "Pitch Black", hex: "#0a0a0a" },
      { name: "Washed Charcoal", hex: "#2b2b2b" },
      { name: "Chalk Off-White", hex: "#f4f3ef" },
      { name: "Muted Olive", hex: "#4b5145" }
    ],
    sizes: [
      { size: "XS", inStock: true },
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true },
      { size: "XL", inStock: true },
      { size: "XXL", inStock: false }
    ],
    images: [
      "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-002",
    name: "Minimalist Structured Boxy Overshirt",
    category: "Outerwear",
    gender: "Men",
    price: 3295,
    salePrice: null,
    isSale: false,
    isNew: true,
    isFeatured: true,
    rating: 5.0,
    reviewCount: 42,
    collection: "essentials",
    tag: "New Arrival",
    shortDesc: "Heavy cotton twill overshirt with clean concealed horn buttons and deep utility patch pockets.",
    description: "An architectural layering staple. The Structured Boxy Overshirt combines crisp tailoring with utilitarian functionality. Cut from a dense 340 GSM Japanese cotton twill with a matte finish, featuring clean concealed front button placket, dual chest pockets, and a clean straight hem.",
    materials: "100% Cotton Milled Twill (340 GSM)",
    care: [
      "Dry clean recommended or delicate machine wash cold",
      "Hang to dry on a wide contoured hanger",
      "Medium steam or iron"
    ],
    details: [
      "Concealed front placket with custom matte horn buttons",
      "Dual architectural chest patch pockets",
      "Square-cut cuff with adjustable button closure",
      "Straight hem designed for elevated layering",
      "Interior French seams throughout"
    ],
    colors: [
      { name: "Matte Black", hex: "#0c0c0c" },
      { name: "Stone Gray", hex: "#8c8b88" },
      { name: "Deep Navy", hex: "#161c28" }
    ],
    sizes: [
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true },
      { size: "XL", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1544441893-675973e31985?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-003",
    name: "Everyday Pleated Wide-Leg Trousers",
    category: "Bottoms",
    gender: "Unisex",
    price: 2695,
    salePrice: 2195,
    isSale: true,
    isNew: false,
    isFeatured: true,
    rating: 4.8,
    reviewCount: 67,
    collection: "essentials",
    tag: "Essential",
    shortDesc: "Double front pleats, elasticated back waistband for comfort, and a relaxed architectural silhouette.",
    description: "Redefining everyday trousers. Designed with deep front pleats that break elegantly over sneakers or loafers. Constructed from a lightweight, fluid poly-viscose blend with natural crease resistance and an internal drawstring elastic waistband for seamless all-day comfort.",
    materials: "68% Polyester, 28% Viscose, 4% Elastane",
    care: [
      "Machine wash delicate cold in laundry bag",
      "Hang dry immediately after washing",
      "Cool iron or steam along pleat lines"
    ],
    details: [
      "Dual sharp front pleats with permanent crease retention",
      "Discreet elastic waistband at back with internal drawstring",
      "Deep slant side pockets and dual welt rear pockets",
      "YKK metal zipper with clean tab button closure",
      "Wide relaxed hem with 2-inch cuff allowance"
    ],
    colors: [
      { name: "Obsidian Black", hex: "#000000" },
      { name: "Smoke Charcoal", hex: "#383838" },
      { name: "Desert Sand", hex: "#c4b59f" }
    ],
    sizes: [
      { size: "XS", inStock: true },
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true },
      { size: "XL", inStock: false }
    ],
    images: [
      "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1509631179647-0177331693ae?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1517445312882-bc9910d016b7?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-004",
    name: "Signature French Terry Heavyweight Hoodie",
    category: "Outerwear",
    gender: "Unisex",
    price: 3495,
    salePrice: null,
    isSale: false,
    isNew: true,
    isFeatured: true,
    rating: 4.9,
    reviewCount: 112,
    collection: "streetwear",
    tag: "Iconic",
    shortDesc: "460 GSM custom looped French terry hoodie with double-layer crossover hood and zero drawstrings.",
    description: "Engineered for maximum substance and structural warmth. The Signature Hoodie is constructed from 460 GSM looped French terry without drawstrings for a sleek minimalist look. Features a spacious double-layer hood, drop shoulders, wide ribbing at cuffs and hem, and a seamless kangaroo pocket.",
    materials: "100% Compact Spun Cotton French Terry (460 GSM)",
    care: [
      "Machine wash cold inside out",
      "Tumble dry low or line dry in shade",
      "Do not dry clean"
    ],
    details: [
      "Ultra-dense 460 GSM custom-knit fabric",
      "Double-lined hood with structured crossover neck",
      "Drawstring-free minimalist design",
      "Heavy 2x2 ribbed spandex waistband and cuffs",
      "Subtle blind-stitched hem BRI APPARELL label"
    ],
    colors: [
      { name: "Void Black", hex: "#080808" },
      { name: "Heather Slate", hex: "#7a7e85" },
      { name: "Vintage Bone", hex: "#eae6df" }
    ],
    sizes: [
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true },
      { size: "XL", inStock: true },
      { size: "XXL", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1509967419530-da38b4704bc6?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-005",
    name: "Architectural Relaxed Camp Collar Shirt",
    category: "Tops",
    gender: "Men",
    price: 2195,
    salePrice: 1795,
    isSale: true,
    isNew: false,
    isFeatured: false,
    rating: 4.7,
    reviewCount: 39,
    collection: "seasonal",
    tag: "Sale",
    shortDesc: "Breathable textured Tencel-linen blend with retro-modern Cuban collar and relaxed drape.",
    description: "The quintessential warm-weather staple. Tailored from a premium breathable Lyocell and Linen weave that drapes softly against the skin. Features a relaxed open camp collar, mother-of-pearl buttons, and a straight hem with subtle side vents.",
    materials: "70% Tencel Lyocell, 30% Belgian Linen",
    care: [
      "Gentle machine wash cold",
      "Line dry in shade",
      "Steam on low to medium heat"
    ],
    details: [
      "Relaxed camp / Cuban collar with loop button",
      "Natural mother-of-pearl engraved buttons",
      "Side hem slits for mobility and un-tucked styling",
      "Silky breathable hand feel with matte texture"
    ],
    colors: [
      { name: "Chalk White", hex: "#f8f8f8" },
      { name: "Onyx Black", hex: "#111111" },
      { name: "Sage Moss", hex: "#5d6a59" }
    ],
    sizes: [
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true },
      { size: "XL", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1589310243389-96a5483213a8?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-006",
    name: "Technical Utility Relaxed Cargo Pants",
    category: "Bottoms",
    gender: "Unisex",
    price: 2995,
    salePrice: null,
    isSale: false,
    isNew: true,
    isFeatured: true,
    rating: 4.9,
    reviewCount: 95,
    collection: "streetwear",
    tag: "Trending",
    shortDesc: "Water-repellent ripstop cotton with magnetic cargo closures and adjustable bungee ankle hems.",
    description: "Form meets technical precision. Crafted from durable cotton-nylon ripstop treated with a DWR water-resistant finish. Features flush low-profile cargo pockets with hidden magnetic snaps, articulated knees, and toggle bungee cords at the hem for versatile straight or tapered styling.",
    materials: "65% Cotton, 35% Nylon Durable Ripstop (220 GSM)",
    care: [
      "Machine wash cold gentle cycle",
      "Fasten all pockets before washing",
      "Tumble dry low or air dry"
    ],
    details: [
      "Low-profile 3D bellowed cargo pockets with magnetic closures",
      "Articulated knee darts for unrestricted movement",
      "Adjustable bungee hem toggles to switch silhouette",
      "Deep front hand pockets with coin pocket and rear flap pockets",
      "Reinforced seat and crotch gusset"
    ],
    colors: [
      { name: "Stealth Black", hex: "#0b0b0b" },
      { name: "Tactical Olive", hex: "#3e4235" },
      { name: "Gunmetal Gray", hex: "#4a4c4e" }
    ],
    sizes: [
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true },
      { size: "XL", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1517445312882-bc9910d016b7?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1542272604-780c96856592?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-007",
    name: "Minimalist Single-Breasted Tailored Blazer",
    category: "Outerwear",
    gender: "Unisex",
    price: 4995,
    salePrice: 3995,
    isSale: true,
    isNew: false,
    isFeatured: true,
    rating: 5.0,
    reviewCount: 31,
    collection: "essentials",
    tag: "Signature Piece",
    shortDesc: "Unstructured tropical wool-blend blazer with notched lapels and fluid modern drape.",
    description: "The centerpiece of modern tailoring. An unstructured, softly tailored blazer crafted from breathable tropical wool and viscose. Clean notch lapels, horn buttons, full cupro lining, and functional interior passport pockets. Built for effortless transition from day to evening.",
    materials: "55% Fine Wool, 42% Polyester, 3% Lycra / 100% Cupro Lining",
    care: [
      "Specialist dry clean only",
      "Use wide padded wooden hanger",
      "Steam lightly to refresh between wears"
    ],
    details: [
      "Soft shoulder construction with minimal padding",
      "Two-button front stance with notched lapels",
      "Double back vents for ease of movement",
      "Functional interior chest and passport pockets",
      "Sleek jetted front waist pockets"
    ],
    colors: [
      { name: "Midnight Black", hex: "#050505" },
      { name: "Deep Charcoal", hex: "#222222" }
    ],
    sizes: [
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true },
      { size: "XL", inStock: false }
    ],
    images: [
      "https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1598808503746-f34c53b9323e?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-008",
    name: "Ribbed Merino Wool Knit Sweater",
    category: "Tops",
    gender: "Women",
    price: 3195,
    salePrice: null,
    isSale: false,
    isNew: true,
    isFeatured: false,
    rating: 4.8,
    reviewCount: 48,
    collection: "seasonal",
    tag: "New",
    shortDesc: "Extra-fine 100% Australian Merino wool knit with mock neck and elongated sleeve cuffs.",
    description: "An extraordinarily soft layer. Spun from 19.5-micron extra-fine Australian Merino wool that is naturally thermoregulating and odor-resistant. Features an elegant mock neck collar, all-over fine ribbing, and extended split cuffs.",
    materials: "100% Extra-Fine Australian Merino Wool",
    care: [
      "Hand wash cold with wool detergent",
      "Do not wring or twist",
      "Dry flat on clean towel away from direct sunlight",
      "Store folded (do not hang)"
    ],
    details: [
      "12-gauge full Milano rib construction",
      "Seamless tubular mock collar",
      "Elongated sleeves with clean knuckle-length cuffs",
      "Zero itch guarantee with ultra-fine fibers"
    ],
    colors: [
      { name: "Ivory Cream", hex: "#f5f3ec" },
      { name: "Raven Black", hex: "#0f0f0f" },
      { name: "Warm Taupe", hex: "#9b8d80" }
    ],
    sizes: [
      { size: "XS", inStock: true },
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1583744946564-b52ac1c389c8?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-009",
    name: "Minimalist Heavy Cotton Canvas Tote",
    category: "Accessories",
    gender: "Unisex",
    price: 1295,
    salePrice: 995,
    isSale: true,
    isNew: false,
    isFeatured: false,
    rating: 4.9,
    reviewCount: 140,
    collection: "essentials",
    tag: "Essential",
    shortDesc: "16oz washed organic cotton canvas with reinforced dual straps and padded laptop compartment.",
    description: "The definitive daily carry. Built from heavy 16oz cotton canvas with reinforced cross-stitching at all stress points. Features a dedicated 15-inch padded laptop sleeve, dual interior slip pockets, a key leash with metal clip, and magnetic top closure.",
    materials: "100% Heavy Organic Cotton Canvas (16oz)",
    care: [
      "Spot clean with mild soap and cold water",
      "Air dry in shade",
      "Do not machine wash or dry clean"
    ],
    details: [
      "Padded interior laptop sleeve (fits up to 16-inch MacBook)",
      "Dual interior organizer pockets and metal key clip",
      "Reinforced box-stitched handles with shoulder and hand drops",
      "Concealed magnetic top button closure",
      "Structured base with internal support panel"
    ],
    colors: [
      { name: "Raw Ecru", hex: "#e8e5dc" },
      { name: "Deep Pitch Black", hex: "#121212" },
      { name: "Faded Olive", hex: "#525749" }
    ],
    sizes: [
      { size: "One Size", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1544816155-12df9643f363?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-010",
    name: "Architectural Cropped Boxy Jacket",
    category: "Outerwear",
    gender: "Women",
    price: 3695,
    salePrice: null,
    isSale: false,
    isNew: true,
    isFeatured: true,
    rating: 4.9,
    reviewCount: 53,
    collection: "seasonal",
    tag: "New",
    shortDesc: "Cropped silhouette in heavy gabardine cotton with exaggerated collar and metal hardware.",
    description: "Modern proportions with clean geometric lines. The Cropped Boxy Jacket features a sharp exaggerated collar, high waistline finish, custom matte gunmetal zip puller, and wide raglan sleeves that allow easy layering.",
    materials: "100% Heavyweight Cotton Gabardine",
    care: [
      "Dry clean or cold hand wash",
      "Hang dry on structured hanger",
      "Cool iron if necessary"
    ],
    details: [
      "Cropped straight hem sitting just above the natural waist",
      "Heavy gauge matte black two-way zipper",
      "Wide articulated cuffs with snap adjusters",
      "Clean internal bound seams with silk tape"
    ],
    colors: [
      { name: "Pitch Black", hex: "#0d0d0d" },
      { name: "Oatmeal Beige", hex: "#d8d3c5" }
    ],
    sizes: [
      { size: "XS", inStock: true },
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1554412933-514a83d2f3c8?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-011",
    name: "Monochrome Low-Profile Minimalist Cap",
    category: "Accessories",
    gender: "Unisex",
    price: 1195,
    salePrice: null,
    isSale: false,
    isNew: false,
    isFeatured: false,
    rating: 4.8,
    reviewCount: 76,
    collection: "streetwear",
    tag: "Essential",
    shortDesc: "Unstructured 6-panel washed cotton cap with understated tonal branding and matte metal buckle.",
    description: "The understated finishing piece. Crafted from enzyme-washed cotton twill for an instant broken-in comfort. Features an unstructured low crown, curved brim, tonal embroidered eyelets, and an adjustable self-fabric strap with an antique matte metal buckle.",
    materials: "100% Washed Cotton Chino Twill",
    care: [
      "Hand wash cold with gentle detergent",
      "Reshape and air dry",
      "Do not machine wash or dry"
    ],
    details: [
      "Unstructured low-profile 6-panel design",
      "Subtle micro tonal BRI APPARELL wordmark at rear",
      "Self-fabric strap with custom matte metal tri-glide slider",
      "Moisture-wicking internal cotton sweatband"
    ],
    colors: [
      { name: "Washed Black", hex: "#1c1c1c" },
      { name: "Chalk Cream", hex: "#e5e2da" },
      { name: "Slate Charcoal", hex: "#3a3d40" }
    ],
    sizes: [
      { size: "One Size", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1575428652377-a2d80e2277fc?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1521369909029-2afed882baee?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-012",
    name: "Everyday Relaxed Heavyweight Shorts",
    category: "Bottoms",
    gender: "Unisex",
    price: 1895,
    salePrice: 1495,
    isSale: true,
    isNew: false,
    isFeatured: false,
    rating: 4.7,
    reviewCount: 62,
    collection: "essentials",
    tag: "Sale",
    shortDesc: "400 GSM unbrushed French terry shorts with thick waistband and custom metal-tipped drawstrings.",
    description: "Lounge or street-ready luxury. Made from 400 GSM loopback cotton with a substantial feel and natural breathability. Designed with a 6.5-inch inseam that hits just above the knee, deep side pockets, and a zippered rear pocket to secure essentials.",
    materials: "100% Ring-Spun Cotton French Terry (400 GSM)",
    care: [
      "Machine wash cold inside out",
      "Tumble dry low or line dry",
      "Warm iron if needed"
    ],
    details: [
      "Substantial 400 GSM loopback cotton",
      "Wide elastic waistband with heavy braided cotton cord",
      "Metal custom engraved drawstring aglets",
      "Discreet zip pocket on rear right hip",
      "6.5-inch modern above-the-knee inseam"
    ],
    colors: [
      { name: "Ink Black", hex: "#0e0e0e" },
      { name: "Cast Iron Grey", hex: "#333333" },
      { name: "Oat Sand", hex: "#d1cbbf" }
    ],
    sizes: [
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true },
      { size: "XL", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1562157873-818bc0726f68?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1509631179647-0177331693ae?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-013",
    name: "Architectural Double-Breasted Wool Coat",
    category: "Outerwear",
    gender: "Unisex",
    price: 6495,
    salePrice: 5195,
    isSale: true,
    isNew: true,
    isFeatured: true,
    rating: 5.0,
    reviewCount: 28,
    collection: "seasonal",
    tag: "Premium",
    shortDesc: "Substantial Melton wool trench silhouette with sharp peak lapels and belted waist.",
    description: "An investment piece of extraordinary refinement. Crafted from a heavyweight 680 GSM Melton wool blend with a smooth matte surface. Features commanding peak lapels, double-breasted 6-button front, removable self-fabric tie belt, and deep welt pockets.",
    materials: "75% Virgin Wool, 25% Polyamide / 100% Cupro Satin Lining",
    care: [
      "Specialist dry clean only",
      "Store on contoured wide wooden coat hanger in garment bag"
    ],
    details: [
      "680 GSM heavy Melton virgin wool",
      "Full satin lining for effortless layering over knitwear",
      "Double-breasted stance with horn button fastenings",
      "Detachable fabric tie belt with belt loops",
      "Single center back storm vent for fluid movement"
    ],
    colors: [
      { name: "Pure Black", hex: "#000000" },
      { name: "Charcoal Heather", hex: "#292929" },
      { name: "Camel", hex: "#a4805c" }
    ],
    sizes: [
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true },
      { size: "XL", inStock: false }
    ],
    images: [
      "https://images.unsplash.com/photo-1544441893-675973e31985?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-014",
    name: "Minimalist Leather Cardholder Wallet",
    category: "Accessories",
    gender: "Unisex",
    price: 1395,
    salePrice: null,
    isSale: false,
    isNew: false,
    isFeatured: false,
    rating: 4.9,
    reviewCount: 89,
    collection: "essentials",
    tag: "Best Seller",
    shortDesc: "Full-grain vegetable-tanned leather with hand-burnished edges and 5 card compartments.",
    description: "Purist pocket luxury. Handcrafted from top-tier full-grain vegetable-tanned leather that develops a rich, unique patina over time. Features 4 exterior card slots and a central pocket for folded cash or receipts, with hand-painted edge finishing.",
    materials: "100% Full-Grain Vegetable-Tanned Italian Leather",
    care: [
      "Wipe with dry microfiber cloth",
      "Apply natural leather balm once every 6 months"
    ],
    details: [
      "4 card slots plus 1 central cash compartment",
      "Ultra-slim 4mm profile",
      "Hand-burnished and painted edge wax finish",
      "Subtle blind-debossed BRI APPARELL logo",
      "Includes microfiber dust pouch and hard-shell gift box"
    ],
    colors: [
      { name: "Nero Black", hex: "#0d0d0d" },
      { name: "Cognac Tan", hex: "#784b28" }
    ],
    sizes: [
      { size: "One Size", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1627123424574-724758594e93?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1590874103328-eac38a683ce7?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-015",
    name: "Contemporary Relaxed Silk-Blend Maxi Dress",
    category: "Women",
    gender: "Women",
    price: 3895,
    salePrice: 3295,
    isSale: true,
    isNew: true,
    isFeatured: true,
    rating: 5.0,
    reviewCount: 41,
    collection: "seasonal",
    tag: "New",
    shortDesc: "High-twist mulberry silk and viscose maxi dress with column silhouette and back slit.",
    description: "Effortless elegance with architectural grace. Cut from a fluid silk-viscose blend that cascades smoothly down the body. Features a minimalist boat neckline, delicate waist darts for soft shaping, and a high center-back walking slit.",
    materials: "35% Mulberry Silk, 65% Lenzing Viscose",
    care: [
      "Dry clean or delicate hand wash cold",
      "Lay flat to dry",
      "Low steam on reverse"
    ],
    details: [
      "Column silhouette with floor-skimming hem",
      "Invisible back zipper with hook-and-eye closure",
      "Center-back walking vent for unrestricted movement",
      "Fully lined in breathable lightweight cupro"
    ],
    colors: [
      { name: "Pure Obsidian", hex: "#050505" },
      { name: "Ivory Silk", hex: "#f5f3ec" }
    ],
    sizes: [
      { size: "XS", inStock: true },
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1554412933-514a83d2f3c8?q=80&w=1000&auto=format&fit=crop"
    ]
  },
  {
    id: "bri-016",
    name: "Classic Supima Cotton Crewneck Tee",
    category: "Tops",
    gender: "Unisex",
    price: 1295,
    salePrice: null,
    isSale: false,
    isNew: false,
    isFeatured: false,
    rating: 4.8,
    reviewCount: 118,
    collection: "essentials",
    tag: "Essential",
    shortDesc: "Extra-long staple American Supima cotton with a regular clean fit and silky soft touch.",
    description: "The fundamental foundation tee. Made exclusively from 100% American-grown Supima cotton, renowned for its superior softness, vibrant color retention, and pill-resistant strength. Tailored with a clean classic fit suitable for base layering or standalone wear.",
    materials: "100% American Supima Cotton (200 GSM)",
    care: [
      "Machine wash cold with like colors",
      "Tumble dry low",
      "Warm iron if needed"
    ],
    details: [
      "Extra-long staple fibers offering unmatched silky softness",
      "Reinforced self-fabric neck binding",
      "Blind-stitched sleeves and bottom hem",
      "Tagless neck print for itch-free comfort"
    ],
    colors: [
      { name: "Bright White", hex: "#ffffff" },
      { name: "Jet Black", hex: "#080808" },
      { name: "Heather Grey", hex: "#a6a6a6" }
    ],
    sizes: [
      { size: "XS", inStock: true },
      { size: "S", inStock: true },
      { size: "M", inStock: true },
      { size: "L", inStock: true },
      { size: "XL", inStock: true },
      { size: "XXL", inStock: true }
    ],
    images: [
      "https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?q=80&w=1000&auto=format&fit=crop",
      "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?q=80&w=1000&auto=format&fit=crop"
    ]
  }
];

const COLLECTIONS = [
  {
    id: "essentials",
    name: "The Essentials Capsule",
    subtitle: "PERMANENT COLLECTION",
    description: "Timeless architectural silhouettes engineered in heavyweight cottons, structured twills, and refined wools. Built to last a lifetime.",
    itemCount: 8,
    image: "https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?q=80&w=1200&auto=format&fit=crop",
    link: "shop.html?collection=essentials"
  },
  {
    id: "streetwear",
    name: "Urban Streetwear Series",
    subtitle: "CONTEMPORARY UTILITY",
    description: "Technical ripstop cargos, drawstring-free 460 GSM looped French terry hoodies, and relaxed oversized silhouettes tailored for city life.",
    itemCount: 5,
    image: "https://images.unsplash.com/photo-1556905055-8f358a7a47b2?q=80&w=1200&auto=format&fit=crop",
    link: "shop.html?collection=streetwear"
  },
  {
    id: "seasonal",
    name: "Seasonal Transition",
    subtitle: "NEW SEASON 2026",
    description: "Lightweight Lyocell linen camp shirts, fluid double-pleated trousers, and structured cropped jackets in muted earth and mineral tones.",
    itemCount: 6,
    image: "https://images.unsplash.com/photo-1509631179647-0177331693ae?q=80&w=1200&auto=format&fit=crop",
    link: "shop.html?collection=seasonal"
  },
  {
    id: "monochrome",
    name: "The All-Black Edition",
    subtitle: "MONOCHROMATIC STUDY",
    description: "A celebration of depth, shadow, and texture. Deep obsidian wools, pitch-black Japanese twills, and washed cotton jersey.",
    itemCount: 10,
    image: "https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=1200&auto=format&fit=crop",
    link: "shop.html?category=all"
  }
];

const PROMO_CODES = [
  {
    code: "BRIFIRST10",
    discountPercent: 10,
    description: "10% off your entire first order",
    minSpend: 1000
  },
  {
    code: "SUMMER30",
    discountPercent: 30,
    description: "30% off selected seasonal collection pieces",
    minSpend: 2500
  },
  {
    code: "FREESHIP2500",
    discountFixed: 150,
    description: "Free nationwide shipping on orders over ₱2,500",
    minSpend: 2500
  }
];

const STORE_CONFIG = {
  currencySymbol: "₱",
  freeShippingThreshold: 2500,
  standardShippingFee: 150,
  expressShippingFee: 350,
  taxRate: 0.12,
  brandName: "BRI APPARELL",
  announcement: "COMPLIMENTARY NATIONWIDE SHIPPING ON ORDERS OVER ₱2,500 | CODE: FREESHIP2500",
  contactEmail: "concierge@briapparell.com",
  contactPhone: "+63 2 8876 5432",
  operatingHours: "Monday – Saturday: 10:00 AM – 8:00 PM PHT",
  flagshipAddress: "Unit 102, The Minimalist Pavilion, Bonifacio High Street, BGC, Taguig, Metro Manila, Philippines"
};

// --- DYNAMIC DATABASE SYNCHRONIZATION ---
// Connects to Python REST API & PostgreSQL/SQLite centralized database
if (typeof window !== 'undefined') {
  fetch('/api/products?include_inactive=false')
    .then(res => res.json())
    .then(data => {
      if (data && data.products && data.products.length > 0) {
        PRODUCTS.length = 0;
        data.products.forEach(p => PRODUCTS.push(p));
        window.dispatchEvent(new CustomEvent('bri:products_synced', { detail: PRODUCTS }));
      }
    })
    .catch(() => {});

  fetch('/api/promotions')
    .then(res => res.json())
    .then(data => {
      if (data && data.promotions && data.promotions.length > 0) {
        PROMO_CODES.length = 0;
        data.promotions.forEach(pr => PROMO_CODES.push({
          code: pr.code,
          discountPercent: pr.discount_percent,
          discountFixed: pr.discount_fixed,
          description: pr.description,
          minSpend: pr.min_spend
        }));
      }
    })
    .catch(() => {});
}

