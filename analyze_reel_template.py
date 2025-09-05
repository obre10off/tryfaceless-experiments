import numpy as np
import matplotlib.pyplot as plt
from torchvision.io import read_video
import cv2  # For layout detection
import easyocr  # For OCR
from moviepy import ImageClip, VideoClip, concatenate_videoclips, vfx
from scipy.optimize import curve_fit  # For fitting fade curves
import os
import json
from datetime import datetime

# Helper functions for fade curve fitting
def linear_fade(t, a, b):  # alpha = a * t + b
    return a * t + b

def quadratic_fade(t, a, b, c):  # alpha = a * t^2 + b * t + c
    return a * t**2 + b * t + c

def fit_curve(times, alphas, func):
    try:
        popt, _ = curve_fit(func, times, alphas, bounds=(-np.inf, np.inf))
        return func, popt
    except Exception:
        return None, None

# Load video
video_path = "viral_ig.mp4"  # Replace with your file
video_name = video_path.replace('.mp4', '').replace('.mov', '').replace('.avi', '')
analysis_folder = f"analysis_results/{video_name}_reel"

# Create analysis folder
os.makedirs(analysis_folder, exist_ok=True)
video, _, metadata = read_video(video_path, pts_unit='sec')  # Ignore audio
fps = metadata['video_fps']
duration = len(video) / fps
num_frames = video.shape[0]
resolution = video.shape[2], video.shape[1]  # width, height
print(f"Video shape: {video.shape}")  # Debug: frames, height, width, channels

print(f"Duration: {duration:.2f}s | FPS: {fps:.2f} | Resolution: {resolution} | Frames: {num_frames}")

# Compute per-frame intensity (mean brightness)
frames = video.float()  # [frames, H, W, channels]
intensity = frames.mean(dim=[1, 2, 3]).numpy()

# Normalize intensity to [0,1] for alpha (assuming fade from/to black)
max_intensity = intensity.max()
norm_intensity = intensity / max_intensity

# Detect fade-in: where intensity is increasing from low
diff = np.diff(norm_intensity)
fade_in_end_idx = np.where(diff < 0.01)[0][0] if np.any(diff < 0.01) else int(0.2 * num_frames)  # Stabilize threshold
fade_in_frames = norm_intensity[:fade_in_end_idx]
fade_in_times = np.arange(len(fade_in_frames)) / fps
fade_in_duration = fade_in_end_idx / fps

# Detect fade-out: where intensity is decreasing at end
fade_out_start_idx = num_frames - np.where(np.flip(diff) < -0.01)[0][0] if np.any(diff < -0.01) else int(0.8 * num_frames)
fade_out_start_idx = min(fade_out_start_idx, num_frames - 1)  # Ensure we don't go out of bounds
fade_out_frames = norm_intensity[fade_out_start_idx:]
fade_out_times = np.arange(len(fade_out_frames)) / fps  # Relative times from 0
fade_out_duration = len(fade_out_frames) / fps

hold_duration = duration - fade_in_duration - fade_out_duration

print(f"Fade-In Duration: {fade_in_duration:.2f}s | Hold: {hold_duration:.2f}s | Fade-Out Duration: {fade_out_duration:.2f}s")

# Fit curves to fades
# Fade-In
best_fit_in, best_popt_in = None, None
for func in [linear_fade, quadratic_fade]:
    fit_func, popt = fit_curve(fade_in_times, fade_in_frames, func)
    if fit_func:
        best_fit_in, best_popt_in = fit_func, popt  # Take last (quadratic preferred if fits)

fade_in_formula = f"alpha = {best_popt_in[0]:.3f}*t^2 + {best_popt_in[1]:.3f}*t + {best_popt_in[2]:.3f}" if len(best_popt_in) == 3 else f"alpha = {best_popt_in[0]:.3f}*t + {best_popt_in[1]:.3f}"
print(f"Fade-In Formula: {fade_in_formula} (t in [0, {fade_in_duration:.2f}])")

# Fade-Out (note: for fade-out, we reverse to model as decreasing alpha)
if fade_out_duration > 0.1:  # Only process if there's a meaningful fade-out
    fade_out_alphas = 1 - norm_intensity[fade_out_start_idx:] / norm_intensity[fade_out_start_idx]  # Normalize decrease
    best_fit_out, best_popt_out = None, None
    for func in [linear_fade, quadratic_fade]:
        fit_func, popt = fit_curve(fade_out_times, fade_out_alphas, func)
        if fit_func:
            best_fit_out, best_popt_out = fit_func, popt

    if best_popt_out is not None:
        fade_out_formula = f"alpha = 1 - ({best_popt_out[0]:.3f}*t^2 + {best_popt_out[1]:.3f}*t + {best_popt_out[2]:.3f})" if len(best_popt_out) == 3 else f"alpha = 1 - ({best_popt_out[0]:.3f}*t + {best_popt_out[1]:.3f})"
        print(f"Fade-Out Formula: {fade_out_formula} (t in [0, {fade_out_duration:.2f}])")
    else:
        fade_out_formula = "No significant fade-out detected"
        print(f"Fade-Out Formula: {fade_out_formula}")
else:
    fade_out_formula = "No significant fade-out detected"
    print(f"Fade-Out Formula: {fade_out_formula}")

# Plot for review
times = np.arange(num_frames) / fps
plt.plot(times, norm_intensity)
plt.axvline(fade_in_duration, color='g', label='Fade-In End')
plt.axvline(duration - fade_out_duration, color='r', label='Fade-Out Start')
plt.xlabel("Time (s)")
plt.ylabel("Normalized Intensity")
plt.legend()
plt.savefig(f"{analysis_folder}/fade_plot.png")
plt.close()

# Extract static frame (middle of hold)
static_idx = fade_in_end_idx + int((fade_out_start_idx - fade_in_end_idx) / 2)
static_frame = video[static_idx].numpy().astype(np.uint8)  # Already HWC format
# Convert from RGB to BGR for OpenCV
static_frame = cv2.cvtColor(static_frame, cv2.COLOR_RGB2BGR)
cv2.imwrite(f"{analysis_folder}/static_frame.png", static_frame)

# Analyze layout on static frame (assume 2x2 grid)
reader = easyocr.Reader(['en'])  # OCR
results = reader.readtext(static_frame)

# Extract texts (group by approximate positions)
texts = [res[1] for res in results]  # Detected texts
print("\nDetected Texts:")
for t in texts:
    print(t)

# Detect image positions (simple: find contours assuming images are rectangular regions with high variance)
gray = cv2.cvtColor(static_frame, cv2.COLOR_RGB2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter to likely image regions (e.g., large rectangles, ignore small text)
image_positions = []
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)
    if w > resolution[0]/4 and h > resolution[1]/4:  # Rough grid size filter
        image_positions.append((x, y, w, h))

print("\nDetected Image Positions (x,y,w,h):")
for pos in sorted(image_positions, key=lambda p: (p[1], p[0])):  # Sort top-left to bottom-right
    print(pos)

# Template dict (enhance as needed)
template = {
    "duration": duration,
    "fps": fps,
    "resolution": resolution,
    "fade_in_duration": fade_in_duration,
    "fade_in_formula": fade_in_formula,
    "hold_duration": hold_duration,
    "fade_out_duration": fade_out_duration,
    "fade_out_formula": fade_out_formula,
    "texts": texts,  # Top, captions, bottom
    "grid_positions": image_positions  # For placing user images
}

print("\nExtracted Template:")
print(template)

# --- Generation Example ---
# Use this to create new reels. Provide your own images/captions.
# Example inputs (replace with paths and strings)
# user_images = ["img1.jpg", "img2.jpg", "img3.jpg", "img4.jpg"]  # 4 images for grid
# user_captions = ["Caption 1", "Caption 2", "Caption 3", "Caption 4"]
# top_text = "Your top text here"
# bottom_text = "Your bottom text here"
# font = "Arial"  # Or path to TTF
# font_size = 40
# text_color = (0, 0, 0)

# Save template data as JSON
template_data = {
    "source_video": video_path,
    "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "video_specs": {
        "duration": float(duration),
        "fps": float(fps),
        "resolution": list(resolution),
        "total_frames": int(num_frames)
    },
    "fade_analysis": {
        "fade_in": {
            "duration": float(fade_in_duration),
            "formula": fade_in_formula,
            "type": "quadratic" if len(best_popt_in) == 3 else "linear",
            "timing": [0.0, float(fade_in_duration)]
        },
        "hold_duration": float(hold_duration),
        "fade_out": {
            "duration": float(fade_out_duration),
            "formula": fade_out_formula,
            "type": "minimal" if fade_out_duration < 0.1 else "detected",
            "timing": [float(duration - fade_out_duration), float(duration)]
        }
    },
    "content_analysis": {
        "texts": texts,
        "layout": {
            "image_regions": [
                {
                    "position": [pos[0], pos[1]],
                    "dimensions": [pos[2], pos[3]],
                    "description": f"Image region {i+1}"
                } for i, pos in enumerate(image_positions)
            ]
        }
    },
    "generation_notes": {
        "format": f"{resolution[0]}x{resolution[1]} {'portrait' if resolution[1] > resolution[0] else 'landscape'}",
        "fade_style": f"Quadratic fade-in ({fade_in_duration:.1f}s), {'minimal' if fade_out_duration < 0.1 else 'detected'} fade-out ({fade_out_duration:.1f}s)",
        "content_style": f"Text-heavy with {len(image_positions)} image region(s)",
        "theme": "Content analysis based on detected text"
    }
}

# Save JSON template
with open(f"{analysis_folder}/template.json", 'w') as f:
    json.dump(template_data, f, indent=2)

# Create analysis report
report_content = f"""# Viral Instagram Reel Analysis Report

**Source Video**: `{video_path}`  
**Analysis Date**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Script Version**: analyze_reel_template.py

## Video Specifications
- **Duration**: {duration:.2f} seconds
- **Frame Rate**: {fps:.2f} FPS
- **Resolution**: {resolution[0]}x{resolution[1]} ({'Portrait' if resolution[1] > resolution[0] else 'Landscape'})
- **Total Frames**: {num_frames}

## Fade Analysis
### Fade-In
- **Duration**: {fade_in_duration:.2f} seconds
- **Formula**: `{fade_in_formula}`
- **Type**: {'Quadratic' if len(best_popt_in) == 3 else 'Linear'} curve
- **Timing**: 0.00s → {fade_in_duration:.2f}s

### Hold Duration
- **Duration**: {hold_duration:.2f} seconds
- **Timing**: {fade_in_duration:.2f}s → {duration - fade_out_duration:.2f}s

### Fade-Out
- **Duration**: {fade_out_duration:.2f} seconds
- **Status**: {'No significant fade-out detected' if fade_out_duration < 0.1 else 'Detected'}
- **Timing**: {duration - fade_out_duration:.2f}s → {duration:.2f}s

## Content Analysis
### Detected Text Elements
The reel contains the following text content:

{chr(10).join([f"{i+1}. \"{text}\"" for i, text in enumerate(texts)])}

### Layout Structure
{chr(10).join([f"- **Image Region {i+1}**: {pos[2]}x{pos[3]} pixels at position ({pos[0]}, {pos[1]})" for i, pos in enumerate(image_positions)])}

## Generated Files
- `fade_plot.png` - Fade curve visualization
- `static_frame.png` - Middle frame for layout analysis
- `template.json` - Complete template data (JSON format)
- `analysis_report.md` - This detailed analysis report

## Usage Notes
This template can be used to generate similar reels by:
1. Replacing the text content with your own messages
2. Using the same fade timing and curves
3. Maintaining the {resolution[0]}x{resolution[1]} format
4. Following the detected layout structure

## Next Steps
1. Uncomment the generation code in `analyze_reel_template.py`
2. Provide your own images and text content
3. Run the script to generate new reels using this template
"""

with open(f"{analysis_folder}/analysis_report.md", 'w') as f:
    f.write(report_content)

print("\n" + "="*60)
print("TEMPLATE ANALYSIS COMPLETE!")
print("="*60)
print(f"✅ Video analyzed successfully: {video_path}")
print(f"✅ Results saved to: {analysis_folder}/")
print(f"   📊 fade_plot.png - Fade curve visualization")
print(f"   🖼️  static_frame.png - Middle frame for layout analysis")
print(f"   📄 template.json - Complete template data")
print(f"   📋 analysis_report.md - Detailed analysis report")
print(f"✅ Template extracted and ready for generation")
print(f"\n📁 Analysis folder: {analysis_folder}")
print("\nTo generate a new reel, uncomment the generation code")
print("and provide your own images and text content.")