
# Image Captioning using Machine Learning

The process of providing a written description of a picture’s content is known as Image
Captioning. To generate captions, it combines computer vision and natural language processing. The project’s objective is to study how
the encoder-decoder Neural architecture works and how making changes to this neural network architecture - specifically the encoder, can
affect the performance. 
Image Captioning is suitable for a wide range of applications, from
social media to help those with visual impairments. Working on this project gave us clarity on different concepts of machine learning
which are further described in detail in this report. We, in this project, have achieved satisfactory BLEU scores by doing comparative
study of different encoders that can be used for the model. Several datasets, including COCO,flicker30k, flicker8k, localized narratives, and
SCICAP, are available for training the model; we investigated these datasets and decided to
use flicker8k dataset for the project. The Code for the project can be found on [GitHub](https://github.com/ameygoes/ASU_MCS/tree/master/FALL_22_CLASSES_SEM_1/CSE_575_STATISTICAL_MACHINE_LEARNING/PROJECTS).




## Environment Variables

To run this project, you will need to set the following variables

- `PROJECT_PATH` - Base Project Path from Drive
- `CAPTION_FILE_PATH` - It would be path till captions.txt File
- `images_path` = It would be path till Image Folder
- `MODEL_WEIGHTS_PATH` = Path to which Model weights will be saved
- `MODEL_PATH` = Path to which Model Path will be saved
- `isXceptionModel` = Set to `True` if want to use Xception Model for Training
                    Set to `False` if want to use ResNet50 Model for Training



## Run Project


To run this project locally, you need to run

```
pip install -r requirements.txt
-- requirements.txt file is in the zip file provided.
```
- Download dataset using [this link](https://www.kaggle.com/datasets/adityajn105/flickr8k/download?datasetVersionNumber=1) 

If you're running this project on Google Colab:
- No need to run above command
- Run Cells of iPython Notebook to get the results
- Need to run iPython Notebook twice for each of the model, by setting and de-setting the variable isXceptionModel
- With Zip file we have provided with the models and weights file as well, in case you don't want to train the
- Upload your dataset to google drive.

With the zip file, we have provided you with two seperate iPython notebooks, one with Xception and ResNet50 model output, if you want to run, you have to run only one of the file, by setting above variables.
## Authors

- [@Amey Bhilegaonkar](https://ameyportfolio.netlify.app/)
- [@Gaurav Hoskote](https://github.com/gauravhoskote)
- [@Ninad Nale](https://github.com/ninadnale)
- [@Apoorv Kakade](https://www.github.com/ameygoes)
- [@Varad Deshmukh](https://github.com/Varad1503)


## Support

For support, email 

    abhilega@asu.edu
    ghoskote@asu.edu
    nnale@asu.edu
    akakade@asu.edu

- with the Subject: CSE575_SML_PROJECT_QUERY, 
- with the Body: 
    - Name:
    - Query:
## 🔗 Links

- Amey Bhilegaonkar
    [![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://ameyportfolio.netlify.app/)
    [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/amey-bhilegaonkar-942b70125/)

- Gaurav Hoskote
    [![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://gauravhoskote.github.io/)
    [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gauravhoskote/)

- Ninad Nale
    [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/apoorv-kakade/)
    
- Apoorv Kakade
    [![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/apoorv-kakade/)

