# Upload Page - Visual Design Reference

## Layout Structure

### Desktop (>1024px)
```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Navigation Bar                                │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌─────────────────────────┐  ┌──────────────────┐
│ Left Guidance    │  │                         │  │ Right Guidance   │
│ Panel            │  │   UPLOAD CARD           │  │ Panel            │
│                  │  │                         │  │                  │
│ ⭕ Natural       │  │  Upload Skin Image      │  │ ⭕ Capture Area  │
│    Lighting      │  │                         │  │    Include full  │
│    Card          │  │  [File Input]           │  │    affected area │
│                  │  │                         │  │                  │
│ ⭕ Clear Focus   │  │  Image Quality Check    │  │ ⭕ No            │
│    Ensure sharp  │  │  ◉ Resolution          │  │    Obstructions  │
│    visibility    │  │  ◉ Lighting            │  │    Avoid shadows │
│                  │  │  ◉ Contrast            │  │                  │
│                  │  │                         │  │                  │
│                  │  │  [Image Preview]        │  │                  │
│                  │  │                         │  │                  │
│                  │  │  [Upload & Process Btn] │  │                  │
│                  │  │                         │  │                  │
│                  │  │  Supported: PNG, JPG   │  │                  │
└──────────────────┘  └─────────────────────────┘  └──────────────────┘

    ←40px gap→     ←←←←  400px upload box  →→→→
    220px width                                    220px width
```

### Tablet (768px-1024px)
```
┌─────────────────────────────────────────────────────────────────────────┐
│                           Navigation Bar                                │
└─────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────┐  ┌────────────────────────────────┐
│ ⭕ Natural Lighting             │  │ ⭕ Capture Area                 │
└────────────────────────────────┘  └────────────────────────────────┘

┌────────────────────────────────┐  ┌────────────────────────────────┐
│ ⭕ Clear Focus                   │  │ ⭕ No Obstructions              │
└────────────────────────────────┘  └────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────┐
│                      UPLOAD CARD (Full Width)                          │
│                                                                        │
│                      Upload Skin Image                                │
│                                                                        │
│                      [File Input Box]                                  │
│                      Image Quality Check...                            │
│                      [Image Preview]                                   │
│                      [Upload & Process Button]                         │
│                                                                        │
└────────────────────────────────────────────────────────────────────────┘
```

### Mobile (<768px)
```
┌─────────────────────────────────┐
│    Navigation Bar               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ ⭕ Natural Lighting              │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ ⭕ Clear Focus                   │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ ⭕ Capture Area                  │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ ⭕ No Obstructions               │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│    UPLOAD CARD (Full Width)      │
│                                  │
│   Upload Skin Image              │
│                                  │
│   [File Input Box]               │
│   Image Quality Check...         │
│   [Image Preview]                │
│   [Upload & Process Button]      │
│                                  │
└─────────────────────────────────┘
```

## Color Palette

### Primary Colors
```
Navy Blue (#0a3d62)
├─ Text headings
├─ Borders/accents
└─ Icons

Medical Red (#ff3f34)
└─ Upload button

Light Background (#f9fbfd)
└─ Page background
```

### Quality Indicator Colors
```
Good Status (#27ae60)          ●
├─ Used for: Positive metrics
└─ Example: High resolution

Warning Status (#f39c12)       ●
├─ Used for: Moderate issues
└─ Example: Low brightness

Critical Status (#e74c3c)      ●
├─ Used for: Major issues
└─ Example: Very low resolution

Unknown Status (#bdc3c7)       ●
└─ Used for: Initial/analyzing state
```

### Secondary Colors
```
Text Secondary (#666)
├─ Body text
└─ Descriptions

Border/Shadow (#ddd, #999)
├─ Dividers
└─ Subtle backgrounds

Panel Background (#f5f9fc)
└─ Quality check panel
```

## Component Dimensions

### Guidance Panels
```
Desktop:
  Width: 220px
  Each card: 20px padding, margin-bottom: 20px
  
Tablet (1200px):
  Width: 180px
  Cards: 16px padding
  
Mobile (1024px and below):
  Grid: 2 columns (or 1)
  Full width allocation
```

### Upload Box
```
Desktop:
  Width: 400px
  Max width: 100%
  Padding: 50px
  
Tablet:
  Width: 100%
  Max width: none
  Padding: 40px
  
Mobile:
  Width: 100%
  Padding: 30px 20px
```

### Buttons
```
Upload Button:
  Width: 100% (of form)
  Padding: 12px
  Font size: 16px
  Font weight: bold
  Border radius: 5px
  
States:
  Normal: #ff3f34
  Hover: #e63929
```

### File Input
```
Width: 100%
Padding: 12px 15px
Border: 2px dashed #0a3d62
Font size: 14px

Focus state: background: #f0f5fa
```

### Image Preview
```
Max height: 200px
Width: 100%
Object fit: contain
Margin top: 15px
Border radius: 6px
Background: #f0f5fa
Display: none (shown on file select)
```

### Quality Check Panel
```
Padding: 15px
Margin top: 20px
Background: #f5f9fc
Border: 1px solid #d0e3f0
Border radius: 6px
Display: none (shown on file select)

Items:
  Line height: Item height 20px
  Margin bottom: 8px (except last)
  Font size: 12px
  
Indicator dot:
  Width: 14px
  Height: 14px
  Border radius: 50%
  Glow: 0 0 4px rgba()
```

## Typography Scale

```
Heading 2 (Upload Title)
  Size: 28px
  Weight: Bold (700)
  Color: #0a3d62
  Margin bottom: 30px

Heading 4 (Guidance Card Titles)
  Size: 13px
  Weight: 600
  Color: #0a3d62
  Text transform: uppercase
  Letter spacing: 0.5px
  Margin bottom: 6px

Body Text (Main copy)
  Size: 14px
  Color: #666
  Margin bottom: 25px
  
Description Text (Small)
  Size: 12px
  Color: #666
  Line height: 1.5
  
Note Text (Footer)
  Size: 12px
  Color: #999
  Margin top: 15px

Quality Text
  Size: 12px
  Color: Status-dependent (#27ae60, #f39c12, #e74c3c)
  Font weight: 500
```

## Spacing System

```
Extra small: 5px
Small: 10px
Regular: 15px
Medium: 20px
Large: 30px
Extra large: 40px
Huge: 50px
```

### Applied Spacing
```
Page padding: 40px 20px
Upload box padding: 50px
Guidance card padding: 20px
Quality panel padding: 15px
Title margin bottom: 30px
Card margin bottom: 20px
Gap between sections: 40px
Gap between guidance cards: 20px
Gap between responsive panels: 15px
```

## Icon Reference

### Guidance Panel Icons
```
💡 Natural Lighting
  Semantic: Light bulb (brightness/lighting)
  
📸 Clear Focus
  Semantic: Camera (photography/focus)
  
📐 Capture Area
  Semantic: Ruler/measurement (framing)
  
✓ No Obstructions
  Semantic: Checkmark (clarity/approval)
```

### Quality Check Icons
```
● Good indicator
  Color: #27ae60 (Green)
  Glow: 0 0 4px rgba(39, 174, 96, 0.3)
  
● Warning indicator
  Color: #f39c12 (Orange)
  Glow: 0 0 4px rgba(243, 156, 18, 0.3)
  
● Critical indicator
  Color: #e74c3c (Red)
  Glow: 0 0 4px rgba(231, 76, 60, 0.3)
  
● Unknown indicator
  Color: #bdc3c7 (Gray)
  Glow: 0 0 4px rgba(189, 195, 199, 0.3)
```

## Shadows & Depth

```
Panel Shadow (Cards & Upload Box):
  0 2px 12px rgba(10, 61, 98, 0.08)
  
Upload Box Shadow (Primary):
  0 10px 40px rgba(0, 0, 0, 0.1)
  
Indicator Glow:
  0 0 4px rgba(color, 0.3)
```

## Border Radius

```
Large (Upload box): 10px
Medium (Cards): 8px
Small (Input/button): 5px
Circular (Indicators): 50%
```

## Responsive Breakpoints

```
Desktop: >1024px
  Full layout with side panels
  
Tablet: 768px - 1024px
  Panels convert to grid
  Upload box full width
  Reduced font sizes
  
Mobile: <768px
  Single column layout
  Guidance panels 1 column
  Upload box full width
  Minimal padding
```

## Animation Reference

```
NOTE: No animations in guidance panels or quality checks
      Only existing upload animations preserved:
      
Progress Bar Fill:
  Linear animation to width percentage
  
Success Checkmark:
  Stroke-dashoffset animation (0.8s ease-out)
  
Page Redirect:
  After success animation (900ms delay)
```

## States & Interactions

### File Input States
```
Default:
  Border: 2px dashed #0a3d62
  Background: white
  
Focus:
  Outline: none
  Background: #f0f5fa
  
With File:
  Quality panel appears
  Preview image shows
  Indicators populate
```

### Upload Button States
```
Default:
  Background: #ff3f34
  Color: white
  Cursor: pointer
  
Hover:
  Background: #e63929
  
Disabled (if implemented):
  Opacity: 0.5
  Cursor: not-allowed
```

### Quality Panel States
```
Hidden:
  Display: none
  
Shown:
  Display: block
  Fade in (natural timing)
  Indicators update in sequence
  
With Results:
  Good: Green indicators
  Warning: Orange indicators
  Critical: Red indicators
```

## Accessibility Specifications

### Color Contrast
```
Text on White (#0a3d62 on white):
  Ratio: 8.5:1 (exceeds AA & AAA)
  
Button Text (white on #ff3f34):
  Ratio: 4.5:1 (meets AA)
  
Secondary Text (#666 on white):
  Ratio: 7:1 (exceeds AA)
```

### Focus Indicators
```
File Input Focus:
  Browser default outline (varies by browser)
  Alternative visual: background color change
  
Button Focus:
  Browser default outline
  
Link Focus:
  Browser default outline
```

### Touch Targets (Mobile)
```
Minimum: 48x48px
Button: 44px height × full width
File input: 40px+ height
Icons/indicators: 32px minimum
```

