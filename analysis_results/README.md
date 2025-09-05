# Analysis Results

This folder contains organized analysis results for viral Instagram reels. Each analyzed video gets its own subfolder with a clear naming convention.

## Folder Structure

```
analysis_results/
├── README.md                           # This file
├── {video_name}_reel/                  # Analysis folder for each video
│   ├── analysis_report.md             # Detailed human-readable analysis
│   ├── template.json                  # Machine-readable template data
│   ├── fade_plot.png                  # Fade curve visualization
│   └── static_frame.png               # Middle frame for layout analysis
```

## Naming Convention

- **Folder names**: `{video_name}_reel`
  - Example: `viral_ig_reel` for `viral_ig.mp4`
  - Example: `my_content_reel` for `my_content.mp4`

## File Descriptions

### `analysis_report.md`
- **Purpose**: Human-readable detailed analysis report
- **Content**: Video specs, fade analysis, content analysis, usage notes
- **Format**: Markdown for easy reading and sharing

### `template.json`
- **Purpose**: Machine-readable template data for programmatic use
- **Content**: Complete template structure with all timing, layout, and content data
- **Format**: JSON for easy integration with other tools

### `fade_plot.png`
- **Purpose**: Visual representation of fade curves
- **Content**: Graph showing intensity over time with fade markers
- **Usage**: Quick visual reference for fade timing and style

### `static_frame.png`
- **Purpose**: Reference frame for layout analysis
- **Content**: Middle frame of the video showing the main content layout
- **Usage**: Visual reference for understanding the template structure

## Usage

1. **View Analysis**: Open `analysis_report.md` for a complete overview
2. **Use Template**: Load `template.json` in your generation scripts
3. **Visual Reference**: Check `fade_plot.png` and `static_frame.png` for visual cues
4. **Compare Templates**: Use different analysis folders to compare different viral formats

## Adding New Analyses

When you analyze a new video, the script will automatically:
1. Create a new folder with the video name
2. Generate all analysis files
3. Save everything in an organized structure

This keeps your analysis results clean, organized, and easy to reference!
