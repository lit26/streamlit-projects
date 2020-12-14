import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image

st.set_option('deprecation.showfileUploaderEncoding', False)
st.header("Image Size Adjuster")
# upload the image
img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
box_color = '#0000FF'

if img_file:
    img = Image.open(img_file)
    if not realtime_update:
        st.write("Double click to save crop")
    st.write("Original Image")

    # Get a cropped image from the frontend
    cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color)

    # Get ratio for the resizing
    st.sidebar.header("Adjust Size")
    ratio = st.sidebar.radio(label="Fit into:", options=["Custom","320x320","640x640","800x800",
                                                         "1024x1024","1280x1280"])
    ratio_dict = {"320x320": (320, 320),
            "640x640": (640, 640),
            "800x800": (800, 800),
            "1024x1024": (1024, 1024),
            "1280x1280": (1280, 1280)}

    if ratio == "Custom":
        width, height = cropped_img.size
        adj_width = st.sidebar.text_input("Cropped Width: {} pixels".format(width), value=width)
        adj_height = st.sidebar.text_input("Cropped Height: {} pixels".format(height), value=height)

        dimensions = (int(adj_width), int(adj_height))
    else:
        dimensions = ratio_dict[ratio]

    image = cropped_img.resize(dimensions, Image.ANTIALIAS)

    st.write("Adjusted Image")
    st.image(image)