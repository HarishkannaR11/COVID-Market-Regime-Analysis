from PIL import Image

# Define the directory containing the images
img_dir = "results/Stability_Analysis_RunLength_Entropy/"

# Load the two images using their full paths
img1 = Image.open(img_dir + "stability_mirror_chart.png")  # System Stability Mirror Chart
img2 = Image.open(img_dir + "stability_switching_frequency.png")  # System Switching Frequency Chart

# Scale both images to the same height using the MAXIMUM height to avoid cropping
target_height = max(img1.height, img2.height)
img1 = img1.resize((int(img1.width * target_height / img1.height), target_height), Image.LANCZOS)
img2 = img2.resize((int(img2.width * target_height / img2.height), target_height), Image.LANCZOS)

# Create a new image with combined width
combined_width = img1.width + img2.width
combined_img = Image.new("RGB", (combined_width, target_height), (255, 255, 255))

# Paste images side by side (align to top)
combined_img.paste(img1, (0, 0))
combined_img.paste(img2, (img1.width, 0))

# Save the result in the same directory
output_path = img_dir + "combined_side_by_side.png"
combined_img.save(output_path, dpi=(300, 300))
print(f"Combined image saved as {output_path}")
