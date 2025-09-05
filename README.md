# TryFaceless Experiments

A powerful tool for analyzing viral Instagram reels and extracting their template structure to create similar content. This project reverse-engineers successful video formats to help content creators replicate viral patterns.

## 🎯 What It Does

This tool analyzes viral Instagram reels to extract:
- **Fade timing and curves** (fade-in/fade-out patterns)
- **Content layout** (text positions, image regions)
- **Video specifications** (duration, resolution, frame rate)
- **Template structure** for generating similar content

## 🚀 Features

- **Automatic Video Analysis**: Analyzes any video file to extract its structure
- **Fade Curve Detection**: Identifies and mathematically models fade patterns
- **OCR Text Recognition**: Extracts all text content from the video
- **Layout Detection**: Finds image regions and positioning
- **Template Generation**: Creates reusable templates for content creation
- **Organized Results**: Saves analysis in structured folders with clear documentation

## 📁 Project Structure

```
tryfaceless-experiments/
├── analyze_reel_template.py          # Main analysis script
├── main.py                          # Entry point
├── pyproject.toml                   # Dependencies
├── viral_ig.mp4                     # Example viral video
├── analysis_results/                # Organized analysis results
│   ├── README.md                    # Analysis structure guide
│   └── viral_ig_reel/               # Analysis for viral_ig.mp4
│       ├── analysis_report.md       # Detailed human-readable report
│       ├── template.json            # Machine-readable template data
│       ├── fade_plot.png            # Fade curve visualization
│       └── static_frame.png         # Layout reference frame
└── README.md                        # This file
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd tryfaceless-experiments
   ```

2. **Install dependencies**:
   ```bash
   bun install
   ```

3. **Install Python packages**:
   ```bash
   python -m pip install torch torchvision matplotlib opencv-python easyocr moviepy scipy numpy av
   ```

## 🎬 Usage

### Basic Analysis

1. **Place your video** in the project root (or update the path in the script)
2. **Run the analysis**:
   ```bash
   python analyze_reel_template.py
   ```

3. **View results** in the `analysis_results/{video_name}_reel/` folder

### Example Analysis

The project includes an example analysis of `viral_ig.mp4`:

- **Duration**: 6.30s at 30 FPS
- **Resolution**: 720x1280 (portrait)
- **Fade-in**: 1.5s quadratic curve
- **Content**: Religious/spiritual struggle theme
- **Layout**: Single large image region

## 📊 Analysis Output

Each analysis creates a structured folder containing:

### `analysis_report.md`
- Complete video specifications
- Fade analysis with mathematical formulas
- Content breakdown and text extraction
- Layout structure details
- Usage instructions

### `template.json`
- Machine-readable template data
- Perfect for programmatic use
- Complete timing and layout information

### `fade_plot.png`
- Visual representation of fade curves
- Shows intensity over time
- Quick reference for fade patterns

### `static_frame.png`
- Middle frame of the video
- Shows main content layout
- Visual reference for structure

## 🔧 Technical Details

### Dependencies
- **PyTorch/TorchVision**: Video loading and processing
- **OpenCV**: Image processing and layout detection
- **EasyOCR**: Text recognition
- **MoviePy**: Video editing capabilities
- **Matplotlib**: Visualization
- **SciPy**: Curve fitting for fade analysis

### Supported Formats
- **Input**: MP4, MOV, AVI video files
- **Output**: PNG images, JSON data, Markdown reports

## 🎨 Template Generation

The extracted templates can be used to generate new content by:

1. **Uncommenting the generation code** in `analyze_reel_template.py`
2. **Providing your own content**:
   - Images for the detected regions
   - Text content to replace detected text
   - Custom styling and fonts
3. **Running the generation** to create new reels

## 📈 Use Cases

- **Content Creators**: Replicate successful video formats
- **Social Media Managers**: Understand viral patterns
- **Video Editors**: Extract timing and layout information
- **Researchers**: Analyze video content structure
- **Automation**: Programmatically generate similar content

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source. Please check the license file for details.

## 🆘 Support

If you encounter any issues:
1. Check the analysis results in the `analysis_results/` folder
2. Review the generated reports for detailed information
3. Open an issue with specific error details

## 🔮 Future Enhancements

- **Batch Processing**: Analyze multiple videos at once
- **Template Library**: Pre-built templates for common formats
- **Generation UI**: Web interface for easy template creation
- **Advanced Analytics**: Performance metrics and optimization suggestions
- **Export Options**: Direct export to various video editing software

---

**Happy Creating!** 🎬✨

Use this tool to understand what makes videos go viral and create your own successful content using proven patterns.

---

