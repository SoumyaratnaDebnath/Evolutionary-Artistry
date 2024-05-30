import streamlit as st
import pandas as pd
from GeneticAlgoArt import GeneticAlgoArt
from GameOfLifeArt import GameOfLifeArt
from makeGIF import makeGIF

st.set_page_config(page_title="Evolutionary Artistry", layout="wide")

with st.container():
    st.markdown("## Create Artworks using Genetic Algorithm")
    st.markdown("#### Use `Genetic Algorithm` and `Game of Life` over use your own image to create beautiful artworks.")

st.write('---')

with st.container():
    # upload a single image
    uploaded_file = st.file_uploader("#### Upload an Image", type=["png", "jpg", "jpeg"])
    # save the uploaded file as img.png
    if uploaded_file is not None:
        with open("inputGA.png", "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("File Uploaded Successfully")
        st.markdown('''
        <style>
            .uploadedFile {display: none}
        <style>''',
        unsafe_allow_html=True)

st.write('---')

if uploaded_file is not None:

    with st.container():
        st.markdown("<h3 style='text-align: center;'>Visualizing the image with a Single Running Line using Genetic Algorithm <br>and using Game of Life to create artworks.</h3>", unsafe_allow_html=True)
        st.write('---')
        with st.container():
            col1, col2, col3 = st.columns((1,7,1))
            with col2:
                col1, col2, col3 = st.columns((4,1,4))
                # create range sliders for the parameters
                with col1:
                    num_generations_ga = st.slider("##### Generations in Genetic Algoritm", 500, 5000, 2000, 500)
                    # solution_per_population = st.slider("##### Population Size", 20, 50, 50, 10)
                    solution_per_population = 50
                with col3:
                    num_generations_gol = st.slider("##### Generations in Game of Life", 200, 2000, 500, 100)
                    # image_size = st.slider("##### Image Size", 128, 1024, 512, 2)
                    image_size = 512
                    save_frequency = int(num_generations_ga/20) # display 250 images in total

        st.markdown("<br>", unsafe_allow_html=True)
        # create a button to start the optimization
        if st.button("Start Visualization using Genetic Algorithm and Game of Life", type="primary"):

            st.info("Genetic Optimization Started")
            _bar = st.progress(0, text='Genetic Algorithm in Progress')
            G = GeneticAlgoArt(num_generations=num_generations_ga+1, sol_per_pop=solution_per_population, image_size=image_size, save_frequency=save_frequency, progress_bar=_bar)
            G.run()
            _bar.progress(1.0, text='Genetic Algorithm Completed')
            makeGIF('GA_images', 'outputGA.gif', duration=500)
            
            col1, col2 = st.columns((1, 1))
            with col1:
                st.image('outputGA.gif', use_column_width=True, caption='GA Optimization over the Generations')
            with col2:
                st.image('outputGA.png', use_column_width=True, caption='Image Visualization as a Single Running Line after', num_generations_ga, 'Generations')

            st.write('---')

            with st.container():
                st.info("Game Of Life Visualization Started")
                _bar = st.progress(0, text='Game of Life in Progress')
                GOL = GameOfLifeArt('outputGA.png', num_generations_gol+1, _bar)
                GOL.run()                    
                _bar.progress(1.0, text='Game of Life in Completed')
                makeGIF('GOL_images', 'outputGOL.gif', duration=10)
                col1, col2, col3 = st.columns((1, 2, 1))
                with col2:
                    st.image('outputGOL.gif', use_column_width=True, caption='Game of Life Simulation over the Generations')
                    



