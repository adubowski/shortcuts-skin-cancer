# Detecting Cheating in Skin Cancer Diagnosis
This project is focused on the topic of Explainable AI in the "Research Experiments in Databases and Information Retrieval" (REDI) course. The project aims to show the undesired bias in skin cancer prediction models when trained on the ISIC dataset which contains coloured patches in the group of non-cancer images, which could potentially result in misdiagnoses when applied in real-life scenarios.

Makes use of code from https://github.com/laura-rieger/deep-explanation-penalization for handling the ISIC Skin Cancer dataset & training a VGG16 classifier to distinguish between malignant and benign lesions. The segmentation masks for identifying the coloured patches in the image are also taken from here.

Uses the GMCNN inpainting model from: https://github.com/shepnerd/inpainting_gmcnn/tree/master/pytorch

More specific detail on which code is copied or original is available either in the sub-directories or at the top of the individual notebooks themselves.

Overall workflow:

1. Download & resize images from ISIC database                      (01_process_data - scripts 00 to 02).
2. Dilate the patch segmentation masks                              (01_process_data - 03_dilate_masks.py).
3. Train the inpainting model                                       (02_inpainting - inpainting_gmcnn_train.ipynb).
4. Apply inpainting to the relevant images for experiments          (02_inpainting - inpainting_gmcnn_test.ipynb).
5. Train the classifier on the original images or inpainted images  (03_classifier - train_classifier.ipynb).
6. Run experiments as reported in the paper                         (03_classifier - compare_predictions.ipynb).
