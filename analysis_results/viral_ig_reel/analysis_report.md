# Viral Instagram Reel Analysis Report

**Source Video**: `viral_ig.mp4`  
**Analysis Date**: 2025-09-05 17:35:01  
**Script Version**: analyze_reel_template.py

## Video Specifications
- **Duration**: 6.30 seconds
- **Frame Rate**: 30.00 FPS
- **Resolution**: 720x1280 (Portrait)
- **Total Frames**: 189

## Fade Analysis
### Fade-In
- **Duration**: 1.50 seconds
- **Formula**: `alpha = 0.003*t^2 + 0.423*t + 0.361`
- **Type**: Quadratic curve
- **Timing**: 0.00s → 1.50s

### Hold Duration
- **Duration**: 4.77 seconds
- **Timing**: 1.50s → 6.27s

### Fade-Out
- **Duration**: 0.03 seconds
- **Status**: No significant fade-out detected
- **Timing**: 6.27s → 6.30s

## Content Analysis
### Detected Text Elements
The reel contains the following text content:

1. "you know the struggle is real if"
2. "you've done these:"
3. "fell asleep praying"
4. "deleted insta (again)"
5. "Deactivate your account"
6. "instead of deleting?"
7. "Deactivating Youf eccount"
8. "Jcmpotan"
9. "Youi Ptolile photo?  comreraand Fiea Kaba"
10. "hidden untayou enable"
11. "Dy loatna bachi"
12. "Dclcting your Jccount"
13. "pcrmancnt"
14. "Youi ptotile photos Vidcos cotincnts nkes"
15. "HollonetsnMbe penunenily dclaled"
16. "silent worship cry"
17. "scrolled during church"
18. "amen if you're pushing through"

### Layout Structure
- **Image Region 1**: 720x960 pixels at position (0, 160)

## Generated Files
- `fade_plot.png` - Fade curve visualization
- `static_frame.png` - Middle frame for layout analysis
- `template.json` - Complete template data (JSON format)
- `analysis_report.md` - This detailed analysis report

## Usage Notes
This template can be used to generate similar reels by:
1. Replacing the text content with your own messages
2. Using the same fade timing and curves
3. Maintaining the 720x1280 format
4. Following the detected layout structure

## Next Steps
1. Uncomment the generation code in `analyze_reel_template.py`
2. Provide your own images and text content
3. Run the script to generate new reels using this template
